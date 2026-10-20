import base64
import json
import re
from datetime import datetime
from typing import Tuple, Optional
from sqlalchemy.orm import Session
from sqlalchemy import desc

from app.models import Order, CustomerSession, MenuItem
from app.menu_data import MENU_CATEGORIES, get_menu_text
from app.services.whatsapp_service import notify_kitchen_new_order, notify_customer_status_change
from app.services.ai_service import client


import os
import tempfile


def transcribe_voice_note(audio_base64: str, mimetype: str = "audio/ogg") -> str:
    """تحويل الرسائل الصوتية (Voice Notes) إلى نص باللغة العربية عبر نموذج Whisper بدقة وسرعة عالية."""
    tmp_path = None
    try:
        audio_bytes = base64.b64decode(audio_base64)
        clean_mime = mimetype.split(";")[0].strip().lower() if mimetype else "audio/ogg"

        ext = ".ogg"
        if "mp4" in clean_mime or "m4a" in clean_mime or "aac" in clean_mime:
            ext = ".m4a"
        elif "mp3" in clean_mime or "mpeg" in clean_mime:
            ext = ".mp3"
        elif "wav" in clean_mime:
            ext = ".wav"

        with tempfile.NamedTemporaryFile(suffix=ext, delete=False) as tmp:
            tmp.write(audio_bytes)
            tmp_path = tmp.name

        text = ""
        for model_name in ["whisper-large-v3", "whisper-large-v3-turbo"]:
            try:
                with open(tmp_path, "rb") as audio_file:
                    transcription = client.audio.transcriptions.create(
                        model=model_name,
                        file=audio_file,
                        language="ar"
                    )
                    text = transcription.text.strip()
                    if text:
                        print(f"🎙️ [Whisper Transcribed via {model_name}]: {text}", flush=True)
                        break
            except Exception as me:
                print(f"⚠️ [Whisper {model_name} Error]: {me}", flush=True)
                continue

        return text
    except Exception as e:
        print(f"❌ [Transcribe Error]: {e}", flush=True)
        return ""
    finally:
        if tmp_path and os.path.exists(tmp_path):
            try:
                os.remove(tmp_path)
            except Exception:
                pass


def get_last_saved_address(db: Session, customer_phone: str) -> Optional[str]:
    """البحث عن آخر عنوان توصيل مسجل للعميل (التعرف على العميل القديم)."""
    last_order = db.query(Order).filter(
        Order.customer_phone == customer_phone,
        Order.delivery_address.isnot(None),
        Order.delivery_address != "",
        Order.delivery_address != "استلام من المطعم (تيك أواي)"
    ).order_by(desc(Order.created_at)).first()

    return last_order.delivery_address if last_order else None


def get_or_create_session(db: Session, customer_phone: str) -> CustomerSession:
    session = db.query(CustomerSession).filter(CustomerSession.customer_phone == customer_phone).first()
    if not session:
        session = CustomerSession(
            customer_phone=customer_phone,
            state="idle",
            current_cart="[]",
            order_type="دليفري"
        )
        db.add(session)
        db.commit()
        db.refresh(session)
    return session


def parse_cart(cart_json: str) -> list:
    try:
        return json.loads(cart_json or "[]")
    except Exception:
        return []


def format_cart_summary(cart: list) -> Tuple[str, float]:
    if not cart:
        return "لا توجد أصناف في السلة حالياً.", 0.0

    lines = []
    total = 0.0
    for item in cart:
        name = item.get("name", "صنف")
        size = item.get("size", "")
        qty = int(item.get("quantity", 1))
        price = float(item.get("price", 0))
        item_total = price * qty
        total += item_total
        size_str = f" ({size})" if size else ""
        lines.append(f"- {qty}x {name}{size_str}: {item_total:g} جنيه")

    return "\n".join(lines), total


