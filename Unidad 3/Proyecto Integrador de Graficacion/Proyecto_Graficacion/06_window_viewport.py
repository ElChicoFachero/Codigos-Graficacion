
import matplotlib.pyplot as plt

# ==========================================
# 1. DATOS DE LA VENTANA Y DEL VIEWPORT
# ==========================================

XMIN_MUNDO = -50
XMAX_MUNDO = 50
YMIN_MUNDO = -50
YMAX_MUNDO = 50

ANCHO_VIEWPORT = 800
ALTO_VIEWPORT = 600

P1 = (10, 10)
P2 = (25, 40)


# ==========================================
# 2. FACTORES DE ESCALA
# ==========================================

def calcular_escala():
    sx = ANCHO_VIEWPORT / (XMAX_MUNDO - XMIN_MUNDO)
    sy = ALTO_VIEWPORT / (YMAX_MUNDO - YMIN_MUNDO)

    return sx, sy


# ==========================================
# 3. TRANSFORMACION WINDOW-TO-VIEWPORT
# ==========================================

def convertir_coordenadas(xw, yw, sx, sy):
    # El origen del dispositivo esta en la esquina superior izquierda.
    xv = (xw - XMIN_MUNDO) * sx
    yv = (YMAX_MUNDO - yw) * sy

    return xv, yv


# ==========================================
# 4. MEMORIA DE CALCULO
# ==========================================

def mostrar_memoria():
    sx, sy = calcular_escala()

    print("=" * 55)
    print("FASE 2: MEMORIA DE CALCULO")
    print("WINDOW-TO-VIEWPORT")
    print("=" * 55)

    print("\n1. FACTORES DE ESCALA")

    print("Sx = (Xvmax - Xvmin) / (Xwmax - Xwmin)")
    print(f"Sx = {ANCHO_VIEWPORT} / "
          f"({XMAX_MUNDO} - ({XMIN_MUNDO}))")
    print(f"Sx = {sx:.2f} pixeles por unidad")

    print("\nSy = (Yvmax - Yvmin) / (Ywmax - Ywmin)")
    print(f"Sy = {ALTO_VIEWPORT} / "
          f"({YMAX_MUNDO} - ({YMIN_MUNDO}))")
    print(f"Sy = {sy:.2f} pixeles por unidad")

    print("\n2. ECUACIONES DE MAPEO")
    print(f"Xv = (Xw - ({XMIN_MUNDO})) * Sx")
    print(f"Yv = ({YMAX_MUNDO} - Yw) * Sy")

    print("\n3. CALCULO DEL PUNTO P1 =", P1)

    x1, y1 = P1
    xv1, yv1 = convertir_coordenadas(x1, y1, sx, sy)

    print(f"Xv = ({x1} - ({XMIN_MUNDO})) * {sx}")
    print(f"Xv = {xv1:.2f}")
    print(f"Yv = ({YMAX_MUNDO} - {y1}) * {sy}")
    print(f"Yv = {yv1:.2f}")
    print(f"P1 en el viewport = ({xv1:.2f}, {yv1:.2f})")

    print("\n4. CALCULO DEL PUNTO P2 =", P2)

    x2, y2 = P2
    xv2, yv2 = convertir_coordenadas(x2, y2, sx, sy)

    print(f"Xv = ({x2} - ({XMIN_MUNDO})) * {sx}")
    print(f"Xv = {xv2:.2f}")
    print(f"Yv = ({YMAX_MUNDO} - {y2}) * {sy}")
    print(f"Yv = {yv2:.2f}")
    print(f"P2 en el viewport = ({xv2:.2f}, {yv2:.2f})")

    print("\n5. CONSERVACION DE PROPORCIONES")

    if sx == sy:
        print("La escala es uniforme.")
        print("Se conservan las proporciones geometricas.")
    else:
        print("La escala horizontal y vertical es diferente.")
        print("Sx =", sx, "y Sy =", sy)
        print("La imagen puede presentar distorsion.")
        print("Para conservar las proporciones se necesita")
        print("una escala uniforme y, si hace falta, margenes.")

    print("\n6. RESULTADOS PARA LA TABLA")

    print(f"P1 {P1} -> ({xv1:.2f}, {yv1:.2f})")
    print(f"P2 {P2} -> ({xv2:.2f}, {yv2:.2f})")

    return (xv1, yv1), (xv2, yv2)


# ==========================================
# 5. GRAFICA DEL VIEWPORT
# ==========================================

def graficar_viewport(p1, p2):
    fig, ax = plt.subplots(figsize=(10, 7))

    ax.set_xlim(0, ANCHO_VIEWPORT)
    ax.set_ylim(ALTO_VIEWPORT, 0)

    # Borde del dispositivo
    ax.plot(
        [0, ANCHO_VIEWPORT, ANCHO_VIEWPORT, 0, 0],
        [0, 0, ALTO_VIEWPORT, ALTO_VIEWPORT, 0],
        color="black",
        linewidth=2,
        label="Viewport 800 x 600"
    )

    # Puntos calculados
    ax.scatter(
        [p1[0], p2[0]],
        [p1[1], p2[1]],
        color=["blue", "red"],
        s=90,
        zorder=3
    )

    ax.annotate(
        f"P1 ({p1[0]:.0f}, {p1[1]:.0f})",
        p1,
        xytext=(10, -15),
        textcoords="offset points"
    )

    ax.annotate(
        f"P2 ({p2[0]:.0f}, {p2[1]:.0f})",
        p2,
        xytext=(10, -15),
        textcoords="offset points"
    )

    ax.set_title("Transformacion Window-to-Viewport")
    ax.set_xlabel("Coordenada X del dispositivo (pixeles)")
    ax.set_ylabel("Coordenada Y del dispositivo (pixeles)")

    ax.set_xticks(range(0, ANCHO_VIEWPORT + 1, 100))
    ax.set_yticks(range(0, ALTO_VIEWPORT + 1, 100))

    ax.grid(True, linestyle="--", alpha=0.5)
    ax.legend()
    plt.tight_layout()
    plt.show()


# ==========================================
# 6. EJECUCION PRINCIPAL
# ==========================================

if __name__ == "__main__":
    punto1, punto2 = mostrar_memoria()
    graficar_viewport(punto1, punto2)
