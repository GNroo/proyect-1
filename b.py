import matplotlib
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import messagebox
import networkx as nx
import matplotlib.image as mpimg
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class Grafo:
    def __init__(self, rutaImagen, nodos, colores={}):
        self.grafo = nx.DiGraph()
        self.nodos = []
        self.posiciones = {}
        for nodo, lista in nodos.items():
            if lista[1] != None:
                posicion = lista[1]
            self.posiciones[nodo] = lista[1]
            self.nodos.append(nodo)

        self.colores = colores
        self.imagen = rutaImagen

        self.grafo.add_nodes_from(self.nodos)

    def agregarArista(self, u, v, peso, color=None):
        self.grafo.add_edge(u, v, weight=peso)
        if color is not None:
            self.colores[u] = color

    def bellmanFord(self, inicio):
        distancia = {nodo: float("inf") for nodo in self.grafo.nodes}
        distancia[inicio] = 0
        predecesores = {nodo: None for nodo in self.grafo.nodes}

        for _ in range(len(self.grafo.nodes) - 1):
            for u, v, data in self.grafo.edges(data=True):
                if distancia[u] != float("inf") and distancia[u] + data["weight"] < distancia[v]:
                    distancia[v] = distancia[u] + data["weight"]
                    predecesores[v] = u

        for u, v, data in self.grafo.edges(data=True):
            if distancia[u] != float("inf") and distancia[u] + data["weight"] < distancia[v]:
                print("Se detectó un ciclo negativo en el grafo")
                return None, None

        return distancia, predecesores

    def pesoArista(self, u, v):
        if self.grafo.has_edge(u, v):
            return self.grafo[u][v]['weight']
        else:
            return 0

    def mostrarGrafo(self, ax):
        imagen = mpimg.imread(self.imagen)
        ax.imshow(imagen, extent=[0, imagen.shape[1], 0, imagen.shape[0]])

        nx.draw(self.grafo, pos=self.posiciones, ax=ax, with_labels=True,
                node_color=[self.colores.get(nodo, "red") for nodo in self.grafo.nodes()],
                node_size=20, font_color="white", font_size=10, edge_color="white")

        ax.set_facecolor("#222222")
        ax.figure.set_facecolor("#222222")


