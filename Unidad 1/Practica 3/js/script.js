const canvas = document.getElementById('lienzoDDA');
const ctx = canvas.getContext('2d');
let puntos = []; // Guardará los clics del usuario

// Función simulada para encender un solo píxel físico en pantalla
function dibujarPixel(x, y) {
  ctx.fillStyle = '#0f172a'; // Color de "tinta"
  ctx.fillRect(Math.round(x), Math.round(y), 2, 2); // 2x2 para mayor visibilidad en resoluciones altas
}

// Algoritmo DDA (Analizador Diferencial Digital)
function algoritmoDDA(x1, y1, x2, y2) {
  let dx = x2 - x1;
  let dy = y2 - y1;
  
  // El número de pasos es la distancia más larga (X o Y)
  let pasos = Math.max(Math.abs(dx), Math.abs(dy));
  
  // Incrementos decimales por iteración
  let incX = dx / pasos;
  let incY = dy / pasos;
  let x = x1;
  let y = y1;

  const txtPendiente = document.getElementById('txtPendiente');
  if (dx !== 0) {
    let m = dy / dx;
    txtPendiente.innerHTML = `<b>Pendiente (m):</b> ${m.toFixed(4)}`;
  } else {
    txtPendiente.innerHTML = `<b>Pendiente (m):</b> Indefinida (Línea vertical)`;
  }

  // Limpiar la tabla antes de dibujar la nueva línea
  const tabla = document.getElementById('tablaCoordenadas');
  tabla.innerHTML = '';

  // Encendemos píxeles iterativamente
  for (let i = 0; i <= pasos; i++) {
    dibujarPixel(x, y);

    if (i < 15) {
      let fila = `<tr>
        <td style="padding: 4px; border: 1px solid #cbd5e1;">${i}</td>
        <td style="padding: 4px; border: 1px solid #cbd5e1;">${x.toFixed(2)}</td>
        <td style="padding: 4px; border: 1px solid #cbd5e1;">${y.toFixed(2)}</td>
        <td style="padding: 4px; border: 1px solid #cbd5e1;">(${Math.round(x)}, ${Math.round(y)})</td>
      </tr>`;
      tabla.innerHTML += fila;
    }

    x += incX;
    y += incY;
  }
}

// Captura de eventos del mouse
canvas.addEventListener('mousedown', function(e) {
  const rect = canvas.getBoundingClientRect();
  const x = e.clientX - rect.left;
  const y = e.clientY - rect.top;
  
  puntos.push({x, y});
  dibujarPixel(x, y); // Marca el punto de inicio
  
  if (puntos.length === 2) {
    algoritmoDDA(puntos[0].x, puntos[0].y, puntos[1].x, puntos[1].y);
    puntos = []; // Resetea para la siguiente línea
  }
});

function limpiarLienzo() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  puntos = [];
  
  document.getElementById('tablaCoordenadas').innerHTML = '';
  document.getElementById('txtPendiente').innerHTML = '<b>Pendiente (m):</b> N/A';
}