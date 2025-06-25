import pygame
import time

class EfectoGolpe:
    
    '''
    Clase que representa un efecto visual de golpe en el juego.
    '''
    
    def __init__(self, x: int, y: int, imagen: pygame.Surface, duracion: float = 0.2):
        
        '''
        Inicializa un efecto de golpe en la posición (x, y) con la imagen dada.
        input:
            x: coordenada x donde se dibujará el efecto
            y: coordenada y donde se dibujará el efecto
            imagen: imagen del efecto de golpe
            duracion: duración del efecto en segundos (por defecto 0.2)
        '''
        
        if not isinstance(x, int) or not isinstance(y, int):
            raise TypeError("Las coordenadas deben ser enteros.")
        
        if not isinstance(imagen, pygame.Surface):
            raise TypeError("La imagen debe ser una instancia de pygame.Surface")
        
        self.x = x
        self.y = y
        self.imagen = imagen
        self.duracion = duracion
        self.tiempo_creacion = time.time()
        self.rect = self.imagen.get_rect(center=(x, y))

    def dibujar(self, ventana: pygame.Surface) -> None:
        
        '''
        Dibuja el efecto de golpe en la ventana.
        input:
            ventana: superficie de Pygame donde se dibujará el efecto
        '''
        
        ventana.blit(self.imagen, self.rect)

    def expiro(self) -> bool:
        
        '''
        Verifica si el efecto ha expirado.
        output:
            True si el efecto ha expirado, False en caso contrario.
        '''
        
        return time.time() - self.tiempo_creacion >= self.duracion
