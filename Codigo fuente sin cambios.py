# pgzero
import random

TITLE = "Flying Bird"
WIDTH = 600  # (Ancho x)
HEIGHT = 499  # (Alto y)
FPS = 60

"""
ÍNDICE:
    DIMENSIONES DEL JUEGO
    CREACIÓN DE ACTORES
    MOVIMIENTO
    MECÁNICA
    267 x 474
"""

# === Actores ===
pajaro = Actor("pajaro", (225, 280), size=(30, 30))
pajaro2 = Actor("pajaro2", (225, 280), size=(30, 30))
pajaro3 = Actor("pajaro3", (225, 280), size=(30, 30))
# Posiciones distintas para la colección
pajaro.pos = (150, 250)
pajaro2.pos = (300, 250)
pajaro3.pos = (450, 250)

fondo = Actor("fondoancho", center=(WIDTH // 2, HEIGHT // 2))
# fondo = Actor("fondoancho",size=(500,474))
piso1 = Actor("piso", (200, HEIGHT - 50), size=(1000, 100))
piso2 = Actor("piso", (piso1.width, HEIGHT - 50), size=(1000, 100))
tuboA = Actor("tubo_verde_arriba", (700, -50), size=(70, 400))
tuboB = Actor("tubo_verde_abajo", (700, tuboA.y + 550), size=(70, 400))
boton_menu = Actor("boton_menu", center=(300, 420), size=(200, 70))
boton_ok = Actor("boton_ok", center=(300, 420), size=(200, 70))
boton_getready = Actor("boton_getready", center=(300, 100))
boton_tap = Actor("boton_tap", center=(300, 200), size=(235, 78))
boton_gameover = Actor("boton_gameover", center=(300, 200), size=(320, 60))
logo_monedas = Actor("logo_monedas", topleft=(10, 10), size=(30, 30))
numero_actual = Actor("0", topleft=(38, 15), size=(20, 20))
personaje_actual = "pajaro"
# === Variables de física y funcionamiento ===
velocidad = 0
gravedad = 0.5
salto = -8
count = 0
pasado = False
mode = "menu"


# === Movimiento de tuberías ===
def movimientoTuberias():
    global pasado
    tuboA.x -= 4
    tuboB.x -= 4
    if tuboA.x <= -70:
        tuboA.x = 700
        tuboA.y = random.randint(-120, 40)
        tuboB.x = 700
        tuboB.y = tuboA.y + 550
        pasado = False


# === Movimiento de pavimento ===
def movimientoPiso():
    piso1.x -= 2
    piso2.x -= 2

    if piso1.right < 200:
        piso1.x = piso2.right
    if piso2.right < 200:
        piso2.x = piso1.right


# === Conteo de Monedas ===
def conteoMonedas():
    global pasado, count, numero_actual
    if tuboA.x < pajaro.x and not pasado:
        count += 1
        pasado = True
    elif count == 0:
        numero_actual.image = "0"
    elif count == 1:
        numero_actual.image = "1"
    elif count == 2:
        numero_actual.image = "2"
    elif count == 3:
        numero_actual.image = "3"
    elif count == 4:
        numero_actual.image = "4"
    elif count == 5:
        numero_actual.image = "5"
    elif count == 6:
        numero_actual.image = "6"
    elif count == 7:
        numero_actual.image = "7"
    elif count == 8:
        numero_actual.image = "8"
    elif count == 9:
        numero_actual.image = "9"


# === Colisiones y salida de pantalla===
def colisiones():
    global mode
    if pajaro.colliderect(tuboA) or pajaro.colliderect(tuboB) or pajaro.colliderect(piso1) or pajaro.colliderect(piso2):
        mode = "game_over"
    if pajaro.y < 0:  # Para que no se salga de la pantalla
        pajaro.y = 0


# === Dibujo general ===
def draw():
    # screen.fill("black")
    fondo.draw()
    if mode == "menu":
        pajaro.draw()
        piso1.draw()
        piso2.draw()
        boton_getready.draw()
        boton_menu.draw()
        boton_tap.draw()
    elif mode == "game":
        piso1.draw()
        piso2.draw()
        tuboA.draw()
        tuboB.draw()
        logo_monedas.draw()
        numero_actual.draw()
        pajaro.draw()
    elif mode == "game_over":
        pajaro.draw()
        piso1.draw()
        piso2.draw()
        tuboA.draw()
        tuboB.draw()
        boton_gameover.draw()
        boton_menu.draw()
        logo_monedas.draw()
        numero_actual.draw()
    elif mode == "coleccion":
        boton_ok.draw()
        logo_monedas.draw()
        numero_actual.draw()
        pajaro.draw()
        pajaro2.draw()
        pajaro3.draw()


def update(dt):
    global velocidad, count, pasado, mode, numero_actual
    if mode == "game":
        velocidad += gravedad
        pajaro.y += velocidad
        movimientoTuberias()
        movimientoPiso()
        conteoMonedas()
        colisiones()

    if pajaro.y > HEIGHT:
        pajaro.y = HEIGHT
        velocidad = 0
    if pajaro.y < 0:
        pajaro.y = 0
        velocidad = 0


def on_mouse_down(button, pos):
    if mode == "game":
        pajaro.y = 250
        velocidad = 0
        tuboA.x = 700
        tuboA.y = random.randint(-120, 80)
        tuboB.x = 700
        tuboB.y = tuboA.y + 400
        count = 0
        numero_actual.image = "0"
        pasado = False
        pajaro.image = personaje_actual


def on_mouse_down(button, pos):
    global velocidad, mode, count, pasado, numero_actual, personaje_actual
    if mode == "menu":
        if boton_tap.collidepoint(pos):
            mode = "game"
        if boton_menu.collidepoint(pos):
            mode = "coleccion"
    elif mode == "game":
        velocidad = salto
        pajaro.image = personaje_actual + "_ojos_cerrados"
        clock.schedule_unique(volver_sprite_normal, 0.2)
    elif mode == "game_over":
        if boton_menu.collidepoint(pos):
            mode = "coleccion"
            pajaro.y = 250
            velocidad = 0
            tuboA.x = 700
            tuboA.y = random.randint(-120, 80)
            tuboB.x = 700
            tuboB.y = tuboA.y + 550
            count = 0
            numero_actual.image = "0"
            pasado = False
            pajaro.image = personaje_actual
    elif mode == "coleccion":
        if boton_ok.collidepoint(pos):
            mode = "menu"
        elif pajaro.collidepoint(pos):
            personaje_actual = "pajaro"
        elif pajaro2.collidepoint(pos):
            personaje_actual = "pajaro2"
        elif pajaro3.collidepoint(pos):
            personaje_actual = "pajaro3"
        pajaro.image = personaje_actual


def volver_sprite_normal():
    pajaro.image = personaje_actual