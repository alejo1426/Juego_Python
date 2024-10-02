import pygame
from pj import Nave
from enemyZ1 import EnemyZ1

import random

#pip install pygame

ANCHO = 1000
ALTO = 800
VENTANA = pygame.display.set_mode([ANCHO,ALTO])
FPS = 60



jugando = True

reloj = pygame.time.Clock()

tiempo_pasado = 0
tiempo_entre_enemigos = 500

cubo = Nave(ANCHO/2,ALTO-75)

enemigos = []

enemigos.append(EnemyZ1(ANCHO/2, 100))

def gestionar_teclas(teclas):
    if teclas[pygame.K_w]:
        cubo.y -= cubo.speed
    if teclas[pygame.K_s]:
        cubo.y += cubo.speed
    if teclas[pygame.K_a]:
        cubo.x -= cubo.speed
    if teclas[pygame.K_d]:
        cubo.x += cubo.speed


while jugando:

    tiempo_pasado += reloj.tick(FPS)

    if tiempo_pasado > tiempo_entre_enemigos:
        enemigos.append(EnemyZ1(random.randint(0,ANCHO),-100))
        tiempo_pasado = 0


    eventos = pygame.event.get()

    teclas = pygame.key.get_pressed()



    gestionar_teclas(teclas)

    for evento in eventos:
        if evento.type == pygame.QUIT:
            jugando = False

    VENTANA.fill("black")
    cubo.dibujar(VENTANA)

    for enemigo in enemigos:
        enemigo.dibujar(VENTANA)
        enemigo.move()

    pygame.display.update()

quit()