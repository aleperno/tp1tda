import Grafo, Casillero, Jugador, random
from math import fabs, sqrt

class Mapa(object):
	def __init__(self, n, m, p):
		""" Constructor de un mapa rectangular de n x m """
		
		# Inicializamos los atributos del mapa
		self.mapa = Grafo.Grafo(1)
		self.filas = n
		self.columnas = m
		self.casillasOro = []
		
		# Llamamos a las funciones que generan el mapa
		self._generarCasillas()
		self._bloquearCasillas()
		self._generarCasillasOro(p)
		self._generarCaminos()

###############################
#    METODOS PRIVADOS PARA    #
#  LA INICIALIZACION DEL MAPA #
###############################

	def _generarCasillas(self):
		""" Genera los casilleros del mapa """
		
		for i in range(self.filas):
			for j in range(self.columnas):
				pos = (i, j)
				altura = random.randrange(-5, 5, 1)
				
				dato = Casillero.Casillero(pos, altura)
				
				# Agrego el vertice al grafo
				vertice = Grafo.Vertice(pos, dato)
				self.mapa.nuevoVertice(vertice)

	def _bloquearCasillas(self):
		""" Bloquea el 10 % de las casillas del mapa """
		
		for i in range(self.filas * self.columnas // 10):
			pos = (random.randrange(0, self.filas), random.randrange(0, self.columnas))
			vertice = self.mapa.obtenerVertice(pos)
			
			while vertice.dato.bloqueado:
				pos = (random.randrange(0, self.filas), random.randrange(0, self.columnas))
				vertice = self.mapa.obtenerVertice(pos)
			
			vertice.dato.bloqueado = True
	
	def _generarCasillasOro(self, p):
		""" Ubica aleatoriamente las monedas de oro en el mapa """
		
		cant = self.filas * self.columnas * p // 100
	
		for i in range(cant):
			pos = (random.randrange(0, self.filas), random.randrange(0, self.columnas))
			
			vertice = self.mapa.obtenerVertice(pos)
			while vertice.dato.bloqueado or vertice.dato.ocupado:
				pos = (random.randrange(0, self.filas), random.randrange(0, self.columnas))
				vertice = self.mapa.obtenerVertice(pos)
				
			vertice.dato.ocupado = True
			vertice.dato.contenido = "O"
			
			self.casillasOro.append(pos)

	def _generarCaminos(self):
		""" Metodo que genera las conexiones entre las casillas """
	
		for i in range(self.filas):
			for j in range(self.columnas):
				pos = (i, j)
				vi = self.mapa.obtenerVertice(pos)
				
				# Si es una casilla bloqueada pasamos a la siguiente
				if vi.dato.bloqueado:
					continue
				
				# Creamos las aristas a las casillas vecinas
				for k in range(-1, 2):
					for l in range(-1, 2):
						pos = (i + k, j + l)
						if pos != (i,  j) and self.mapa.existeVertice(pos):
							vf = self.mapa.obtenerVertice(pos)
							
							# Si no esta bloqueado creamos la arista
							if not vf.dato.bloqueado:
								peso = vi.dato.altura - vf.dato.altura
								
								# Si esta subiendo, se duplica el esfuerzo
								if peso < 0:
									peso *= 2
								
								self.mapa.crearArista(vi, vf, fabs(peso))

###############################
#  METODOS PUBLICOS DEL MAPA  #
###############################

	def existeCasilla(self, clave):
		""" Metodo que devuelve el objeto casillero correspondiente a la posicion pedida """
		
		return self.mapa.existeVertice(clave)

	def obtenerCasilla(self, clave):
		""" Metodo que devuelve el objeto casillero correspondiente a la posicion pedida """
		
		return self.mapa.obtenerVertice(clave).dato

	def ubicarJugadores(self, jugadores):
		""" Metodo que ubica los jugadores en el mapa """

		# Ubicamos al jugador en el mapa
		for jugador in jugadores:
			pos = (random.randrange(0, self.filas), random.randrange(0, self.columnas))
			vertice = self.mapa.obtenerVertice(pos)

			while vertice.dato.bloqueado or vertice.dato.ocupado:
				pos = (random.randrange(0, self.filas), random.randrange(0, self.columnas))
				vertice = self.mapa.obtenerVertice(pos)

			# Ocupamos la casilla
			jugador.posicion = pos
			vertice.dato.ocupado = True
			vertice.dato.contenido = jugador

	def obtenerTurnos(self, casilla_ant, casilla_act):
		""" Metodo que obtiene la cantidad de turnos que debe esperar el jugador en la 
			posicion actual """
		
		return self.mapa.obtenerPesoArista(casilla_ant.posicion, casilla_act.posicion)
	
	def dijkstra(self, clave, heuristica):
		return self.mapa.dijkstra(self.mapa.obtenerVertice(clave), heuristica)