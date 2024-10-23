import pygame

class Bala:
    def __init__(self, posi_x, posi_y):
        self.x = posi_x
        self.y = posi_y
        self.ancho = 20
        self.alto = 20
        self.speed = 10
        self.color = "white"
        self.rect = pygame.Rect(self.x, self.y,self.ancho, self.alto )

    def dibujar(self, ventana):
        self.rect = pygame.Rect(self.x, self.y,self.ancho, self.alto )
        pygame.draw.rect(ventana, self.color, self.rect)

    def movimiento (self):
        self.y -= self.speed