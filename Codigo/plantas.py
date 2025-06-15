import pygame
import time
from funciones import *

tamaño_celda = 100
tiempo_soles = 8


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

    def dibujar(self, ventana, offset_y=0):
        self.rect.topleft = (self.x, self.y + offset_y)
        if self.imagen:
            ventana.blit(self.imagen, self.rect)
        else:
            pygame.draw.rect(ventana, (0, 100, 0), self.rect)

    def devolver_coords(self):
        return (self.x, self.y)


class Girasol(Planta):
    def __init__(self, fila, columna, imagen):
        super().__init__(fila, columna, imagen, vida=6)
        self.tiempo_ultimo_sol = time.time()
        self.intervalo_sol = 8
        self.sol_activo = None  # apunta al sol que generó

    def valor(self):
        self.valor = 50

    def puede_generar(self):
        return (
            self.sol_activo is None
            and time.time() - self.tiempo_ultimo_sol >= self.intervalo_sol
        )


class Lanzaguisantes(Planta):
    def __init__(self, fila, columna, imagen, imagen_disparo):
        super().__init__(fila, columna, imagen, vida=6)
        self.imagen_normal = imagen
        self.imagen_disparo = imagen_disparo
        self.estado = "normal"  # puede ser "normal" o "preparando"
        self.tiempo_preparacion = 0.3  # segundos de preparación
        self.ultimo_disparo = time.time()
        self.inicio_preparacion = 0
        self.proyectil_pendiente = False

    def puede_disparar(self):
        return time.time() - self.ultimo_disparo >= 2 and self.estado == "normal"

    def preparar_disparo(self):
        self.estado = "preparando"
        self.inicio_preparacion = time.time()
        self.proyectil_pendiente = True

    def actualizar_animacion(self):
        if self.estado == "preparando":
            if time.time() - self.inicio_preparacion >= self.tiempo_preparacion:
                self.estado = "normal"
                self.ultimo_disparo = time.time()
                return True
        return False

    def disparar(self, img_proyectil):
        return Proyectiles(self.x + 60, self.y, img_proyectil)

    def dibujar(self, ventana, offset_y=0):
        if self.estado == "preparando":
            ventana.blit(self.imagen_disparo, (self.x, self.y + offset_y))
        else:
            ventana.blit(self.imagen_normal, (self.x, self.y + offset_y))

    def valor(self):
        self.valor = 100

class LanzaguisantesTriple(Planta):
    def __init__(self, fila, columna, imagen, imagen_disparo):
        super().__init__(fila, columna, imagen, vida=6)
        self.imagen_normal = imagen
        self.imagen_disparo = imagen_disparo
        self.estado = "normal"
        self.cooldown = 5
        self.ultimo_disparo = time.time() - self.cooldown  # arranca disponible
        self.proyectiles_restantes = 0
        self.tiempo_entre_proyectiles = 0.2
        self.ultimo_proyectil_disparado = 0

    def puede_disparar(self):
        return (time.time() - self.ultimo_disparo >= self.cooldown) and self.estado == "normal"

    def preparar_disparo(self):
        self.estado = "disparando"
        self.proyectiles_restantes = 3
        self.ultimo_proyectil_disparado = time.time()

    def disparar(self, img_proyectil):
        proyectiles = []
        tiempo_actual = time.time()

        if self.estado == "disparando":
            if self.proyectiles_restantes > 0 and (tiempo_actual - self.ultimo_proyectil_disparado >= self.tiempo_entre_proyectiles):
                proyectiles.append(Proyectiles(self.x + 60, self.y, img_proyectil))
                self.proyectiles_restantes -= 1
                self.ultimo_proyectil_disparado = tiempo_actual

                if self.proyectiles_restantes == 0:
                    self.estado = "normal"
                    self.ultimo_disparo = time.time()

        return proyectiles

    def dibujar(self, ventana, offset_y=0):
        if self.estado == "disparando":
            ventana.blit(self.imagen_disparo, (self.x, self.y + offset_y))
        else:
            ventana.blit(self.imagen_normal, (self.x, self.y + offset_y))


class Nuez(Planta):
    def __init__(self, fila, columna, imagen_sana, imagen_mitad, imagen_dañada):
        super().__init__(fila, columna, imagen_sana, vida=60)
        self.imagen_sana = imagen_sana
        self.imagen_mitad = imagen_mitad
        self.imagen_dañada = imagen_dañada
        self.actualizar_imagen()

    def actualizar_imagen(self):
        if self.vida <= 15:
            self.imagen = self.imagen_dañada
        elif self.vida <= 30:
            self.imagen = self.imagen_mitad
        else:
            self.imagen = self.imagen_sana
        self.rect = self.imagen.get_rect(topleft=(self.x, self.y))

    def recibedaño(self):
        self.vida -= 1
        self.actualizar_imagen()
        return self.vida <= 0

    def valor(self):
        self.valor = 50


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

    def dibujar(self, ventana, offset_y=0):
        self.rect.y = self.y + offset_y
        if self.imagen:
            ventana.blit(self.imagen, self.rect)
        else:
            pygame.draw.rect(ventana, (0, 255, 0), self.rect)

    def devolver_coords(self):
        return (self.x, self.y)
