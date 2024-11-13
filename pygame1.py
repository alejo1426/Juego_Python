import pygame
from pj import Nave
from enemyZ1 import EnemyZ1
from bala import Bala
from powerup import item  # Asegúrate de que el nombre de la clase esté en minúscula como en tu código original
import random

pygame.init()
pygame.mixer.init()

# Obtener tamaño de pantalla del sistema
info_pantalla = pygame.display.Info()
ANCHO = int(info_pantalla.current_w * 0.9)  # Usar un 90% del ancho total
ALTO = int(info_pantalla.current_h * 0.9)   # Usar un 90% del alto total

# Configurar la ventana
VENTANA = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Juego adaptado a la pantalla")

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
mostrar_mensaje_full = False  # Variable para mostrar el mensaje de "Full"
tiempo_mensaje_full = 0  # Tiempo en el que se muestra el mensaje

# Variables de tiempo
tiempo_pasado = 0
ultima_aparicion_powerup = 0  # Tiempo de la última aparición de power-up
tiempo_entre_powerups = 20000  # 20 segundos en milisegundos
tiempo_entre_enemigos = 5000  # 5 segundos al principio
tiempo_entre_enemigos_base = 5000  # 5 segundos base
ultima_aparicion_enemigos = 0  # Tiempo de la última aparición de enemigos

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
enemigos.append(EnemyZ1(ANCHO / 2, 100))

def crear_bala():
    global ultima_bala

    if pygame.time.get_ticks() - ultima_bala > tiempo_entre_balas:
        balas.append(Bala(cubo.rect.centerx, cubo.rect.centery))
        ultima_bala = pygame.time.get_ticks()
        Sonido_Disparo.play()

def gestionar_teclas(teclas):
    if teclas[pygame.K_w]:
        if cubo.y >= 0:
            cubo.y -= cubo.speed
    if teclas[pygame.K_s]:
        if cubo.y + cubo.alto <= ALTO:
            cubo.y += cubo.speed
    if teclas[pygame.K_a]:
        if cubo.x >= 0:
            cubo.x -= cubo.speed
    if teclas[pygame.K_d]:
        if cubo.x + cubo.ancho <= ANCHO:
            cubo.x += cubo.speed
    if teclas[pygame.K_SPACE]:
        crear_bala()

while jugando and vida > 0:
    tiempo_pasado += reloj.tick(FPS)

    # Ajustar el tiempo de aparición de los enemigos según el tiempo transcurrido
    if tiempo_pasado > 15000 and tiempo_entre_enemigos == 5000:
        tiempo_entre_enemigos = 3000  # Cambiar a 3 segundos después de 15 segundos
        ultima_aparicion_enemigos = pygame.time.get_ticks()  # Resetear el tiempo de aparición
    elif tiempo_pasado > 30000 and tiempo_entre_enemigos == 3000:
        tiempo_entre_enemigos = 1000  # Cambiar a 1 segundo después de otros 15 segundos
        ultima_aparicion_enemigos = pygame.time.get_ticks()  # Resetear el tiempo de aparición

    # Lógica para generar enemigos
    if pygame.time.get_ticks() - ultima_aparicion_enemigos > tiempo_entre_enemigos:
        # Generar enemigo dentro de los bordes laterales de la ventana
        x_pos = random.randint(0, ANCHO - 50)  # Ajustar para que no se salga de los bordes
        enemigos.append(EnemyZ1(x_pos, -100))  # Generar enemigo
        ultima_aparicion_enemigos = pygame.time.get_ticks()  # Actualizar el tiempo de aparición

        # Ajustar el tiempo entre enemigos para la próxima aparición
        tiempo_entre_enemigos = random.randint(1000, tiempo_entre_enemigos_base)

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

    VENTANA.fill("black")
    cubo.dibujar(VENTANA)

    # Dibujar y mover el power-up si existe
    if powerup:
        powerup.dibujar(VENTANA)
        powerup.move()

        # Verificar colisión entre el power-up y la nave
        if pygame.Rect.colliderect(cubo.rect, powerup.rect):

            if powerup.tipo == 1:
                if vida < 6:  # Limitar la vida máxima a 6
                    vida += 1  # Efecto del power-up (puedes personalizarlo)
                else:
                    # Mostrar el mensaje de "Full" si la vida ya está en el máximo
                    mostrar_mensaje_full = True
                    tiempo_mensaje_full = pygame.time.get_ticks()
                powerup = None  # Eliminar el power-up después de recogerlo
            elif powerup.tipo == 2:
                cubo.speed += 1
                powerup = None 
        # Verificar si el power-up ha salido de la pantalla
        if powerup and powerup.y > ALTO:
            powerup = None  # Eliminar el power-up

    # Mostrar mensaje de "Full" si está activo y no ha pasado el tiempo límite
    if mostrar_mensaje_full:
        if pygame.time.get_ticks() - tiempo_mensaje_full < 2000:  # Mostrar durante 2 segundos
            texto_full = FUENTE.render("Full", True, "yellow")
            VENTANA.blit(texto_full, (20, 90))
        else:
            mostrar_mensaje_full = False  # Dejar de mostrar el mensaje después de 2 segundos

    # Actualizar y dibujar enemigos
    for enemigo in enemigos[:]:  # Usar una copia de la lista para evitar problemas al eliminar
        enemigo.dibujar(VENTANA)
        enemigo.move()

        if pygame.Rect.colliderect(cubo.rect, enemigo.rect):
            vida -= 1
            print(f"Te golpearon, vidas restantes: {vida}")
            if enemigo in enemigos:
                enemigos.remove(enemigo)

        if enemigo.y > ALTO:
            puntos += 1
            if enemigo in enemigos:
                enemigos.remove(enemigo)

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
    for bala in balas[:]:  # Usar una copia de la lista
        bala.dibujar(VENTANA)
        bala.movimiento()

        if bala.y < 0:
            balas.remove(bala)

    VENTANA.blit(texto_vida, (20, 20))
    VENTANA.blit(texto_puntos, (20, 70))

    pygame.display.update()

Sonido_Muertepj.play()
pygame.quit()

nombre = input("Introduce tu nombre:  ")
with open('puntuaciones.txt', 'a') as archivo:
    archivo.write(f"{nombre} - {puntos}\n")

quit()
