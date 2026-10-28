import numpy as np
import matplotlib.pyplot as plt

def linea_bresenham(x0, y0, x1, y1, buffer):
    """Enciende los pixeles de una linea usando Bresenham."""
    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    error = dx - dy
    pixeles = []

    while True:
        buffer[y0, x0] = 1
        pixeles.append((x0, y0))
        if x0 == x1 and y0 == y1:
            break

        e2 = 2 * error
        if e2 > -dy:
            error -= dy
            x0 += sx
        if e2 < dx:
            error += dx
            y0 += sy
    return pixeles

if __name__ == "__main__":
    buffer = np.zeros((15, 15), dtype=int)
    pixeles = linea_bresenham(2, 3, 11, 8, buffer)

    print("Pixeles encendidos (x, y):")
    print(pixeles)
    print("Total de pixeles:", len(pixeles))

    plt.figure(figsize=(7, 6))
    plt.imshow(buffer, cmap="Blues", origin="lower",
               extent=(-0.5, 14.5, -0.5, 14.5), vmin=0, vmax=1)
    plt.xticks(range(15))
    plt.yticks(range(15))
    plt.grid(True, color="gray", linestyle=":", linewidth=0.7)
    plt.scatter([p[0] for p in pixeles], [p[1] for p in pixeles],
                color="red", s=35, label="Pixeles calculados")
    plt.title("Rasterizacion de linea - Bresenham")
    plt.xlabel("Coordenada X")
    plt.ylabel("Coordenada Y")
    plt.legend()
    plt.tight_layout()
    plt.show()
