import csv
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, ttk

import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure


# Aristas del cubo 3D
ARISTAS_CUBO = [
    (0, 1), (1, 2), (2, 3), (3, 0),
    (4, 5), (5, 6), (6, 7), (7, 4),
    (0, 4), (1, 5), (2, 6), (3, 7),
]

# Datos iniciales
EJEMPLOS = {
    2: {
        "vertices": "1,1\n4,1\n4,3\n1,3",
        "operaciones": "S 1.5 0.5\nRP 30 centro\nT 3 2",
    },
    3: {
        "vertices": (
            "-1,-1,-1\n"
            "1,-1,-1\n"
            "1,1,-1\n"
            "-1,1,-1\n"
            "-1,-1,1\n"
            "1,-1,1\n"
            "1,1,1\n"
            "-1,1,1"
        ),
        "operaciones": "S 1.5 0.8 2\nRZ 35\nT 3 1 2",
    },
}

# Leer vertices
def leer_vertices(texto, dimension):
    puntos = []
    for numero, linea in enumerate(texto.splitlines(), 1):
        linea = linea.split("#", 1)[0].strip()
        if not linea:
            continue
        partes = linea.replace(",", " ").split()
        puntos.append(puntos)
    if len(puntos) < 2:
        raise ValueError("Ingresa al menos dos vertices.")
    return np.asarray(puntos, dtype=float)

# Leer operaciones
def leer_operaciones(texto):
    operaciones = []
    for numero, linea in enumerate(texto.splitlines(), 1):
        linea = linea.split("#", 1)[0].strip()
        if linea:
            partes = linea.replace(",", " ").upper().split()
            operaciones.append((numero, partes))
    if not operaciones:
        raise ValueError("Escribe por lo menos una operacion.")
    return operaciones

# Matriz de traslacion
def trasladar(*valores):
    matriz = np.eye(len(valores) + 1)
    matriz[:-1, -1] = valores
    return matriz

# Matriz de escalamiento
def escalar(*valores):
    return np.diag([*valores, 1.0]).astype(float)

# Rotacion 2D
def rotar_2d(angulo):
    t = np.deg2rad(angulo)
    c, s = np.cos(t), np.sin(t)

    return np.array([
        [c, -s, 0],
        [s,  c, 0],
        [0,  0, 1]
    ], dtype=float)

# Rotacion 3D
def rotar_3d(eje, angulo):
    t = np.deg2rad(angulo)
    c, s = np.cos(t), np.sin(t)

    matriz = np.eye(4)

    if eje == "RX":
        matriz[:3, :3] = [
            [1, 0, 0],
            [0, c, -s],
            [0, s, c]
        ]

    elif eje == "RY":
        matriz[:3, :3] = [
            [c, 0, s],
            [0, 1, 0],
            [-s, 0, c]
        ]

    else:
        matriz[:3, :3] = [
            [c, -s, 0],
            [s, c, 0],
            [0, 0, 1]
        ]

    return matriz

# Aplicar matriz a los vertices
def aplicar(matriz, vertices):
    homogeneos = np.c_[
        vertices,
        np.ones(len(vertices))
    ]

    return (matriz @ homogeneos.T).r[:, :vertices.shape[1]]

