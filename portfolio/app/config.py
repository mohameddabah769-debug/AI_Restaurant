"""
Configuration and Profile Data for Eng. Mohamed Dabah Portfolio
"""

PROFILE = {
    "name": "ENG / MOHAMED DABAH",
    "short_name": "Mohamed Dabah",
    "title": "Computer Engineer 💻 | AI & Software Systems",
    "status": "Available for High-Impact Projects",
    "tagline": "Computer Engineer specializing in Enterprise Software, AI Automation, E-Commerce & 3D Web",
    "bio": (
        "مهندس حاسبات وبرمجيات (Computer Engineer) متخصص في بناء وتطوير الأنظمة البرمجية المتكاملة للشركات، "
        "مواقع التجارة الإلكترونية، أنظمة الذكاء الاصطناعي وأتمتة الواتساب، وحلول المحافظ الرقمية والحجوزات الذكية "
        "بأعلى معايير الأمان والسرعة."
    ),
    "experience_years": "3+",
    "completed_projects": "30+",
    "happy_clients": "100%",
    "phone": "+201095744676",
    "email": "contact@mohamed-dabah.tech",
    "location": "Cairo, Egypt",
}

SOCIAL_CHANNELS = [
    {
        "id": "whatsapp",
        "name": "WhatsApp",
        "title": "محادثة فورية عبر واتساب",
        "handle": "+20 109 574 4676",
        "url": "https://wa.me/201095744676?text=مرحباً%20بشمهندس%20محمد،%20اطلعت%20على%20أعمالك%20وأود%20طلب%20مشروع",
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
        "badge": "AI Powered",
        "description": "منظومة متطورة مدعومة بالذكاء الاصطناعي لأتمتة طلبات المطاعم وإدارة المنيو والتوصيل بالكامل عبر واتساب مع لوحة تحكم إدارية فورية.",
        "highlights": [
            "معالجة لغة طبيعية تفهم طلبات العملاء بالعامية المصرية",
            "سيرفر FastAPI فائق السرعة مع قاعدة بيانات للطلبات",
            "ربط مباشر مع WhatsApp Cloud / Bridge",
            "لوحة تحكم حية لمتابعة الإحصائيات والمبيعات"
        ],
        "technologies": ["Python", "FastAPI", "Generative AI", "WhatsApp API", "SQLite/Postgres"],
        "color": "#00f0ff",
    },
    {
        "id": "invoices-inventory-sales",
        "title": "Enterprise Invoices, Sales & Inventory System",
        "arabic_title": "منظومة إدارة المخازن والفواتير والمبيعات للشركات",
        "category": "Business Systems",
        "badge": "ERP Solution",
        "description": "نظام محاسبي وإداري متكامل لإدارة حركة المخزون، إصدار فواتير البيع والشراء الإلكترونية، وتتبع الأرباح وحسابات الموردين والعملاء.",
        "highlights": [
            "إصدار فواتير ضريبية وإلكترونية بأكواد QR ذكية",
            "تتبع دقيق لحركات المخازن وتنبيهات نواقص المنتجات",
            "تقارير محاسبية تفصيلية للأرباح والمبيعات بالرسوم البيانية",
            "صلاحيات متعددة للمستخدمين والكاشير والمحاسبين"
        ],
        "technologies": ["Python", "FastAPI / Django", "PostgreSQL", "Chart.js", "Electronic Invoices"],
        "color": "#10b981",
    },
    {
        "id": "client-payroll-system",
        "title": "Client Payroll & Financial Accounting System",
        "arabic_title": "نظام تنظيم المرتبات والحسابات المالية للشركات",
        "category": "Business Systems",
        "badge": "Finance Core",
        "description": "نظام مالي متخصص لتنظيم مستحقات الموظفين، حساب المرتبات والبدلات والخصومات الشهرية، وإصدار مسيرات الرواتب تلقائياً.",
        "highlights": [
            "حساب تلقائي لمرتبات الموظفين ومكافآت الحوافز والتأخيرات",
            "إصدار إيصالات استلام الرواتب وكشوفات الحسابات PDF",
            "إدارة العقود والأقساط والتأمينات بكل دقة",
            "تشفير بنكي للبيانات المالية وحماية متقدمة"
        ],
        "technologies": ["Python", "PostgreSQL", "ReportLab PDF", "REST APIs", "Data Encryption"],
        "color": "#f59e0b",
    },
    {
        "id": "student-accounts-system",
        "title": "Student Accounts & Academic Management",
        "arabic_title": "نظام إدارة حسابات الطلاب والمدارس والمراكز التعليمية",
        "category": "Educational",
        "badge": "EdTech",
        "description": "منصة شاملة للمؤسسات التعليمية والسناتر لإدارة شؤون الطلاب، تحصيل المصروفات والأقساط، ومتابعة الحضور والانصراف والدرجات.",
        "highlights": [
            "تتبع اشتراكات وأقساط الطلاب وتنبيهات أولياء الأمور",
            "إدارة مجموعات الدروس وجداول المواعيد والغياب بكارت QR",
            "تقارير دراسية ومحاسبية تفصيلية للإدارة",
            "بوابة خاصة لولي الأمر لمتابعة الطالب لحظياً"
        ],
        "technologies": ["Python", "FastAPI", "Modern UI", "QR Attendance", "Cloud Database"],
        "color": "#8b5cf6",
    },
    {
        "id": "ecommerce-platform",
        "title": "Modern E-Commerce & Multi-Vendor Store",
        "arabic_title": "متاجر ومنصات تسوق إلكتروني متكاملة (E-Commerce)",
        "category": "Innovative Web",
        "badge": "High Conversion",
        "description": "مواقع تجارة إلكترونية عصرية وسريعة جداً، مزودة بسلة تسوق متقدمة، بوابات دفع إلكترونية متعددة، وإدارة المنتجات والشحن.",
        "highlights": [
            "ربط بوابات الدفع الإلكتروني (Visa, Mastercard, Fawry, Vodafone Cash)",
            "لوحة تحكم كاملة لإدارة المنتجات، العروض، وأكواد الخصم",
            "تتبع شحنات الطلبات وتنبيهات فورية عبر واتساب للعميل",
            "تصميم متجاوب بنسبة 100% مع تجربة شراء سلسة"
        ],
        "technologies": ["Full-Stack Web", "Python / Node.js", "Payment Gateways", "Tailwind CSS", "Redis"],
        "color": "#ec4899",
    },
    {
        "id": "digital-wallet-fintech",
        "title": "Digital Wallet & Secure Fintech Solutions",
        "arabic_title": "أنظمة المحافظ الرقمية والمدفوعات الإلكترونية السريعة",
        "category": "Fintech & Bookings",
        "badge": "Fintech Safe",
        "description": "حلول برمجية للمحافظ الإلكترونية تمكّن المستخدمين من شحن الرصيد، تحويل الأموال داخلياً، والدفع السريع بأعلى بروتوكولات الأمان.",
        "highlights": [
            "محفظة رصيد إلكترونية مع تحويل لحظي بين الحسابات",
            "تأكيد العمليات بـ OTP ومصادقة ثنائية 2FA",
            "سجل حركات مالية مشفر وغير قابل للتلاعب",
            "لوحة تحكم إدارية لمتابعة السيولة وعمليات السحب والإيداع"
        ],
        "technologies": ["Python", "FastAPI", "WebSockets", "Bank-Level Security", "PostgreSQL"],
        "color": "#06b6d4",
    },
    {
        "id": "ticket-booking-engine",
        "title": "Smart Ticket Booking & Reservation Engine",
        "arabic_title": "منظومة حجز التذاكر والمواعيد والفعاليات الذكية",
        "category": "Fintech & Bookings",
        "badge": "Live Booking",
        "description": "مواقع وأنظمة مخصصة لحجز تذاكر الحفلات، المباريات، العيادات، والقاعات مع حجز المقاعد تفاعلياً وتوليد تذاكر رقمية فورية.",
        "highlights": [
            "خريطة مقاعد تفاعلية تمكّن العميل من اختيار مكانه المفضل",
            "توليد تذاكر إلكترونية ذكية مشفرة بـ QR Code لمنع التزوير",
            "تأكيد الحجز الفوري وإرسال التذكرة للعميل عبر واتساب وإيميل",
            "تكامل مباشر مع بوابات الدفع الإلكترونية السريعة"
        ],
        "technologies": ["Python", "Three.js / Canvas", "QR Engine", "Payment API", "AsyncIO"],
        "color": "#3b82f6",
    },
    {
        "id": "library-cloud-notes",
        "title": "Smart Library Management & Cloud Notes",
        "arabic_title": "نظام إدارة المكتبات الرقمية وأرشفة الملاحظات اليومية",
        "category": "Educational",
        "badge": "Smart Archive",
        "description": "منصة أرشفة وإدارة للمكتبات والكتب والوثائق مع نظام متقدم للملاحظات اليومية المشفرة والمزامنة الفورية عبر الأجهزة.",
        "highlights": [
            "فهرسة وبحث فوري في الكتب والملفات والمستندات",
            "نظام استعارة ذكي مع تتبع مواعيد الإرجاع وتنبيهات التأخير",
            "مفكرة سحابية يومية لحفظ الملاحظات والمشاريع مع وسم Tagging",
            "أرشفة سحابية آمنة مع نسخ احتياطي تلقائي"
        ],
        "technologies": ["Python", "SQLite / PostgreSQL", "Cloud Sync", "FTS Search", "REST APIs"],
        "color": "#a855f7",
    },
    {
        "id": "interactive-kids-game",
        "title": "Interactive Kids Educational Game Platform",
        "arabic_title": "ألعاب ومنصات تعليمية تفاعلية للأطفال (Gamification)",
        "category": "Innovative Web",
        "badge": "Gamified UX",
        "description": "تطبيقات ويب وألعاب تعليمية تفاعلية تعتمد على الرسوم المتحركة والأصوات المشوقة لتعليم الأطفال الحساب واللغات والتفكير المنطقي.",
        "highlights": [
            "تجارب بصرية تفاعلية تجذب الطفل وتزيد من تركيزه",
            "مؤثرات صوتية وجرافيكس كارتوني ناعم وممتع",
            "نظام مكافآت ونقاط ولوحة شرف لأعلى النتائج",
            "تعمل بسلاسة فائقة على شاشات الموبايل والتابلت"
        ],
        "technologies": ["HTML5 Canvas", "Modern JavaScript", "Web Audio API", "CSS3 Animations"],
        "color": "#f43f5e",
    },
    {
        "id": "health-fitness-platform",
        "title": "Health & Fitness Analytics Platform",
        "arabic_title": "مواقع وتطبيقات الصحة واللياقة البدنية وحساب السعرات",
        "category": "Innovative Web",
        "badge": "Health Tech",
        "description": "منصات رقمية متطورة للجيمات ومدربي اللياقة والمهتمين بالصحة، تتضمن جداول التمارين، حساب السعرات والماكروز، وتتبع الوزن.",
        "highlights": [
            "حاسبة ذكية للسعرات الحرارية والكتلة العضلية والماكروز",
            "خطط تمارين وجداول غذائية مخصصة لكل متدرب",
            "رسوم بيانية حية توضح تطور الوزن والدهون بمرور الوقت",
            "نظام حجز جلسات التدريب والمتابعة أونلاين"
        ],
        "technologies": ["Python Data Analytics", "Chart.js", "Responsive UI", "FastAPI"],
        "color": "#14b8a6",
    },
]

