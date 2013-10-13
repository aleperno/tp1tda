class Jugador(object):
	def __init__(self, nombre, estrategia):
		""" Constructor de la clase Jugador """
		
		self.nombre = nombre
		self.estrategia = estrategia
		self.vivo = True
		self.oro = 0
		self.posicion = (None, None)
		self.espera = 0
		self.direccion = (1, 1) # IZQ, ARR = -1, DER, ABA = 1
		self.imagen = None