# Componer transformaciones
def componer(vertices, operaciones):
    dimension = vertices.shape[1]
    matriz = np.eye(dimension + 1)
    historial = []

    for numero, partes in operaciones:
        nombre, *argumentos = partes

        try:
            if nombre == "T" and len(argumentos) == dimension:
                operacion = trasladar(
                    *(float(x) for x in argumentos)
                )
            elif nombre == "S" and len(argumentos) == dimension:
                operacion = escalar(
                    *(float(x) for x in argumentos)
                )
            elif (
                dimension == 2
                and nombre == "RP"
                and len(argumentos) in (2, 3)
            ):
                angulo = float(argumentos[0])
                if (
                    len(argumentos) == 2
                    and argumentos[1] == "CENTRO"
                ):
                    pivote = aplicar(
                        matriz, vertices
                    ).mean(axis=0)
                elif len(argumentos) == 3:
                    pivote = np.asarray(
                        [float(x) for x in argumentos[1:]],
                        dtype=float
                    )
                else:
                    raise ValueError(
                        "Usa RP 30 centro o RP 30 x y."
                    )
                operacion = (
                    trasladar(*pivote)
                    @ rotar_2d(angulo)
                    @ trasladar(*(-pivote))
                )
            elif (
                dimension == 2
                and nombre == "R"
                and len(argumentos) == 1
            ):
                operacion = rotar_2d(
                    float(argumentos[0])
                )

            elif (
                dimension == 3
                and nombre in ("RX", "RY", "RZ")
                and len(argumentos) == 1
            ):
                operacion = rotar_3d(
                    nombre, float(argumentos[0])
                )
            else:
                raise ValueError(
                    "Operacion o cantidad de argumentos incorrecta."
                )
            if not np.isfinite(operacion).all():
                raise ValueError(
                    "Solo se admiten numeros finitos."
                )
        except (ValueError, OverflowError) as exc:
            raise ValueError(
                f"Error en la operacion de la linea {numero} "
                f"({' '.join(partes)}): {exc}"
            ) from exc

        # Aplicar las operaciones en el orden escrito
        matriz = operacion @ matriz
        historial.append((nombre, operacion.copy()))

    resultado = aplicar(matriz, vertices)

    if not np.isfinite(resultado).all():
        raise ValueError("El resultado contiene numeros no finitos.")
    return matriz, resultado, historial

# Mostrar resultados numericos
def descripcion(resultado, dimension, operaciones, invertido=None):
    matriz, vertices, historial = resultado

    lineas = [ "Matriz compuesta final (M):",
        np.array2string(matriz, precision=3, suppress_small=True),
        "","Coordenadas transformadas:"]

    for indice, punto in enumerate(vertices, 1):
        lineas.append(
            f"V{indice:02d}: "
            + ", ".join(f"{x:.3f}" for x in punto)
        )

    lineas += ["","Orden aplicado: " + " -> ".join(" ".join(p) for _, p in operaciones)]

    if invertido is not None:
        matriz_b, vertices_b, _ = invertido
        diferencia = np.linalg.norm(vertices - vertices_b)

        lineas += ["", "Matriz con orden inverso:",
            np.array2string(matriz_b, precision=3, suppress_small=True),
            "", f"Diferencia entre resultados: {diferencia:.6f}",
            "Invertir el orden puede cambiar la figura."]

    return "\n".join(lineas)

# Dibujar figura 2D
def dibujar_2d(ax, original, transformado, inverso=None):

    def poligono(puntos, titulo, color, estilo="-"):
        puntos = np.asarray(puntos, dtype=float)

        # Cerrar el poligono
        cerrado = (np.vstack([puntos, puntos[0]])
            if len(puntos) >= 3
            else puntos
        )

        ax.plot(cerrado[:, 0], cerrado[:, 1],marker="o", linestyle=estilo,
            color=color, linewidth=2.5, markersize=7,label=titulo)

        # Numerar los vertices
        for i, (x, y) in enumerate(puntos, 1):
            ax.annotate(str(i), (x, y), xytext=(5, 5), textcoords="offset points", fontsize=10, color="#111827")

    # Gris: figura original
    poligono(original, "Original", "#64748b")
    # Azul: figura transformada
    poligono(transformado, "Transformado", "#1688b8")

    # Rojo: operaciones en orden inverso
    if inverso is not None:
        poligono(inverso,"Orden inverso", "#dc2626","--")

    ax.set_title("Transformaciones geométricas 2D",fontsize=15)
    ax.set_xlabel("X", fontsize=12)
    ax.set_ylabel("Y", fontsize=12)

    ax.axhline(0, color="gray", linewidth=0.7)
    ax.axvline(0, color="gray", linewidth=0.7)

    ax.grid(alpha=0.25)
    ax.set_aspect("equal", adjustable="datalim")
    ax.legend(loc="best")
    ax.margins(x=0.08, y=0.10)


