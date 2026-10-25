/**
 * UI Interactions, 3D Tilt Effects, Audio Synthesizer & Modals
 * Developed for Eng. Mohamed Dabah Portfolio
 */

document.addEventListener('DOMContentLoaded', () => {
    // 1. Audio Synthesizer (Cyber SFX using Web Audio API)
    let audioCtx = null;
    let soundEnabled = true;

    function playCyberBeep(freq = 600, type = 'sine', duration = 0.08) {
        if (!soundEnabled) return;
        try {
            if (!audioCtx) audioCtx = new (window.AudioContext || window.webkitAudioContext)();
            if (audioCtx.state === 'suspended') audioCtx.resume();
            
            const osc = audioCtx.createOscillator();
            const gain = audioCtx.createGain();
            
            osc.type = type;
            osc.frequency.setValueAtTime(freq, audioCtx.currentTime);
            osc.frequency.exponentialRampToValueAtTime(freq * 1.5, audioCtx.currentTime + duration);
            
            gain.gain.setValueAtTime(0.04, audioCtx.currentTime);
            gain.gain.exponentialRampToValueAtTime(0.0001, audioCtx.currentTime + duration);
            
            osc.connect(gain);
            gain.connect(audioCtx.destination);
            
            osc.start();
            osc.stop(audioCtx.currentTime + duration);
        } catch (e) {
            // Audio context blocked or not supported
        }
    }

    // Attach sound to interactive buttons
    document.querySelectorAll('.btn-cyber, .social-card, .project-card, .nav-link').forEach(el => {
        el.addEventListener('mouseenter', () => playCyberBeep(750, 'triangle', 0.05));
        el.addEventListener('click', () => playCyberBeep(1100, 'sine', 0.1));
    });

    // 2. 3D Tilt Effect on Cards
    const tiltCards = document.querySelectorAll('.tilt-card');
    tiltCards.forEach(card => {
        card.addEventListener('mousemove', (e) => {
            const rect = card.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            
            const centerX = rect.width / 2;
            const centerY = rect.height / 2;
            
            const rotateX = ((y - centerY) / centerY) * -10;
            const rotateY = ((x - centerX) / centerX) * 10;
            
            card.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) translateY(-6px)`;
            
            // Dynamic glare effect
            const glare = card.querySelector('.glare-effect');
            if (glare) {
                glare.style.background = `radial-gradient(circle at ${x}px ${y}px, rgba(255,255,255,0.18) 0%, rgba(255,255,255,0) 60%)`;
            }
        });

        card.addEventListener('mouseleave', () => {
            card.style.transform = 'perspective(1000px) rotateX(0deg) rotateY(0deg) translateY(0px)';
            const glare = card.querySelector('.glare-effect');
            if (glare) {
                glare.style.background = 'transparent';
            }
        });
    });

    // 3. Project Filter Tabs
    const filterBtns = document.querySelectorAll('.filter-btn');
    const projectCards = document.querySelectorAll('.project-card');

    filterBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            filterBtns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            
            const filter = btn.getAttribute('data-filter');
            projectCards.forEach(card => {
                if (filter === 'all' || card.getAttribute('data-category') === filter) {
                    card.style.display = 'flex';
                    setTimeout(() => { card.style.opacity = '1'; card.style.transform = 'scale(1)'; }, 50);
                } else {
                    card.style.opacity = '0';
                    card.style.transform = 'scale(0.95)';
                    setTimeout(() => { card.style.display = 'none'; }, 250);
                }
            });
        });
    });

        // 4. Contact Form Handling (Fast, Bulletproof & Works on Static + Server)
    const contactForm = document.getElementById('contact-form');
    const formResponse = document.getElementById('form-response');

    if (contactForm) {
        contactForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const submitBtn = contactForm.querySelector('button[type="submit"]');
            const originalText = submitBtn.innerHTML;
            
            submitBtn.disabled = true;
            submitBtn.innerHTML = `<span>جاري تجهيز الرسالة...</span>`;
            
            const formData = new FormData(contactForm);
            const name = (formData.get('name') || '').trim();
            const email = (formData.get('email') || '').trim();
            const phone = (formData.get('phone') || '').trim();
            const message = (formData.get('message') || '').trim();

            const waNumber = "201095744676";
            let waText = `مرحباً بشمهندس محمد، أنا ${name}.\n`;
            if (phone) waText += `📱 رقم الهاتف: ${phone}\n`;
            if (email) waText += `📧 البريد: ${email}\n`;
            waText += `💬 تفاصيل الرسالة:\n"${message}"`;
            const directWaUrl = `https://wa.me/${waNumber}?text=${encodeURIComponent(waText)}`;

            // If on local server or custom backend, attempt background API call
            if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
                try {
                    fetch('/api/contact', { method: 'POST', body: formData }).catch(() => {});
                } catch(e) {}
            }

            // Immediately display success and trigger direct WhatsApp
            if (formResponse) {
                formResponse.className = 'form-alert success';
                formResponse.style.display = 'block';
                formResponse.innerHTML = `
                    <div style="display:flex; align-items:center; gap:8px; margin-bottom:8px;">
                        <span style="font-size:1.2rem;">✅</span>
                        <span>شكراً لك يا <strong>${name}</strong>! تم استلام وتجهيز رسالتك بنجاح.</span>
                    </div>
                    <div style="margin-top:12px;">
                        <a href="${directWaUrl}" target="_blank" class="btn-cyber btn-primary" style="width:100%; justify-content:center; padding:12px 20px; font-size:0.92rem; text-decoration:none;">
                            <i data-lucide="message-circle"></i>
                            <span>فتح محادثة واتساب وإرسال الرسالة الآن 🚀</span>
                        </a>
                    </div>
                `;
                if (window.lucide) lucide.createIcons();
            }

            // Open WhatsApp directly in new tab
            window.open(directWaUrl, '_blank');

            contactForm.reset();
            submitBtn.disabled = false;
            submitBtn.innerHTML = originalText;
        });
    }

    // 5. QR Code Modal Viewer
    const qrModal = document.getElementById('qr-modal');
    const modalQrImg = document.getElementById('modal-qr-img');
    const modalQrTitle = document.getElementById('modal-qr-title');
    const modalQrLink = document.getElementById('modal-qr-link');
    const closeModal = document.getElementById('close-modal');

    document.querySelectorAll('.btn-zoom-qr').forEach(btn => {
        btn.addEventListener('click', (e) => {
            e.stopPropagation();
            const qrSrc = btn.getAttribute('data-qr');
            const title = btn.getAttribute('data-title');
            const link = btn.getAttribute('data-link');
            
            if (qrModal && modalQrImg) {
                modalQrImg.src = qrSrc;
                modalQrTitle.textContent = title;
                modalQrLink.href = link;
                qrModal.classList.add('active');
            }
        });
    });

    if (closeModal && qrModal) {
        closeModal.addEventListener('click', () => qrModal.classList.remove('active'));
        qrModal.addEventListener('click', (e) => {
            if (e.target === qrModal) qrModal.classList.remove('active');
        });
    }

        // 6. Mobile Menu Toggle
    const mobileMenuBtn = document.getElementById('mobile-menu-toggle');
    const navLinks = document.getElementById('nav-links');
    if (mobileMenuBtn && navLinks) {
        mobileMenuBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            mobileMenuBtn.classList.toggle('active');
            navLinks.classList.toggle('active');
        });
        
        document.querySelectorAll('.nav-link').forEach(link => {
            link.addEventListener('click', () => {
                mobileMenuBtn.classList.remove('active');
                navLinks.classList.remove('active');
            });
        });

        document.addEventListener('click', (e) => {
            if (!navLinks.contains(e.target) && !mobileMenuBtn.contains(e.target)) {
                mobileMenuBtn.classList.remove('active');
                navLinks.classList.remove('active');
            }
        });
    }

    // 7. Ultra-Fast Typewriter Effect (Zero Lag)
    const typeWriterEl = document.getElementById('typewriter-text');
    if (typeWriterEl) {
        let phrases = [
            'Computer Engineer 💻',
            'AI & Software Systems Specialist ⚡',
            'Enterprise ERP & Invoices Architect 🏢',
            'Next-Gen 3D Web & Full-Stack Developer 🚀'
        ];
        window.updateTypewriterPhrases = function(newPhrases) {
            phrases = newPhrases;
            pIdx = 0;
            charIdx = 0;
            isDeleting = false;
        };
        let pIdx = 0, charIdx = 0, isDeleting = false;
        
        function tickTypewriter() {
            const current = phrases[pIdx];
            if (isDeleting) {
                charIdx--;
                typeWriterEl.textContent = current.substring(0, charIdx);
            } else {
                charIdx++;
                typeWriterEl.textContent = current.substring(0, charIdx);
            }
            
            let speed = isDeleting ? 30 : 65;
            
            if (!isDeleting && charIdx === current.length) {
                speed = 2200; // Pause at end of text
                isDeleting = true;
            } else if (isDeleting && charIdx === 0) {
                isDeleting = false;
                pIdx = (pIdx + 1) % phrases.length;
                speed = 400; // Pause before typing next
            }
            setTimeout(tickTypewriter, speed);
        }
        setTimeout(tickTypewriter, 700);
    }

    // 8. Native Hardware-Accelerated Scroll Observer (Zero Overhead)
    const revealElements = document.querySelectorAll('.scroll-reveal');
    if ('IntersectionObserver' in window && revealElements.length > 0) {
        const observer = new IntersectionObserver((entries, obs) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('revealed');
                    obs.unobserve(entry.target); // Release memory immediately
                }
            });
        }, { threshold: 0.08, rootMargin: '0px 0px -40px 0px' });
        
        revealElements.forEach(el => observer.observe(el));
    } else {
        // Fallback for older browsers
        revealElements.forEach(el => el.classList.add('revealed'));
    }


    // Certificate Lightbox Handler
    window.openCertModal = function(imgSrc, title, issuer) {
        var modal = document.getElementById('cert-lightbox-modal');
        var mImg = document.getElementById('cert-modal-img');
        var mTitle = document.getElementById('cert-modal-title');
        var mIssuer = document.getElementById('cert-modal-issuer');
        var mDl = document.getElementById('cert-modal-download');
        if (modal && mImg) {
            mImg.src = imgSrc;
            if (mTitle) mTitle.textContent = title;
            if (mIssuer) mIssuer.textContent = issuer;
            if (mDl) mDl.href = imgSrc;
            modal.classList.add('active');
        }
    };

    window.closeCertModal = function() {
        var modal = document.getElementById('cert-lightbox-modal');
        if (modal) modal.classList.remove('active');
    };

    var certModalEl = document.getElementById('cert-lightbox-modal');
    if (certModalEl) {
        certModalEl.addEventListener('click', function(e) {
            if (e.target === certModalEl) closeCertModal();
        });
    }

    // Certificate Filters
    var certFilterBtns = document.querySelectorAll('.cert-filter');
    var certCards = document.querySelectorAll('.cert-card');
    certFilterBtns.forEach(function(btn) {
        btn.addEventListener('click', function() {
            certFilterBtns.forEach(function(b) { b.classList.remove('active'); });
            btn.classList.add('active');
            var filter = btn.getAttribute('data-cert-filter');
            certCards.forEach(function(card) {
                var cat = card.getAttribute('data-cert-cat');
                if (filter === 'all' || cat === filter) {
                    card.style.display = 'flex';
                    setTimeout(function() { card.style.opacity = '1'; card.style.transform = 'scale(1)'; }, 40);
                } else {
                    card.style.opacity = '0';
                    card.style.transform = 'scale(0.95)';
                    setTimeout(function() { card.style.display = 'none'; }, 200);
                }
            });
        });
    });

});