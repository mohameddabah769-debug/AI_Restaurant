import os
from dotenv import load_dotenv
from openai import OpenAI  # استخدام مكتبة OpenAI للاتصال بـ Groq

load_dotenv()

# إعداد عميل Groq باستخدام مفتاح الـ API الخاص بـ Groq
client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1",
)


def get_restaurant_ai_response(user_message: str, menu_context: str) -> str:
    message = user_message.strip().lower()

    # ردود مباشرة من غير استخدام الذكاء الاصطناعي
    greetings = [
        "السلام عليكم",
        "السلام عليكم ورحمة الله",
        "السلام عليكم ورحمة الله وبركاته",
        "سلام عليكم",
        "اهلا",
        "أهلا",
        "اهلا وسهلا",
        "أهلاً وسهلاً",
        "صباح الخير",
        "مساء الخير",
        "هاي",
        "hello",
        "hi",
    ]

    if message in greetings:
        if "صباح الخير" in message:
            return "صباح النور ❤️ أهلاً بيك في مطعم روستيكا، تحب تطلب إيه؟"

        if "مساء الخير" in message:
            return "مساء النور ❤️ نورت مطعم روستيكا، تحب تطلب إيه؟"

        return "وعليكم السلام ورحمة الله وبركاته ❤️ أهلاً بيك في مطعم روستيكا، نورتنا! تحب تطلب إيه؟"

    # الرد على الشكر من غير استخدام الذكاء الاصطناعي
    if message in ["شكرا", "شكرًا", "متشكر", "تسلم", "تسلم ايدك"]:
        return "العفو يا فندم ❤️ ده من ذوقك، ونورت مطعم روستيكا!"

    # باقي الرسائل تستخدم نموذج Groq
    try:
        completion = client.chat.completions.create(
            # يمكنك استخدام llama-3.3-70b-versatile أو llama-3.1-8b-instant وهي مجانية وسريعة جداً
            model="openai/gpt-oss-120b",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "أنت موظف خدمة عملاء في مطعم روستيكا في جرجا.\n"
                        "رد باللغة العربية وبأسلوب مصري بسيط وودود.\n"
                        "لو العميل بيسأل عن المنيو، اعرض الأقسام والأصناف والأسعار الموجودة فقط.\n"
                        "لو الصنف له أحجام (صغير/وسط/كبير) اذكر الأسعار حسب الحجم.\n"
                        "احسب الإجمالي بدقة من أسعار المنيو، ولو الحجم مش واضح اسأل العميل.\n"
                        "لا تخترع أصناف أو أسعارًا غير موجودة في المنيو."
                    ),
                },
                {
                    "role": "user",
                    "content": f"المنيو:\n{menu_context}\n\nرسالة العميل:\n{user_message}",
                },
            ],
            temperature=0.7,
        )

        response_text = completion.choices[0].message.content
        if response_text:
            return response_text

        return "أهلًا بيك في مطعم روستيكا ❤️ ممكن توضح طلبك؟"

    except Exception as e:
        print(f"خطأ Groq: {repr(e)}", flush=True)
        return "أهلًا بيك في مطعم روستيكا ❤️ خدمة الرد الذكي مش متاحة مؤقتًا. تقدر تسألنا عن المنيو أو تحاول تاني بعد شوية."