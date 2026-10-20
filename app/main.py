import os
from typing import Optional
from datetime import datetime, date

from fastapi import Depends, FastAPI, Form, HTTPException
from fastapi.responses import HTMLResponse, FileResponse, Response
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import desc, func

from app.database import Base, engine, get_db, auto_migrate, SessionLocal
from app.menu_data import get_menu_text
from app.models import MenuItem, Order, CustomerSession
from app.services.order_service import handle_incoming_message, transcribe_voice_note
from app.services.whatsapp_service import notify_customer_status_change
from app.services.ai_service import get_restaurant_ai_response
from app.seed import seed_menu

# إنشاء جداول قاعدة البيانات والترقية التلقائية للأعمدة
Base.metadata.create_all(bind=engine)
auto_migrate()

# ملء قاعدة البيانات بالمنيو تلقائياً لو كانت جديدة أو فارغة
try:
    with SessionLocal() as _db:
        if _db.query(MenuItem).count() == 0:
            print("🌱 [Auto-seed]: قاعدة البيانات فارغة، جاري تحميل منيو روستيكا تلقائياً...", flush=True)
            seed_menu()
except Exception as _e:
    print(f"⚠️ [Auto-seed Note]: {_e}", flush=True)

app = FastAPI(title="Rostica Restaurant AI Bot & Dashboard")


class ChatRequest(BaseModel):
    message: Optional[str] = ""
    customer_phone: Optional[str] = "غير محدد"
    audio_base64: Optional[str] = None
    mimetype: Optional[str] = "audio/ogg"


class MenuItemCreate(BaseModel):
    name: str
    category: str
    price: float
    description: Optional[str] = None
    is_available: Optional[bool] = True


class MenuItemUpdate(BaseModel):
    name: Optional[str] = None
    category: Optional[str] = None
    price: Optional[float] = None
    description: Optional[str] = None
    is_available: Optional[bool] = None


# ==========================================
# 1. لوحة تحكم المطبخ والكاشير (Dashboard UI)
# ==========================================
@app.get("/dashboard", response_class=HTMLResponse)
def get_dashboard():
    dashboard_path = os.path.join(os.path.dirname(__file__), "templates", "dashboard.html")
    if os.path.exists(dashboard_path):
        return FileResponse(dashboard_path)
    return "<h1>قالب لوحة التحكم غير موجود</h1>"


# ==========================================
# 2. واجهات برمجة الطلبات للوحة التحكم (API)
# ==========================================
@app.get("/api/orders")
def get_orders_api(db: Session = Depends(get_db)):
    orders = db.query(Order).order_by(desc(Order.created_at)).limit(100).all()

    # إحصائيات سريعة
    total_orders = len(orders)
    total_sales = sum(o.total_price for o in orders if o.status != "Cancelled")
    in_prep = sum(1 for o in orders if o.status == "In_Preparation")
    out_delivery = sum(1 for o in orders if o.status == "Out_For_Delivery")

    orders_list = []
    for o in orders:
        orders_list.append({
            "id": o.id,
            "customer_phone": o.customer_phone,
            "customer_name": o.customer_name or "عميل روستيكا",
            "order_type": o.order_type or "دليفري",
            "delivery_address": o.delivery_address,
            "items_summary": o.items_summary,
            "total_price": o.total_price,
            "status": o.status,
            "created_at": o.created_at.strftime("%I:%M %p") if o.created_at else "",
            "created_date": o.created_at.strftime("%Y-%m-%d") if o.created_at else ""
        })

    return {
        "orders": orders_list,
        "stats": {
            "total_orders": total_orders,
            "total_sales": total_sales,
            "in_prep": in_prep,
            "out_delivery": out_delivery
        }
    }


