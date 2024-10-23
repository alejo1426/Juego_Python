import pygame

class Nave:
    def __init__(self, posi_x, posi_y):
        self.x = posi_x
        self.y = posi_y
        self.ancho = 50
        self.alto = 50
        self.speed = 5
        self.color = "purple"
        self.rect = pygame.Rect(self.x, self.y,self.ancho, self.alto )

    def dibujar(self, ventana):
        self.rect = pygame.Rect(self.x, self.y,self.ancho, self.alto )
        pygame.draw.rect(ventana, self.color, self.rect)