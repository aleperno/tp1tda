import Juego, sys, pygame

def _ingresar(msj, msjError, valMin, valMax):
	""" Funcion que pide un dato al usuario y lo valida """
	
	valor = valMin -1
	while valor < valMin or valor > valMax:
		valor = int(input(msj))
		
		if valor < valMin or valor > valMax:
			print (msjError)

	return valor

def dibujarMapa(n, m, juego, screen, agua, tierra, oro):
	""" Funcion que muestra el estado actual del mapa en la pantalla """
	
	for i in range(0, n):
		for j in range(0, m):
			casilla = juego.mapa.obtenerCasilla((i, j))
			pos = (i * 40, j * 40)
			
			if casilla.ocupado:
				if casilla.contenido == "O":
					screen.blit(cofre, pos)
				else:
					screen.blit(tierra, pos)
					if casilla.contenido.vivo:
						screen.blit(casilla.contenido.imagen, pos)
			else:
				if casilla.bloqueado:
					screen.blit(agua, pos)
				else:
					screen.blit(tierra, pos)

# Ingreso de los parametros del juego
n = _ingresar("Ingrese cuantas columnas desea que tenga el mapa (4-20): ", "Ha ingresado una cantidad invalida. Intente nuevamente.", 4, 20)
m = _ingresar("Ingrese cuantas filas desea que tenga el mapa (4-20): ", "Ha ingresado una cantidad invalida. Intente nuevamente.", 4, 20)
k = _ingresar("Ingrese cuantos jugadores desea (4-8): ", "Ha ingresado una cantidad invalida. Intente nuevamente.", 4, 8)
p = _ingresar("Ingrese el porcentaje de celdas con monedas (10-40): ", "Ha ingresado una cantidad invalida. Intente nuevamente.", 10, 40)

# Creacion del juego
juego = Juego.Juego(n, m, k, p)

# Creacion de la ventana
size = width, height = n * 40, m * 40
screen = pygame.display.set_mode(size)

# Carga de las imagenes del area de juego
agua = pygame.image.load("images/agua.png")
pasto = pygame.image.load("images/pasto.png")
cofre = pygame.image.load("images/cofre.png")

# Carga de las imagenes de los personajes
i = 1
for jugador in juego.jugadores:
	jugador.imagen = pygame.image.load("images/" + str(i) + ".png")
	i += 1

# Dibujo del mapa en la pantalla
dibujarMapa(n, m, juego, screen, agua, pasto, cofre)
pygame.display.update()

# Loop del juego
running = True
while running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT: running = False
	
	if juego.jugar():
		break

	dibujarMapa(n, m, juego, screen, agua, pasto, cofre)
	pygame.display.update()
	pygame.time.delay(10) 

pygame.quit()

# Imprimimos la tabla de puntajes y el ganador
oro = -1
ganador = None
for jugador in juego.jugadores:
	print (str(jugador.nombre) + " " + str(jugador.oro)),
	
	if jugador.estrategia == 1:
		print (" estrategia RANDOM")
	elif jugador.estrategia == 2:
		print (" estrategia FIJA")
	elif jugador.estrategia == 3:
		print (" estrategia A*")
	else:
		print (" estrategia A* alejandose de los enemigos")
	
	if jugador.oro > oro:
		ganador = jugador
		oro = jugador.oro

print ("Ganador:" + str(ganador.nombre))
