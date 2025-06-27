import pygame
import random
import time

tamaño_celda = 100


class Zombie:
    """
    Clase que representa a un zombie en el juego.
    """

    def __init__(self, tipo, imagen):
        """
        Inicializa un objeto Zombie con un tipo y una imagen.
        input:
            tipo: tipo de zombi (normal, cono, balde)
            imagen: imagen del zombi

        """
        self.fila = random.randint(0, 4)
        self.x = 1010
        self.y = self.fila * tamaño_celda
        self.velocidad = 0.25
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

    def recibedaño(self) -> bool:
        """
        Reduce la vida del zombie en 1 y verifica si ha muerto.

        output:
            True si el zombie ha muerto, False en caso contrario.
        """

        self.vida -= 1
        return self.vida <= 0

    def ataque(self) -> bool:
        """
        Verifica si el zombie puede atacar.
        output:
            True si puede atacar, False en caso contrario.
        """
        if time.time() - self.ultimo_ataque > 1:
            self.ultimo_ataque = time.time()
            return True
        return False

    def mover(self) -> None:
        """
        Mueve el zombie hacia la izquierda a su velocidad definida.
        """
        self.x -= self.velocidad
        self.rect.x = self.x

    def dibujar(self, ventana: pygame.Surface, offset_y: int = 0) -> None:
        """
        Dibuja el zombie en la ventana.
        input:
            ventana: superficie donde se dibuja el zombie
            offset_y: desplazamiento vertical opcional para el dibujo
        """

        self.rect.topleft = (self.x, self.y + offset_y)
        if self.imagen:
            ventana.blit(self.imagen, self.rect)
        else:
            pygame.draw.rect(ventana, (100, 0, 0), self.rect)

    def devolver_coords(self) -> tuple:
        return (self.x, self.y)

    def actualizar_imagen(self, zombie: pygame.Surface, zombie_sin_brazo: pygame.Surface, zombie_cono_roto: pygame.Surface, zombie_balde_roto: pygame.Surface) -> None:
        if self.tipo == "cono" and self.vida <= 15 and self.vida > 10:
            self.imagen = zombie_cono_roto

        elif self.tipo == "cono" and self.vida <= 10:
            self.imagen = zombie
            self.tipo = "normal"

        elif self.tipo == "balde" and self.vida <= 20 and self.vida > 10:
            self.imagen = zombie_balde_roto

        elif self.tipo == "balde" and self.vida <= 10:
            self.imagen = zombie
            self.tipo = "normal"

        elif self.tipo == "normal" and self.vida <= 5:
            self.imagen = zombie_sin_brazo
