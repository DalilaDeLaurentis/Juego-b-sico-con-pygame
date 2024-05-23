import pygame
import random

# Inicializar pygame
pygame.init()

# Constantes
ANCHO_PANTALLA = 800
ALTO_PANTALLA = 600
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)

# Inicialización de la pantalla
pantalla = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
pygame.display.set_caption("ASTRONAUTA VS ALIENS")

# Reloj para controlar la velocidad de fotogramas
reloj = pygame.time.Clock()

# Cargar imágenes
fondo = pygame.image.load('assets/background.gif')
fondo = pygame.transform.scale(fondo, (ANCHO_PANTALLA, ALTO_PANTALLA))
imagen_jugador = pygame.image.load('assets/player.gif')
imagen_jugador = pygame.transform.scale(imagen_jugador, (50, 40))  # Ajustar tamaño del jugador
imagen_enemigo = pygame.image.load('assets/enemy.gif')
imagen_enemigo = pygame.transform.scale(imagen_enemigo, (50, 50))  # Ajustar tamaño del enemigo

# Fuente para el texto
fuente = pygame.font.Font(None, 36)

# Clase Jugador
class Jugador:
    def __init__(self, x, y):
        self.imagen = imagen_jugador
        self.rect = self.imagen.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.velocidad = 5

    def mover_izquierda(self):
        self.rect.x -= self.velocidad

    def mover_derecha(self):
        self.rect.x += self.velocidad

    def dibujar(self, pantalla):
        pantalla.blit(self.imagen, self.rect)

# Clase Enemigo
class Enemigo:
    def __init__(self, x, y):
        self.imagen = imagen_enemigo
        self.rect = self.imagen.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.velocidad = 2

    def mover(self):
        self.rect.y += self.velocidad
        if self.rect.y > ALTO_PANTALLA:
            self.rect.y = 0
            self.rect.x = random.randint(0, ANCHO_PANTALLA - self.rect.width)

    def dibujar(self, pantalla):
        pantalla.blit(self.imagen, self.rect)

# Función para detectar colisiones
def detectar_colisiones(jugador, enemigos):
    for enemigo in enemigos:
        if jugador.rect.colliderect(enemigo.rect):
            return True
    return False

# Función principal del juego
def juego():
    jugador = Jugador(ANCHO_PANTALLA // 2, ALTO_PANTALLA - 50)
    enemigos = [Enemigo(random.randint(0, ANCHO_PANTALLA - 50), random.randint(-300, 0)) for _ in range(5)]

    mostrar_mensaje_colision = False
    corriendo = True
    while corriendo:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                corriendo = False

        # Mover el jugador
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_LEFT]:
            jugador.mover_izquierda()
        if teclas[pygame.K_RIGHT]:
            jugador.mover_derecha()

        # Actualizar posiciones de los enemigos
        for enemigo in enemigos:
            enemigo.mover()

        # Detectar colisiones
        if detectar_colisiones(jugador, enemigos):
            mostrar_mensaje_colision = True

        # Dibujar todo
        pantalla.blit(fondo, (0, 0))
        jugador.dibujar(pantalla)
        for enemigo in enemigos:
            enemigo.dibujar(pantalla)

        if mostrar_mensaje_colision:
            mensaje_colision = fuente.render("¡Colisión detectada!", True, BLANCO)
            pantalla.blit(mensaje_colision, (ANCHO_PANTALLA // 2 - mensaje_colision.get_width() // 2, ALTO_PANTALLA // 2))
            pygame.display.flip()
            pygame.time.delay(2000)  # Mostrar el mensaje de colisión durante 2 segundos
            corriendo = False

        pygame.display.flip()
        reloj.tick(60)

# Función para mostrar el menú principal
def menu_principal(pantalla):
    texto_instruccion = fuente.render("Pulsa Enter para jugar", True, BLANCO)
    texto_rect = texto_instruccion.get_rect(center=(ANCHO_PANTALLA // 2, ALTO_PANTALLA // 2))

    esperando = True
    while esperando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                quit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN:
                    esperando = False

        pantalla.fill(NEGRO)
        pantalla.blit(texto_instruccion, texto_rect)
        pygame.display.flip()

    return True

# Mostrar menú principal
if menu_principal(pantalla):
    juego()

pygame.quit()

