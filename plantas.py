import pygame
import time

tamaño_celda = 100


class Planta:
    def __init__(self, fila, columna, imagen, vida):
        self.fila = fila
        self.columna = columna
        self.x = columna * tamaño_celda
        self.y = fila * tamaño_celda
        self.vida = vida
        self.imagen = imagen
        self.rect = pygame.Rect(self.x, self.y, 100, 100)

    def recibedaño(self):
        self.vida -= 1
        return self.vida <= 0

    def dibujar(self, ventana):
        if self.imagen:
            ventana.blit(self.imagen, self.rect)
        else:
            pygame.draw.rect(ventana, (0, 100, 0), self.rect)


class Girasol(Planta):
    def __init__(self, fila, columna, imagen):
        super().__init__(fila, columna, imagen, vida=6)

    # quiero ver si es asi, borrador
    def puede_generar(self):
        return time.time()


class Lanzaguisantes(Planta):
    def __init__(self, fila, columna, imagen):
        super().__init__(fila, columna, imagen, vida=6)
        self.ultimo_disparo = time.time()

    def puede_disparar(self):
        return time.time() - self.ultimo_disparo >= 2

    def disparar(self, img_proyectil):
        self.ultimo_disparo = time.time()
        return Proyectiles(self.x + 60, self.y, img_proyectil)

    def devolver_coords(self):
        return self.x, self.y


class Nuez(Planta):
    def __init__(self, fila, columna, imagen):
        super().__init__(fila, columna, imagen, vida=60)


class Proyectiles:
    def __init__(self, x, y, imagen):
        self.x = x
        self.y = y + 15
        self.velocidad = 5
        self.ancho = 30
        self.alto = 30
        if imagen:
            self.imagen = pygame.transform.scale(imagen, (self.ancho, self.alto))
        else:
            self.imagen = None

        self.rect = pygame.Rect(self.x, self.y, self.ancho, self.alto)

    def mover(self):
        self.x += self.velocidad
        self.rect.x = self.x

    def dibujar(self, ventana):
        if self.imagen:
            ventana.blit(self.imagen, self.rect)
        else:
            pygame.draw.rect(ventana, (0, 255, 0), self.rect)

    def devolver_coords(self):
        return self.x, self.y
