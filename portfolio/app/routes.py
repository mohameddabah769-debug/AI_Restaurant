"""
Routes and Endpoints for Eng. Mohamed Dabah Portfolio
Equipped with Rate Limiting, Input Sanitization, WhatsApp Dispatch & Local Archive
"""

import time
import html
import json
import urllib.parse
from datetime import datetime
from collections import defaultdict
from pathlib import Path
import httpx
from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates

from .config import PROFILE, SOCIAL_CHANNELS, PROJECTS, SKILLS_CATEGORIES

router = APIRouter()

BASE_DIR = Path(__file__).resolve().parent
templates_path = BASE_DIR / "templates"
templates = Jinja2Templates(directory=str(templates_path))
MESSAGES_LOG_FILE = BASE_DIR / "messages.json"

# Mohamed's phone configuration
ADMIN_WHATSAPP_PHONE = "201095744676"
LOCAL_WHATSAPP_BRIDGE = "http://127.0.0.1:3001/send-message"

# In-Memory Rate Limiting per IP for Contact Form (Max 5 requests per 10 minutes)
IP_REQUEST_LOG = defaultdict(list)
MAX_REQUESTS_PER_WINDOW = 5
WINDOW_SECONDS = 600

def check_rate_limit(client_ip: str) -> bool:
    now = time.time()
    timestamps = [ts for ts in IP_REQUEST_LOG[client_ip] if now - ts < WINDOW_SECONDS]
    IP_REQUEST_LOG[client_ip] = timestamps
    if len(timestamps) >= MAX_REQUESTS_PER_WINDOW:
        return False
    IP_REQUEST_LOG[client_ip].append(now)
    return True

def archive_message(msg_data: dict):
    """Safely archive message locally in JSON so no inquiries are lost."""
    try:
        data = []
        if MESSAGES_LOG_FILE.exists():
            with open(MESSAGES_LOG_FILE, "r", encoding="utf-8") as f:
                try:
                    data = json.load(f)
                except Exception:
                    data = []
        data.append(msg_data)
        with open(MESSAGES_LOG_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"[Archive Error]: {e}")

async def dispatch_whatsapp_notification(name: str, email: str, phone: str, message: str):
    """
    Attempts to send immediate WhatsApp alert to Eng. Mohamed Dabah's phone via bridge.
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %I:%M %p")
    alert_text = (
        f"🚨 *إشعار رسالة جديدة من موقعك (Portfolio)* 🚀\n"
        f"━━━━━━━━━━━━━━━━━━\n"
        f"👤 *المرسل:* {name}\n"
        f"📧 *البريد:* {email}\n"
        f"📱 *الهاتف:* {phone or 'غير مسجل'}\n"
        f"💬 *نص الرسالة:*\n{message}\n"
        f"━━━━━━━━━━━━━━━━━━\n"
        f"🕒 *التوقيت:* {timestamp}"
    )

    try:
        async with httpx.AsyncClient(timeout=3.0) as client:
            res = await client.post(
                LOCAL_WHATSAPP_BRIDGE,
                json={"to": ADMIN_WHATSAPP_PHONE, "message": alert_text}
            )
            if res.status_code == 200:
                print(f"✅ WhatsApp notification delivered to {ADMIN_WHATSAPP_PHONE}")
                return True
    except Exception:
        # Bridge might be offline or sleeping; message is still saved in JSON archive
        pass
    return False

@router.get("/", response_class=HTMLResponse)
async def home_page(request: Request):
    """
    Renders the main 3D interactive portfolio page.
    """
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "profile": PROFILE,
            "social_channels": SOCIAL_CHANNELS,
            "projects": PROJECTS,
            "skills_categories": SKILLS_CATEGORIES,
        }
    )

@router.post("/api/contact")
async def contact_form(
    request: Request,
    name: str = Form(...),
    email: str = Form(...),
    phone: str = Form(""),
    message: str = Form(...)
):
    """
    Handles visitor contact inquiries:
    1. Rate limiting & sanitization
    2. Archiving to messages.json
    3. Auto-forwarding alert to Mohamed Dabah's WhatsApp
    4. Returning direct WhatsApp pre-filled chat link
    """
    client_ip = request.client.host if request.client else "unknown"

    # 1. Rate Limiting Check
    if not check_rate_limit(client_ip):
        return JSONResponse(
            status_code=429,
            content={
                "status": "error",
                "message": "عذراً، لقد قمت بإرسال عدد كبير من الرسائل. يرجى الانتظار بضع دقائق أو مراسلتي عبر واتساب مباشرة."
            }
        )

    # 2. Input Sanitization
    clean_name = html.escape(name.strip())[:100]
    clean_email = html.escape(email.strip())[:150]
    clean_phone = html.escape(phone.strip())[:50]
    clean_message = html.escape(message.strip())[:2000]

    if len(clean_name) < 2 or len(clean_message) < 5:
        return JSONResponse(
            status_code=400,
            content={
                "status": "error",
                "message": "يرجى التأكد من كتابة الاسم وتفاصيل الرسالة بشكل صحيح."
            }
        )

    # 3. Archive Locally
    msg_record = {
        "timestamp": datetime.now().isoformat(),
        "name": clean_name,
        "email": clean_email,
        "phone": clean_phone,
        "message": clean_message,
        "client_ip": client_ip,
    }
    archive_message(msg_record)

    # 4. Dispatch WhatsApp Alert to Mohamed's Phone (+201095744676)
    await dispatch_whatsapp_notification(clean_name, clean_email, clean_phone, clean_message)

    # 5. Generate direct WhatsApp URL for visitor
    encoded_text = urllib.parse.quote(
        f"مرحباً بشمهندس محمد، أنا {clean_name}.\nأرسلت لك عبر موقعك:\n\"{clean_message}\""
    )
    direct_wa_url = f"https://wa.me/{ADMIN_WHATSAPP_PHONE}?text={encoded_text}"

    return JSONResponse({
        "status": "success",
        "message": f"شكراً لك يا {clean_name}! تم استلام رسالتك وتوجيه إشعار للبشمهندس محمد دباح فوراً.",
        "whatsapp_url": direct_wa_url
    })
