import Mapa, Jugador, random
from math import sqrt
from sys import maxsize

class Juego(object):
	def __init__(self, n, m, k, p):
		""" Creacion de un juego nuevo """
		
		self.turno = 0

		# Creacion del mapa de juego
		self.mapa = Mapa.Mapa(n, m, p)

		# Creacion y ubicacion de los jugadores
		self.cantJugadores = k
		self.jugadores = []
		
		for i in range(k):
			self.jugadores.append(Jugador.Jugador(i + 1, (i % 4) + 1))

		self.mapa.ubicarJugadores(self.jugadores)

	def jugar(self):
		""" Metodo que realiza el movimiento del jugador al que le toca jugar """
		
		# Si se termina el oro, termina el juego
		if len(self.mapa.casillasOro) == 0:
			return True
			
		jugador = self.jugadores[self.turno]
		
		if jugador.vivo:
			# Si todavia no cumplio los turnos que le lleva llegar a la casilla, tiene que esperar
			if jugador.espera > 0:
				jugador.espera -= 1
			else:
				# Sacamos al jugador de su casilla
				casilla_ant = self.mapa.obtenerCasilla(jugador.posicion)
				casilla_ant.ocupado = False
				casilla_ant.contenido = None
				
				# Lo movemos
				self._mover(jugador)

				casilla_act = self.mapa.obtenerCasilla(jugador.posicion)
				
				# Seteamos el tiempo de espera
				jugador.espera = self.mapa.obtenerTurnos(casilla_ant, casilla_act)
				
				if casilla_act.ocupado:
					if type(casilla_act.contenido) == Jugador.Jugador:
						# Si hay un jugador se pelean a muerte
						self._pelear(jugador, casilla_act.contenido)
						
						# Si sobrevive, ocupa la casilla
						if jugador.vivo:
							casilla_act.contenido = jugador
					else: 
						# Si hay oro lo agarra, ocupa la casilla y la eliminamos de la lista de casillas con oro
						casilla_act.contenido = jugador
						jugador.oro += 1
						self.mapa.casillasOro.remove(jugador.posicion)
				else:
					casilla_act.ocupado = True
					casilla_act.contenido = jugador

		# Le toca al proximo jugador
		self.turno = (self.turno + 1) % self.cantJugadores
		return False

	def _mover(self, jugador):
		""" Metodo que mueve al jugador segun la estrategia que tiene """
		
		if jugador.estrategia == 1:
			self._moverRandom(jugador)
		elif jugador.estrategia == 2:
			self._moverFijo(jugador)
		elif jugador.estrategia == 3:
			# A* AL ORO
			self._moverAEstrella(jugador)
		else:
			# A* AL ORO ALEJANDOSE DE LOS ENEMIGOS
			self._moverAEstrellaEnemigos(jugador)

	def _pelear(self, jug1, jug2):
		""" Metodo que define aleatoriamente cual de los dos jugadores gana la pelea """
		
		if random.randrange(0, 1):
			jug1.vivo = False
		else: 
			jug2.vivo = False

	def _moverRandom(self, jugador):
		""" Metodo que mueve el jugador a una posicion vecina aleatoriamente """
		
		fila, col = jugador.posicion
		
		posibles_casillas = []
		
		for i in range(-1, 2):
			for j in range(-1, 2):
				if i == 0 and j == 0:
					continue
				
				pos = (fila + i, col + j)
				
				# Agrega a la lista las posiciones a las que se puede mover
				if self.mapa.existeCasilla(pos):
					if not self.mapa.obtenerCasilla(pos).bloqueado:
						posibles_casillas.append(pos)
		
		jugador.posicion = random.choice(posibles_casillas)

	def _moverFijo(self, jugador):
		""" Mueve siempre en la misma direccion hasta que llega a un borde """
		
		x, y = jugador.posicion
		dirx, diry = jugador.direccion
		
		# Cambia la direccion horizontal
		if not self.mapa.existeCasilla((x + dirx, y)):
			dirx *= -1

		# Cambia la direccion vertical
		if not self.mapa.existeCasilla((x, y + diry)):
			diry *= -1

		# Movimiento horizontal
		x += dirx

		# Verifica si es una casilla valida
		if not self.mapa.existeCasilla((x, y)) or self.mapa.obtenerCasilla((x, y)).bloqueado:
			x, y = jugador.posicion
			
			# Movimiento vertical
			y += diry
		
		if not self.mapa.existeCasilla((x, y)) or self.mapa.obtenerCasilla((x, y)).bloqueado:
			x, y = jugador.posicion

			if self.mapa.existeCasilla((x + dirx, y + diry)) and not self.mapa.obtenerCasilla((x + dirx, y + diry)).bloqueado:
				# Movimiento diagonal
				x += dirx
				y += diry
		
		jugador.posicion = (x, y)
		jugador.direccion = (dirx, diry)

	def heuristica(self, v1, v2):
		""" Metodo heuristico que devuelve la distancia geometrica entre 2 puntos """

		return sqrt((v2.clave[0] - v1.clave[0]) ** 2 + (v2.clave[1] - v1.clave[1]) ** 2)

	def _moverAEstrella(self, jugador):
		""" Metodo que, utilizando la funcion heuristica, determina el camino minimo al proximo oro """
		
		distancias, caminos = self.mapa.dijkstra(jugador.posicion, self.heuristica)
		
		dist_oro = maxsize
		oro = None
		for casilla in self.mapa.casillasOro:
			if distancias[casilla] < dist_oro:
				dist_oro = distancias[casilla]
				oro = casilla

		jugador.posicion = caminos[oro][0]

	def _moverAEstrellaEnemigos(self, jugador):
		""" Metodo que, utilizando la funcion heuristica, determina el camino minimo al proximo oro 
			alejandose de los enemigos al mismo tiempo """
		
		distancias, caminos = self.mapa.dijkstra(jugador.posicion, self.heuristica)

		distancias_enemigos = []
		
		# Buscamos el camino al oro que mas se aleje de los enemigos
		for casilla in self.mapa.casillasOro:
			pos = caminos[casilla][0]
			dist2, cam2 = self.mapa.dijkstra(pos, self.heuristica)
			
			# Calculamos para cada camino la distancia al enemigo mas cercano
			dist_enemigo_cercano = maxsize
			for enemigo in self.jugadores:
				if enemigo.nombre == jugador.nombre or not enemigo.vivo:
					continue
				
				if dist2[enemigo.posicion] < dist_enemigo_cercano:
					dist_enemigo_cercano = dist2[enemigo.posicion]

			distancias_enemigos.append(dist_enemigo_cercano)
		
		# Buscamos el que tiene el enemigo mas cercano mas lejos
		indice = 0
		for i in range(1, len(distancias_enemigos)):
			if distancias_enemigos[i] > distancias_enemigos[indice]:
				indice = i
		
		jugador.posicion = caminos[self.mapa.casillasOro[indice]][0]
