class Casillero(object):
	def __init__(self, posicion, altura = 0, bloqueado = False):
		""" Constructor de la clase casillero """

		self.posicion = posicion
		self.altura = altura
		self.bloqueado = bloqueado
		self.ocupado = False
		self.contenido = None
