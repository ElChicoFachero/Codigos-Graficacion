import numpy as np
import matplotlib.pyplot as plt

#En nuestro array ingresamos nuesteos 20 puntos originales
puntos = np.array ([ #Escalacion
    [18,21], [5,60], [24,36], [40,2], [0,40],
    [27,20], [7,16], [16,63], [18,10], [28,14],
    [63,5], [24,20], [1,8], [36,72], [56,6],
    [45,121], [5,4], [32,5], [6,70], [10,45]
])

# Traslacion
tx = 3
ty = 2

puntos_traslacion = puntos + [tx, ty]

# Escalacion
sx = 2
sy = 1.5

puntos_escalacion = puntos * [sx, sy]

#Rotacion

grados = 45
theta = np.radians(grados)

matriz_rotacion = np.array([
    [np.cos(theta), -np.sin(theta)],
    [np.sin(theta), np.cos(theta)]
])

puntos_rotacion = puntos @ matriz_rotacion.T

#Grafica

plt.figure(figsize = (10, 8))

#Puntos originales
plt.scatter(
    puntos[:,0],
    puntos[:,1],
    label = "Original"
)

plt.scatter(
    puntos_traslacion[:,0],
    puntos_traslacion[:,1],
    label = "Traslacion"
)

plt.scatter(
    puntos_escalacion[:,0],
    puntos_escalacion[:,1],
    label = "Escalacion"
)

plt.scatter(
    puntos_rotacion[:,0],
    puntos_rotacion[:,1],   
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