@app.post("/api/orders/{order_id}/status")
def update_order_status(order_id: int, status: str, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    order.status = status
    db.commit()

    # إرسال إشعار تلقائي للعميل عبر الواتساب بتحديث الحالة
    notify_customer_status_change(order)

    return {"status": "success", "new_status": status, "order_id": order_id}


# ==========================================
# 3. إدارة الأصناف وإيقاف النافذ (Out-of-Stock)
# ==========================================
@app.get("/api/menu-items")
def get_all_menu_items(db: Session = Depends(get_db)):
    items = db.query(MenuItem).order_by(MenuItem.category, MenuItem.name).all()
    return [
        {
            "id": item.id,
            "name": item.name,
            "category": item.category,
            "price": item.price,
            "is_available": item.is_available,
        }
        for item in items
    ]


@app.post("/api/menu-items/{item_id}/toggle")
def toggle_menu_item_availability(item_id: int, db: Session = Depends(get_db)):
    item = db.query(MenuItem).filter(MenuItem.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    item.is_available = not item.is_available
    db.commit()

@app.post("/api/menu-items")
def create_menu_item(item_data: MenuItemCreate, db: Session = Depends(get_db)):
    """إضافة صنف جديد للمنيو بواسطة صاحب المطعم."""
    new_item = MenuItem(
        name=item_data.name.strip(),
        category=item_data.category.strip(),
        price=float(item_data.price),
        description=item_data.description.strip() if item_data.description else None,
        is_available=item_data.is_available if item_data.is_available is not None else True,
    )
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return {
        "status": "success",
        "item": {
            "id": new_item.id,
            "name": new_item.name,
            "category": new_item.category,
            "price": new_item.price,
            "is_available": new_item.is_available,
            "description": new_item.description,
        }
    }


@app.put("/api/menu-items/{item_id}")
def update_menu_item(item_id: int, item_data: MenuItemUpdate, db: Session = Depends(get_db)):
    """تعديل اسم أو سعر أو قسم صنف موجود في المنيو."""
    item = db.query(MenuItem).filter(MenuItem.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    if item_data.name is not None and item_data.name.strip():
        item.name = item_data.name.strip()
    if item_data.category is not None and item_data.category.strip():
        item.category = item_data.category.strip()
    if item_data.price is not None:
        item.price = float(item_data.price)
    if item_data.description is not None:
        item.description = item_data.description.strip() if item_data.description else None
    if item_data.is_available is not None:
        item.is_available = item_data.is_available

    db.commit()
    db.refresh(item)
    return {
        "status": "success",
        "item": {
            "id": item.id,
            "name": item.name,
            "category": item.category,
            "price": item.price,
            "is_available": item.is_available,
            "description": item.description,
        }
    }


@app.delete("/api/menu-items/{item_id}")
def delete_menu_item(item_id: int, db: Session = Depends(get_db)):
    """حذف صنف من المنيو نهائياً."""
    item = db.query(MenuItem).filter(MenuItem.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    db.delete(item)
    db.commit()
    return {"status": "success", "deleted_id": item_id}


# ==========================================
# 4. استقبال ومعالجة رسائل الواتساب والريكوردات
# ==========================================
@app.post("/order")
def create_order_from_chat(request: ChatRequest, db: Session = Depends(get_db)):
    """يستقبل الرسائل من جسر الواتساب ويدعم النصوص والريكوردات الصوتية (Whisper)."""
    user_message = request.message or ""

    # لو الرسالة ريكورد صوتي، نقوم بتفريغها أولاً
    if request.audio_base64:
        print(f"🎙️ [سيرفر بايثون]: تم استلام ملف صوتي بحجم {len(request.audio_base64)} بايت ونوع {request.mimetype}", flush=True)
        transcription = transcribe_voice_note(request.audio_base64, request.mimetype or "audio/ogg")
        if transcription:
            print(f"✅ [تفريغ الصوت]: {transcription}", flush=True)
            user_message = transcription
        else:
            return {
                "status": "success",
                "reply": "عذراً يا فندم، لم أتمكن من سماع التسجيل الصوتي بوضوح. برجاء إعادة إرسال الريكورد أو كتابة طلبك نصياً وسأساعدك فوراً ❤️"
            }

    reply = handle_incoming_message(db, request.customer_phone, user_message)
    return {
        "status": "success",
        "reply": reply
    }


# ==========================================
# 5. عرض المنيو
# ==========================================
@app.get("/menu")
def get_menu(db: Session = Depends(get_db)):
    items = db.query(MenuItem).filter(MenuItem.is_available.is_(True)).all()
    if not items:
        return {"source": "file", "menu": get_menu_text()}

    grouped = {}
    for item in items:
        grouped.setdefault(item.category, []).append(
            {
                "id": item.id,
                "name": item.name,
                "price": item.price,
                "description": item.description,
            }
        )
    return {"source": "database", "categories": grouped}


@app.post("/whatsapp")
async def whatsapp_webhook(
    Body: str = Form(...), From: str = Form(...), db: Session = Depends(get_db)
):
    reply = handle_incoming_message(db, From, Body)
    twiml_response = f"""<Response><Message>{reply}</Message></Response>"""
    return Response(content=twiml_response, media_type="application/xml")
