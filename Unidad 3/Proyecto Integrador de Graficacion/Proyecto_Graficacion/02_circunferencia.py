import numpy as np
import matplotlib.pyplot as plt

def circunferencia_punto_medio(radio, buffer, cx=0, cy=0):
    """Calcula una circunferencia con el algoritmo del punto medio."""
    x, y = 0, radio
    p = 1 - radio
    puntos = set()

    while x <= y:
        simetricos = [
            (cx + x, cy + y), (cx - x, cy + y),
            (cx + x, cy - y), (cx - x, cy - y),
            (cx + y, cy + x), (cx - y, cy + x),
            (cx + y, cy - x), (cx - y, cy - x)
        ]
        for px, py in simetricos:
            if 0 <= py < buffer.shape[0] and 0 <= px < buffer.shape[1]:
                buffer[py, px] = 1
                puntos.add((px, py))

        x += 1
        if p < 0:
            p += 2 * x + 1
        else:
            y -= 1
            p += 2 * (x - y) + 1

    return sorted(puntos)

if __name__ == "__main__":
    radio = 8
    # Buffer 21x21 para representar coordenadas de -10 a 10.
    buffer = np.zeros((21, 21), dtype=int)
    puntos = circunferencia_punto_medio(radio, buffer, cx=10, cy=10)

    print("Radio:", radio)
    print("Numero de pixeles encendidos:", len(puntos))
    print("Primeros puntos (coordenadas de la matriz):", puntos[:12])

    plt.figure(figsize=(7, 7))
    plt.imshow(buffer, cmap="Greens", origin="lower",
               extent=(-10.5, 10.5, -10.5, 10.5), vmin=0, vmax=1)
    plt.xticks(range(-10, 11, 1))
    plt.yticks(range(-10, 11, 1))
    plt.grid(True, linestyle=":", linewidth=0.5)
    plt.title("Circunferencia por punto medio (r = 8)")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.axis("equal")
    plt.tight_layout()
    plt.show()
