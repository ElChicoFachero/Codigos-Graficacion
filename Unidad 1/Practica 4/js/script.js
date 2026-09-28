const canvas = document.getElementById('lienzoImagen');
const ctx = canvas.getContext('2d');
const rangeUmbral = document.getElementById('rangeUmbral');
const valUmbral = document.getElementById('valUmbral'); 

//Dibuja una imagen de prueba "Simulando un sello aduanal a color"
function dibujarImagenPrueba(){
    //Fondo Claro
    ctx.fillStyle = '#fef08a';
    ctx.fillRect(0, 0, 400, 300);

    //Circulo rojo (Sello)
    ctx.fillStyle = '#ef4444';
    ctx.beginPath();
    ctx.arc(200,150,80,0, Math.PI * 2);
    ctx.fill();

    //Texto azul (Firma)
    ctx.fillStyle = '#1d4ed8';
    ctx.font = '30px Arial';
    ctx.fillText("APROBADO", 110, 160);
}

//Filtro a escala de grises
function aplicarEscalaGrises(){
    //Extraemos la matriz unidimensional [R,G,B,A, R,G,B,A...]
    let imgData = ctx.getImageData(0,0,canvas.width,canvas.height);
    let datos = imgData.data;

    //Iteramos de 4 en 4 bytes
    for (let i = 0; i < datos.length; i += 4){
        let r = datos [i];
        let g = datos [i + 1];
        let b = datos [i + 2];
        //datos [i + 3] es la transparencia

        //Ecuacion de luminiscencia estandar
        let gris = (r * 0.3) + (g * 0,59) + (b * 0.11);

        //Sobreescribimos los canales originales
        datos [i] = gris;
        datos [i + 1] = gris;
        datos [i + 2] = gris;
    }
    //Regresamos la matriz procesada a la pantalla
    ctx.putImageData(imgData, 0, 0);
}

//Filtro de binarizacion (Blanco y negro Puro) para lectura OCR
function aplicarUmbral(){
    dibujarImagenPrueba();
    let umbralActual = parseInt(rangeUmbral.value);
    let imgData = ctx.getImageData(0, 0 , canvas.width, canvas.height);
    let datos = imgData.data;
 
    for (let i = 0; i < datos.length; i += 4){
        let r = datos [i];
        let g = datos[i + 1];
        let b = datos [i + 2];
        let gris = (r * 0.3) + (g * 0.59) + (b * 0.11);

        //Si es mas oscuro que 128, lo hacemos negro, si no, blanco
        let colorFinal = (gris > umbralActual) ? 255 : 0;

        datos [i] = colorFinal;
        datos [i + 1] = colorFinal;
        datos [i + 2] = colorFinal;
    }
    ctx.putImageData(imgData, 0, 0);
}

//Actualizar valor mostrado del umbral
rangeUmbral.addEventListener('input', () => {
 valUmbral.textContent = rangeUmbral.value;
});

//Events Listeners
document.getElementById ('btnGris').addEventListener('click', aplicarEscalaGrises);
document.getElementById ('btnUmbral').addEventListener('click', aplicarUmbral);
document.getElementById ('btnReset').addEventListener('click', dibujarImagenPrueba);

//Ejecucion inicial
dibujarImagenPrueba();