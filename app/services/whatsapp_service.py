import os
import requests
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

WHATSAPP_BRIDGE_URL = os.getenv("WHATSAPP_BRIDGE_URL", "http://127.0.0.1:3001/send-message")
KITCHEN_PHONE = os.getenv("KITCHEN_PHONE")  # e.g., "201012345678" or group id
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")


def send_whatsapp_message(to_phone: str, text: str) -> bool:
    """Send an outbound WhatsApp message via the local Node.js bridge."""
    try:
        response = requests.post(
            WHATSAPP_BRIDGE_URL,
            json={"to": to_phone, "message": text},
            timeout=5
        )
        return response.status_code == 200
    except Exception as e:
        print(f"[WhatsApp Bridge Send Error]: {e}", flush=True)
        return False


def send_telegram_alert(text: str) -> bool:
    """Optionally send alert to Telegram group/bot if configured."""
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        return False
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        res = requests.post(url, json={"chat_id": TELEGRAM_CHAT_ID, "text": text, "parse_mode": "Markdown"}, timeout=5)
        return res.status_code == 200
    except Exception as e:
        print(f"[Telegram Alert Error]: {e}", flush=True)
        return False


def notify_kitchen_new_order(order) -> None:
    """Notify the kitchen/cashier of a newly confirmed order."""
    time_str = datetime.now().strftime("%I:%M %p")
    clean_phone = order.customer_phone.split('@')[0] if order.customer_phone else "غير محدد"
    msg = (
        f"🚨 *أوردر جديد للنقل في الورقة 📝* 🚨\n"
        f"━━━━━━━━━━━━━━━\n"
        f"📋 *رقم الأوردر:* #{order.id}\n"
        f"📱 *رقم العميل:* {clean_phone}\n"
        f"🛵 *نوع الطلب:* {order.order_type}\n"
        f"📍 *العنوان:* {order.delivery_address or 'استلام من الفرع'}\n"
        f"━━━━━━━━━━━━━━━\n"
        f"🛒 *الأصناف المطلوبة:*\n{order.items_summary}\n"
        f"━━━━━━━━━━━━━━━\n"
        f"💰 *المبلغ المطلوب تحصيله:* {order.total_price:g} جنيه\n"
        f"⏰ *الوقت:* {time_str}\n"
        f"━━━━━━━━━━━━━━━"
    )

    # 1. Send to kitchen WhatsApp if configured
    if KITCHEN_PHONE:
        send_whatsapp_message(KITCHEN_PHONE, msg)

    # 2. Send to Telegram if configured
    if TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID:
        send_telegram_alert(msg)

    print(f"[Kitchen Alert]: Order #{order.id} notification dispatched.", flush=True)


def notify_customer_status_change(order) -> bool:
    """Send status update to customer on WhatsApp when cashier updates order."""
    status_messages = {
        "In_Preparation": f"👨‍🍳 طلبك رقم #{order.id} شيف روستيكا بدأ في تحضيره حالياً بأعلى جودة وسخونة! 🔥",
        "Out_For_Delivery": f"🛵💨 طلبك رقم #{order.id} خرج الآن مع طيار الدليفري وفي الطريق إليك! جهز نفسك لوجبة مميزة من روستيكا ❤️",
        "Delivered": f"✅ تم تسليم طلبك رقم #{order.id} بنجاح! بالهنا والشفا، ويسعدنا دائماً خدمتك في مطعم روستيكا ❤️",
        "Cancelled": f"❌ تم إلغاء طلبك رقم #{order.id}. لأي استفسار يسعدنا تواصلك معنا دائماً."
    }

    text = status_messages.get(order.status)
    if text and order.customer_phone:
        return send_whatsapp_message(order.customer_phone, text)
    return False