# Dibujar cubo 3D
def dibujar_3d(ax, original, transformado, inverso=None):
    figuras = [
        (original, "Original", "#64748b", "-"),
        (transformado, "Transformado", "#1688b8", "-")
    ]

    if inverso is not None:
        figuras.append(
            (inverso, "Orden inverso", "#dc2626", "--")
        )

    for puntos, titulo, color, estilo in figuras:
        ax.scatter(*puntos.T, color=color, s=28)

        if len(puntos) == 8:
            aristas = ARISTAS_CUBO
        else:
            aristas = [(i, i + 1)
                for i in range(len(puntos) - 1)
            ]

        for i, j in aristas:
            ax.plot(*zip(puntos[i], puntos[j]),color=color,linestyle=estilo,linewidth=1.7)

        ax.plot([], [], [], color=color, linestyle=estilo, label=titulo)

    todos = np.vstack([figura[0] for figura in figuras])
    mn, mx = todos.min(axis=0), todos.max(axis=0)

    lado = max(float(np.max(mx - mn)), 1.0) * 0.6
    centro = (mn + mx) / 2

    ax.set(
        xlim=(centro[0] - lado, centro[0] + lado),
        ylim=(centro[1] - lado, centro[1] + lado),
        zlim=(centro[2] - lado, centro[2] + lado),
        xlabel="X",
        ylabel="Y",
        zlabel="Z",
        title="Transformaciones geométricas 3D"
    )

    ax.set_box_aspect((1, 1, 1))
    ax.legend(loc="upper left")

