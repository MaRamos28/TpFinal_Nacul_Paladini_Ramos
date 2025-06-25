import pygame
import time
from funciones import *

tamaño_celda = 100
tiempo_soles = 15

class Planta:
    
    '''
    Clase padre para todas las plantas.
    '''

    def __init__(self, fila:int, columna:int, imagen:pygame.Surface, vida:int) -> None:

        '''
        Inicializa una planta en una posición específica de la cuadrícula.
        input:
            fila: fila en la que se va a encontrar la planta
            columna: columna en la que se va a encontrar la planta
            imagen: imagen de la planta
            vida: puntos de vida de la planta
        '''
        
        self.fila = fila
        self.columna = columna
        self.x = columna * tamaño_celda
        self.y = fila * tamaño_celda
        self.vida = vida
        self.imagen = imagen
        self.rect = pygame.Rect(self.x, self.y, 100, 100)

    def recibedaño(self) -> bool:
        
        '''
        Reduce la vida de la planta en 1 punto.
        output:
            True si la planta ha sido destruida, False en caso contrario.
        '''
        
        self.vida -= 1
        return self.vida <= 0

    def dibujar(self, ventana: pygame.Surface, offset_y: int = 0) -> None:
        
        '''
        Dibuja la planta en la ventana.
        input:
            ventana: superficie donde se dibuja la planta
            offset_y: desplazamiento vertical para el dibujo de la planta
        '''
        
        self.rect.topleft = (self.x, self.y + offset_y)
        if self.imagen:
            ventana.blit(self.imagen, self.rect)
        else:
            pygame.draw.rect(ventana, (0, 100, 0), self.rect)

    def devolver_coords(self) -> tuple[int, int]:
        
        '''
        Devuelve las coordenadas (x, y) de la planta.
        output:
            (x, y) donde x es la coordenada horizontal y y es la coordenada vertical.
        '''
        
        return (self.x, self.y)


class Girasol(Planta):
    
    '''
    Clase que representa un girasol en el juego (Clase hija de Planta).
    '''
    
    def __init__(self, fila:int, columna:int, imagen:pygame.Surface) -> None:
        
        '''
        Inicializa un girasol en una posición específica de la grilla.
        input: 
            fila: fila en la que se va a iniciar el girasol
            columna: columna en la que se va a iniciar el girasol
            imagen: imagen del girasol
        '''
        
        super().__init__(fila, columna, imagen, vida=6)
        self.tiempo_ultimo_sol = time.time()
        self.intervalo_sol = tiempo_soles
        self.sol_activo = None  # apunta al sol que generó

    def puede_generar(self) -> bool:
        
        '''
        Devuelve True si el girasol puede generar un nuevo sol, False en caso contrario.
        output:
            True si puede generar, False en caso contrario.
        '''
        
        return (self.sol_activo is None and time.time() - self.tiempo_ultimo_sol >= self.intervalo_sol)


class Lanzaguisantes(Planta):
    
    '''
    Clase que representa un lanzaguisantes en el juego (Clase hija de Planta).
    '''
    
    def __init__(self, fila:int, columna:int, imagen:pygame.Surface, imagen_disparo:pygame.Surface) -> None:
        
        '''
        Inicializa un lanzaguisantes en una posición específica de la grilla.
        input:
            fila: fila en la que se va a iniciar el lanzaguisantes
            columna: columna en la que se va a iniciar el lanzaguisantes
            imagen: imagen del lanzaguisantes
            imagen_disparo: imagen de cuando el lanzaguisantes va a disparar
        '''
        
        super().__init__(fila, columna, imagen, vida=6)
        self.imagen_normal = imagen
        self.imagen_disparo = imagen_disparo
        self.estado = "normal"  # puede ser "normal" o "preparando"
        self.tiempo_preparacion = 0.3  # segundos de preparación
        self.ultimo_disparo = time.time()
        self.inicio_preparacion = 0
        self.proyectil_pendiente = False

    def puede_disparar(self) -> bool:
        
        '''
        Devuelve True si el lanzaguisantes puede disparar, False en caso contrario.
        output:
            True si puede disparar, False en caso contrario.
        '''
        
        return time.time() - self.ultimo_disparo >= 2 and self.estado == "normal"

    def preparar_disparo(self) -> None:
        
        '''
        Cambia el estado del lanzaguisantes a "preparando" y registra el tiempo de inicio de la preparación.
        '''
        
        self.estado = "preparando"
        self.inicio_preparacion = time.time()
        self.proyectil_pendiente = True

    def actualizar_animacion(self) -> bool:
        
        '''
        Actualiza el estado del lanzaguisantes. Si está en "preparando" y ha pasado el tiempo de preparación, cambia a "normal".
        output:
            True si el disparo se ha completado, False en caso contrario.
        '''
        
        if self.estado == "preparando":
            if time.time() - self.inicio_preparacion >= self.tiempo_preparacion:
                self.estado = "normal"
                self.ultimo_disparo = time.time()
                return True
        return False

    def disparar(self, img_proyectil: pygame.Surface) -> 'Proyectiles':

        '''
        Crea un nuevo proyectil en la posición del lanzaguisantes.
        
        input:
            img_proyectil: imagen del proyectil que se va a disparar
        output:
            Un objeto Proyectiles que representa el proyectil disparado.
        '''
        
        return Proyectiles(self.x + 60, self.y, img_proyectil)

    def dibujar(self, ventana: pygame.Surface, offset_y: int = 0) -> None:
        
        '''
        Dibuja el lanzaguisantes en la ventana, dependiendo el estado, usa distintas imagenes.
        input:
            ventana: superficie donde se dibuja el lanzaguisantes
            offset_y: desplazamiento vertical para el dibujo del lanzaguisantes
        '''
        
        if self.estado == "preparando":
            ventana.blit(self.imagen_disparo, (self.x, self.y + offset_y))
        else:
            ventana.blit(self.imagen_normal, (self.x, self.y + offset_y))
        self.rect.topleft = (self.x, self.y + offset_y)  # actualizar rect
        
