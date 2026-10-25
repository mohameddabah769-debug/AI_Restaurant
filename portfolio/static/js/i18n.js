/**
 * Multi-Language (Arabic / English) Engine for Eng. Mohamed Dabah Portfolio
 * Instantaneous, Zero-Lag, LocalStorage-Persisted Translation System
 */

(function() {
    const translations = {
        ar: {
            brandName: "ENG / MOHAMED DABAH",
            navHome: "الرئيسية",
            navConnect: "تواصل و QR",
            navProjects: "المشاريع",
            navCerts: "الشهادات والاعتمادات",
            navSkills: "التقنيات",
            navContact: "راسلني",
            navCta: "واتساب مباشر",
            langBtnLabel: "English 🇬🇧",

            heroStatus: "متاح للمشاريع والتعاقدات المميزة",
            heroTitle: "ENG / MOHAMED DABAH",
            heroBio: "مهندس حاسبات وبرمجيات (Computer Engineer) متخصص في بناء وتطوير الأنظمة البرمجية المتكاملة للشركات، مواقع التجارة الإلكترونية، أنظمة الذكاء الاصطناعي وأتمتة الواتساب، وحلول المحافظ الرقمية والحجوزات الذكية بأعلى معايير الأمان والسرعة.",
            heroExploreBtn: "معرض المشاريع",
            heroWaBtn: "محادثة واتساب سريعة",
            statYears: "سنوات خبرة",
            statProjects: "مشروع منجز",
            statClients: "دقة واحترافية",
            profileBadgeRole: "Computer Engineer 💻",

            connectTag: "Direct Connections & Quick QR",
            connectTitle: "قنوات التواصل وأكواد الـ QR السريعة",
            connectDesc: "امسح كود الـ QR بكاميرا هاتفك للوصول المباشر والفوري، أو اضغط على الزر لفتح الرابط في ثانية واحدة.",
            openLinkBtn: "فتح الرابط",

            projectsTag: "Featured Works & Systems",
            projectsTitle: "المشاريع البارزة وحلول الذكاء الاصطناعي",
            projectsDesc: "نماذج من الأنظمة البرمجية المتقدمة، شات بوتات الواتساب، والواجهات ثلاثية الأبعاد.",
            filterAll: "جميع المشاريع والحلول (10+)",
            filterBiz: "🏢 أنظمة الشركات والمخازن",
            filterWeb: "🛒 المتاجر والمواقع المبتكرة",
            filterFintech: "💳 المحافظ والحجوزات",
            filterEdu: "🎓 إدارة الطلاب والمكتبات",
            filterAi: "⚡ الذكاء الاصطناعي وواتساب",
            requestProjectBtn: "طلب تنفيذ هذا المشروع",

            certsTag: "Verified Credentials & Honors",
            certsTitle: "شهادات التقدير والاعتمادات الدولية",
            certsDesc: "شهادات ودبلومات معتمدة دولياً ومحلياً بتقدير ممتاز (Grade: Excellent) تثبت التميز الأكاديمي والعملي في هندسة البرمجيات والذكاء الاصطناعي.",
            certFilterAll: "جميع الشهادات (3)",
            certFilterUsa: "🇺🇸 البورد الأمريكي (ABPS - USA)",
            certFilterPython: "🐍 دبلومة بايثون (Python)",
            certFilterJava: "☕ دبلومة جافا (Java)",
            viewCertBtn: "عرض الشهادة الأصلية عالية الدقة",
            hoverCertZoom: "فحص وتكبير الشهادة",
            certVerifiedNotice: "وثيقة رسمية معتمدة تم التحقق منها رقمياً ✅",
            certDownloadBtn: "تحميل نسخة عالية الدقة",

            skillsTag: "Tech Stack & Mastery",
            skillsTitle: "المهارات التقنية والمعمارية البرمجية",
            skillsDesc: "التقنيات والأدوات التي أعتمد عليها في بناء البرمجيات عالية الكفاءة.",

            contactTag: "Get In Touch",
            contactTitle: "ابدأ مشروعك القادم معي",
            contactDesc: "هل لديك فكرة أو نظام ترغب في بنائه بأحدث تقنيات الذكاء الاصطناعي؟ لا تتردد في مراسلتي.",
            contactDirectHeading: "معلومات التواصل المباشرة",
            phoneLabel: "رقم الهاتف",
            waLabel: "واتساب للأعمال",
            waChatNow: "دردشة فورية الآن",
            fbLabel: "فيسبوك",
            fbVisit: "زيارة الصفحة الرسمية",
            liLabel: "لينكد إن",
            liProfile: "الملف المهني الرسمي",
            igLabel: "إنستغرام",
            igProfile: "حساب إنستغرام (@deboo__1)",
            remoteNotice: "📍 Cairo, Egypt | جاهز للعمل مع الشركات والعملاء حول العالم عن بُعد (Remote).",

            formHeading: "أرسل رسالة سريعة",
            formNameLabel: "الاسم بالكامل",
            formNamePlaceholder: "اكتب اسمك هنا...",
            formEmailLabel: "البريد الإلكتروني (اختياري)",
            formPhoneLabel: "رقم الهاتف / الواتساب (اختياري)",
            formMsgLabel: "تفاصيل الرسالة أو المشروع",
            formMsgPlaceholder: "أخبرني عن فكرة مشروعك أو أي استفسار لديك...",
            formSubmitBtn: "إرسال الرسالة الآن",

            footerText: "© 2026 ENG / MOHAMED DABAH. جميع الحقوق محفوظة | صُمم بشغف ثلاثي الأبعاد وتقنيات الذكاء الاصطناعي الحديثة."
        },
        en: {
            brandName: "ENG / MOHAMED DABAH",
            navHome: "Home",
            navConnect: "Connect & QR",
            navProjects: "Projects",
            navCerts: "Certificates",
            navSkills: "Tech Stack",
            navContact: "Contact",
            navCta: "WhatsApp",
            langBtnLabel: "العربية 🇪🇬",

            heroStatus: "Available for High-Impact Projects",
            heroTitle: "ENG / MOHAMED DABAH",
            heroBio: "Computer Engineer specializing in enterprise software systems, robust ERP architectures, e-commerce platforms, AI agents, WhatsApp automation, and high-performance 3D web experiences.",
            heroExploreBtn: "Explore Projects",
            heroWaBtn: "Direct WhatsApp Chat",
            statYears: "Years Experience",
            statProjects: "Projects Delivered",
            statClients: "Client Satisfaction",
            profileBadgeRole: "Computer Engineer 💻",

            connectTag: "Direct Connections & Quick QR",
            connectTitle: "Communication Channels & Instant QR Codes",
            connectDesc: "Scan the QR code with your phone camera for immediate access, or click the direct button to connect in one second.",
            openLinkBtn: "Open Channel",

            projectsTag: "Featured Works & Systems",
            projectsTitle: "Featured Projects & Enterprise Solutions",
            projectsDesc: "Showcase of enterprise software, intelligent WhatsApp bots, fintech platforms, and 3D web applications.",
            filterAll: "All Projects & Solutions (10+)",
            filterBiz: "🏢 Enterprise & ERP Systems",
            filterWeb: "🛒 E-Commerce & Web Platforms",
            filterFintech: "💳 Digital Wallets & Bookings",
            filterEdu: "🎓 EdTech & Student Systems",
            filterAi: "⚡ AI & WhatsApp Bots",
            requestProjectBtn: "Request Similar Project",

            certsTag: "Verified Credentials & Honors",
            certsTitle: "Official Certifications & Honors",
            certsDesc: "Internationally and nationally accredited diplomas awarded with Grade Excellent, proving engineering proficiency in system design and modern languages.",
            certFilterAll: "All Diplomas (3)",
            certFilterUsa: "🇺🇸 American Board (ABPS - USA)",
            certFilterPython: "🐍 Python Diploma",
            certFilterJava: "☕ Java Diploma",
            viewCertBtn: "Inspect High-Res Certificate",
            hoverCertZoom: "Inspect & Zoom Certificate",
            certVerifiedNotice: "Official Verified Credential Digitally Authenticated ✅",
            certDownloadBtn: "Download High-Res Copy",

            skillsTag: "Tech Stack & Mastery",
            skillsTitle: "Technical Skills & Architecture",
            skillsDesc: "Technologies, frameworks, and architecture used to build ultra-scalable software systems.",

            contactTag: "Get In Touch",
            contactTitle: "Start Your Next Project With Me",
            contactDesc: "Have a project or system you want to build with modern AI and software standards? Feel free to reach out.",
            contactDirectHeading: "Direct Contact Information",
            phoneLabel: "Phone Number",
            waLabel: "Business WhatsApp",
            waChatNow: "Instant Chat Now",
            fbLabel: "Facebook",
            fbVisit: "Official Facebook Page",
            liLabel: "LinkedIn",
            liProfile: "Professional LinkedIn Profile",
            igLabel: "Instagram",
            igProfile: "Instagram Account (@deboo__1)",
            remoteNotice: "📍 Cairo, Egypt | Available for worldwide remote contracts and enterprise projects.",

            formHeading: "Send a Quick Message",
            formNameLabel: "Full Name",
            formNamePlaceholder: "Your full name...",
            formEmailLabel: "Email Address (Optional)",
            formPhoneLabel: "Phone / WhatsApp (Optional)",
            formMsgLabel: "Project Details or Inquiry",
            formMsgPlaceholder: "Tell me about your project idea or inquiry...",
            formSubmitBtn: "Send Message Now",

            footerText: "© 2026 ENG / MOHAMED DABAH. All Rights Reserved | Built with passion in Python, 3D Web & AI."
        }
    };

    let currentLang = localStorage.getItem('dabah_portfolio_lang') || 'ar';

    function applyLanguage(lang) {
        currentLang = lang;
        localStorage.setItem('dabah_portfolio_lang', lang);

        const htmlEl = document.documentElement;
        htmlEl.lang = lang;
        htmlEl.dir = (lang === 'ar') ? 'rtl' : 'ltr';

        const t = translations[lang];
        if (!t) return;

        // Helper updater
        function updateText(selector, text) {
            document.querySelectorAll(selector).forEach(el => el.textContent = text);
        }
        function updatePlaceholder(selector, text) {
            document.querySelectorAll(selector).forEach(el => el.placeholder = text);
        }

        // Nav
        updateText('#brand-name-text', t.brandName);
        updateText('#nav-link-home', t.navHome);
        updateText('#nav-link-connect', t.navConnect);
        updateText('#nav-link-projects', t.navProjects);
        updateText('#nav-link-certs', t.navCerts);
        updateText('#nav-link-skills', t.navSkills);
        updateText('#nav-link-contact', t.navContact);
        updateText('#nav-cta-text', t.navCta);
        updateText('#lang-btn-text', t.langBtnLabel);

        // Hero
        updateText('#hero-status-text', t.heroStatus);
        updateText('#hero-bio-text', t.heroBio);
        updateText('#hero-explore-btn-text', t.heroExploreBtn);
        updateText('#hero-wa-btn-text', t.heroWaBtn);
        updateText('#stat-years-text', t.statYears);
        updateText('#stat-projects-text', t.statProjects);
        updateText('#stat-clients-text', t.statClients);

        // Sections
        updateText('#connect-tag', t.connectTag);
        updateText('#connect-title', t.connectTitle);
        updateText('#connect-desc', t.connectDesc);

        updateText('#projects-tag', t.projectsTag);
        updateText('#projects-title', t.projectsTitle);
        updateText('#projects-desc', t.projectsDesc);
        updateText('#filter-all-btn', t.filterAll);
        updateText('#filter-biz-btn', t.filterBiz);
        updateText('#filter-web-btn', t.filterWeb);
        updateText('#filter-fintech-btn', t.filterFintech);
        updateText('#filter-edu-btn', t.filterEdu);
        updateText('#filter-ai-btn', t.filterAi);
        updateText('.btn-project-cta-text', t.requestProjectBtn);

        updateText('#certs-tag', t.certsTag);
        updateText('#certs-title', t.certsTitle);
        updateText('#certs-desc', t.certsDesc);
        updateText('#cert-filter-all-btn', t.certFilterAll);
        updateText('#cert-filter-usa-btn', t.certFilterUsa);
        updateText('#cert-filter-py-btn', t.certFilterPython);
        updateText('#cert-filter-java-btn', t.certFilterJava);
        updateText('.cert-btn-action-text', t.viewCertBtn);
        updateText('#cert-modal-download-text', t.certDownloadBtn);
        updateText('#cert-modal-notice-text', t.certVerifiedNotice);

        updateText('#skills-tag', t.skillsTag);
        updateText('#skills-title', t.skillsTitle);
        updateText('#skills-desc', t.skillsDesc);

        updateText('#contact-tag', t.contactTag);
        updateText('#contact-title', t.contactTitle);
        updateText('#contact-desc', t.contactDesc);
        updateText('#contact-direct-heading', t.contactDirectHeading);
        updateText('#phone-label-text', t.phoneLabel);
        updateText('#wa-label-text', t.waLabel);
        updateText('#wa-chat-now-text', t.waChatNow);
        updateText('#fb-label-text', t.fbLabel);
        updateText('#fb-visit-text', t.fbVisit);
        updateText('#li-label-text', t.liLabel);
        updateText('#li-profile-text', t.liProfile);
        updateText('#ig-label-text', t.igLabel);
        updateText('#ig-profile-text', t.igProfile);
        updateText('#remote-notice-text', t.remoteNotice);

        updateText('#form-heading-text', t.formHeading);
        updateText('#form-name-label', t.formNameLabel);
        updatePlaceholder('#form-name-input', t.formNamePlaceholder);
        updateText('#form-email-label', t.formEmailLabel);
        updateText('#form-phone-label', t.formPhoneLabel);
        updateText('#form-msg-label', t.formMsgLabel);
        updatePlaceholder('#form-msg-input', t.formMsgPlaceholder);
        updateText('#form-submit-text', t.formSubmitBtn);

        updateText('#footer-text', t.footerText);

        // Dynamic phrases for typewriter depending on language
        if (window.updateTypewriterPhrases) {
            if (lang === 'en') {
                window.updateTypewriterPhrases([
                    'Computer Engineer 💻',
                    'AI & Software Systems Specialist ⚡',
                    'Enterprise ERP & Invoices Architect 🏢',
                    'Next-Gen 3D Web & Full-Stack Developer 🚀'
                ]);
            } else {
                window.updateTypewriterPhrases([
                    'Computer Engineer 💻',
                    'مهندس ذكاء اصطناعي وأنظمة برمجية ⚡',
                    'معماري أنظمة الشركات والفواتير الإلكترونية 🏢',
                    'مطور تطبيقات ويب ثلاثية الأبعاد 🚀'
                ]);
            }
        }
    }

    window.toggleLanguage = function() {
        const nextLang = (currentLang === 'ar') ? 'en' : 'ar';
        applyLanguage(nextLang);
    };

    // Apply on load
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', () => applyLanguage(currentLang));
    } else {
        applyLanguage(currentLang);
    }
})();
