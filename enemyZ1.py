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
        self.imagen = pygame.image.load("imagenes/enemigo1.png") #cargar imagen
        self.imagen = pygame.transform.scale(self.imagen, (self.ancho, self.alto)) #dimensionar imagen en tamaño del rectangulo
        self.vida = 3

    def dibujar(self, ventana):
        self.rect = pygame.Rect(self.x, self.y,self.ancho, self.alto )
        #pygame.draw.rect(ventana, self.color, self.rect)
        ventana.blit(self.imagen, (self.x, self.y)) #poner imagen sobre rectangulo

    def move (self):
        self.y += self.speed