class App:
    def __init__(self, master):
        self.master = master
        master.title("UPViajes")
        self.bg = "#0f3a5b"
        self.fg = "#dddddd"
        master.configure(bg=self.bg)
        self.master.bind("<Escape>", self.cerrarAplicacion)
        self.master.bind("Q", self.cerrarAplicacion)
        self.master.bind("q", self.cerrarAplicacion)

        self.puntoInicio = ""
        self.puntoDestino = ""
        self.nodos = {
                "CDMX": ("Ciudad de México", (577, 1694)),
                "NYC": ("Nueva York", (1010, 2176)),
                "OTT": ("Ottawa", (1187, 2286)),
                "MAD": ("Madrid", (2295, 2151)),
                "PR": ("París", (2430, 2320)),
                "PE": ("Pekín", (4308, 2176)),
                "TYO": ("Tokio", (4681, 2058)),
                }
        """
        self.nodos = ["CDMX", "NYC", "OTT", "MAD", "PR", "PE", "JP"]
        self.posiciones = {
            "CDMX": (577, 1694),
            "NYC": (1010, 2176),
            "OTT": (1187, 2286),
            "MAD": (2295, 2151),
            "PR": (2430, 2320),
            "PE": (4308, 2176),
            "JP": (4681, 2058),
        }
        """
        self.colores = {
            "CDMX": (1, 0, 0),
            "NYC": (0, 0, 0),
            "OTT": (0, 1, 0),
        }
        self.descuentos = {
                "CDMX": 0.3,
                "NYC": 0.1,
                "PE": 0.15,
                }

        self.g = Grafo("mapaMundial.png", nodos=self.nodos)
        self.g.agregarArista("CDMX", "NYC", 300)
        self.g.agregarArista("CDMX", "PR", 600)
        self.g.agregarArista("NYC", "TYO", 700)
        self.g.agregarArista("NYC", "PE", 650)
        self.g.agregarArista("PR", "TYO", 800)
        self.g.agregarArista("TYO", "PE", 200)
        self.g.agregarArista("PE", "CDMX", 500)

        self.titulo = tk.Label(master, text="AeroUPV", bg=self.bg, fg=self.fg, font=("Helvetica", 32,"bold"))
        self.vuelos = tk.LabelFrame(master, text="Vuelos Disponibles", bg="#e60408", fg=self.fg, bd=0, highlightthickness=0, font=("Helvetica", 18,"bold"))
        self.precios = tk.LabelFrame(master, text="Simulación de\nCambio en Precios", bg=self.bg, fg=self.fg, bd=0, highlightthickness=0, font=("Helvetica", 18,"bold"))
        self.canvas = tk.Canvas(master, width=800, height=600)
        self.listaVuelos = tk.Listbox(self.vuelos, bg=self.bg, fg=self.fg, font="Helvetica", bd=0, highlightthickness=0)
        self.listaPrecios = tk.Listbox(self.precios, bg=self.bg, fg=self.fg, font="Helvetica", bd=0, highlightthickness=0)
        self.btnCostos = tk.Button(master, text="Costos", command=self.calcularCostos)
        self.btnInicio = tk.Button(master, text="Punto de Partida", command=lambda: self.aeropuertos("Inicio"))
        self.btnDestino = tk.Button(master, text="Punto de Destino", command=lambda: self.aeropuertos("Destino"))

        self.listaVuelos.insert(1, "Ciudad de México -> Nueva York")
        self.listaVuelos.insert(2, "Ciudad de México -> París")
        self.listaVuelos.insert(3, "Nueva York -> Tokio")
        self.listaVuelos.insert(4, "Nueva York -> Pekín")
        self.listaVuelos.insert(5, "París -> Tokio")
        self.listaVuelos.insert(6, "Tokio -> Pekín")
        self.listaVuelos.insert(7, "Pekín -> Ciudad de México")

        self.listaPrecios.insert(1, "30% Ciudad de México")
        self.listaPrecios.insert(2, "10% Nueva York")
        self.listaPrecios.insert(3, "15% Pekín")

        self.titulo.grid(row=0, column=1, columnspan=3, sticky="nsew")
        self.vuelos.grid(row=1, column=0, sticky="nsew")
        self.precios.grid(row=1, column=4, sticky="nsew")
        self.canvas.grid(row=1, column=1, columnspan=3, sticky="nsew")
        self.btnCostos.grid(row=2, column=1, sticky="nsew")
        self.btnInicio.grid(row=2, column=2, sticky="nsew")
        self.btnDestino.grid(row=2, column=3, sticky="nsew")

        self.listaVuelos.bind('<<ListboxSelect>>', self.vueloSugerido)

        self.listaVuelos.grid(row=0, column=0, sticky="nsew")
        self.listaPrecios.grid(row=0, column=0, sticky="nsew")

        self.vuelos.grid_rowconfigure(0, weight=1)
        self.vuelos.grid_columnconfigure(0, weight=1)

        self.precios.grid_rowconfigure(0, weight=1)
        self.precios.grid_columnconfigure(0, weight=1)

        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_rowconfigure(1, weight=1)
        self.master.grid_rowconfigure(2, weight=1)
        self.master.grid_columnconfigure(0, weight=1)
        self.master.grid_columnconfigure(1, weight=1)
        self.master.grid_columnconfigure(2, weight=1)
        self.master.grid_columnconfigure(3, weight=1)
        self.master.grid_columnconfigure(4, weight=1)

        fig, ax = plt.subplots(figsize=(8, 6))
        self.g.mostrarGrafo(ax)
        self.canvas.figure = fig
        self.canvas_widget = FigureCanvasTkAgg(fig, master=self.canvas)
        self.canvas_widget.draw()
        self.canvas_widget.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    def cerrarAplicacion(self, event):
        self.master.quit()

    def aeropuertos(self, tipo):
        menu = tk.Toplevel(self.master)
        menu.title("Menú")
        menu.configure(bg=self.bg)

        lista = tk.Listbox(menu, bg=self.bg, fg=self.fg, font="Helvetica")
        opciones = self.nodos
        for opcion in opciones:
            lista.insert(tk.END, opcion)
        lista.pack(padx=10, pady=10)

        def guardar():
            seleccion = lista.curselection()
            if seleccion:
                opcion = lista.get(seleccion)
                if tipo == "Inicio":
                    self.puntoInicio = opcion
                    messagebox.showinfo("Selección guardada", f"Punto de Partida: {opcion}")
                elif tipo == "Destino":
                    self.puntoDestino = opcion
                    messagebox.showinfo("Selección guardada", f"Punto de Destino: {opcion}")
            else:
                messagebox.showwarning("Advertencia", "Por favor, selecciona una opción")

        btnGuardar = tk.Button(menu, text="Guardar Selección", command=guardar)
        btnGuardar.pack(pady=5)

        btnSalir = tk.Button(menu, text="Salir", command=menu.destroy)
        btnSalir.pack(pady=5)

    def vueloSugerido(self, event):
        seleccion = self.listaVuelos.curselection()
        if seleccion:
            valor = self.listaVuelos.get(seleccion)
            origen, destino = valor.split(" -> ")
            for nodo, lista in self.nodos.items():
                if lista[0] == origen:
                    self.puntoInicio = nodo
                elif lista[0] == destino:
                    self.puntoDestino = nodo
            self.calcularCostos

    def calcularCostos(self):
        if not self.puntoInicio or not self.puntoDestino:
            messagebox.showwarning("Advertencia", "Por favor, selecciona un punto de partida y un destino")
            return

        distancia, predecesores = self.g.bellmanFord(self.puntoInicio)

        if distancia is None:
            return

        if distancia[self.puntoDestino] == float("inf"):
            messagebox.showinfo("Resultado", f"No hay ruta disponible desde {self.nodos[self.puntoInicio][0]} a {self.nodos[self.puntoDestino][0]}")
            return

        ruta = []
        nodo_actual = self.puntoDestino
        while nodo_actual is not None:
            ruta.append(nodo_actual)
            nodo_actual = predecesores[nodo_actual]
        ruta.reverse()

        total = distancia[self.puntoDestino]
        for nodo, descuento in self.descuentos.items():
            resta = 0
            for i in range(len(ruta) - 1):
                if nodo == ruta[i]:
                    nodo2 = ruta[i+1]
                    resta = self.g.pesoArista(nodo, nodo2) * descuento
            total -= resta
        listaRuta = " -> ".join(ruta)
        nombresRuta = []
        for ciudad in ruta:
            nombresRuta.append(self.nodos[ciudad][0])
        nombresRuta = " -> ".join(nombresRuta)
        info = f"""
        Origen: {self.nodos[self.puntoInicio][0]} ({self.puntoInicio})
        Destino: {self.nodos[self.puntoDestino][0]} ({self.puntoDestino})\n        
        Ruta: {listaRuta}
{nombresRuta}\n\n
        Costo Total: {total:.2f}
        """
        messagebox.showinfo("Ruta más barata", info)


if __name__ == "__main__":
    matplotlib.use("TkAgg")
    ventana = tk.Tk()
    app = App(ventana)
    ventana.mainloop()
