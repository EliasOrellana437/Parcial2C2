import pygame
import sys
import random

# Inicializar sonido antes de pygame.init()
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()

# Configuración de la ventana
Ancho, Alto = 600, 400
Celda = 20
Ventana = pygame.display.set_mode((Ancho, Alto))
pygame.display.set_caption("Snake Mejorado con Sonido")

# Colores
Negro = (0, 0, 0)
Verde = (0, 255, 0)
Blanco = (255, 255, 255)

# Reloj y FPS
Clock = pygame.time.Clock()
FPS = 10

# Fuente
Fuente = pygame.font.SysFont("arial", 25)
FuenteTitulo = pygame.font.SysFont("arial", 45, bold=True)

# Cargar imagen graciosa
try:
    ImagenBroma = pygame.image.load("image.png")
    ImagenBroma = pygame.transform.scale(ImagenBroma, (200, 200))
except:
    ImagenBroma = None

# Cargar imagen de manzana
try:
    ImagenManzana = pygame.image.load("manzana2.png")
    ImagenManzana = pygame.transform.scale(ImagenManzana, (Celda, Celda))
except:
    ImagenManzana = None

# Cargar sonidos
try:
    SonidoComer = pygame.mixer.Sound("eatsound.wav")
    SonidoComer.set_volume(1.0)
except pygame.error:
    SonidoComer = None
    print("No se pudo cargar Comer.wav")

try:
    SonidoGameOver = pygame.mixer.Sound("deadsound.wav")
    SonidoGameOver.set_volume(1.0)
except pygame.error:
    SonidoGameOver = None
    print("No se pudo cargar GameOver.wav")

# Cargar música de fondo 
try:
    pygame.mixer.music.load("Musicafondo.mp3")  # Hay que asegurarse que el nombre coincida
    pygame.mixer.music.set_volume(0.2)  # Volumen bajo (20%)
except pygame.error as e:
    print("No se pudo cargar Musicafondo.mp3:", e)

# Función para mostrar puntaje
def MostrarPuntaje(Puntaje):
    Texto = Fuente.render(f"Puntaje: {Puntaje}", True, Blanco)
    Ventana.blit(Texto, (10, 10))

# Generar comida
def GenerarComida():
    return (random.randrange(0, Ancho // Celda) * Celda,
            random.randrange(0, Alto // Celda) * Celda)

# Crear nueva partida
def NuevaPartida():
    Serpiente = [(100, 100), (80, 100), (60, 100)]
    Direccion = "DERECHA"
    Comida = GenerarComida()
    Puntaje = 0
    return Serpiente, Direccion, Comida, Puntaje

# Dibujar serpiente
def DibujarSerpiente(Serpiente):
    for Parte in Serpiente:
        pygame.draw.rect(Ventana, Verde, (Parte[0], Parte[1], Celda, Celda))

# Mover serpiente
def MoverSerpiente(Serpiente, Direccion):
    X, Y = Serpiente[0]
    if Direccion == "ARRIBA": Y -= Celda
    elif Direccion == "ABAJO": Y += Celda
    elif Direccion == "IZQUIERDA": X -= Celda
    elif Direccion == "DERECHA": X += Celda
    Serpiente.insert(0, (X, Y))

# Pantalla Game Over
def PantallaGameOver(Puntaje):
    # Detener música de fondo al morir
    pygame.mixer.music.stop()

    if SonidoGameOver:
        SonidoGameOver.play()

    while True:
        Ventana.fill(Negro)
        Texto1 = FuenteTitulo.render("¡GAME OVER!", True, (255, 0, 0))
        Texto2 = Fuente.render(f"Puntaje final: {Puntaje}", True, Blanco)
        Texto3 = Fuente.render("Presiona ENTER para volver a jugar", True, Blanco)
        Texto4 = Fuente.render("Presiona ESC para salir", True, Blanco)

        Ventana.blit(Texto1, (Ancho/2 - Texto1.get_width()/2, 100))
        Ventana.blit(Texto2, (Ancho/2 - Texto2.get_width()/2, 170))
        Ventana.blit(Texto3, (Ancho/2 - Texto3.get_width()/2, 230))
        Ventana.blit(Texto4, (Ancho/2 - Texto4.get_width()/2, 260))
        pygame.display.flip()

        for Evento in pygame.event.get():
            if Evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif Evento.type == pygame.KEYDOWN:
                if Evento.key == pygame.K_RETURN:
                    return True
                elif Evento.key == pygame.K_ESCAPE:
                    return PantallaConfirmarSalida()

# Pantalla Confirmar salida
def PantallaConfirmarSalida():
    while True:
        Ventana.fill(Negro)
        Texto = FuenteTitulo.render("¿Estás seguro?", True, (255, 0, 0))
        Ventana.blit(Texto, (Ancho/2 - Texto.get_width()/2, 80))

        if ImagenBroma:
            Ventana.blit(ImagenBroma, (Ancho/2 - 100, 150))
        else:
            Texto2 = Fuente.render("(Falta la imagen image.png)", True, Blanco)
            Ventana.blit(Texto2, (Ancho/2 - Texto2.get_width()/2, 200))

        Texto3 = Fuente.render("Presiona S para salir o N para cancelar", True, Blanco)
        Ventana.blit(Texto3, (Ancho/2 - Texto3.get_width()/2, 370))
        pygame.display.flip()

        for Evento in pygame.event.get():
            if Evento.type == pygame.KEYDOWN:
                if Evento.key == pygame.K_s:
                    pygame.quit()
                    sys.exit()
                elif Evento.key == pygame.K_n:
                    return False

# Bucle principal
while True:
    Serpiente, Direccion, Comida, Puntaje = NuevaPartida()

    #Iniciar música de fondo al comenzar la partida
    try:
        pygame.mixer.music.play(-1)  # -1 = reproducir en bucle infinito
    except:
        pass

    while True:
        for Evento in pygame.event.get():
            if Evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif Evento.type == pygame.KEYDOWN:
                if Evento.key == pygame.K_UP and Direccion != "ABAJO":
                    Direccion = "ARRIBA"
                elif Evento.key == pygame.K_DOWN and Direccion != "ARRIBA":
                    Direccion = "ABAJO"
                elif Evento.key == pygame.K_LEFT and Direccion != "DERECHA":
                    Direccion = "IZQUIERDA"
                elif Evento.key == pygame.K_RIGHT and Direccion != "IZQUIERDA":
                    Direccion = "DERECHA"

        MoverSerpiente(Serpiente, Direccion)

        # Comer comida
        if Serpiente[0] == Comida:
            Puntaje += 1
            Comida = GenerarComida()
            if SonidoComer:
                SonidoComer.play()
        else:
            Serpiente.pop()

        # Colisiones
        X, Y = Serpiente[0]
        if (X < 0 or X >= Ancho or Y < 0 or Y >= Alto or Serpiente[0] in Serpiente[1:]):
            Volver = PantallaGameOver(Puntaje)
            if not Volver:
                pygame.quit()
                sys.exit()
            break

        # Dibujar todo
        Ventana.fill(Negro)
        DibujarSerpiente(Serpiente)
        if ImagenManzana:
            Ventana.blit(ImagenManzana, Comida)
        else:
            pygame.draw.rect(Ventana, (255, 0, 0), (Comida[0], Comida[1], Celda, Celda))
        MostrarPuntaje(Puntaje)
        pygame.display.flip()

        Clock.tick(FPS)
