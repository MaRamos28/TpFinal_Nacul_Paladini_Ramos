import pygame
import time
import random


class Soles:
    
    '''
    Clase que representa los soles en el juego.
    Cada sol puede ser del tipo "planta" o "cielo" para diferenciar su origen.
    
    '''

    def __init__(self, columna:int, fila:int, imagen:pygame.Surface, tipo:str, ancho:int, alto:int) -> None:
        
        '''
        Inicializa un sol en una posición específica de la cuadrícula.
        input:
            columna: columna en la que se va a iniciar el sol
            fila: fila en la que se va a iniciar el sol
            imagen: imagen del sol
            tipo: origen del sol ("planta" o "cielo")
            ancho: ancho del sol
            alto: alto del sol
        '''
        
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

    def dibujar(self, ventana: pygame.Surface, offset_y: int = 0) -> None:
        
        '''
        Dibuja el sol en la ventana.
        input:
            ventana: superficie donde se dibuja el sol
            offset_y: desplazamiento vertical para el dibujo del sol
        '''
        
        self.rect.topleft = (self.x, self.y + offset_y)
        if self.imagen:
            ventana.blit(self.imagen, self.rect)
        else:
            pygame.draw.rect(ventana, (255, 255, 0), self.rect)

    def planta_cielo(self) -> str:
        
        '''
        Devuelve el tipo de sol ("planta" o "cielo").
        '''
        
        return self.tipo

    def expiro(self, tiempo_actual: float, tiempo_limite: float = 10) -> bool:
        
        '''
        Verifica si el sol ha expirado.
        input:
            tiempo_actual: tiempo actual en segundos
            tiempo_limite: tiempo límite para la expiración en segundos
        output:
            True si el sol ha expirado, False en caso contrario.
        '''
        
        return tiempo_actual - self.tiempo_creacion > tiempo_limite

    def caida(self) -> None:
        
        '''
        Si el sol es del tipo "cielo", se mueve hacia abajo hasta alcanzar una altura random dentro de la grilla
        '''
        
        if self.tipo == "cielo":
            if self.y < self.altura_random:
                self.y += 0.8
            else:
                self.y = self.altura_random
            self.rect.y = self.y  # sin offset aquí, se suma al dibujar

    def agarrar_sol(self, x: int, y: int, offset_y: int = 0) -> bool:
        
        '''
        Verifica si el sol ha sido agarrado por el jugador.
        input:
            x: coordenada x del clic del jugador
            y: coordenada y del clic del jugador
            offset_y: desplazamiento vertical para el clic 
        
        output:
            True si el sol ha sido agarrado, False en caso contrario.
        '''
        
        rect_click = self.rect.copy()
        rect_click.y = self.y + offset_y
        return rect_click.collidepoint(x, y)