def get_unavailable_items_text(db: Session) -> str:
    """استرجاع الأصناف غير المتاحة (خلصانة من المطبخ) لإبلاغ الذكاء الاصطناعي بها."""
    unavailable = db.query(MenuItem).filter(MenuItem.is_available.is_(False)).all()
    if not unavailable:
        return ""
    names = [f"- {item.name} ({item.category})" for item in unavailable]
    return "الأصناف التالية غير متاحة اليوم (نافذة من المطبخ - Out of Stock):\n" + "\n".join(names)


def check_order_tracking(db: Session, customer_phone: str, message: str) -> Optional[str]:
    tracking_keywords = [
        "فين الاوردر", "فين الطلب", "حالة الطلب", "الاوردر اتأخر", 
        "طلب رقم", "أوردر رقم", "حالة اوردري", "الطلب فين", "وصل ولا لسه",
        "تتبع", "متابعة الطلب", "الأوردر فين"
    ]
    if any(k in message for k in tracking_keywords):
        latest_order = db.query(Order).filter(
            Order.customer_phone == customer_phone
        ).order_by(desc(Order.created_at)).first()

        if not latest_order:
            return "يا فندم لا يوجد أي أوردر مسجل بهذا الرقم حالياً. تحب تطلب أي وجبة من المنيو؟ ❤️"

        status_arabic = {
            "Confirmed": "تم استلام طلبك وجاري إرساله للمطبخ 📋",
            "In_Preparation": "شيف مطعم روستيكا شغال في تحضير طلبك حالياً بأعلى جودة 🔥👨‍🍳",
            "Out_For_Delivery": "طلبك خرج الآن مع كابتن التوصيل وفي الطريق إليك 🛵💨",
            "Delivered": "تم تسليم طلبك بنجاح! بالهنا والشفا، نورت روستيكا ❤️",
            "Cancelled": "تم إلغاء هذا الطلب ❌"
        }

        desc_status = status_arabic.get(latest_order.status, latest_order.status)
        return (
            f"🔍 *حالة طلبك رقم #{latest_order.id}:*\n\n"
            f"📌 الحالة: {desc_status}\n"
            f"🛒 الأصناف:\n{latest_order.items_summary}\n"
            f"💰 الإجمالي: {latest_order.total_price:g} جنيه\n"
            f"🛵 النوع: {latest_order.order_type}\n\n"
            f"لأي مساعدة تواصل معنا في أي وقت!"
        )
    return None


def check_kitchen_admin_commands(db: Session, customer_phone: str, message: str) -> Optional[str]:
    """أوامر تحكم سريعة للكاشير عبر الواتساب: إيقاف وتشغيل الأصناف عند نفاذها دون الحاجة لفتح شاشات."""
    from app.services.whatsapp_service import KITCHEN_PHONE
    clean_sender = re.sub(r'[^0-9]', '', customer_phone)
    clean_admin = re.sub(r'[^0-9]', '', KITCHEN_PHONE or "")

    if not clean_admin:
        return None

    # التحقق من أن المرسل هو هاتف الكاشير المعتمد
    if not (clean_sender.endswith(clean_admin[-9:]) or clean_admin.endswith(clean_sender[-9:])):
        return None

    msg = message.strip()
    msg_lower = msg.lower()

    # 1. أوامر إيقاف صنف (خلص / خلصان / نفذ / وقف)
    for prefix in ["خلصان ", "خلص ", "خلصانه ", "خلصت ", "وقف ", "نافذ ", "خلص: ", "خلصان: "]:
        if msg_lower.startswith(prefix):
            target_name = msg[len(prefix):].strip()
            item = db.query(MenuItem).filter(MenuItem.name.ilike(f"%{target_name}%")).first()
            if item:
                item.is_available = False
                db.commit()
                return f"تم يا فندم! ❌ تم إيقاف صنف ({item.name} - {item.category}) اليوم.\nالبوت سيعتذر لأي عميل يطلبه ويقترح عليه بديلاً متاحاً فوراً."
            return f"عذراً يا فندم، لم أجد صنفاً بالاسم ({target_name}). يرجى كتابة اسم الصنف بدقة كما في المنيو."

    # 2. أوامر إعادة تفعيل صنف (متاح / متوفر / شغال)
    for prefix in ["متاح ", "متوفر ", "شغال ", "رجع ", "متاح: ", "متوفر: "]:
        if msg_lower.startswith(prefix):
            target_name = msg[len(prefix):].strip()
            item = db.query(MenuItem).filter(MenuItem.name.ilike(f"%{target_name}%")).first()
            if item:
                item.is_available = True
                db.commit()
                return f"تم يا فندم! ✅ تم إعادة تفعيل صنف ({item.name} - {item.category}) وأصبح متاحاً للطلب مجدداً."
            return f"عذراً يا فندم، لم أجد صنفاً بالاسم ({target_name})."

    # 3. استعراض الأصناف المتوقفة
    if msg_lower in ["النافذ", "المخلصان", "الاصناف النافذة", "المنتهي", "الاصناف المنتهية"]:
        unavailable = db.query(MenuItem).filter(MenuItem.is_available.is_(False)).all()
        if not unavailable:
            return "جميع أصناف المنيو متاحة للطلب حالياً ولا يوجد أي صنف نافذ! ✅"
        lines = [f"- {it.name} ({it.category})" for it in unavailable]
        return "📋 الأصناف غير المتاحة اليوم:\n" + "\n".join(lines) + "\n\n💡 لإعادة تشغيل أي صنف اكتب:\nمتاح [اسم الصنف]"

    return None


