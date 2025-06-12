import pygame
class cortadora():
    def __init__(self, x, y, velocidad):
        
        self.x = x
        self.y = y
        self.velocidad = 10

    def movimiento(self):
        
        self.x = self.x + self.velocidad
        self.rect.x = self.x

    def dibujar(self, ventana, offset_y=0):
        self.rect.topleft = (self.x, self.y + offset_y)
        if self.imagen:
            ventana.blit(self.imagen, self.rect)
        else:
            pygame.draw.rect(ventana, (100, 0, 0), self.rect)