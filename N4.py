import os
import pygame
from pj import Nave
from enemyZ1 import EnemyZ4
from bala import Bala
from powerup import item
import random

pygame.init()
pygame.mixer.init()

# Obtener tamaño de pantalla del sistema
info_pantalla = pygame.display.Info()
ANCHO = int(info_pantalla.current_w * 0.5)
ALTO = int(info_pantalla.current_h * 0.8)

# Configurar la ventana
VENTANA = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Juego adaptado a la pantalla")

# Cargar la imagen de fondo
fondo = pygame.image.load('imagenes/infierno.png')
fondo = pygame.transform.scale(fondo, (ANCHO, ALTO))

# Configuración del juego
FPS = 60
FUENTE = pygame.font.SysFont("Times New Roman", 40)
Sonido_Disparo = pygame.mixer.Sound('assets/disparo.wav')
Sonido_Muertepj = pygame.mixer.Sound('assets/muertePJ.wav')
Sonido_MuerteEnemy = pygame.mixer.Sound('assets/muerteEnemy.wav')

jugando = True
reloj = pygame.time.Clock()

vida = 5
puntos = 0
mostrar_mensaje_full = False
tiempo_mensaje_full = 0

# Variables de tiempo
tiempo_pasado = 0
ultima_aparicion_enemigos = 0
ultima_aparicion_powerup = 0
tiempo_entre_powerups = 20000
tiempo_entre_enemigos = 1000

# Crear la nave
cubo = Nave(ANCHO / 2, ALTO - 75)

# Listas de enemigos y balas
enemigos = []
balas = []

ultima_bala = 0
tiempo_entre_balas = 100

# Inicializar un power-up (vacío al inicio)
powerup = None

# Agregar un enemigo inicial
enemigos.append(EnemyZ4(ANCHO / 2, 100))

