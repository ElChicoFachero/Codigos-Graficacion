import matplotlib.pyplot as plt

INSIDE, LEFT, RIGHT, BOTTOM, TOP = 0, 1, 2, 4, 8

def outcode(x, y, xmin, ymin, xmax, ymax):
    code = INSIDE
    if x < xmin:
        code |= LEFT
    elif x > xmax:
        code |= RIGHT
    if y < ymin:
        code |= BOTTOM
    elif y > ymax:
        code |= TOP
    return code

def recortar_linea(x0, y0, x1, y1, xmin, ymin, xmax, ymax):
    """Devuelve (aceptada, x0, y0, x1, y1) tras recortar el segmento."""
    c0 = outcode(x0, y0, xmin, ymin, xmax, ymax)
    c1 = outcode(x1, y1, xmin, ymin, xmax, ymax)

    while True:
        if c0 == 0 and c1 == 0:
            return True, x0, y0, x1, y1
        if c0 & c1:
            return False, x0, y0, x1, y1

        c = c0 if c0 != 0 else c1
        if c & TOP:
            if y1 == y0: return False, x0, y0, x1, y1
            x = x0 + (x1-x0) * (ymax-y0) / (y1-y0)
            y = ymax
        elif c & BOTTOM:
            if y1 == y0: return False, x0, y0, x1, y1
            x = x0 + (x1-x0) * (ymin-y0) / (y1-y0)
            y = ymin
        elif c & RIGHT:
            if x1 == x0: return False, x0, y0, x1, y1
            y = y0 + (y1-y0) * (xmax-x0) / (x1-x0)
            x = xmax
        else:  # LEFT
            if x1 == x0: return False, x0, y0, x1, y1
            y = y0 + (y1-y0) * (xmin-x0) / (x1-x0)
            x = xmin

        if c == c0:
            x0, y0 = x, y
            c0 = outcode(x0, y0, xmin, ymin, xmax, ymax)
        else:
            x1, y1 = x, y
            c1 = outcode(x1, y1, xmin, ymin, xmax, ymax)

if __name__ == "__main__":
    xmin, ymin, xmax, ymax = 2.0, 2.0, 8.0, 7.0
    x0, y0, x1, y1 = 0.0, 4.0, 10.0, 8.0
    aceptada, ax0, ay0, ax1, ay1 = recortar_linea(
        x0, y0, x1, y1, xmin, ymin, xmax, ymax
    )

    print("Outcode P1:", format(outcode(x0,y0,xmin,ymin,xmax,ymax), "04b"))
    print("Outcode P2:", format(outcode(x1,y1,xmin,ymin,xmax,ymax), "04b"))
    print("Aceptada:", aceptada)
    if aceptada:
        print(f"P1' = ({ax0:.3f}, {ay0:.3f})")
        print(f"P2' = ({ax1:.3f}, {ay1:.3f})")

    plt.figure(figsize=(7, 5))
    plt.plot([xmin,xmax,xmax,xmin,xmin],
             [ymin,ymin,ymax,ymax,ymin], "k-", linewidth=2,
             label="Ventana de recorte")
    plt.plot([x0,x1], [y0,y1], "r--o", label="Linea original")
    if aceptada:
        plt.plot([ax0,ax1], [ay0,ay1], "g-o", linewidth=2.5,
                 label="Segmento recortado")
    plt.xlim(-1, 11); plt.ylim(0, 10)
    plt.xlabel("X"); plt.ylabel("Y")
    plt.title("Recorte Cohen-Sutherland")
    plt.grid(True); plt.legend(); plt.axis("equal")
    plt.tight_layout()
    plt.show()
