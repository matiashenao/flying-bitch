#pgzero
import pgzrun
import random
import asyncio  # NECESARIO PARA LA WEB

TITLE = "Flying Bird"
WIDTH = 600
HEIGHT = 499
FPS = 60

# === Actores ===
# Asegúrate de que los archivos en la carpeta /images se llamen exactamente así en minúsculas
pajaro = Actor("pajaro", (150, 250))
pajaro2 = Actor("pajaro2", (300, 250))
pajaro3 = Actor("pajaro3", (450, 250))

fondo = Actor("fondoancho", center=(WIDTH // 2, HEIGHT // 2))
piso1 = Actor("piso", (200, HEIGHT - 50))
piso2 = Actor("piso", (600, HEIGHT - 50)) # Ajustado para que sigan uno al otro

tuboA = Actor("tubo_verde_arriba", (700, -50))
tuboB = Actor("tubo_verde_abajo", (700, tuboA.y + 550))

boton_menu = Actor("boton_menu", center=(300, 420))
boton_ok = Actor("boton_ok", center=(300, 420))
boton_getready = Actor("boton_getready", center=(300, 100))
boton_tap = Actor("boton_tap", center=(300, 200))
boton_gameover = Actor("boton_gameover", center=(300, 200))
logo_monedas = Actor("logo_monedas", topleft=(10, 10))
numero_actual = Actor("0", topleft=(38, 15))

# === Variables de estado ===
personaje_actual = "pajaro"
velocidad = 0
gravedad = 0.5
salto = -8
count = 0
pasado = False
mode = "menu"

# === Funciones de Lógica ===
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

def movimientoPiso():
    piso1.x -= 2
    piso2.x -= 2
    if piso1.right < 0:
        piso1.left = piso2.right
    if piso2.right < 0:
        piso2.left = piso1.right

def conteoMonedas():
    global pasado, count
    if tuboA.x < pajaro.x and not pasado:
        count += 1
        pasado = True
        # Actualizamos la imagen del número (asegúrate de tener imágenes "0.png", "1.png", etc.)
        if count <= 9:
            numero_actual.image = str(count)

def colisiones():
    global mode 
    if pajaro.colliderect(tuboA) or pajaro.colliderect(tuboB) or pajaro.colliderect(piso1) or pajaro.colliderect(piso2):
        mode = "game_over"

def volver_sprite_normal():
    pajaro.image = personaje_actual

# === Dibujo ===
def draw():
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
    global velocidad, mode
    if mode == "game":
        velocidad += gravedad
        pajaro.y += velocidad
        movimientoTuberias()
        movimientoPiso()
        conteoMonedas()
        colisiones()
    
    # Límites de pantalla
    if pajaro.y > HEIGHT:
        pajaro.y = HEIGHT
        velocidad = 0
    if pajaro.y < 0:
        pajaro.y = 0
        velocidad = 0

# UNIFICAMOS on_mouse_down (Solo puede haber una función con este nombre)
def on_mouse_down(pos):
    global velocidad, mode, count, pasado, personaje_actual
    
    if mode == "menu":
        if boton_tap.collidepoint(pos):
            mode = "game"
        elif boton_menu.collidepoint(pos):
            mode = "coleccion"
            
    elif mode == "game":
        velocidad = salto
        # Cambia imagen si existe el archivo (ej: pajaro_ojos_cerrados.png)
        try:
            pajaro.image = personaje_actual + "_ojos_cerrados"
            clock.schedule_unique(volver_sprite_normal, 0.2)
        except:
            pass # Si no existe la imagen de ojos cerrados, no hace nada
            
    elif mode == "game_over":
        if boton_menu.collidepoint(pos):
            mode = "coleccion"
            # Reset de posiciones
            pajaro.y = 250
            velocidad = 0
            tuboA.x = 700
            tuboB.x = 700
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

# === MOTOR PARA LA WEB (Pygbag) ===
async def main():
    # pgzrun.go() se encarga de iniciar el loop de Pygame Zero
    pgzrun.go()
    # Este loop mantiene el juego "vivo" asíncronamente en el navegador
    while True:
        await asyncio.sleep(0)

if __name__ == "__main__":
    asyncio.run(main())