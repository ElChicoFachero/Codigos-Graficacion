
window.addEventListener("load", function () {

    // =====================================
    // 1. DIMENSIONES EN PIES
    // =====================================
    const L = 43;
    const A = 8;
    const H = 8.5;

    const escenaDiv = document.getElementById("escena");

    // =====================================
    // 2. ESCENA Y CÁMARA
    // =====================================
    const escena = new THREE.Scene();
    escena.background = new THREE.Color(0xdce6ef);

    const camara = new THREE.PerspectiveCamera(
        40,
        escenaDiv.clientWidth / escenaDiv.clientHeight,
        0.1,
        1000
    );

    camara.position.set(48, 28, 38);
    camara.lookAt(0, H / 2, 0);

    // =====================================
    // 3. RENDERIZADOR
    // =====================================
    const renderizador = new THREE.WebGLRenderer({
        antialias: true
    });

    renderizador.setPixelRatio(
        Math.min(window.devicePixelRatio, 2)
    );

    renderizador.setSize(
        escenaDiv.clientWidth,
        escenaDiv.clientHeight
    );

    renderizador.outputEncoding = THREE.sRGBEncoding;
    renderizador.shadowMap.enabled = true;
    renderizador.shadowMap.type = THREE.PCFSoftShadowMap;

    escenaDiv.appendChild(renderizador.domElement);

    // =====================================
    // 4. CONTROLES 3D
    // =====================================
    const controles = new THREE.OrbitControls(
        camara,
        renderizador.domElement
    );

    controles.target.set(0, H / 2, 0);
    controles.enableDamping = true;
    controles.minDistance = 15;
    controles.maxDistance = 120;

    // =====================================
    // 5. MATERIALES
    // =====================================
    const azul = new THREE.MeshStandardMaterial({
        color: 0x164f82,
        roughness: 0.7,
        metalness: 0.25,
        side: THREE.DoubleSide
    });

    const azulClaro = new THREE.MeshStandardMaterial({
        color: 0x286b9e,
        roughness: 0.65,
        metalness: 0.3
    });

    const azulOscuro = new THREE.MeshStandardMaterial({
        color: 0x103653,
        roughness: 0.65,
        metalness: 0.3
    });

    const metal = new THREE.MeshStandardMaterial({
        color: 0xb9c4cc,
        roughness: 0.35,
        metalness: 0.75
    });

    const negro = new THREE.MeshStandardMaterial({
        color: 0x252c32,
        roughness: 0.7
    });

    // =====================================
    // 6. FUNCIÓN PARA CREAR PIEZAS
    // =====================================
    function caja(
        nombre,
        x, y, z,
        sx, sy, sz,
        material
    ) {
        const geometria = new THREE.BoxGeometry(
            sx, sy, sz
        );

        const objeto = new THREE.Mesh(
            geometria,
            material
        );

        objeto.name = nombre;
        objeto.position.set(x, y, z);
        objeto.castShadow = true;
        objeto.receiveShadow = true;

        escena.add(objeto);
        return objeto;
    }

    // =====================================
    // 7. BASE Y TECHO
    // =====================================

    // Piso
    caja(
        "Piso", 0, 0.12, 0,
        L, 0.24, A,
        azulOscuro
    );

    // Techo
    caja(
        "Techo", 0, H - 0.08, 0,
        L, 0.16, A,
        azul
    );

    // =====================================
    // 8. PAREDES LATERALES
    // =====================================

    // Panel lateral izquierdo y derecho
    caja(
        "Lateral izquierdo",
        0, H / 2, -A / 2,
        L, H, 0.12,
        azul
    );

    caja(
        "Lateral derecho",
        0, H / 2, A / 2,
        L, H, 0.12,
        azul
    );

    // Nervaduras verticales de las paredes
    // Proporcionan la apariencia de lámina ondulada
    const cantidadNervaduras = 44;

    for (let i = 0; i <= cantidadNervaduras; i++) {

        const x = -L / 2 + (L / cantidadNervaduras) * i;

        // Lateral izquierdo
        caja(
            "Nervadura izquierda",
            x, H / 2, -A / 2 - 0.09,
            0.16, H - 0.35, 0.12,
            azulClaro
        );

        // Lateral derecho
        caja(
            "Nervadura derecha",
            x, H / 2, A / 2 + 0.09,
            0.16, H - 0.35, 0.12,
            azulClaro
        );
    }

    // =====================================
    // 9. NERVADURAS DEL TECHO
    // =====================================

    for (let i = 0; i <= 24; i++) {

        const x = -L / 2 + (L / 24) * i;

        caja(
            "Nervadura del techo",
            x, H + 0.025, 0,
            0.12, 0.07, A - 0.3,
            azulClaro
        );
    }

    // =====================================
    // 10. PARED FRONTAL
    // =====================================

    caja(
        "Frente",
        -L / 2, H / 2, 0,
        0.16, H, A,
        azul
    );

    // Refuerzos de la pared frontal
    for (let i = 0; i <= 8; i++) {

        const z = -A / 2 + (A / 8) * i;

        caja(
            "Refuerzo frontal",
            -L / 2 - 0.1, H / 2, z,
            0.10, H - 0.3, 0.10,
            azulClaro
        );
    }

    // =====================================
    // 11. PUERTAS TRASERAS
    // =====================================

    const xPuertas = L / 2 + 0.08;
    const anchoPuerta = A / 2 - 0.08;

    // Dos hojas de las puertas
    caja(
        "Puerta izquierda",
        xPuertas, H / 2, -A / 4,
        0.16, H - 0.3, anchoPuerta,
        azul
    );

    caja(
        "Puerta derecha",
        xPuertas, H / 2, A / 4,
        0.16, H - 0.3, anchoPuerta,
        azul
    );

    // Ondulaciones verticales de las puertas
    for (let i = 0; i <= 16; i++) {

        const z = -A / 2 + (A / 16) * i;

        caja(
            "Nervadura de puerta",
            xPuertas + 0.1,
            H / 2,
            z,
            0.07,
            H - 0.55,
            0.09,
            azulClaro
        );
    }

    // Barras verticales de cierre
    [-A / 4, A / 4].forEach(function (z) {

        caja(
            "Barra de cierre",
            xPuertas + 0.18,
            H / 2,
            z,
            0.10,
            H - 0.8,
            0.10,
            metal
        );

        // Manijas
        [H * 0.35, H * 0.65].forEach(function (y) {

            caja(
                "Manija",
                xPuertas + 0.25,
                y,
                z - 0.12,
                0.08,
                0.45,
                0.18,
                metal
            );
        });
    });

    // Bisagras en los extremos de las puertas
    [-A / 2 + 0.15, -0.15, 0.15, A / 2 - 0.15]
        .forEach(function (z) {

            [1, 3.2, 5.5, 7.4].forEach(function (y) {

                caja(
                    "Bisagra",
                    xPuertas + 0.18,
                    y,
                    z,
                    0.12,
                    0.38,
                    0.16,
                    metal
                );
            });
        });

    // =====================================
    // 12. POSTES Y ESQUINAS REFORZADAS
    // =====================================

    const esquinas = [
        [-L / 2, -A / 2],
        [-L / 2, A / 2],
        [L / 2, -A / 2],
        [L / 2, A / 2]
    ];

    esquinas.forEach(function (p) {

        caja(
            "Poste de esquina",
            p[0], H / 2, p[1],
            0.38, H, 0.38,
            azulOscuro
        );

        // Bloques de esquina superior e inferior
        [0.2, H - 0.2].forEach(function (y) {

            caja(
                "Bloque de esquina",
                p[0], y, p[1],
                0.65, 0.4, 0.65,
                metal
            );
        });
    });

    // =====================================
    // 13. TRAVESAÑOS SUPERIORES
    // =====================================

    caja(
        "Travesaño superior izquierdo",
        0, H - 0.15, -A / 2,
        L, 0.3, 0.3,
        azulOscuro
    );

    caja(
        "Travesaño superior derecho",
        0, H - 0.15, A / 2,
        L, 0.3, 0.3,
        azulOscuro
    );

    // =====================================
    // 14. TRAVESAÑOS INFERIORES
    // =====================================

    caja(
        "Travesaño inferior izquierdo",
        0, 0.2, -A / 2,
        L, 0.4, 0.35,
        azulOscuro
    );

    caja(
        "Travesaño inferior derecho",
        0, 0.2, A / 2,
        L, 0.4, 0.35,
        azulOscuro
    );

    // =====================================
    // 15. ILUMINACIÓN Y SUELO
    // =====================================

    escena.add(
        new THREE.HemisphereLight(
            0xffffff,
            0x697786,
            2
        )
    );

    const luzPrincipal = new THREE.DirectionalLight(
        0xffffff, 2.5
    );

    luzPrincipal.position.set(15, 35, 25);
    luzPrincipal.castShadow = true;

    escena.add(luzPrincipal);

    const suelo = new THREE.Mesh(
        new THREE.PlaneGeometry(120, 120),
        new THREE.MeshStandardMaterial({
            color: 0xc4cdd5,
            roughness: 0.9
        })
    );

    suelo.rotation.x = -Math.PI / 2;
    suelo.position.y = -0.15;
    suelo.receiveShadow = true;

    escena.add(suelo);

    // Rejilla discreta en el suelo
    const rejilla = new THREE.GridHelper(
        100, 50, 0x8495a5, 0xb6c2cc
    );

    rejilla.position.y = -0.13;
    escena.add(rejilla);

    // =====================================
    // 16. BOTONES DE VISTA
    // =====================================

    function cambiarVista(x, y, z) {

        camara.position.set(x, y, z);
        controles.target.set(0, H / 2, 0);
        controles.update();
    }

    document.getElementById("vistaCompleta")
        .addEventListener("click", function () {

            cambiarVista(48, 28, 38);
        });

    document.getElementById("vistaPuertas")
        .addEventListener("click", function () {

            cambiarVista(60, 18, 0);
        });

    document.getElementById("vistaLateral")
        .addEventListener("click", function () {

            cambiarVista(0, 18, 48);
        });

    // =====================================
    // 17. ANIMACIÓN
    // =====================================

    function animar() {

        requestAnimationFrame(animar);

        controles.update();
        renderizador.render(escena, camara);
    }

    animar();

    // =====================================
    // 18. AJUSTE DE PANTALLA
    // =====================================

    window.addEventListener("resize", function () {

        const anchoPantalla = escenaDiv.clientWidth;
        const altoPantalla = escenaDiv.clientHeight;

        camara.aspect = anchoPantalla / altoPantalla;
        camara.updateProjectionMatrix();

        renderizador.setSize(
            anchoPantalla,
            altoPantalla
        );
    });

});
