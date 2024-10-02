import pygame

class EnemyZ1:
    def __init__(self, posi_x, posi_y):
        self.x = posi_x
        self.y = posi_y
        self.ancho = 75
        self.alto = 75
        self.speed = 1
        self.color = "Blue"
        self.rect = pygame.Rect(self.x, self.y,self.ancho, self.alto )

    def dibujar(self, ventana):
        self.rect = pygame.Rect(self.x, self.y,self.ancho, self.alto )
        pygame.draw.rect(ventana, self.color, self.rect)

    def move (self):
        self.y += self.speed