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
        self.imagen = pygame.image.load("imagenes/laser1.png")  # Cargar imagen
        self.imagen = pygame.transform.scale(self.imagen, (self.ancho, self.alto))  # Escalar imagen

    def dibujar(self, ventana):
        ventana.blit(self.imagen, (self.x, self.y))  # Dibuja la bala

    def movimiento(self):
        self.y -= self.speed
        self.rect.y = self.y  # Actualiza la posición del rectángulo