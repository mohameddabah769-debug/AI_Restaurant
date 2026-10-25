"""
Configuration and Profile Data for Eng. Mohamed Dabah Portfolio
"""

PROFILE = {
    "name": "ENG / MOHAMED DABAH",
    "short_name": "Mohamed Dabah",
    "title": "Computer Engineer 💻 | AI & Software Systems",
    "status": "Available for High-Impact Projects",
    "tagline": "Computer Engineer specializing in AI Systems, Intelligent Automation & 3D Web",
    "bio": (
        "مهندس حاسبات وبرمجيات (Computer Engineer) متخصص في بناء الأنظمة الذكية المستقلة (AI Agents)، "
        "روبوتات الأعمال وأتمتة الواتساب، وتطوير تطبيقات الويب ثلاثية الأبعاد الفاخرة "
        "بأعلى معايير السرعة والأداء."
    ),
    "experience_years": "3+",
    "completed_projects": "25+",
    "happy_clients": "100%",
    "phone": "+20109574467",
    "email": "contact@mohamed-dabah.tech",
    "location": "Cairo, Egypt",
}

SOCIAL_CHANNELS = [
    {
        "id": "whatsapp",
        "name": "WhatsApp",
        "title": "محادثة فورية عبر واتساب",
        "handle": "+20 109 574 467",
        "url": "https://wa.me/20109574467?text=مرحباً%20بشمهندس%20محمد،%20اطلعت%20على%20أعمالك%20وأود%20التواصل%20معك",
        "icon": "message-circle",
        "color": "#25D366",
        "qr_file": "qr_whatsapp.png",
        "badge": "Direct Chat",
    },
    {
        "id": "facebook",
        "name": "Facebook",
        "title": "الصفحة الشخصية على فيسبوك",
        "handle": "Mohamed Dabah",
        "url": "https://www.facebook.com/share/1HBcw7nEo6/",
        "icon": "facebook",
        "color": "#1877F2",
        "qr_file": "qr_facebook.png",
        "badge": "Official Profile",
    },
    {
        "id": "linkedin",
        "name": "LinkedIn",
        "title": "الملف المهني على لينكد إن",
        "handle": "mohamed-mustafa-8a9042445",
        "url": "https://www.linkedin.com/in/mohamed-mustafa-8a9042445?utm_source=share_via&utm_content=profile&utm_medium=member_android",
        "icon": "linkedin",
        "color": "#0A66C2",
        "qr_file": "qr_linkedin.png",
        "badge": "Professional",
    },
    {
        "id": "instagram",
        "name": "Instagram",
        "title": "حساب إنستغرام",
        "handle": "@deboo__1",
        "url": "https://www.instagram.com/deboo__1?mdxt=MjRpZnlwYmRieml3",
        "icon": "instagram",
        "color": "#E4405F",
        "qr_file": "qr_instagram.png",
        "badge": "Connect",
    },
]

