import pygame
class cortadora():
    def __init__(self, fila, imagen):
        self.fila = fila
        self.imagen = imagen
        self.y = fila * 100
        self.x = 0
        self.velocidad = 8
        self.activada = False
        self.imagen = pygame.transform.scale(imagen,(100,100))
        self.rect = pygame.Rect(self.x, self.y, 100, 100)
        self.ya_sono = False  # <-- AHORA SÍ, este es el atributo correcto

    def activar(self):
        self.activada = True
        
    def esta_activada(self):
        return self.activada
        
    def movimiento(self):   
        if self.activada:
            self.x = self.x + self.velocidad
            self.rect.x = self.x

    def dibujar(self, ventana, offset_y=0):
        self.rect.topleft = (self.x, self.y + offset_y)
        if self.imagen:
            ventana.blit(self.imagen, self.rect)
        else:
            pygame.draw.rect(ventana, (100, 0, 0), self.rect)

    def puede_reproducir_sonido(self):
        """Solo devuelve True la primera vez que se activa"""
        if self.activada and not self.ya_sono:
            self.ya_sono = True
            return True
        return False
