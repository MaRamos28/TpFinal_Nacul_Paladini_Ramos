import pygame

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

class Lanzaguisantes(Planta):
    def __init__(self, fila, columna, imagen):
        super().__init__(fila, columna, imagen, vida=6)

class Nuez(Planta):
    def __init__(self, fila, columna, imagen):
        super().__init__(fila, columna, imagen, vida=60)
