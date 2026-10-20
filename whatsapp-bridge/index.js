const http = require('http');
const { Client, LocalAuth } = require('whatsapp-web.js');
const qrcode = require('qrcode-terminal');
const axios = require('axios');

const client = new Client({
    authStrategy: new LocalAuth(),
    puppeteer: {
        headless: true,
        args: [
            '--no-sandbox',
            '--disable-setuid-sandbox',
            '--disable-dev-shm-usage',
            '--disable-accelerated-2d-canvas',
            '--no-first-run',
            '--no-zygote',
            '--disable-gpu'
        ]
    }
});

// عرض QR Code في التيرمينال
client.on('qr', (qr) => {
    console.log('📌 امسح الـ QR Code التالي للربط بالواتساب:');
    qrcode.generate(qr, { small: true });
});

// عند نجاح الاتصال
client.on('ready', () => {
    console.log('✅ تم ربط الواتساب بنجاح وجاهز لاستقبال الرسائل!');
});

// استقبال الرسائل وإرسالها لسيرفر بايثون (دعم النصوص والرسائل الصوتية)
client.on('message', async (msg) => {
    // 1. تجاهل رسائل البوت نفسه
    if (msg.fromMe) return;

    // 2. تجاهل حالات الواتساب والجروبات
    if (msg.from === 'status@broadcast' || msg.from.endsWith('@g.us')) return;

    console.log(`📩 رسالة خاصة وصلت من [${msg.from}] - النوع: [${msg.type}]`);

    try {
        let payload = {
            message: msg.body || '',
            customer_phone: msg.from
        };

        // فحص إذا كانت الرسالة ريكورد صوتي (Voice Note / Audio)
        if (msg.hasMedia && (msg.type === 'audio' || msg.type === 'ptt' || msg.type === 'document')) {
            console.log(`🎙️ تم رصد رسالة صوتية/ميديا نوع: [${msg.type}] من [${msg.from}]. جاري التحميل...`);
            try {
                const media = await msg.downloadMedia();
                if (media && media.data) {
                    console.log(`✅ تم تحميل الصوت بنجاح! النوع: [${media.mimetype}] - الحجم: [${media.data.length}] بايت`);
                    if (msg.type === 'audio' || msg.type === 'ptt' || (media.mimetype && media.mimetype.includes('audio'))) {
                        payload.audio_base64 = media.data;
                        payload.mimetype = media.mimetype || 'audio/ogg';
                    }
                } else {
                    console.log('⚠️ لم يرجع ملف الميديا أي بيانات.');
                }
            } catch (mediaErr) {
                console.error('❌ خطأ في تحميل ملف الصوت من واتساب:', mediaErr.message);
            }
        }

        // إرسال البيانات لسيرفر بايثون (/order) مع مهلة كافية لتفريغ الصوت
        const response = await axios.post('http://127.0.0.1:8000/order', payload, {
            timeout: 35000
        });

        if (response.data && response.data.reply) {
            await msg.reply(response.data.reply);
            console.log(`📤 تم الرد بنجاح على [${msg.from}]`);
        }
    } catch (error) {
        console.error('❌ خطأ في الاتصال بسيرفر بايثون:', error.message);
    }
});

// سيرفر HTTP لاستقبال رسائل الإشعارات من بايثون وإرسالها للعملاء أو المطبخ
const server = http.createServer(async (req, res) => {
    if (req.method === 'POST' && req.url === '/send-message') {
        let body = '';
        req.on('data', chunk => { body += chunk.toString(); });
        req.on('end', async () => {
            try {
                const { to, message } = JSON.parse(body);
                if (!to || !message) {
                    res.writeHead(400, { 'Content-Type': 'application/json' });
                    return res.end(JSON.stringify({ error: 'Missing to or message' }));
                }

                // ضبط صيغة المعرف لواتساب
                let target = to;
                if (!target.includes('@')) {
                    target = `${target.replace(/[^0-9]/g, '')}@c.us`;
                }

                await client.sendMessage(target, message);
                console.log(`📤 [إشعار خارجي] تم إرسال رسالة إلى [${target}]`);
                res.writeHead(200, { 'Content-Type': 'application/json' });
                res.end(JSON.stringify({ success: true }));
            } catch (err) {
                console.error('❌ خطأ في إرسال الرسالة الخارجية:', err.message);
                res.writeHead(500, { 'Content-Type': 'application/json' });
                res.end(JSON.stringify({ error: err.message }));
            }
        });
    } else {
        res.writeHead(404);
        res.end();
    }
});

const OUTBOUND_PORT = 3001;
server.listen(OUTBOUND_PORT, () => {
    console.log(`📡 سيرفر الرسائل الخارجية (Outbound) جاهز على المنفذ ${OUTBOUND_PORT}`);
});

client.initialize();