PROJECTS = [
    {
        "id": "ai-restaurant",
        "title": "AI Restaurant & WhatsApp Bot",
        "arabic_title": "نظام المطعم الذكي وروبوت الواتساب التفاعلي",
        "category": "AI & Automation",
        "featured": True,
        "description": "منظومة متطورة مدعومة بالذكاء الاصطناعي لأتمتة طلبات المطاعم وإدارة المنيو والتوصيل بالكامل عبر واتساب مع واجهة لوحة تحكم تفاعلية.",
        "highlights": [
            "معالجة لغة طبيعية لفهم طلبات العملاء بالعامية المصرية",
            "سيرفر FastAPI فائق السرعة مع قاعدة بيانات للطلبات",
            "ربط مباشر مع WhatsApp Cloud / Bridge",
            "لوحة تحكم حية لمتابعة الإحصائيات والمبيعات"
        ],
        "technologies": ["Python", "FastAPI", "Generative AI", "WhatsApp API", "SQLite/Postgres"],
        "icon": "bot",
        "color": "#00f0ff",
    },
    {
        "id": "autonomous-agents",
        "title": "Autonomous Multi-Agent AI Engine",
        "arabic_title": "محرك عملاء الذكاء الاصطناعي المستقلة",
        "category": "AI & LLMs",
        "featured": True,
        "description": "نظام متعدد الوكلاء (Agents) يقوم بتحليل المهام وتوزيعها ذاتياً واتخاذ القرارات الذكية للأعمال المعقدة بدون تدخل بشري.",
        "highlights": [
            "وكلاء تفاعليون للبحث والتنفيذ والتحقق",
            "تكامل مع نماذج الذكاء الاصطناعي الأحدث",
            "معالجة متزامنة غير متزامنة Async Pipeline"
        ],
        "technologies": ["Python", "LangChain", "OpenAI / Gemini", "Vector DB", "AsyncIO"],
        "icon": "cpu",
        "color": "#8b5cf6",
    },
    {
        "id": "3d-interactive-web",
        "title": "Immersive 3D Web & Visualizer",
        "arabic_title": "تطبيقات الويب التفاعلية ثلاثية الأبعاد",
        "category": "3D & Frontend",
        "featured": True,
        "description": "واجهات وتجارب رقمية سينمائية تعتمد على Three.js و WebGL تقدم مجسمات 3D تفاعلية تنبض بالحياة مع تفاعل الماوس واللمس.",
        "highlights": [
            "محرك جرافيكس خفيف الوزن Three.js",
            "مؤثرات Glassmorphism وإضاءات نيون ديناميكية",
            "أداء 60+ FPS على الموبايل وأجهزة سطح المكتب"
        ],
        "technologies": ["Three.js", "WebGL", "Modern JavaScript", "Tailwind CSS"],
        "icon": "box",
        "color": "#ec4899",
    },
    {
        "id": "smart-vision-system",
        "title": "Smart Computer Vision Analytics",
        "arabic_title": "نظام الرؤية الحاسوبية والتحليل البصري الذكي",
        "category": "Computer Vision",
        "featured": False,
        "description": "حلول متقدمة للتعرف على الأشخاص والوجوه وتتبع العناصر واستخراج البيانات في الزمن الحقيقي من كاميرات المراقبة والفيديو.",
        "highlights": [
            "اكتشاف وتتبع دقيق للوجوه والأنماط",
            "معالجة الفيديو Real-time Video Stream",
            "تنبيهات فورية وتحليلات إحصائية"
        ],
        "technologies": ["Python", "OpenCV", "PyTorch", "YOLOv8"],
        "icon": "eye",
        "color": "#f59e0b",
    },
]

SKILLS_CATEGORIES = [
    {
        "name": "Artificial Intelligence & Agents",
        "arabic_name": "الذكاء الاصطناعي والعملاء الأذكياء",
        "skills": ["LLMs & Prompt Engineering", "AI Autonomous Agents", "LangChain / AI Pipelines", "Computer Vision (OpenCV)", "Conversational AI & NLP"]
    },
    {
        "name": "Backend & System Architecture",
        "arabic_name": "الأنظمة الخلفية وقواعد البيانات",
        "skills": ["Python (Expert)", "FastAPI & High-Speed APIs", "Flask & Django", "PostgreSQL & SQLite", "WebSockets & Async Systems"]
    },
    {
        "name": "3D & Modern Frontend",
        "arabic_name": "الواجهات التفاعلية والـ 3D",
        "skills": ["Three.js & WebGL", "Interactive 3D Canvases", "Glassmorphism & Cyber Design", "Responsive Web Apps", "Dynamic Animations"]
    },
    {
        "name": "Automation & Integration",
        "arabic_name": "الأتمتة والربط السحابي",
        "skills": ["WhatsApp Business Automation", "REST APIs & Webhooks", "Docker & Deployment", "Git & CI/CD", "Third-party Integrations"]
    }
]
