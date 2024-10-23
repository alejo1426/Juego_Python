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
        self.imagen = pygame.image.load("imagenes/laser1.png") #cargar imagen
        self.imagen = pygame.transform.scale(self.imagen, (self.ancho, self.alto)) #dimensionar imagen en tamaño del rectangulo

    def dibujar(self, ventana):
        self.rect = pygame.Rect(self.x, self.y,self.ancho, self.alto )
        #pygame.draw.rect(ventana, self.color, self.rect)
        ventana.blit(self.imagen, (self.x, self.y)) #poner imagen sobre rectangulo

    def movimiento (self):
        self.y -= self.speed