class LanzaguisantesTriple(Planta):
    
    '''
    Clase que representa un lanzaguisantes triple en el juego (Clase hija de Planta).
    '''
    
    def __init__(self, fila:int, columna:int, imagen:pygame.Surface, imagen_disparo:pygame.Surface) -> None:
        
        '''
        Inicializa un lanzaguisantes triple en una posición específica de la grilla.
        input:
            fila: fila en la que se va a iniciar el lanzaguisantes triple
            columna: columna en la que se va a iniciar el lanzaguisantes triple
            imagen: imagen del lanzaguisantes triple en estado normal
            imagen_disparo: imagen del proyectil cuando va a disparar
        '''
    
        super().__init__(fila, columna, imagen, vida=6)
        self.imagen_normal = imagen
        self.imagen_disparo = imagen_disparo
        self.estado = "normal"
        self.cooldown = 5
        self.ultimo_disparo = time.time() - self.cooldown
        self.proyectiles_restantes = 0
        self.tiempo_entre_proyectiles = 0.2
        self.ultimo_proyectil_disparado = 0

    def puede_disparar(self) -> bool:
        
        '''
        Devuelve True si el lanzaguisantes triple puede disparar, False en caso contrario.
        output:
            True si puede disparar, False en caso contrario.
        '''
        
        return (time.time() - self.ultimo_disparo >= self.cooldown) and self.estado == "normal"

    def preparar_disparo(self) -> None:
        
        '''
        Cambia el estado del lanzaguisantes triple a "disparando" y reinicia los contadores de proyectiles.
        '''
        
        self.estado = "disparando"
        self.proyectiles_restantes = 3
        self.ultimo_proyectil_disparado = time.time()

    def disparar(self, img_proyectil: pygame.Surface) -> list['Proyectiles']:
        
        '''
        Crea y devuelve una lista de proyectiles disparados por el lanzaguisantes triple.
        input:
            img_proyectil: imagen del proyectil que se va a disparar
        output:
            Una lista de objetos Proyectiles que representan los proyectiles disparados.
        '''

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

    def dibujar(self, ventana: pygame.Surface, offset_y:int=0) -> None:
        
        '''
        Dibuja la planta en la ventana de juego, utilizando diferentes imágenes según su estado actual.
        input:
            ventana: La superficie donde se dibuja la planta.
            offset_y: Desplazamiento vertical adicional para la posición de la planta. Por defecto es 0.
        '''
        
        if self.estado == "disparando":
            ventana.blit(self.imagen_disparo, (self.x, self.y + offset_y))
        else:
            ventana.blit(self.imagen_normal, (self.x, self.y + offset_y))
        self.rect.topleft = (self.x, self.y + offset_y)  # ← también acá

    def dejar_de_disparar(self) -> None:
        
        '''
        En caso de que no este disparando, vuelve a estado normal
        '''
        
        if self.estado != "disparando":
            self.estado = "normal"



class Nuez(Planta):
    # Clase Nuez, clase hija de Planta
    def __init__(self, fila: int, columna:int , imagen_sana:pygame.surface, imagen_mitad:pygame.surface, imagen_dañada:pygame.surface):
        
        '''
        '''
        
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


class Proyectiles:
    def __init__(self, x, y, imagen):
        self.x = x
        self.y = y + 15
        self.velocidad = 7
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
