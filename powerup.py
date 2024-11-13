import pygame
import random

class item:
    def __init__(self, posi_x, posi_y):
        self.x = posi_x
        self.y = posi_y
        self.ancho = 35
        self.alto = 35
        self.speed = 1
        self.tipo = random.randint(1,2)
        self.color = "Red" if self.tipo == 1 else "Blue"
        self.rect = pygame.Rect(self.x, self.y, self.ancho, self.alto)

    def dibujar(self, ventana):
        pygame.draw.rect(ventana, self.color, self.rect)  # Dibuja el power-up

    def move(self):
        self.y += self.speed
        self.rect.y = self.y  # Actualiza la posición del rectángulo