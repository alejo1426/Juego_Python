import pygame

class EnemyZ1:
    def __init__(self, posi_x, posi_y):
        self.x = posi_x
        self.y = posi_y
        self.ancho = 75
        self.alto = 75
        self.speed = 1
        self.rect = pygame.Rect(self.x, self.y, self.ancho, self.alto)
        self.imagen = pygame.image.load("imagenes/enemigo1.png")  # Cargar imagen
        self.imagen = pygame.transform.scale(self.imagen, (self.ancho, self.alto))  # Escalar imagen
        self.vida = 3

    def dibujar(self, ventana):
        ventana.blit(self.imagen, (self.x, self.y))  # Dibuja el enemigo

    def move(self):
        self.y += self.speed
        self.rect.y = self.y  # Actualiza la posición del rectángulo