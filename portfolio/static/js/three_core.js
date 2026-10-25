/**
 * Three.js 3D Interactive AI Quantum Core & Particle Universe
 * Developed for Eng. Mohamed Dabah Portfolio
 */

(function() {
    const container = document.getElementById('webgl-canvas-container');
    if (!container) return;

    let scene, camera, renderer;
    let coreGroup, innerSphere, wireframeMesh, rings = [], particles;
    let mouseX = 0, mouseY = 0;
    let targetX = 0, targetY = 0;
    let windowHalfX = window.innerWidth / 2;
    let windowHalfY = window.innerHeight / 2;
    let clock = new THREE.Clock();

    function init() {
        // 1. Scene setup
        scene = new THREE.Scene();
        scene.fog = new THREE.FogExp2(0x060814, 0.0018);

        // 2. Camera setup
        camera = new THREE.PerspectiveCamera(60, window.innerWidth / window.innerHeight, 0.1, 1500);
        camera.position.z = 240;

        // 3. Renderer setup
        renderer = new THREE.WebGLRenderer({ alpha: true, antialias: true, powerPreference: "high-performance" });
        renderer.setSize(window.innerWidth, window.innerHeight);
        renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
        renderer.toneMapping = THREE.ACESFilmicToneMapping;
        renderer.toneMappingExposure = 1.2;
        container.appendChild(renderer.domElement);

        // 4. Lighting
        const ambientLight = new THREE.AmbientLight(0x101530, 2.5);
        scene.add(ambientLight);

        const pointLight1 = new THREE.PointLight(0x00f0ff, 4, 350);
        pointLight1.position.set(80, 60, 100);
        scene.add(pointLight1);

        const pointLight2 = new THREE.PointLight(0x8b5cf6, 4, 350);
        pointLight2.position.set(-80, -60, -80);
        scene.add(pointLight2);

        const pointLight3 = new THREE.PointLight(0xff007f, 3, 250);
        pointLight3.position.set(0, 100, -50);
        scene.add(pointLight3);

        // 5. Build 3D Core Group
        coreGroup = new THREE.Group();
        scene.add(coreGroup);

        // Inner glowing core
        const coreGeo = new THREE.IcosahedronGeometry(28, 2);
        const coreMat = new THREE.MeshStandardMaterial({
            color: 0x07112c,
            roughness: 0.2,
            metalness: 0.9,
            emissive: 0x005577,
            emissiveIntensity: 0.4,
            wireframe: false
        });
        innerSphere = new THREE.Mesh(coreGeo, coreMat);
        coreGroup.add(innerSphere);

        // Holographic wireframe overlay
        const wireGeo = new THREE.IcosahedronGeometry(34, 1);
        const wireMat = new THREE.MeshBasicMaterial({
            color: 0x00f0ff,
            wireframe: true,
            transparent: true,
            opacity: 0.45
        });
        wireframeMesh = new THREE.Mesh(wireGeo, wireMat);
        coreGroup.add(wireframeMesh);

        // Outer Cyber Gyro Rings
        const ringConfigs = [
            { radius: 46, tube: 0.7, color: 0x00f0ff, rotX: 0.4, rotY: 0.2 },
            { radius: 56, tube: 0.6, color: 0x8b5cf6, rotX: -0.6, rotY: 0.5 },
            { radius: 68, tube: 0.5, color: 0xec4899, rotX: 1.1, rotY: -0.3 }
        ];

        ringConfigs.forEach(cfg => {
            const ringGeo = new THREE.TorusGeometry(cfg.radius, cfg.tube, 16, 100);
            const ringMat = new THREE.MeshStandardMaterial({
                color: cfg.color,
                emissive: cfg.color,
                emissiveIntensity: 0.8,
                roughness: 0.1,
                metalness: 0.9
            });
            const ringMesh = new THREE.Mesh(ringGeo, ringMat);
            ringMesh.rotation.x = cfg.rotX;
            ringMesh.rotation.y = cfg.rotY;
            coreGroup.add(ringMesh);
            rings.push({ mesh: ringMesh, speedX: (Math.random() - 0.5) * 0.015, speedY: (Math.random() - 0.5) * 0.015 });
        });

        // Orbiting Data Nodes
        const nodeGeo = new THREE.SphereGeometry(2.2, 16, 16);
        const nodeMat = new THREE.MeshBasicMaterial({ color: 0x00ffff });
        for (let i = 0; i < 6; i++) {
            const node = new THREE.Mesh(nodeGeo, nodeMat);
            const angle = (i / 6) * Math.PI * 2;
            const dist = 60 + (i % 2) * 15;
            node.position.set(Math.cos(angle) * dist, (Math.sin(angle) * 18), Math.sin(angle) * dist);
            coreGroup.add(node);
        }

        // 6. Deep Space Particle Universe
        const particleCount = 1400;
        const particleGeo = new THREE.BufferGeometry();
        const positions = new Float32Array(particleCount * 3);
        const colors = new Float32Array(particleCount * 3);

        const colorPalette = [
            new THREE.Color(0x00f0ff),
            new THREE.Color(0x8b5cf6),
            new THREE.Color(0xffffff),
            new THREE.Color(0x38bdf8)
        ];

        for (let i = 0; i < particleCount; i++) {
            positions[i * 3] = (Math.random() - 0.5) * 1200;
            positions[i * 3 + 1] = (Math.random() - 0.5) * 1200;
            positions[i * 3 + 2] = (Math.random() - 0.5) * 1200;

            const c = colorPalette[Math.floor(Math.random() * colorPalette.length)];
            colors[i * 3] = c.r;
            colors[i * 3 + 1] = c.g;
            colors[i * 3 + 2] = c.b;
        }

        particleGeo.setAttribute('position', new THREE.BufferAttribute(positions, 3));
        particleGeo.setAttribute('color', new THREE.BufferAttribute(colors, 3));

        const particleMat = new THREE.PointsMaterial({
            size: 2.2,
            vertexColors: true,
            transparent: true,
            opacity: 0.75,
            blending: THREE.AdditiveBlending
        });

        particles = new THREE.Points(particleGeo, particleMat);
        scene.add(particles);

        // Event listeners
        window.addEventListener('resize', onWindowResize, false);
        document.addEventListener('mousemove', onDocumentMouseMove, false);
        window.addEventListener('touchmove', onTouchMove, { passive: true });
        
        // Interactive Click Pulse
        window.addEventListener('pointerdown', onSceneClick, false);

        animate();
    }

    function onWindowResize() {
        windowHalfX = window.innerWidth / 2;
        windowHalfY = window.innerHeight / 2;
        camera.aspect = window.innerWidth / window.innerHeight;
        camera.updateProjectionMatrix();
        renderer.setSize(window.innerWidth, window.innerHeight);
    }

    function onDocumentMouseMove(event) {
        mouseX = (event.clientX - windowHalfX) * 0.05;
        mouseY = (event.clientY - windowHalfY) * 0.05;
    }

    function onTouchMove(event) {
        if (event.touches.length > 0) {
            mouseX = (event.touches[0].clientX - windowHalfX) * 0.05;
            mouseY = (event.touches[0].clientY - windowHalfY) * 0.05;
        }
    }

    function onSceneClick() {
        // Dynamic pulse animation on interaction
        if (!coreGroup) return;
        const startScale = coreGroup.scale.x;
        let progress = 0;
        function pulse() {
            progress += 0.08;
            const s = startScale + Math.sin(progress * Math.PI) * 0.18;
            coreGroup.scale.set(s, s, s);
            if (progress < 1) {
                requestAnimationFrame(pulse);
            } else {
                coreGroup.scale.set(1, 1, 1);
            }
        }
        pulse();
    }

    function animate() {
        requestAnimationFrame(animate);

        const delta = clock.getDelta();
        const time = clock.getElapsedTime();

        // Smooth mouse parallax
        targetX += (mouseX - targetX) * 0.05;
        targetY += (mouseY - targetY) * 0.05;

        if (coreGroup) {
            coreGroup.rotation.y += 0.008;
            coreGroup.rotation.x = targetY * 0.02 + Math.sin(time * 0.8) * 0.08;
            coreGroup.rotation.z = targetX * 0.02 + Math.cos(time * 0.6) * 0.06;
            
            // Hover floating movement
            coreGroup.position.y = Math.sin(time * 1.5) * 8;
        }

        if (wireframeMesh) {
            wireframeMesh.rotation.y -= 0.012;
            wireframeMesh.rotation.x += 0.006;
        }

        rings.forEach((r, idx) => {
            r.mesh.rotation.x += r.speedX + Math.sin(time * 0.5 + idx) * 0.005;
            r.mesh.rotation.y += r.speedY + Math.cos(time * 0.5 + idx) * 0.005;
        });

        if (particles) {
            particles.rotation.y = time * 0.015 + targetX * 0.005;
            particles.rotation.x = time * 0.008 + targetY * 0.005;
        }

        renderer.render(scene, camera);
    }

    // Launch when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();
