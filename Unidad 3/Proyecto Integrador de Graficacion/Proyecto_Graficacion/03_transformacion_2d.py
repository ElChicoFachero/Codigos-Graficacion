import numpy as np
import matplotlib.pyplot as plt

def traslacion(tx, ty):
    return np.array([[1, 0, tx],
                     [0, 1, ty],
                     [0, 0, 1]], dtype=float)

def rotacion(grados):
    a = np.radians(grados)
    return np.array([[np.cos(a), -np.sin(a), 0],
                     [np.sin(a),  np.cos(a), 0],
                     [0, 0, 1]], dtype=float)

def escalacion(sx, sy):
    return np.array([[sx, 0, 0],
                     [0, sy, 0],
                     [0, 0, 1]], dtype=float)

if __name__ == "__main__":
    # Vertices A(2,2), B(6,2), C(4,6), cerrando el triangulo.
    vertices = np.array([[2, 6, 4, 2],
                         [2, 2, 6, 2],
                         [1, 1, 1, 1]], dtype=float)
    px, py = 4, 3

    T1 = traslacion(-px, -py)
    R = rotacion(45)
    S = escalacion(1.5, 1.5)
    T2 = traslacion(px, py)
    M = T2 @ R @ S @ T1
    transformados = M @ vertices

    print("Matriz compuesta T2 @ R @ S @ T1:")
    print(np.round(M, 4))
    print("\nVertices transformados:")
    for nombre, i in zip(("A", "B", "C"), range(3)):
        print(f"{nombre}: ({transformados[0, i]:.3f}, {transformados[1, i]:.3f})")

    plt.figure(figsize=(7, 7))
    plt.plot(vertices[0], vertices[1], "bo-", label="Original")
    plt.plot(transformados[0], transformados[1], "ro--", label="Transformado")
    plt.scatter([px], [py], marker="X", s=120, color="green", label="Pivote (4,3)")
    plt.axhline(0, color="gray", linewidth=0.7)
    plt.axvline(0, color="gray", linewidth=0.7)
    plt.grid(True)
    plt.axis("equal")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.title("Transformacion compuesta 2D")
    plt.legend()
    plt.tight_layout()
    plt.show()
