import pygame
import random
import time

tamaño_celda = 100


class Zombie:
    def __init__(self, tipo, imagen):
        self.fila = random.randint(0, 4)
        self.x = 900
        self.y = self.fila * tamaño_celda
        self.velocidad = 100 / 6
        self.daño = 1
        self.tipo = tipo
        self.imagen = imagen
        self.ancho = 100
        self.alto = 100

        if tipo == "normal":
            self.vida = 10
        elif tipo == "cono":
            self.vida = 20
        elif tipo == "balde":
            self.vida = 30

        self.rect = pygame.Rect(self.x, self.y, self.ancho, self.alto)
        self.ultimo_movimiento = time.time()
        self.ultimo_ataque = time.time()

    def recibedaño(self):
        self.vida -= 1
        return self.vida <= 0

    def ataque(self):
        if time.time() - self.ultimo_ataque > 1:
            self.ultimo_ataque = time.time()
            return True
        return False

    def mover(self):
        if time.time() - self.ultimo_movimiento > 1:
            self.x -= self.velocidad
            self.rect.x = self.x
            self.ultimo_movimiento = time.time()

    def dibujar(self, ventana):
        if self.imagen:
            ventana.blit(self.imagen, self.rect)
        else:
            pygame.draw.rect(ventana, (100, 0, 0), self.rect)

    def devolver_coords(self):
        return self.x, self.y
