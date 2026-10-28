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

vertices = np.array([ #Cubo Original
    [-1, -1, -1],
    [1, -1, -1],
    [1, 1, -1],
    [-1, 1, -1],
    [-1, -1, 1],
    [1, -1, 1],
    [1, 1, 1],
    [-1, 1, 1]

], dtype=float)

aristas = [(0,1),(1,2),(2,3),(3,0),
           (4,5),(5,6),(6,7),(7,4),
           (0,4),(1,5),(2,6),(3,7)]

#Coordenada Homogeneas
VH = np.c_[vertices, np.ones(len(vertices))]

#Original
V_Original = vertices
#Escalacion
S = obtener_matriz_escalacion_3d(1.5, 0.8, 2.0)
V_Escalado = (S @ VH.T).T[:, :3]
#Traslacion
T = obtener_matriz_traslacion_3d(3, 1, 2)
V_Trasladado = (T @ VH.T).T[:, :3]
#Rotacion
R = rotacion_x(35)
V_Rotado = (R @ VH.T).T[:, :3]

#Mostrar Matrices

print ("Matriz de Escalacion:\n", S)
print ("Matriz de Traslacion:\n", T)    
print ("Matriz de Rotacion:\n", R)

#Grafica
fig = plt.figure(figsize= (8,6))
ax = fig.add_subplot(111, projection="3d")

#Cubo original
def dibujar_cubo(V, color):
    for i, j in aristas:
        ax.plot(
            [V[i,0],V[j,0]],
            [V[i,1],V[j,1]],
            [V[i,2],V[j,2]],
            color=color,
            linewidth=2
    )

#Dibujar los 4 cubos
dibujar_cubo(V_Original, "blue")
dibujar_cubo(V_Escalado, "green")    
dibujar_cubo(V_Trasladado, "red")
dibujar_cubo(V_Rotado, "purple")

#Nombres
ax.text(0, 0, 0, "Original", color="black")
ax.text(3, 1, 2, "Trasladado", color="blue")
ax.text(0, 0, 0, "Escalado", color="green")
ax.text(0, 0, 0, "Rotado", color="red")

ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_zlabel("Z")

ax.set_title("Cubo original y transformaciones por separado")
plt.show()
