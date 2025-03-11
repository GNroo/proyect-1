import matplotlib
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import messagebox
import networkx as nx
import matplotlib.image as mpimg
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class Grafo:
    	def __init__(self, rutaImagen, nodos, colores={}):
    	"""
    	Inicializa el grafo con una imagen de fondo, nodos y colores opcionales.
    	:param rutaImagen: Ruta de la imagen que se usará como fondo del mapa.
    	:param nodos: Diccionario de nodos donde la clave es el identificador de la ciudad
                    	y el valor es una tupla con el nombre y la posición (x, y).
    	:param colores: Diccionario opcional que asigna colores a los nodos.
    	"""
    	self.grafo = nx.DiGraph()  # Crea un grafo dirigido
    	self.nodos = []
    	self.posiciones = {}
    	for nodo, lista in nodos.items():
            	if lista[1] is not None:
            	posicion = lista[1]
            	self.posiciones[nodo] = lista[1]
            	self.nodos.append(nodo)
    	self.colores = colores
    	self.imagen = rutaImagen
    	self.grafo.add_nodes_from(self.nodos)  # Agrega los nodos al grafo

    	def agregarArista(self, u, v, peso, color=None):
    	"""
    	Agrega una arista al grafo entre dos nodos con un peso y un color opcional.
    	:param u: Nodo de origen.
    	:param v: Nodo de destino.
    	:param peso: Peso de la arista.
    	:param color: Color opcional de la arista.
    	"""
    	self.grafo.add_edge(u, v, weight=peso)  # Agrega la arista con su peso
    	if color is not None:
            	self.colores[u] = color  # Asigna color si se proporciona

    	def bellmanFord(self, inicio):
    	"""
    	Implementa el algoritmo de Bellman-Ford para encontrar la ruta más corta
    	desde un nodo de inicio a todos los demás nodos.
    	:param inicio: Nodo de inicio para el cálculo de distancias.
    	:return: Tupla con un diccionario de distancias y un diccionario de predecesores.
    	"""
    	distancia = {nodo: float("inf") for nodo in self.grafo.nodes}
    	distancia[inicio] = 0
    	predecesores = {nodo: None for nodo in self.grafo.nodes}

    	# Relajación de aristas
    	for _ in range(len(self.grafo.nodes) - 1):
            	for u, v, data in self.grafo.edges(data=True):
            	if distancia[u] != float("inf") and distancia[u] + data["weight"] < distancia[v]:
                    	distancia[v] = distancia[u] + data["weight"]
                    	predecesores[v] = u

    	# Comprobación de ciclos negativos
    	for u, v, data in self.grafo.edges(data=True):
            	if distancia[u] != float("inf") and distancia[u] + data["weight"] < distancia[v]:
            	print("Se detectó un ciclo negativo en el grafo")
            	return None, None
    	return distancia, predecesores

    	def pesoArista(self, u, v):
    	"""
    	Devuelve el peso de la arista entre dos nodos.
    	:param u: Nodo de origen.
    	:param v: Nodo de destino.
    	:return: Peso de la arista o 0 si no existe.
    	"""
    	if self.grafo.has_edge(u, v):
            	return self.grafo[u][v]['weight']
    	else:
            	return 0

    	def mostrarGrafo(self, ax):
    	"""
    	Muestra el grafo en un eje de matplotlib.
    	:param ax: Eje de matplotlib donde se dibujará el grafo.
    	"""
    	imagen = mpimg.imread(self.imagen)  # Carga la imagen de fondo
    	ax.imshow(imagen, extent=[0, imagen.shape[1], 0, imagen.shape[0]])

    	# Dibuja el grafo sobre la imagen
    	nx.draw(self.grafo, pos=self.posiciones, ax=ax, with_labels=True,
            	node_color=[self.colores.get(nodo, "red") for nodo in self.grafo.nodes()],
            	node_size=20, font_color="white", font_size=10, edge_color="white")
    	ax.set_facecolor("#222222")  # Establece el color de fondo del eje
    	ax.figure.set_facecolor("#222222”) # Color del fondo de la figura


class App:
    	def __init__(self, master):
    	"""
    	Inicializa la aplicación principal de la interfaz gráfica.
    	:param master: Ventana principal de la aplicación.
    	"""
    	self.master = master
    	master.title("UPViajes")  # Título de la ventana
    	self.bg = "#0f3a5b"  # Color de fondo
    	self.fg = "#dddddd"  # Color de texto
    	master.configure(bg=self.bg)  # Configura el color de fondo de la ventana
    	self.master.bind("<Escape>", self.cerrarAplicacion)  # Asigna la tecla Escape para cerrar la aplicación
    	self.master.bind("Q", self.cerrarAplicacion)  # Asigna la tecla Q para cerrar la aplicación
    	self.master.bind("q", self.cerrarAplicacion)  # Asigna la tecla q para cerrar la aplicación

    	self.puntoInicio = ""  # Almacena el punto de inicio seleccionado
    	self.puntoDestino = ""  # Almacena el punto de destino seleccionado
    	self.nodos = {
            	"CDMX": ("Ciudad de México", (577, 1694)),
            	"NYC": ("Nueva York", (1010, 2176)),
            	"OTT": ("Ottawa", (1187, 2286)),
            	"MAD": ("Madrid", (2295, 2151)),
            	"PR": ("París", (2430, 2320)),
            	"PE": ("Pekín", (4308, 2176)),
            	"TYO": ("Tokio", (4681, 2058)),
    	}

    	self.colores = {
            	"CDMX": (1, 0, 0),  # Color para Ciudad de México
            	"NYC": (0, 0, 0),   # Color para Nueva York
            	"OTT": (0, 1, 0),   # Color para Ottawa
    	}

    	self.descuentos = {
            	"CDMX": 0.3,  # Descuento para Ciudad de México
            	"NYC": 0.1,   # Descuento para Nueva York
            	"PE": 0.15,   # Descuento para Pekín
    	}

    	# Inicializa el grafo con la imagen de fondo y los nodos
    	self.g = Grafo("mapaMundial.png", nodos=self.nodos)
    	# Agrega las aristas con sus respectivos pesos
    	self.g.agregarArista("CDMX", "NYC", 300)
    	self.g.agregarArista("CDMX", "PR", 600)
    	self.g.agregarArista("NYC", "TYO", 700)
    	self.g.agregarArista("NYC", "PE", 650)
    	self.g.agregarArista("PR", "TYO", 800)
    	self.g.agregarArista("TYO", "PE", 200)
    	self.g.agregarArista("PE", "CDMX", 500)

    	# Configuración de la interfaz gráfica
    	self.titulo = tk.Label(master, text="AeroUPV", bg=self.bg, fg=self.fg, font=("Helvetica", 32, "bold"))
    	self.vuelos = tk.LabelFrame(master, text="Vuelos Disponibles", bg="#e60408", fg=self.fg, bd=0, highlightthickness=0, font=("Helvetica", 18, "bold"))
    	self.precios = tk.LabelFrame(master, text="Simulación de\nCambio en Precios", bg=self.bg, fg=self.fg, bd=0, highlightthickness=0, font=("Helvetica", 18, "bold"))
    	self.canvas = tk.Canvas(master, width=800, height=600)
    	self.listaVuelos = tk.Listbox(self.vuelos, bg=self.bg, fg=self.fg, font="Helvetica", bd=0, highlightthickness=0)
    	self.listaPrecios = tk.Listbox(self.precios, bg=self.bg, fg=self.fg, font="Helvetica", bd=0, highlightthickness=0)
    	self.btnCostos = tk.Button(master, text="Costos", command=self.calcularCostos)
    	self.btnInicio = tk.Button(master, text="Punto de Partida", command=lambda: self.aeropuertos("Inicio"))
    	self.btnDestino = tk.Button(master, text="Punto de Destino", command=lambda: self.aeropuertos("Destino"))

    	# Agrega opciones de vuelos disponibles a la lista
    	self.listaVuelos.insert(1, "Ciudad de México -> Nueva York")
    	self.listaVuelos.insert(2, "Ciudad de México -> París")
    	self.listaVuelos.insert(3, "Nueva York -> Tokio")
    	self.listaVuelos.insert(4, "Nueva York -> Pekín")
    	self.listaVuelos.insert(5, "París -> Tokio")
    	self.listaVuelos.insert(6, "Tokio -> Pekín")
    	self.listaVuelos.insert(7, "Pekín -> Ciudad de México")

    	# Agrega opciones de precios disponibles a la lista
    	self.listaPrecios.insert(1, "30% Ciudad de México")
    	self.listaPrecios.insert(2, "10% Nueva York")
    	self.listaPrecios.insert(3, "15% Pekín")

    	# Organiza los elementos en la cuadrícula
    	self.titulo.grid(row=0, column=1, columnspan=3, sticky="nsew")
    	self.vuelos.grid(row=1, column=0, sticky="nsew")
    	self.precios.grid(row=1, column=4, sticky="nsew")
    	self.canvas.grid(row=1, column=1, columnspan=3, sticky="nsew")
    	self.btnCostos.grid(row=2, column=1, sticky="nsew")
    	self.btnInicio.grid(row=2, column=2, sticky="nsew")
    	self.btnDestino.grid(row=2, column=3, sticky="nsew")

    	# Vincula la selección de vuelos a una función
    	self.listaVuelos.bind('<<ListboxSelect>>', self.vueloSugerido)

    	# Configura las listas de vuelos y precios
    	self.listaVuelos.grid(row=0, column=0, sticky="nsew")
    	self.listaPrecios.grid(row=0, column=0, sticky="nsew")

    	# Configura el comportamiento de la cuadrícula
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

    	# Crea y muestra el grafo en la interfaz
    	fig, ax = plt.subplots(figsize=(8, 6))
    	self.g.mostrarGrafo(ax)
    	self.canvas.figure = fig
    	self.canvas_widget = FigureCanvasTkAgg(fig, master=self.canvas)
    	self.canvas_widget.draw()
    	self.canvas_widget.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    	def cerrarAplicacion(self, event):
    	"""
    	Cierra la aplicación cuando se presiona la tecla Escape o Q.
    	:param event: Evento de la tecla presionada.
    	"""
    	self.master.quit()

    	def aeropuertos(self, tipo):
    	"""
    	Muestra un menú para seleccionar un aeropuerto (punto de partida o destino).
    	:param tipo: Indica si se está seleccionando el punto de partida o el destino.
    	"""
    	menu = tk.Toplevel(self.master)
    	menu.title("Menú")
    	menu.configure(bg=self.bg)
    	lista = tk.Listbox(menu, bg=self.bg, fg=self.fg, font="Helvetica")
    	opciones = self.nodos
    	for opcion in opciones:
            	lista.insert(tk.END, opcion)  # Agrega cada nodo a la lista
    	lista.pack(padx=10, pady=10)

    	def guardar():
            	"""
            	Guarda la selección del aeropuerto y muestra un mensaje de confirmación.
            	"""
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
    	"""
    	Maneja la selección de un vuelo sugerido y actualiza los puntos de inicio y destino.
    	:param event: Evento de selección en la lista de vuelos.
    	"""
    	seleccion = self.listaVuelos.curselection()
    	if seleccion:
            	valor = self.listaVuelos.get(seleccion)
            	origen, destino = valor.split(" -> ")
            	for nodo, lista in self.nodos.items():
            	if lista[0] == origen:
                    	self.puntoInicio = nodo
            	elif lista[0] == destino:
                    	self.puntoDestino = nodo
            	self.calcularCostos()  # Llama a calcularCostos para obtener el costo del vuelo

    	def calcularCostos(self):
    	"""
    	Calcula los costos del vuelo desde el punto de inicio al destino utilizando el algoritmo de Bellman-Ford.
    	Muestra la ruta más barata y el costo total en un cuadro de mensaje.
    	"""
    	if not self.puntoInicio or not self.puntoDestino:
            	messagebox.showwarning("Advertencia", "Por favor, selecciona un punto de partida y un destino")
            	return

    	distancia, predecesores = self.g.bellmanFord(self.puntoInicio)

    	if distancia is None:
            	return  # Si hay un ciclo negativo, no se puede continuar

    	if distancia[self.puntoDestino] == float("inf"):
            	messagebox.showinfo("Resultado", f"No hay ruta disponible desde {self.nodos[self.puntoInicio][0]} a {self.nodos[self.puntoDestino][0]}")
            	return

    	# Reconstruye la ruta más corta
    	ruta = []
    	nodo_actual = self.puntoDestino
    	while nodo_actual is not None:
            	ruta.append(nodo_actual)
            	nodo_actual = predecesores[nodo_actual]
    	ruta.reverse()  # Invierte la ruta para mostrarla desde el inicio al destino

    	total = distancia[self.puntoDestino]  # Costo total inicial
    	for nodo, descuento in self.descuentos.items():
            	resta = 0
            	for i in range(len(ruta) - 1):
            	if nodo == ruta[i]:
                    	nodo2 = ruta[i + 1]
                    	resta = self.g.pesoArista(nodo, nodo2) * descuento  # Aplica el descuento
            	total -= resta  # Resta el descuento al costo total

    	# Formatea la información de la ruta para mostrarla
    	listaRuta = " -> ".join(ruta)
    	nombresRuta = [self.nodos[ciudad][0] for ciudad in ruta]  # Obtiene los nombres de las ciudades
    	nombresRuta = " -> ".join(nombresRuta)
    	info = f"""
    	Origen: {self.nodos[self.puntoInicio][0]} ({self.puntoInicio})
    	Destino: {self.nodos[self.puntoDestino][0]} ({self.puntoDestino})\n
    	Ruta: {listaRuta}
    	{nombresRuta}\n\n
    	Costo Total: {total:.2f}
    	"""
    	messagebox.showinfo("Ruta más barata", info)  # Muestra la información en un cuadro de mensaje


if __name__ == "__main__":
    	matplotlib.use("TkAgg")  # Usa el backend TkAgg para matplotlib
    	ventana = tk.Tk()  # Crea la ventana principal
    	app = App(ventana)  # Inicializa la aplicación
    	ventana.mainloop()  # Inicia el bucle principal de la interfaz gráfica

