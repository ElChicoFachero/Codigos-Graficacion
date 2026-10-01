import numpy as np
import matplotlib.pyplot as plt

#En nuestro array ingresamos nuesteos 20 puntos originales
puntos = np.array ([ #Escalacion
    [2,7], [9,3], [5,10], [1,6], [8,4],
    [3,9], [10,2], [4,1], [7,8], [0,5],
    [3,2], [9,10], [7,4], [1,4], [8,7],
    [2,9], [6,1], [3,10], [4,7], [7,2],
    [9,1], [7,5], [3,10], [8,2], [1,4],
    [1,2], [6,9], [6,8], [8,6], [7,1],
    [9,12], [5,11], [1,4], [5,1], [4,5],
    [8,1], [1,10], [6,7], [2,5], [5,9]
])

#Homogenea
puntos_h = np.hstack([
    puntos, np.ones((len(puntos), 1))
])

#Grafica Homogenea 3D
fig = plt.figure(figsize =(10,8))
ax = fig.add_subplot(111, projection ='3d')

ax.plot(
    puntos_h[:,0],
    puntos_h[:,1],
    puntos_h[:,2],
    marker = "o",
    label = "Coordenadas Homogeneas"
)

ax.set_xlabel("X")
ax.set_xlabel("Y")
ax.set_xlabel("Z")

ax.set_title("Puntos en Coordenadas Homogeneas")
ax.legend()
plt.show()

# Traslacion
tx = 3
ty = 2

matriz_traslacion = np.array([
    [1,0,tx],
    [0,1,ty],
    [0,0,1]
])
puntos_traslacion = puntos_h @ matriz_traslacion.T

# Escalacion
sx = 2
sy = 1.5

matriz_escalacion = np.array([
    [sx,0,0],
    [0,sy,0],
    [0,0,1]
])
puntos_escalacion = puntos_h @ matriz_escalacion.T
#Rotacion

grados = 45
theta = np.radians(grados)

matriz_rotacion = np.array([
    [np.cos(theta), -np.sin(theta),0],
    [np.sin(theta), np.cos(theta), 0],
    [0,0,1]
])
puntos_rotacion = puntos_h @ matriz_rotacion.T
#Aplicar transformaciones
puntos_traslacion = puntos_traslacion[:, :2]
puntos_escalacion = puntos_escalacion[:, :2]
puntos_rotacion = puntos_rotacion[:, :2]


#Grafica

plt.figure(figsize = (10, 8))

#Puntos originales
plt.plot(
    puntos[:,0],
    puntos[:,1],
    marker = "o",
    label = "Original"
)

plt.plot(
    puntos_traslacion[:,0],
    puntos_traslacion[:,1],
    marker = "o",
    label = "Traslacion"
)

plt.plot(
    puntos_escalacion[:,0],
    puntos_escalacion[:,1],
    marker = "o",
    label = "Escalacion"
)

plt.plot(
    puntos_rotacion[:,0],
    puntos_rotacion[:,1],  
    marker = "o", 
    label = "Rotacion"
)

#Lineas de Referencia
plt.axhline(0)
plt.axvline(0)

plt.grid(True)

plt.xlabel("Eje X")
plt.ylabel("Eje Y")

plt.title ("Transformaciones de 20 puntos")

plt.legend()

plt.axis("equal")

plt.show()