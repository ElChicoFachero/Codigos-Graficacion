import numpy as np
import matplotlib.pyplot as plt

def traslacion (tx, ty):
    return np.array([
        [1, 0, tx],
        [0, 1, ty],
        [0, 0, 1]
    ], dtype = float)

def escalacion (sx, sy):
    return np.array([
        [sx, 0, 0],
        [0, sy, 0],
        [0, 0, 1]
    ], dtype = float)

def rotacion (grados):
    theta = np.radians (grados)
    c, s = np.cos (theta), np.sin(theta)
    return np.array([
        [c, -s, 0],
        [s, c, 0],
        [0, 0, 1],
    ], dtype = float)

def aplicar(M, vertices):
    vh = np.c_[vertices, np.ones (len(vertices))]
    return (M @ vh.T).T[:, :2]

vertices = np.array ([[1,1],[4,1],[4,3],[1,3]], dtype=float)

V_t = aplicar (traslacion(3,2), vertices)
V_s = aplicar (escalacion(1.5, 0.5), vertices)
V_r = aplicar (rotacion(45), vertices)

print ('Traslado: \n', V_t)
print ('Escalado: \n', V_s)
print ('Rotado: \n', V_r)

#Ejercicio de Reforzamiento

print ('\n Ejercicio de Reforzamiento')

#Ejercicio 1
p1 = np.array([[5, -1]],dtype=float)
P_translacion = aplicar (traslacion(-2,4),p1)
print ("P =",p1[0])
print ("Resultado: ",P_translacion[0])

#Ejercicio 2
triangulo = np.array([[0,0],[2,0],[1,2]], dtype=float)
triangulo_escalado = aplicar(escalacion(2,3),triangulo)

print ("Triangulo Original:")
print (triangulo)

print ("Triangulo Escalado:")
print (triangulo_escalado)

#Ejercicio 3
p1_rotar = np.array ([[3,0]],dtype = float)
print ("\n Ejercicio 3")
for grados in [90, 180, 270]:
    resultado = aplicar (rotacion(grados),p1_rotar)
print (f"Rotacion {grados}º:",np.round(resultado[0],2))

#Dibujo de las 4 versiones

print("Figura Original")
figura = np.array ([
    [1,1],
    [4,1],
    [4,3],
    [1,3],
    [1,1]
], dtype = float)

print ("Translacion")
figura_transladada = aplicar (traslacion(3,2),figura)
print ("Escalacion")
figura_escalada = aplicar (escalacion(1.5,0.5),figura)
print ("Rotacion")
figura_rotada = aplicar (rotacion(45),figura)

#Grafica
plt.figure (figsize = (8,7))
plt.plot (
    figura[:, 0],
    figura[:, 1],
    marker = 'o',
    label = 'Original'
)

plt.plot (
    figura_transladada[:, 0],
    figura_transladada[:, 1],
    marker = 'o',
    label = 'Traslacion'
)
plt.plot (
    figura_rotada[:, 0],
    figura_rotada[:, 1],
    marker = 'o',
    label = 'Rotacion 45'
)

plt.axhline(0, color = 'black', linewidth = 0.8)
plt.axhline(0, color = 'black', linewidth = 0.8)

plt.grid (True)

plt.xlabel("X")
plt.ylabel("Y")

plt.title ("Transformaciones Geometricas")

plt.legend()

plt.axis('equal')

plt.show()
