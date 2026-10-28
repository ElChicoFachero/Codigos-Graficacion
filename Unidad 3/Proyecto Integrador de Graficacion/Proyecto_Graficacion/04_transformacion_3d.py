import numpy as np
import matplotlib.pyplot as plt

def rotacion_x(grados):
    a = np.radians(grados)
    return np.array([[1, 0, 0, 0],
                     [0, np.cos(a), -np.sin(a), 0],
                     [0, np.sin(a),  np.cos(a), 0],
                     [0, 0, 0, 1]], dtype=float)

def rotacion_y(grados):
    a = np.radians(grados)
    return np.array([[ np.cos(a), 0, np.sin(a), 0],
                     [0, 1, 0, 0],
                     [-np.sin(a), 0, np.cos(a), 0],
                     [0, 0, 0, 1]], dtype=float)

def proyeccion_isometrica(p):
    """Proyeccion isometrica aproximada a 2D: (x,y,z) -> (u,v)."""
    x, y, z = p
    u = (x - y) * np.cos(np.radians(30))
    v = (x + y) * np.sin(np.radians(30)) - z
    return np.array([u, v])

if __name__ == "__main__":
    # Cubo de lado 4 centrado en el origen.
    vertices3 = np.array([
        [-2,-2,-2], [2,-2,-2], [2,2,-2], [-2,2,-2],
        [-2,-2, 2], [2,-2, 2], [2,2, 2], [-2,2, 2]
    ], dtype=float)
    aristas = [
        (0,1),(1,2),(2,3),(3,0),
        (4,5),(5,6),(6,7),(7,4),
        (0,4),(1,5),(2,6),(3,7)
    ]

    homog = np.vstack([vertices3.T, np.ones(8)])
    M = rotacion_y(45) @ rotacion_x(30)
    transformados = (M @ homog)[:3].T
    proyectados = np.array([proyeccion_isometrica(p) for p in transformados])

    print("Vertices rotados (x, y, z):")
    for i, v in enumerate(transformados, 1):
        print(f"V{i}: ({v[0]:.3f}, {v[1]:.3f}, {v[2]:.3f})")

    fig = plt.figure(figsize=(12, 5))
    ax1 = fig.add_subplot(121, projection="3d")
    ax1.scatter(vertices3[:,0], vertices3[:,1], vertices3[:,2], color="blue")
    for a, b in aristas:
        ax1.plot(*zip(vertices3[a], vertices3[b]), color="gray")
    ax1.set_title("Cubo original 3D")
    ax1.set_xlabel("X"); ax1.set_ylabel("Y"); ax1.set_zlabel("Z")
    ax1.set_box_aspect((1,1,1))

    ax2 = fig.add_subplot(122)
    for a, b in aristas:
        # Se dibujan segmentos entre puntos ya calculados; no se usa un algoritmo
        # automatico para decidir los vertices de rasterizacion.
        ax2.plot([proyectados[a,0], proyectados[b,0]],
                 [proyectados[a,1], proyectados[b,1]], color="darkorange")
    ax2.scatter(proyectados[:,0], proyectados[:,1], color="red")
    ax2.set_title("Cubo rotado y proyectado a 2D")
    ax2.set_xlabel("U"); ax2.set_ylabel("V")
    ax2.axis("equal"); ax2.grid(True)
    plt.tight_layout()
    plt.show()