SKILLS_CATEGORIES = [
    {
        "name": "Enterprise & Business Systems",
        "arabic_name": "أنظمة الشركات وإدارة الأعمال (ERP)",
        "skills": [
            "أنظمة الفواتير والمبيعات الإلكترونية",
            "إدارة المخازن وتتبع المنتجات بدقة",
            "تنظيم المرتبات وشؤون الموظفين (Payroll)",
            "إدارة حسابات واشتراكات الطلاب والمدارس",
            "إدارة المكتبات والأرشفة السحابية"
        ]
    },
    {
        "name": "Innovative Web & E-Commerce",
        "arabic_name": "المواقع المبتكرة والتجارة الإلكترونية",
        "skills": [
            "متاجر إلكترونية متكاملة مع بوابات الدفع (E-Commerce)",
            "أنظمة المحافظ الرقمية والمدفوعات (Digital Wallets)",
            "مواقع حجز التذاكر والمواعيد التفاعلية",
            "مواقع البورتفوليو والمدونات الاحترافية",
            "منصات الصحة واللياقة والألعاب التعليمية"
        ]
    },
    {
        "name": "Artificial Intelligence & Automation",
        "arabic_name": "الذكاء الاصطناعي والأتمتة الذكية",
        "skills": [
            "روبوتات واتساب لخدمة العملاء وأخذ الطلبات",
            "نماذج الذكاء الاصطناعي وتوليد النصوص (LLMs)",
            "العملاء الأذكياء المستقلة (Autonomous AI Agents)",
            "الرؤية الحاسوبية وتتبع الوجوه (Computer Vision)",
            "أتمتة العمليات والربط السحابي (APIs & Webhooks)"
        ]
    },
    {
        "name": "Core Technologies & Architecture",
        "arabic_name": "التقنيات البرمجية وهندسة الأنظمة",
        "skills": [
            "Python (FastAPI, Django, Flask)",
            "قواعد البيانات (PostgreSQL, SQLite, Redis)",
            "الواجهات التفاعلية ثلاثية الأبعاد (Three.js & WebGL)",
            "أمن المعلومات والتشفير وحماية البيانات",
            "بناء واجهات REST APIs & WebSockets فائقة السرعة"
        ]
    }
]
