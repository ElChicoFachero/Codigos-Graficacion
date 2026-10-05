import numpy as np

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

vertices = np.array([[1,1],[4,1],[4,3],[1,3]], dtype=float)
centro = vertices.mean(axis = 0) #Donde se parte la figura
cx, cy = centro

M_pivote = (
    traslacion(cx,cy)
    @ rotacion (30)
    @ traslacion (-cx, -cy)
)

rotados_centro = aplicar (M_pivote, vertices) #Puntos a iniciar y trabajar

P = np.array([[2,1]], dtype=float)
M_A = traslacion(5,0) @ rotacion(90)
M_B = rotacion(90) @ traslacion(5,0)

print ('Centro: ', centro)
print ('Rotacion sobre Centro:\n', rotados_centro)
print ('Caso A: ', aplicar(M_A, P)[0])
print ('Caso B: ', aplicar(M_B, P)[0])