import pygame
import time
import random


class Soles:
    def __init__(self, columna, fila, imagen, tipo, ancho, alto):
        self.columna = columna
        self.fila = fila
        self.tipo = tipo  # "planta" o "cielo"
        self.ancho = ancho
        self.alto = alto
        self.altura_random = random.randint(1, 4) * 100
        self.tiempo_creacion = time.time()

        self.y_base = fila * 100
        self.x = columna * 100
        self.y = self.y_base  # Y actual (puede caer si es del cielo)

        if imagen:
            self.imagen = pygame.transform.scale(imagen, (self.ancho, self.alto))
        else:
            self.imagen = None

        self.rect = pygame.Rect(self.x, self.y, self.ancho, self.alto)

    def dibujar(self, ventana, offset_y=0):
        self.rect.topleft = (self.x, self.y + offset_y)
        if self.imagen:
            ventana.blit(self.imagen, self.rect)
        else:
            pygame.draw.rect(ventana, (255, 255, 0), self.rect)

    def planta_cielo(self):
        return self.tipo

    def expiro(self, tiempo_actual, tiempo_limite=10):
        return tiempo_actual - self.tiempo_creacion > tiempo_limite

    def caida(self):
        if self.tipo == "cielo":
            if self.y < self.altura_random:
                self.y += 0.8
            else:
                self.y = self.altura_random
            self.rect.y = self.y  # sin offset aquí, se suma al dibujar

    def agarrar_sol(self, x, y, offset_y=0):
        rect_click = self.rect.copy()
        rect_click.y = self.y + offset_y
        return rect_click.collidepoint(x, y)

