import pygame
import random

class item:
    def __init__(self, posi_x, posi_y):
        self.x = posi_x
        self.y = posi_y
        self.ancho = 35
        self.alto = 35
        self.speed = 1
        self.tipo = random.randint(1, 2)

        # Cargar imágenes según el tipo
        self.imagen = pygame.image.load("imagenes/pocionVida.png") if self.tipo == 1 else pygame.image.load("imagenes/pocionVelocidad.png")
        self.imagen = pygame.transform.scale(self.imagen, (self.ancho, self.alto))

        self.rect = pygame.Rect(self.x, self.y, self.ancho, self.alto)

    def dibujar(self, ventana):
        # Dibujar la imagen en la ventana
        ventana.blit(self.imagen, (self.rect.x, self.rect.y))

    def move(self):
        self.y += self.speed
        self.rect.y = self.y  # Actualiza la posición del rectángulo