# Función para mostrar el mensaje de nivel completado
def mostrar_mensaje_nivel_completado():
    ventana_nivel = True
    trofeo = pygame.image.load('imagenes/trofeo.gif')  # Asegúrate de tener una imagen de trofeo
    trofeo = pygame.transform.scale(trofeo, (100, 100))  # Ajustar tamaño del trofeo si es necesario

    input_box = pygame.Rect(ANCHO // 2 - 100, ALTO // 2 + 130, 200, 40)
    submit_button = pygame.Rect(ANCHO // 2 - 50, ALTO // 2 + 190, 100, 40)

    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive
    active = False
    text = ''
    font_game_over = pygame.font.SysFont("Times New Roman", 60)
    font_normal = pygame.font.SysFont("Times New Roman", 32)

    while ventana_nivel:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN:
                    # Guardar la puntuación en el archivo
                    with open('puntuaciones.txt', 'a') as archivo:
                        archivo.write(f"{text} - {puntos} - {'Completo el juego'}\n")
                    pygame.quit()  # Cierra la ventana del juego después de guardar la puntuación
                    quit()
                elif evento.key == pygame.K_BACKSPACE:
                    text = text[:-1]
                else:
                    text += evento.unicode

        VENTANA.fill("black")

        # Texto "FELICITACIONES"
        texto_completado = font_game_over.render("¡FELICITACIONES!", True, "yellow")
        texto_completado_rect = texto_completado.get_rect(center=(ANCHO // 2, ALTO // 2 - 150))
        VENTANA.blit(texto_completado, texto_completado_rect)

        # Imagen del trofeo
        trofeo_rect = trofeo.get_rect(center=(ANCHO // 2, ALTO // 2 - 50))
        VENTANA.blit(trofeo, trofeo_rect)

        # Texto "Completaste el juego"
        texto_completado2 = font_game_over.render("Completaste el juego", True, "white")
        texto_completado2_rect = texto_completado2.get_rect(center=(ANCHO // 2, ALTO // 2 + 20))
        VENTANA.blit(texto_completado2, texto_completado2_rect)

        # Texto "Ingresa tu nombre"
        texto_ingresar_nombre = font_normal.render("Ingresa tu nombre", True, "white")
        texto_ingresar_nombre_rect = texto_ingresar_nombre.get_rect(center=(ANCHO // 2, ALTO // 2 + 90))
        VENTANA.blit(texto_ingresar_nombre, texto_ingresar_nombre_rect)

        # Campo de entrada de texto
        txt_surface = font_normal.render(text, True, color)
        width = max(200, txt_surface.get_width() + 10)
        input_box.w = width
        VENTANA.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
        pygame.draw.rect(VENTANA, color, input_box, 2)

        # Botón de enviar
        pygame.draw.rect(VENTANA, pygame.Color('red'), submit_button, border_radius=10)  # Redondeo del borde
        texto_enviar = font_normal.render("Enviar", True, "white")
        VENTANA.blit(texto_enviar, (submit_button.x + 10, submit_button.y + submit_button.height // 2 - texto_enviar.get_height() // 2))

        pygame.display.flip()
        reloj.tick(30)

# Función para mostrar el mensaje de "Game Over" y permitir ingresar el nombre
def mostrar_game_over():
    Sonido_Muertepj.play()
    input_box = pygame.Rect(ANCHO // 2 - 100, ALTO // 2 + 20, 200, 40)
    submit_button = pygame.Rect(ANCHO // 2 - 50, ALTO // 2 + 80, 100, 40)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive
    active = False
    text = ''
    font_game_over = pygame.font.SysFont("Times New Roman", 60)  # Fuente más grande para "GAME OVER"
    font_normal = pygame.font.SysFont("Times New Roman", 32)  # Fuente normal para los otros textos
    clock = pygame.time.Clock()

    # Mostrar el mensaje de "Game Over" primero
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                quit()

            if evento.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(evento.pos):
                    active = True
                else:
                    active = False
                color = color_active if active else color_inactive

            if evento.type == pygame.KEYDOWN:
                if active:
                    if evento.key == pygame.K_RETURN:
                        # Guardar la puntuación en el archivo
                        with open('puntuaciones.txt', 'a') as archivo:
                            archivo.write(f"{text} - {puntos} - {'Alcanzo Nivel 4'}\n")
                        pygame.quit()  # Cierra la ventana del juego después de guardar la puntuación
                        quit()
                    elif evento.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += evento.unicode

        VENTANA.fill((0, 0, 0))

        # Mostrar el mensaje "Game Over" con una fuente más grande
        texto_game_over = font_game_over.render("GAME OVER", True, "red")
        VENTANA.blit(texto_game_over, (ANCHO // 2 - texto_game_over.get_width() // 2, ALTO // 2 - 100))

        # Mostrar el texto "Ingresa tu nombre" con la fuente normal
        texto_ingresar_nombre = font_normal.render("Ingresa tu nombre", True, "white")
        VENTANA.blit(texto_ingresar_nombre, (ANCHO // 2 - texto_ingresar_nombre.get_width() // 2, ALTO // 2 - 40))

        # Dibujar el campo de texto
        txt_surface = font_normal.render(text, True, color)
        width = max(200, txt_surface.get_width() + 10)
        input_box.w = width
        VENTANA.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
        pygame.draw.rect(VENTANA, color, input_box, 2)

        # Dibujar el botón de enviar con bordes redondeados y espaciado interno
        pygame.draw.rect(VENTANA, pygame.Color('red'), submit_button, border_radius=10)  # Redondeamos los bordes
        texto_enviar = font_normal.render("enviar", True, "white")
        # Añadir espaciado interno entre el texto "enviar" y el borde
        VENTANA.blit(texto_enviar, (submit_button.x + 10, submit_button.y + submit_button.height // 2 - texto_enviar.get_height() // 2))

        pygame.display.flip()
        clock.tick(30)

def crear_bala():
    global ultima_bala
    if pygame.time.get_ticks() - ultima_bala > tiempo_entre_balas:
        balas.append(Bala(cubo.rect.centerx, cubo.rect.centery))
        ultima_bala = pygame.time.get_ticks()
        Sonido_Disparo.play()

def gestionar_teclas(teclas):
    if teclas[pygame.K_w] and cubo.y >= 0:
        cubo.y -= cubo.speed
    if teclas[pygame.K_s] and cubo.y + cubo.alto <= ALTO:
        cubo.y += cubo.speed
    if teclas[pygame.K_a] and cubo.x >= 0:
        cubo.x -= cubo.speed
    if teclas[pygame.K_d] and cubo.x + cubo.ancho <= ANCHO:
        cubo.x += cubo.speed
    if teclas[pygame.K_SPACE]:
        crear_bala()

while jugando:
    tiempo_pasado += reloj.tick(FPS)

    # Verificar si el jugador alcanzó la meta de puntos
    if puntos >= 1500:
        mostrar_mensaje_nivel_completado()
        puntos = 0
        enemigos.clear()
        continue

    # Lógica para generar enemigos
    if pygame.time.get_ticks() - ultima_aparicion_enemigos > tiempo_entre_enemigos:
        x_pos = random.randint(0, ANCHO - 50)
        enemigos.append(EnemyZ4(x_pos, -100))
        ultima_aparicion_enemigos = pygame.time.get_ticks()

    # Verificar si es momento de generar un power-up
    if pygame.time.get_ticks() - ultima_aparicion_powerup > tiempo_entre_powerups:
        powerup = item(random.randint(0, ANCHO - 35), random.randint(0, ALTO - 35))
        ultima_aparicion_powerup = pygame.time.get_ticks()

    eventos = pygame.event.get()
    teclas = pygame.key.get_pressed()

    texto_vida = FUENTE.render(f"Vida:  {vida}", True, "white")
    texto_puntos = FUENTE.render(f"Puntos:  {puntos}", True, "white")

    gestionar_teclas(teclas)

    for evento in eventos:
        if evento.type == pygame.QUIT:
            jugando = False

    # Dibujar el fondo
    VENTANA.blit(fondo, (0, 0))
    cubo.dibujar(VENTANA)

    # Dibujar y manejar el power-up
    if powerup:
        powerup.dibujar(VENTANA)
        powerup.move()
        if pygame.Rect.colliderect(cubo.rect, powerup.rect):
            if powerup.tipo == 1:
                if vida < 6:
                    vida += 1
                else:
                    mostrar_mensaje_full = True
                    tiempo_mensaje_full = pygame.time.get_ticks()
                powerup = None
            elif powerup.tipo == 2:
                cubo.speed += 1
                powerup = None
        if powerup and powerup.y > ALTO:
            powerup = None

    if mostrar_mensaje_full:
        if pygame.time.get_ticks() - tiempo_mensaje_full < 2000:
            texto_full = FUENTE.render("Full", True, "yellow")
            VENTANA.blit(texto_full, (20, 120))
        else:
            mostrar_mensaje_full = False

    # Actualizar y dibujar enemigos
    for enemigo in enemigos[:]:
        enemigo.dibujar(VENTANA)
        enemigo.move()

        # Colisión con el jugador
        if pygame.Rect.colliderect(cubo.rect, enemigo.rect):
            vida -= 1
            if vida <= 0:
                mostrar_game_over()
            if enemigo in enemigos:
                enemigos.remove(enemigo)

        # Verificar si el enemigo salió de la pantalla
        if enemigo.y > ALTO:
            puntos -= 2
            if puntos <= 0:
                puntos = 0
                mostrar_game_over()
            if enemigo in enemigos:
                enemigos.remove(enemigo)

        # Colisión con las balas
        for bala in balas:
            if pygame.Rect.colliderect(bala.rect, enemigo.rect):
                enemigo.vida -= 1
                balas.remove(bala)
            if enemigo.vida <= 0:
                Sonido_MuerteEnemy.play()
                if enemigo in enemigos:
                    enemigos.remove(enemigo)
                    puntos += 5

    # Actualizar y dibujar balas
    for bala in balas[:]:
        bala.dibujar(VENTANA)
        bala.movimiento()
        if bala.y < 0:
            balas.remove(bala)

    VENTANA.blit(texto_vida, (20, 20))
    VENTANA.blit(texto_puntos, (20, 70))

    pygame.display.update()

Sonido_Muertepj.play()
pygame.quit()

quit()
