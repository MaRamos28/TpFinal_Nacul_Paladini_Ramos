import pygame
import time
import random


class Soles:
    def __init__(self, columna, fila, imagen, tipo, ancho, alto):
        self.columna = columna
        self.fila = fila
        self.tipo = tipo
        self.ancho = ancho
        self.alto = alto
        self.altura_random = random.randint(1, 4) * 100

        self.fila_pos_y = fila * 100
        self.fila_pos_x = columna * 100

        # redimensionar la imagen
        if imagen:
            self.imagen = pygame.transform.scale(imagen, (self.ancho, self.alto))
        else:
            self.imagen = None

        self.rect = pygame.Rect(self.fila_pos_x, self.fila_pos_y, 100, 100)

    def dibujar(self, ventana):
        if self.imagen:
            ventana.blit(self.imagen, self.rect)

        else:
            pygame.draw.rect(ventana, (0, 100, 0), self.rect)

    def planta_cielo(self):
        return self.tipo

    def caida(self):

        if self.tipo == "cielo":

            if self.fila_pos_y < self.altura_random:
                self.fila_pos_y += 0.8
            else:
                self.fila_pos_y = self.altura_random

            self.rect.y = self.fila_pos_y

    def agarrar_sol(self, x, y):
        if self.rect.collidepoint(x, y):
            return True
        return False
