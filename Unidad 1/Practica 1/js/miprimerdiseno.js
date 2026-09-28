const canvas = document.getElementById('lienzo');
const ctx = canvas.getContext('2d');

// Tamaño del canvas
const ancho = canvas.width;
const alto = canvas.height;

// Centro del plano
const centroX = ancho / 2;
const centroY = alto / 2;

// Separación de la cuadrícula: cada 50 píxeles
const separacion = 50;

function convertirCoordenadas(x_mate, y_mate) {
    return {
        x: centroX + x_mate,
        y: centroY - y_mate
    };
}

function dibujarCuadricula() {

    ctx.strokeStyle = '#e2e8f0';
    ctx.lineWidth = 1;

    // Líneas verticales hacia la derecha
    for (let x = centroX; x <= ancho; x += separacion) {
        ctx.beginPath();
        ctx.moveTo(x, 0);
        ctx.lineTo(x, alto);
        ctx.stroke();
    }

    // Líneas verticales hacia la izquierda
    for (let x = centroX; x >= 0; x -= separacion) {
        ctx.beginPath();
        ctx.moveTo(x, 0);
        ctx.lineTo(x, alto);
        ctx.stroke();
    }

    // Líneas horizontales hacia abajo
    for (let y = centroY; y <= alto; y += separacion) {
        ctx.beginPath();
        ctx.moveTo(0, y);
        ctx.lineTo(ancho, y);
        ctx.stroke();
    }

    // Líneas horizontales hacia arriba
    for (let y = centroY; y >= 0; y -= separacion) {
        ctx.beginPath();
        ctx.moveTo(0, y);
        ctx.lineTo(ancho, y);
        ctx.stroke();
    }
}

function dibujarEjes() {

    ctx.strokeStyle = '#64748b';
    ctx.lineWidth = 2;

    ctx.beginPath();

    // Eje X
    ctx.moveTo(0, centroY);
    ctx.lineTo(ancho, centroY);

    // Eje Y
    ctx.moveTo(centroX, 0);
    ctx.lineTo(centroX, alto);

    ctx.stroke();
}

function dibujarEtiquetas() {

    ctx.fillStyle = '#000';
    ctx.font = '12px Arial';

    // -------------------------
    // Etiquetas del eje X
    // -------------------------
    for (let x = -centroX; x <= centroX; x += separacion) {

        if (x !== 0) {

            let punto = convertirCoordenadas(x, 0);

            ctx.fillText(
                x,
                punto.x - 10,
                centroY + 15
            );
        }
    }

    // -------------------------
    // Etiquetas del eje Y
    // -------------------------
    for (let y = -centroY; y <= centroY; y += separacion) {

        if (y !== 0) {

            let punto = convertirCoordenadas(0, y);

            ctx.fillText(
                y,
                centroX + 8,
                punto.y + 5
            );
        }
    }

    // -------------------------
    // Origen
    // -------------------------
    ctx.fillText(
        "(0,0)",
        centroX + 5,
        centroY + 15
    );
}


const rackVertices = [
    { x: -150, y: 100 },
    { x: 150, y: 100 },
    { x: 150, y: -100 },
    { x: -150, y: -100 }
];


// ==========================================
// DIBUJAR RECTÁNGULO
// ==========================================
function dibujarRack() {

    ctx.strokeStyle = '#2563eb';
    ctx.lineWidth = 3;

    ctx.beginPath();

    for (let i = 0; i < rackVertices.length; i++) {

        let punto = convertirCoordenadas(
            rackVertices[i].x,
            rackVertices[i].y
        );

        if (i === 0) {
            ctx.moveTo(punto.x, punto.y);
        } else {
            ctx.lineTo(punto.x, punto.y);
        }
    }

    ctx.closePath();
    ctx.stroke();
}


// ==========================================
// EJECUTAR
// ==========================================
dibujarCuadricula();
dibujarEjes();
dibujarEtiquetas();
dibujarRack();