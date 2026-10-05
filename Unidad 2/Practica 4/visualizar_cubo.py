import numpy as np
import matplotlib.pyplot as plt

#Reutilizar matrices 4x4 de la practica 2.3
def obtener_matriz_traslacion_3d(tx,ty,tz):
    return np.array([
        [1, 0, 0, tx],
        [0, 1, 0, ty],
        [0, 0, 1, tz],
        [0, 0, 0, 1]
    ], dtype = float)

def obtener_matriz_escalacion_3d(sx,sy, sz):
    return np.array([
        [sx, 0, 0, 0],
        [0, sy, 0, 0],
        [0, 0, sz, 0],
        [0, 0, 0, 1]
    ], dtype = float)

def rotacion_x(grados):
    t = np.radians(grados)
    c, s = np.cos(t), np.sin(t)
    return np.array([
        [1, 0, 0, 0],
        [0, c, -s, 0],
        [0, s, c, 0],
        [0, 0, 0, 1]
    ], dtype = float)

def rotacion_y(grados):
    t = np.radians(grados)
    c, s = np.cos(t), np.sin(t)
    return np.array([
        [c, 0, s, 0],
        [0, 1, 0, 0],
        [-s, 0, c, 0],
        [0, 0, 0, 1]
    ], dtype = float)

def rotacion_z(grados):
    t = np.radians(grados)
    c, s = np.cos(t), np.sin(t)
    return np.array([
        [c, -s, 0, 0],
        [s, c, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ], dtype = float)

vertices = np.array([
    [-1,-1,-1],[1,-1,-1],[1,1,-1],[-1,1,-1],
    [-1,-1, 1],[1,-1, 1],[1, 1, 1],[-1, 1, 1]
], dtype=float)

aristas = [(0,1),(1,2),(2,3),(3,0),
           (4,5),(5,6),(6,7),(7,4),
           (0,4),(1,5),(2,6),(3,7)]

Vh = np.c_[vertices, np.ones(len(vertices))] 
M = (obtener_matriz_traslacion_3d(3,1,2) @ rotacion_x(35) @ obtener_matriz_escalacion_3d(1.5, 0.8, 2.0))
V2 = (M @ Vh.T).T[:, :3]

# Visualizar el cubo
fig = plt.figure(figsize=(8, 6))
ax = fig.add_subplot(111, projection='3d')

# Dibujar las aristas
for i, j in aristas:
    ax.plot(*zip(vertices[i], vertices[j]))
    ax.plot(*zip(V2[i], V2[j]))

ax.set_xlabel('X'); ax.set_ylabel('Y'); ax.set_zlabel('Z')
ax.set_title('Cubo Original vs Transformado')

plt.show()