const colorPicker = document.getElementById('colorPicker');

const boxBase = document.getElementById('boxBase');
const boxHover = document.getElementById('boxHover');
const boxDisabled = document.getElementById('boxDisabled');
const boxContrast = document.getElementById('boxContrast');

//Elemento donde mostraremos los valores
const valuesBase = document.getElementById('valuesBase');
const valuesHover = document.getElementById('valuesHover');
const valuesDisabled = document.getElementById('valuesDisabled'); 

let valuesContrast = document.getElementById('valuesContrast');

if (!valuesContrast) {
    valuesContrast = document.createElement('div');
    valuesContrast.id = 'valuesContrast';
    boxContrast.parentElement.appendChild(valuesContrast);
}

//Convierte de HEX a RGB
function hexToRGB(hex){
    let r = parseInt(hex.substring(1,3),16);
    let g = parseInt(hex.substring(3,5),16);
    let b = parseInt(hex.substring(5,7),16);
    return {r,g,b};
}

//Convierte de RGB a HSL (Matematic pura de la teoria del color)
function rgbToHSL(r,g,b){
    r /= 255; 
    g/=255; 
    b/=255;
    let max = Math.max(r,g,b);
    let min = Math.min (r,g,b);
    let h,s,l = (max + min) /2;

    if (max == min){
        h = s = 0; //Escala de Grises
    } else {
        let d = max - min;
        s = l > 0.5 ? d / (2 - max - min) : d / (max + min);
        switch(max){
            case r: h = (g - b) / d + (g < b ? 6 : 0); break;
            case g: h = (b - r) / d + 2; break;
            case b: h = (r - g) / d + 4; break;
        }
        h /= 6;
    }
    return {h: Math.round(h*360), s:Math.round(s*100), l:Math.round(l*100)};
}

//Convierte de RGB a HEX
function rgbToHex(r,g,b){
    return "#" + [r,g,b].map(valor => valor.toString(16).padStart(2,'0')).join('').toUpperCase();
}
// Calcula el color de texto con mayor contraste
function obtenerAltoContraste(rgb) {
    const luminosidad =
        (0.299 * rgb.r) +
        (0.587 * rgb.g) +
        (0.114 * rgb.b);

    // Si el fondo es claro usamos texto negro,
    // si el fondo es oscuro usamos texto blanco
    if (luminosidad > 128) {
        return { r: 0, g: 0, b: 0 };
    } else {
        return { r: 255, g: 255, b: 255 };
    }
}
//Actualiza los valores mostrados en pantalla
function mostrarValoresColores (elemento, hex, rgb, hsl){
elemento.innerHTML = `<p><strong>HEX:</strong> ${hex}</p><p><strong>
RGB:</strong> rgb(${rgb.r}, ${rgb.g}, ${rgb.b})</p><p><strong>
HSL:</strong> hsl(${hsl.h}, ${hsl.s}%, ${hsl.l}%)</p>`;
}

//Calcula la Luminosidad relativa para accesibilidad
function luminosidadRelativa(rgb){
    const valores = [rgb.r,rgb.g,rgb.b].map(valor => {
        valor /= 255;
        if (valor <= 0.03928) {
            return valor / 12.92;
        } else {
            return Math.pow((valor + 0.055) / 1.055, 2.4);
        }
    });
    return (0.2126 * valores[0] + 0.7152 * valores[1] + 0.0722 * valores[2]);
}
//Calcula el color de alto Contraste
function obtenerAltoConstraste(rgb){
    //Luminosidad relativa aproximada
    const luminosidad = (0.299 * rgb.r + 0.587 * rgb.g + 0.114 * rgb.b);
    //Si el color es oscuro, usuamos blanco, y si es claro, usamos negro
    if (luminosidad > 128){
        return {r:0, g:0, b:0};
    } else {
        return {r:255, g:255, b:255};
    }
}

