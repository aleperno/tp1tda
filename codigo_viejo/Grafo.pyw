import heapq

class Vertice(object):
	""" Clase que moldea un vertice de un grafo y diversas operaciones sobre ellos. """

	def __init__(self, clave, dato = None):
		""" Constructor de la clase Vertice. """

		# Clave con la que se identificara al vertice dentro del grafo
		self.clave = clave

		# Dato contenido en el vertice
		self.dato = dato
	
		#Para los recorridos y caminos minimos
		self.color = "BLANCO"
		self.padre = None
		
	def __eq__(self, vertice):
		""" Funcion de igualdad """
		
		return self.clave == vertice.clave

	def __lt__(self, vertice):
                """ Funcion de comparacion """

                if self.clave < vertice.clave:
                        return -1
                elif self.clave == vertice.clave:
                        return 0
                else:
                        return 1

class Grafo(object):
	""" Clase Grafo que posee las operaciones basicas de los grafos. """

###############################
#         CONSTRUCTOR         #
###############################

	def __init__(self, dirigido = 0):
		""" Constructor de la clase Grafo."""
	
		# Cantidad de vertices en el grafo.
		self._vcant = 0
		
		# Listas de adyacencia
		self._dicc_adyacencia = {}
		
		# Diccionario de vertices
		self._dicc_vertices = {}
		
		# Para setear si el grafo es dirigido o no
		self.dirigido = dirigido

###############################
#     OPERACIONES BASICAS     #
###############################

	def nuevoVertice(self, vert):
		""" Agrega un vertice al grafo"""
		
		# Aumenta la cantidad de vertices
		self._vcant += 1
		
		# Crea la lista de adyacencia para el vertice
		self._dicc_adyacencia[vert.clave] = []
 
		# Agrega el vertice al diccionario
		self._dicc_vertices[vert.clave] = vert
 
	def borrarVertice(self, v):
		""" Elimina un vertice del grafo."""
	
		# Disminuye el contador de vertices
		self._vcant -= 1
	
		# Elimina la lista de adyacencia
		self._dicc_adyacencia.pop(v.clave)

		# Elimina el vertice del diccionario
		self._dicc_vertices.pop(v.clave)
		
		# Elimina las aristas incidentes en v
		for lista in self._dicc_adyacencia.values():
			for vert, valor in lista:
				if vert == v:
					lista.remove((vert, valor))
 
	def crearArista(self, vi, vf, valor = None):
		""" Aniade un arco o arista (vi,vf) al grafo. Recibe el vertice
		de partida, el vertice destino y la valoracion de la arista en
		caso de estarse utilizandolo como grafo ponderado. En caso
		contrario no se le debe pasar este ultimo parametro."""
 
		self._dicc_adyacencia[vi.clave].append((vf, valor))
		
		if not self.dirigido:
			self._dicc_adyacencia[vf.clave].append((vi, valor))

	def borrarArista(self, vi, vf):
		""" Elimina un arco o arista (vi, vf) del grafo. Recibe el ver-
		tice de partida y el vertice destino. """
		
		l = self._dicc_adyacencia[vi.clave]
		
		for i in range(len(l)):
			v_act, valor = l[i]
			if v_act == vf:
				del l[i]
				break

	def existeVertice(self, clave):
		""" Devuelve TRUE si el grafo contiene un vertice con la clave indicada. """
		return clave in self._dicc_vertices

	def obtenerVertice(self, clave):
		""" Devuelve el vertice correspondiente a la clave. La existencia del mismo
			debe ser verificada por el usuario. """
		return self._dicc_vertices[clave]
		
	def adyacencia(self, v):
		""" Devuelve la lista de adyacencia correspondiente al vertice.
			La existencia del mismo debe ser verificada por el usuario. """
		return self._dicc_adyacencia[v.clave]
		
	def obtenerPesoArista(self, clave1, clave2):
		""" Devuelve el peso de la arista entre dos vertices. """
		
		lista = self._dicc_adyacencia[clave1]
		
		for v, peso in lista:
			if v.clave == clave2:
				return peso
		
###############################
#         RECORRIDOS          #
###############################

	def dfs(self, funcion):
		""" Recorrido en profundidad del grafo """
		
		# Seteo inicial de los vertices
		for vert in self._dicc_vertices.values():
			vert.color = "BLANCO"
			vert.padre = None
			
		for vert in self._dicc_vertices.values():
			if vert.color == "BLANCO":
				self._dfs_visita(vert, funcion)
				
				
	def _dfs_visita(self, vert, funcion):
		""" Funcion auxiliar para el recorrido DFS """
		
		vert.color = "GRIS"
		
		for vecino, peso in self._dicc_adyacencia[vert.clave]:
			if vecino.color == "BLANCO":
				vecino.padre = vert
				self._dfs_visita(vecino,funcion)

		funcion(vert)
		vert.color = "NEGRO"

###############################
#       CAMINOS MINIMOS       #
###############################

	def dijkstra(self, origen, heuristica = None):
		""" Caminos minimos por el algoritmo de Dijkstra.
			Si se pasa una funcion heuristica se transforma en A*"""

		distancias = {}
		caminos = {}
		heap = []
		
		heapq.heappush(heap, (0, origen, []))
		
		while heap:
			(dist, vert, camino) = heapq.heappop(heap)
			
			if vert.clave in distancias:
				continue
			
			distancias[vert.clave] = dist
			caminos[vert.clave] = camino

			for vecino, peso in self._dicc_adyacencia[vert.clave]:
				vd_dist = distancias[vert.clave] + peso
				
				if heuristica:
					vd_dist += heuristica(vert, vecino)
				
				camino = caminos[vert.clave] + [vecino.clave]
				heapq.heappush(heap,(vd_dist, vecino, camino))
		
		return (distancias, caminos)

	
