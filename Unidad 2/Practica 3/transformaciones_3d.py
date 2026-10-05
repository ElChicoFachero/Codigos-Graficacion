import numpy as np

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

vertice = np.array([2,3,0,1], dtype=float)
T = obtener_matriz_traslacion_3d(5,-2, 1)
S = obtener_matriz_escalacion_3d(2, 2, 1)
M_compuesta = T @ S
vertice_transformado = M_compuesta @ vertice

print ('Vertice original: ', vertice[:3])
print ('Vertice transformado: ', vertice_transformado[:3])

#Reto Numero 1
p = np.array([1,2,3,1], dtype=float)

print ('Reto 1: Rotacion')
print ('Original: ', p[:3])
print ('Rotacion X:', np.round(rotacion_x(90) @ p, 2)[:3])
print ('Rotacion Y:', np.round(rotacion_y(90) @ p, 2)[:3])
print ('Rotacion Z:', np.round(rotacion_z(90) @ p, 2)[:3])

#Reto Numero 2
T = obtener_matriz_traslacion_3d(5, -2, 1)
R = rotacion_z(90)
S = obtener_matriz_escalacion_3d(2, 2, 1)

M = T @ R @ S
vertice = np.array([2, 3, 0, 1], dtype=float)
resultado = M @ vertice

print ('Reto 2: Transformacion compuesta')
print ('Original: ', vertice[:3])
print ('Transformado: ', np.round(resultado, 2)[:3])

#Reto Numero 3
P = np.array([1,2,3,1], dtype=float)
R = rotacion_z(45)
P_rotado = R @ P

distancia_original = np.sqrt(P[0]**2 + P[1]**2)
distancia_rotada = np.sqrt(P_rotado[0]**2 + P_rotado[1]**2)

print ('Reto 3: Distancia al Eje 2')
print ('Distancia Original: ', np.round(distancia_original, 4))
print ('Distancia Rotada: ', np.round(distancia_rotada, 4))
print ('¿Se conserva la distancia?', np.isclose(distancia_original, distancia_rotada))