# Ventana principal
class VentanaMotor(tk.Tk):

    def __init__(self):
        super().__init__()

        self.title(
            "Graficación SCC-1010 | Proyecto integrador: "
            "Mini motor 2D y 3D"
        )
        self.geometry("1220x810")
        self.minsize(900, 640)

        self.vistas = {}
        self.ultima_salida = {}

        contenedor = ttk.Notebook(self)
        contenedor.pack(expand=True,fill="both",padx=10, pady=10)

        for dimension, titulo in (
            (2, "Motor 2D"),
            (3, "Motor 3D (reto)")
        ):
            panel = ttk.Frame(contenedor)
            contenedor.add(panel, text=titulo)
            self.crear_pestana(panel, dimension)

        # Mostrar los ejemplos al iniciar
        for dimension in (2, 3):
            self.ejecutar(dimension)

    # Crear las entradas y botones
    def crear_pestana(self, panel, dimension):
        panel.columnconfigure(1, weight=1)
        panel.rowconfigure(0, weight=1)

        izquierdo = ttk.Frame(panel, padding=8)
        izquierdo.grid(row=0, column=0, sticky="nsew")

        derecho = ttk.Frame(panel, padding=8)
        derecho.grid(row=0, column=1, sticky="nsew")

        derecho.columnconfigure(0, weight=1)
        derecho.rowconfigure(0, weight=3)
        derecho.rowconfigure(1, weight=0)
        derecho.rowconfigure(2, weight=2)

        ttk.Label(
            izquierdo,
            text=f"Vertices {dimension}D (uno por linea)",
            font=("Arial", 11, "bold")
        ).pack(anchor="w")

        entradas_vertices = scrolledtext.ScrolledText(izquierdo, width=32, height=10)
        entradas_vertices.pack(fill="x", pady=(5, 12))
        entradas_vertices.insert("1.0", EJEMPLOS[dimension]["vertices"])

        ttk.Label(izquierdo,text="Secuencia de operaciones (de arriba hacia abajo)",font=("Arial", 10, "bold")).pack(anchor="w")

        entrada_ops = scrolledtext.ScrolledText(izquierdo, width=32, height=8)
        entrada_ops.pack(fill="x", pady=(5, 6))
        entrada_ops.insert("1.0", EJEMPLOS[dimension]["operaciones"])

        if dimension == 2:
            ayuda = (
                "T 3 2 | S 1.5 0.5 | R 45\n"
                "RP 30 centro | RP 30 2.5 2"
            )
        else:
            ayuda = (
                "T 3 1 2 | S 1.5 0.8 2\n"
                "RX 45 | RY 30 | RZ 90\n"
                "Para mostrar un cubo usa sus 8 vertices en orden"
            )

        ttk.Label(izquierdo, text=ayuda, justify="left", foreground="#334155").pack(anchor="w")

        botones = ttk.Frame(izquierdo)
        botones.pack(fill="x", pady=14)

        ttk.Button(botones, text="Aplicar", command=lambda d=dimension: self.ejecutar(d)).pack(fill="x", pady=3)

        ttk.Button(botones, text="Comparar orden inverso", command=lambda d=dimension: self.ejecutar(d, comparar=True)).pack(fill="x", pady=3)

        ttk.Button(botones, text="Exportar coordenadas CSV", command=lambda d=dimension: self.exportar(d)).pack(fill="x", pady=3)

        figura = Figure(figsize=(7, 5), dpi=100, constrained_layout=True)

        eje = figura.add_subplot(111, projection="3d" if dimension == 3 else None)

        lienzo = FigureCanvasTkAgg(figura, master=derecho)
        lienzo.get_tk_widget().grid(row=0, column=0, sticky="nsew")

        barra = NavigationToolbar2Tk(lienzo, derecho, pack_toolbar=False)
        barra.grid(row=1, column=0, sticky="w")

        salida = scrolledtext.ScrolledText(derecho, height=12, font=("Consolas", 9), state="disabled")
        salida.grid(row=2, column=0, sticky="nsew", pady=(9, 0))

        self.vistas[dimension] = (entradas_vertices, entrada_ops, eje, lienzo, salida)

    # Ejecutar transformaciones
    def ejecutar(self, dimension, comparar=False):
        (entrada_vertices, entrada_ops, eje, lienzo, salida) = self.vistas[dimension]

        try:
            vertices = leer_vertices(entrada_vertices.get("1.0", "end"),dimension)

            operaciones = leer_operaciones(entrada_ops.get("1.0", "end"))

            resultado = componer(vertices, operaciones)

            inverso = (componer(vertices,list(reversed(operaciones)))
                if comparar
                else None
            )

            eje.clear()

            if dimension == 2:
                dibujar_2d(eje, vertices, resultado[1],inverso[1] if inverso else None)
            else:
                dibujar_3d(eje,vertices, resultado[1], inverso[1] if inverso else None)

            lienzo.draw_idle()

            salida.configure(state="normal")
            salida.delete("1.0", "end")
            salida.insert("1.0",descripcion(resultado,dimension, operaciones, inverso))
            salida.configure(state="disabled")

            self.ultima_salida[dimension] = (vertices, resultado[1])

        except (ValueError, IndexError, TypeError, OverflowError) as exc:
            messagebox.showerror("Revisa los datos", str(exc))

    # Exportar resultados a CSV
    def exportar(self, dimension):
        if dimension not in self.ultima_salida:
            messagebox.showwarning("Sin resultados", "Primero aplica una transformacion valida.")
            return

        ruta = filedialog.asksaveasfilename(
            title="Guardar coordenadas transformadas",
            defaultextension=".csv",
            filetypes=[("CSV", "*.csv")],
            initialfile=f"Coordenadas_{dimension}d.csv"
        )

        if not ruta:
            return

        original, nuevo = self.ultima_salida[dimension]
        ejes = list("xyz"[:dimension])

        try:
            with open(ruta,"w", newline="", encoding="utf-8-sig") as archivo:
                escritor = csv.writer(archivo)
                escritor.writerow(
                    ["vertice"]
                    + [f"original_{e}" for e in ejes]
                    + [f"transformado_{e}" for e in ejes]
                )

                for i, (a, b) in enumerate(
                    zip(original, nuevo), 1
                ):
                    escritor.writerow([i, *a, *b])

            messagebox.showinfo("CSV exportado", f"Coordenadas guardadas en:\n{ruta}")

        except OSError as exc:
            messagebox.showerror("No se pudo guardar", str(exc))

# Iniciar programa
if __name__ == "__main__":
    app = VentanaMotor()
    app.mainloop()
