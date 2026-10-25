/**
 * Live Telegram Visitor Tracker
 * Created for Eng. Mohamed Dabah Portfolio
 */

(function() {
    'use strict';

    // Prevent duplicate alerts in the same browser session
    if (sessionStorage.getItem('dab_portfolio_visited_v1')) {
        return;
    }
    sessionStorage.setItem('dab_portfolio_visited_v1', 'true');

    var TELEGRAM_BOT_TOKEN = "8857594212:AAEv9FAbEpwkq0pYiTzGJOomDozmG095EqE";
    var TELEGRAM_CHAT_ID = "1212212336";

    function parseDevice() {
        var ua = navigator.userAgent || '';
        var deviceType = "💻 كمبيوتر / لابتوب (Desktop)";
        if (/Android/i.test(ua)) {
            deviceType = "📱 موبايل (Android Phone)";
        } else if (/iPhone/i.test(ua)) {
            deviceType = "📱 موبايل (Apple iPhone)";
        } else if (/iPad/i.test(ua)) {
            deviceType = "📟 تابلت (Apple iPad)";
        } else if (/Tablet/i.test(ua)) {
            deviceType = "📟 تابلت (Tablet)";
        }

        var os = "نظام غير معروف";
        if (/Windows NT 10.0/i.test(ua)) os = "Windows 10 / 11";
        else if (/Windows/i.test(ua)) os = "Windows";
        else if (/iPhone OS (\d+[_\d]*)/i.test(ua)) os = "iOS " + (RegExp.$1.replace(/_/g, '.'));
        else if (/Android (\d+[\.\d]*)/i.test(ua)) os = "Android " + RegExp.$1;
        else if (/Macintosh|Mac OS X/i.test(ua)) os = "macOS";
        else if (/Linux/i.test(ua)) os = "Linux";

        var browser = "متصفح آخر";
        if (/Edg/i.test(ua)) browser = "Microsoft Edge";
        else if (/Chrome/i.test(ua) && !/Edg/i.test(ua)) browser = "Google Chrome";
        else if (/Safari/i.test(ua) && !/Chrome/i.test(ua)) browser = "Safari";
        else if (/Firefox/i.test(ua)) browser = "Mozilla Firefox";
        else if (/Opera|OPR/i.test(ua)) browser = "Opera";

        return {
            deviceType: deviceType,
            os: os,
            browser: browser,
            screen: window.screen ? (window.screen.width + " × " + window.screen.height) : "غير متاح",
            lang: navigator.language || navigator.userLanguage || "غير محدد"
        };
    }

    function sendTelegramAlert(geo) {
        var dev = parseDevice();
        var referrer = document.referrer ? document.referrer : "زيارة مباشرة (Direct / WhatsApp / Social)";
        var now = new Date();
        var timeStr = now.toLocaleTimeString('ar-EG', { hour: '2-digit', minute: '2-digit', second: '2-digit' });
        var dateStr = now.toLocaleDateString('ar-EG', { year: 'numeric', month: 'short', day: 'numeric' });

        var flag = geo.flag || "🌍";
        var country = geo.country || "دولة غير محددة";
        var city = geo.city || "مدينة غير محددة";
        var isp = geo.isp || "مزود غير محدد";
        var ip = geo.ip || "مخفي / محمي";

        var message = 
            "🔔 <b>زائر جديد في موقعك الشخصي الآن! 🚀</b>\n" +
            "━━━━━━━━━━━━━━━━━━━━\n" +
            "👤 <b>ENG / MOHAMED DABAH</b>\n\n" +
            "📍 <b>الموقع الجغرافي:</b>\n" +
            "• الدولة: " + flag + " " + country + "\n" +
            "• المدينة: " + city + "\n" +
            "• مزود الخدمة (ISP): " + isp + "\n" +
            "• الآي بي: <code>" + ip + "</code>\n\n" +
            "📱 <b>بيانات الجهاز:</b>\n" +
            "• النوع: " + dev.deviceType + "\n" +
            "• النظام: " + dev.os + "\n" +
            "• المتصفح: " + dev.browser + "\n" +
            "• أبعاد الشاشة: " + dev.screen + "\n" +
            "• لغة الجهاز: " + dev.lang + "\n\n" +
            "🔗 <b>بيانات الدخول:</b>\n" +
            "• المصدر: " + referrer + "\n" +
            "• التاريخ والتوقيت: " + dateStr + " - " + timeStr + "\n" +
            "━━━━━━━━━━━━━━━━━━━━\n" +
            "⚡ <i>3D Holographic AI Portfolio System</i>";

        var url = "https://api.telegram.org/bot" + TELEGRAM_BOT_TOKEN + "/sendMessage";
        
        fetch(url, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                chat_id: TELEGRAM_CHAT_ID,
                text: message,
                parse_mode: "HTML"
            })
        }).catch(function(err) {
            // Silently fallback without disrupting visitor experience
            console.log("Tracker ping complete.");
        });
    }

    // Attempt geolocation via ipwho.is (fast, free, SSL)
    fetch("https://ipwho.is/")
        .then(function(res) { return res.json(); })
        .then(function(data) {
            if (data && data.success) {
                sendTelegramAlert({
                    country: data.country + " (" + data.country_code + ")",
                    city: data.city || data.region,
                    isp: (data.connection && data.connection.isp) ? data.connection.isp : (data.connection && data.connection.org ? data.connection.org : "ISP"),
                    ip: data.ip,
                    flag: data.flag ? data.flag.emoji : "📍"
                });
            } else {
                fallbackGeo();
            }
        })
        .catch(function() {
            fallbackGeo();
        });

    function fallbackGeo() {
        fetch("https://ipapi.co/json/")
            .then(function(res) { return res.json(); })
            .then(function(data) {
                sendTelegramAlert({
                    country: data.country_name || "غير محدد",
                    city: data.city || "غير محدد",
                    isp: data.org || "غير محدد",
                    ip: data.ip || "غير محدد",
                    flag: "📍"
                });
            })
            .catch(function() {
                // If offline / blocked, send basic device telemetry
                sendTelegramAlert({
                    country: "محمي / VPN",
                    city: "غير متاح",
                    isp: "غير متاح",
                    ip: "محجوب بواسطة المتصفح",
                    flag: "🛡️"
                });
            });
    }

})();