def is_restaurant_open() -> bool:
    """المطعم يعمل يومياً من الساعة 3:00 عصراً (15:00) حتى الساعة 3:00 صباحاً (03:00)."""
    current_hour = datetime.now().hour
    return current_hour >= 15 or current_hour < 3


def handle_incoming_message(db: Session, customer_phone: str, user_message: str) -> str:
    msg = user_message.strip()
    msg_clean = re.sub(r'[\s\.\،\,\!\?]+', ' ', msg).lower()

    # 0. أوامر الكاشير السريعة لإيقاف وتفعيل الأصناف عبر الواتساب
    admin_reply = check_kitchen_admin_commands(db, customer_phone, user_message)
    if admin_reply:
        return admin_reply

    # 1. خدمة العملاء والتحويل لإدارة المطعم (Human Handover)
    contact_keywords = [
        "عايز اكلم حد", "عاوز اكلم حد", "كلم حد", "خدمة العملاء", "خدمه العملاء",
        "رقم الادارة", "رقم الإدارة", "اشتكي", "شكوى", "مدير", "بني ادم", "بني آدم",
        "حد يكلمني", "اتصل بيا", "اتصلوا بيا", "رقم التليفون", "رقم الفون", "رقم الدليفري"
    ]
    if any(k in msg_clean for k in contact_keywords):
        return (
            "📞 *خدمة عملاء وإدارة مطعم روستيكا:*\n"
            "يسعدنا تواصلك معنا مباشرة يا فندم في أي وقت!\n"
            "📱 هاتف / واتساب الإدارة: *01557095082*\n"
            "📍 العنوان: جرجا - شارع الساحة (أمام مدرسة التجارة).\n"
            "فريق العمل في خدمتك لمساعدتك والرد على أي استفسار فوراً ❤️"
        )

    # 2. فحص مواعيد العمل (من 3:00 م حتى 3:00 ص)
    if not is_restaurant_open():
        # السماح فقط بالاستفسارات عن المنيو أو العنوان أو مواعيد العمل
        allowed_inquiries = ["المنيو", "منيو", "مكانكم", "عنوانكم", "مواعيد", "شغالين", "لوكيشن"]
        if not any(k in msg_clean for k in allowed_inquiries):
            return (
                "أهلاً بيك في مطعم روستيكا ❤️\n"
                "المطعم مغلق حالياً 🌙\n"
                "⏰ مواعيد العمل الرسمية يومياً من **الساعة 3:00 عصراً حتى 3:00 صباحاً**.\n\n"
                "يسعدنا جداً استقبال طلبك وخدمتك فور فتح المطعم في تمام الساعة 3 عصراً! 🛵"
            )

    # 3. تتبع الأوردر
    tracking_reply = check_order_tracking(db, customer_phone, msg_clean)
    if tracking_reply:
        return tracking_reply

    # 4. الأسئلة الشائعة وموقع المطعم
    if any(q in msg_clean for q in ["مكانكم فين", "عنوانكم", "المكان فين", "اللوكيشن", "لوكيشن", "فين المطعم", "عنوان المطعم", "الموقع", "مكان المطعم"]):
        maps_link = os.getenv("GOOGLE_MAPS_URL", "https://maps.app.goo.gl/peeunLih4gD1nwyCA?g_st=ac")
        return (
            "📍 *عنوان مطعم روستيكا:*\n"
            "جرجا - شارع الساحة (أمام مدرسة التجارة).\n\n"
            f"🗺️ *رابط اللوكيشن على خرائط جوجل:*\n{maps_link}\n\n"
            "تنورنا في أي وقت! وتقدر تطلب دليفري من هنا مباشرة ويجيلك لحد عندك 🛵"
        )

    if any(q in msg_clean for q in ["مواعيد العمل", "شغالين لحد امتى", "بتفتحوا امتى", "الساعة كام"]):
        return "⏰ مواعيد العمل في مطعم روستيكا يومياً من الساعة 3:00 عصراً حتى 3:00 صباحاً.\nخدمة الدليفري متاحة طوال ساعات العمل 🛵"

    session = get_or_create_session(db, customer_phone)
    cart = parse_cart(session.current_cart)

    # 3. الإلغاء
    if any(k in msg_clean for k in ["الغاء الطلب", "إلغاء الطلب", "كنسل", "cancel", "الغاء"]):
        if cart or session.state != "idle":
            session.state = "idle"
            session.current_cart = "[]"
            session.delivery_address = None
            db.commit()
            return "تم إلغاء السلة وإعادة التعيين يا فندم. نتشرف بخدمتك في أي وقت ❤️ تحب تطلب إيه؟"

    # 4. ميزة التحقق من العنوان القديم للعميل (Returning Customer)
    if session.state == "awaiting_address_confirmation":
        saved_addr = get_last_saved_address(db, customer_phone)
        positive_answers = ["نعم", "ايوه", "تمام", "اه", "اوك", "نفس العنوان", "على نفس العنوان", "هو"]
        if any(w in msg_clean.split() for w in positive_answers) or msg_clean in ["نعم", "ايوه", "اه", "تمام"]:
            session.delivery_address = saved_addr
        else:
            # اعتبر الرسالة هي العنوان الجديد
            session.delivery_address = msg

        session.state = "awaiting_confirmation"
        db.commit()

        items_text, total = format_cart_summary(cart)
        return (
            f"🧾 *ملخص الفاتورة النهائية:*\n"
            f"━━━━━━━━━━━━━━━\n"
            f"{items_text}\n"
            f"━━━━━━━━━━━━━━━\n"
            f"💰 *الإجمالي:* {total:g} جنيه\n"
            f"🛵 *طريقة الاستلام:* دليفري\n"
            f"📍 *العنوان:* {session.delivery_address}\n"
            f"━━━━━━━━━━━━━━━\n"
            f"لإرسال الطلب للمطبخ فوراً، اكتب *تأكيد* (أو *1*)."
        )

    # 5. حالة انتظار إدخال العنوان الجديد
    if session.state == "awaiting_address":
        if len(msg) < 5:
            return "برجاء كتابة العنوان بالتفصيل يا فندم (اسم الشارع، علامة مميزة) لنتمكن من توصيل الطلب بدقة 📍"

        session.delivery_address = msg
        session.state = "awaiting_confirmation"
        db.commit()

        items_text, total = format_cart_summary(cart)
        return (
            f"🧾 *ملخص الفاتورة النهائية:*\n"
            f"━━━━━━━━━━━━━━━\n"
            f"{items_text}\n"
            f"━━━━━━━━━━━━━━━\n"
            f"💰 *الإجمالي:* {total:g} جنيه\n"
            f"🛵 *طريقة الاستلام:* دليفري\n"
            f"📍 *العنوان:* {msg}\n"
            f"━━━━━━━━━━━━━━━\n"
            f"لإرسال الطلب للمطبخ فوراً، اكتب *تأكيد* (أو *1*)."
        )

    # 6. حالة انتظار التأكيد النهائي
    if session.state == "awaiting_confirmation":
        confirm_words = ["تأكيد", "تاكيد", "تمام", "1", "اوك", "أكد", "اكيد", "نعم", "موافق", "اعتمد"]
        if any(w in msg_clean.split() for w in confirm_words) or msg_clean in ["1", "تمام", "تأكيد", "تاكيد"]:
            items_text, total = format_cart_summary(cart)

            new_order = Order(
                customer_phone=customer_phone,
                order_type=session.order_type or "دليفري",
                delivery_address=session.delivery_address,
                items_summary=items_text,
                total_price=total,
                status="Confirmed"
            )
            db.add(new_order)

            session.state = "idle"
            session.current_cart = "[]"
            session.delivery_address = None
            db.commit()
            db.refresh(new_order)

            notify_kitchen_new_order(new_order)

            return (
                f"🎉 *تم تأكيد طلبك بنجاح برقم #{new_order.id}!* 🎉\n\n"
                f"شيف روستيكا استلم الأوردر وجاري تجهيزه بكل حب وإتقان 🔥\n"
                f"سنقوم بإشعارك هنا على الواتساب أول ما يخرج مع طيار الدليفري 🛵.\n\n"
                f"شكراً لاختيارك مطعم روستيكا ❤️"
            )

    # 7. إذا اختار العميل دليفري (تطبيق ميزة العنوان السابق)
    if any(w in msg_clean for w in ["دليفري", "توصيل", "يوصل البيت", "ديليفري"]):
        if cart:
            session.order_type = "دليفري"
            saved_addr = get_last_saved_address(db, customer_phone)
            if saved_addr:
                session.state = "awaiting_address_confirmation"
                db.commit()
                return (
                    f"نورتنا تاني يا فندم ❤️\n"
                    f"تحب نوصلك على نفس عنوانك السابق المسجل لدينا:\n"
                    f"📍 *({saved_addr})*؟\n\n"
                    f"اكتب *نعم* للتأكيد، أو اكتب العنوان الجديد لو تحب تغييره."
                )
            else:
                session.state = "awaiting_address"
                db.commit()
                return "منورنا يا فندم! برجاء إرسال عنوان التوصيل بالتفصيل (اسم الشارع، رقم العمارة أو علامة مميزة) 📍"

    # 8. إذا اختار العميل استلام من الفرع
    if any(w in msg_clean for w in ["استلام من الفرع", "تيك اواي", "تيك أواي", "هاجي اخده", "هاخده بنفسي"]):
        if cart:
            session.order_type = "استلام من الفرع"
            session.state = "awaiting_confirmation"
            session.delivery_address = "استلام من المطعم (تيك أواي)"
            db.commit()
            items_text, total = format_cart_summary(cart)
            return (
                f"🧾 *ملخص طلبك (استلام من الفرع):*\n"
                f"━━━━━━━━━━━━━━━\n"
                f"{items_text}\n"
                f"━━━━━━━━━━━━━━━\n"
                f"💰 *الإجمالي:* {total:g} جنيه\n"
                f"🏃‍♂️ *الاستلام:* من فرع جرجا - شارع الساحة (أمام مدرسة التجارة)\n"
                f"━━━━━━━━━━━━━━━\n"
                f"لتأكيد الطلب اكتب *تأكيد* (أو *1*)."
            )

    # 9. الذكاء الاصطناعي لفهم الطلبات مع استثناء الأصناف غير المتاحة (Out-of-Stock)
    return process_ai_ordering(db, session, cart, msg)