function generarPaleta(){
    let hex = colorPicker.value; //Obtener el color seleccionado
    let rgb = hexToRGB(hex); //Convertir de HEX a RGB
    let hsl = rgbToHSL(rgb.r, rgb.g, rgb.b); //Convertir de RGB a HSL

    //1.Color Base
    boxBase.style.backgroundColor = hex;
    mostrarValoresColores (valuesBase, hex, rgb, hsl);

    //2.Color Hover (Restamos 15% a la Luminosidad, evitando numeros negativos)
    let hoverL = Math.max(0, hsl.l -15);
    boxHover.style.backgroundColor=`hsl(${hsl.h}, ${hsl.s}%, ${hoverL}%)`;
    //Convertirmos el HSL del Hover a RGB
    let hoverHsl = {h: hsl.h, s: hsl.s, l: hoverL} //Mostrar los valores

    //Convertimos el color Hover a RGB
    let hoverRGB = hslToRGB(hsl.h, hsl.s, hoverL);
    let hoverHex = rgbToHex(hoverRGB.r, hoverRGB.g, hoverRGB.b);

    mostrarValoresColores (valuesHover, hoverHex, hoverRGB, hoverHsl);

    //3.Color Disabled (Saturacion a 0, Luminopsidad a 80 para gris claro)
    boxDisabled.style.backgroundColor=`hsl(${hsl.h}, 0%, 80%)`;
    //Convertimos el HSL a un RGB aproximado para mostrarlo
    let disabledRGB = {r:204, g:204, b:204}; //Aproximado para hsl(0,0%,80%)
    let disabledHex = rgbToHex (disabledRGB.r, disabledRGB.g, disabledRGB.b);
    let disabledHsl = rgbToHSL(disabledRGB.r, disabledRGB.g, disabledRGB.b);
    boxDisabled.style.color = "black";
    mostrarValoresColores (valuesDisabled, disabledHex, disabledRGB, disabledHsl);

    //4. Alto Constraste
    let contrasteRGB = obtenerAltoConstraste(rgb);
    let contrasteHex = rgbToHex(contrasteRGB.r, contrasteRGB.g, contrasteRGB.b);
    let contrasteHsl = rgbToHSL(contrasteRGB.r, contrasteRGB.g, contrasteRGB.b);
   
    //Mantiene el color base como fondo
    boxContrast.style.backgroundColor= hex;

    //Cambia el textp a negro o blanco
    boxContrast.style.color = contrasteHex;

    //Quitamos la sombra para que el texto sea mas claro
    boxContrast.style.textShadow = "none";
    
    //Mostrar los valores del color del Texto
    mostrarValoresColores (valuesContrast, contrasteHex, contrasteRGB, contrasteHsl);
}


// Convierte de HSL a RGB
function hslToRGB(h, s, l) {

    s /= 100;
    l /= 100;

    let c = (1 - Math.abs(2 * l - 1)) * s;
    let x = c * (1 - Math.abs((h / 60) % 2 - 1));
    let m = l - c / 2;

    let r = 0;
    let g = 0;
    let b = 0;

    if (h >= 0 && h < 60) {
        r = c;
        g = x;
        b = 0;
    } 
    else if (h >= 60 && h < 120) {
        r = x;
        g = c;
        b = 0;
    } 
    else if (h >= 120 && h < 180) {
        r = 0;
        g = c;
        b = x;
    } 
    else if (h >= 180 && h < 240) {
        r = 0;
        g = x;
        b = c;
    } 
    else if (h >= 240 && h < 300) {
        r = x;
        g = 0;
        b = c;
    } 
    else if (h >= 300 && h <= 360) {
        r = c;
        g = 0;
        b = x;
    }

    return {
        r: Math.round((r + m) * 255),
        g: Math.round((g + m) * 255),
        b: Math.round((b + m) * 255)
    };
}

//Escuchar cambios en el input
colorPicker.addEventListener('input', generarPaleta);

//Ejecucion inicial para mostrar la paleta al cargar la pagina
generarPaleta();