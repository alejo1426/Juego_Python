import pygame
from pj import Nave
from enemyZ1 import EnemyZ1
import random

ANCHO = 1000
ALTO = 800
VENTANA = pygame.display.set_mode([ANCHO, ALTO])
FPS = 60

PLAYING = True

reloj = pygame.time.Clock()

tiempo = 0
spawn = 500


nave = Nave(100, 100)

enemys = []
enemys.append(EnemyZ1(ANCHO/2, -75))

def Orden_Keys(keys):
    if keys[pygame.K_w]:
        nave.y -= nave.speed
    if keys[pygame.K_s]:
        nave.y += nave.speed
    if keys[pygame.K_a]:
        nave.x -= nave.speed
    if keys[pygame.K_d]:
        nave.x += nave.speed


while PLAYING:
    tiempo += reloj.tick(FPS)
    if tiempo > spawn:
        enemys.append(EnemyZ1(random.randint(0,ANCHO),-100))
        tiempo = 0

    eventos = pygame.event.get()

    keys = pygame.key.get_pressed()

    Orden_Keys(keys)

    for evento in eventos:
        if evento.type == pygame.QUIT:
            PLAYING = False

    VENTANA.fill("black")
    nave.dibujar(VENTANA)

    for enemy in enemys:
        enemy.dibujar(VENTANA)
        enemy.move()

    pygame.display.update()

quit()