def get_dynamic_menu_text(db: Session) -> str:
    """استرجاع المنيو المحدث لحظياً من قاعدة البيانات ليعكس أي تعديل في الأسعار أو إضافة أصناف فوراً."""
    items = db.query(MenuItem).filter(MenuItem.is_available.is_(True)).all()
    if not items:
        return get_menu_text()

    grouped = {}
    for item in items:
        grouped.setdefault(item.category, []).append(item)

    lines = ["قائمة طعام مطعم روستيكا (جرجا - شارع الساحة أمام مدرسة التجارة). الأسعار بالجنيه المصري.", ""]
    for category, category_items in grouped.items():
        lines.append(f"{category}:")
        for item in category_items:
            extra = f" - {item.description}" if item.description else ""
            lines.append(f"- {item.name}: {item.price:g} جنيه{extra}")
        lines.append("")

    lines.append("لو العميل ما حددش الحجم، اسأله على الحجم قبل تأكيد السعر.")
    lines.append("لا تخترع أصناف أو أسعار غير موجودة فوق.")
    return "\n".join(lines)


def process_ai_ordering(db: Session, session: CustomerSession, cart: list, user_message: str) -> str:
    menu_context = get_dynamic_menu_text(db)
    unavailable_context = get_unavailable_items_text(db)
    cart_summary, current_total = format_cart_summary(cart)

    system_prompt = f"""أنت موظف استقبال واستلام طلبات ذكي وودود في "مطعم روستيكا" بجرجا - سوهاج.
تتحدث باللغة العربية بلهجة مصرية محترمة وبسيطة.

المنيو المتاح بدقة:
{menu_context}

{unavailable_context}

السلة الحالية للعميل:
{cart_summary} (المجموع: {current_total:g} جنيه)

مهمتك:
1. إذا كان العميل يحيي أو يسأل عن المنيو، رد بود واعرض له الأقسام والأصناف المناسبة.
2. هام جداً: إذا طلب العميل أي صنف من الأصناف المذكورة أعلاه أنها (غير متاحة / نافذة من المطبخ)، اعتذر له بلباقة واذكر أنها خلصت اليوم واقترح بديلاً متاحاً، ولا تضف الصنف المنتهي للسلة.
3. إذا طلب أصنافاً متاحة، استخرج الصنف والكمية والحجم والسعر بدقة من المنيو.
4. إذا كان الصنف له أحجام (صغير/وسط/كبير) ولم يحدد العميل الحجم، اسأله عن الحجم المفضل وسعره.
5. بعد إضافة الأصناف للسلة، اقترح بلباقة إضافة بطاطس أو بيبسي (Upselling) واسأله: "تحب نأكد الطلب دليفري 🛵 ولا استلام من المطعم 🏃‍♂️؟".
6. يجب أن تجيب دائماً بصيغة JSON فقط كالتالي:
{{
  "reply": "الرد الذي سيرسل للعميل بالعامية المصرية",
  "new_items": [
    {{"name": "اسم الصنف", "size": "الحجم إن وجد", "quantity": 1, "price": 100}}
  ]
}}
إذا لم يطلب أصناف جديدة جديدة اجعل "new_items" مصفوفة فارغة [].
"""

    try:
        completion = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
            response_format={"type": "json_object"},
            temperature=0.4
        )

        raw_content = completion.choices[0].message.content
        data = json.loads(raw_content)

        new_items = data.get("new_items", [])
        if new_items:
            for ni in new_items:
                cart.append({
                    "name": ni.get("name"),
                    "size": ni.get("size", ""),
                    "quantity": int(ni.get("quantity", 1)),
                    "price": float(ni.get("price", 0))
                })
            session.current_cart = json.dumps(cart, ensure_ascii=False)
            session.state = "ordering"
            db.commit()

        return data.get("reply", "أهلاً بيك في مطعم روستيكا! تحب تطلب إيه اليوم؟ ❤️")

    except Exception as e:
        print(f"[AI Ordering Error]: {e}", flush=True)
        return "أهلاً بك في مطعم روستيكا ❤️ يمكنك كتابة ما ترغب بطلبه بالتفصيل (مثل: 2 كريب ميكس جبن و1 بيبسي) وسأقوم بحساب الفاتورة لك فوراً!"
