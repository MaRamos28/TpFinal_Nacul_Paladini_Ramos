import pygame
import time

class EfectoGolpe:
    def __init__(self, x, y, imagen, duracion=0.2):
        self.x = x
        self.y = y
        self.imagen = imagen
        self.duracion = duracion
        self.tiempo_creacion = time.time()
        self.rect = self.imagen.get_rect(center=(x, y))

    def dibujar(self, ventana):
        ventana.blit(self.imagen, self.rect)

    def expiro(self):
        return time.time() - self.tiempo_creacion >= self.duracion
