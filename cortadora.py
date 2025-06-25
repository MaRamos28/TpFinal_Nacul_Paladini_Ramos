import pygame
class cortadora():
    '''
    Clase que representa a la cortadora de césped en el juego.
    '''
    def __init__(self, fila:int, imagen:pygame.Surface):
        
        '''
        Inicializa la cortadora de césped en la fila dada con la imagen proporcionada.
        input:
            fila: fila en la que se encuentra la cortadora
            imagen: imagen de la cortadora
        '''
        
        self.fila = fila
        self.imagen = imagen
        self.y = fila * 100
        self.x = 0
        self.velocidad = 8
        self.activada = False
        self.imagen = pygame.transform.scale(imagen,(100,100))
        self.rect = pygame.Rect(self.x, self.y, 100, 100)
        self.ya_sono = False

    def activar(self) -> None:
        
        '''
        Activa la cortadora de césped, permitiendo que se mueva y pueda reproducir sonido.
        '''
        
        self.activada = True

    def esta_activada(self) -> bool:
        
        '''
        Devuelve True si la cortadora está activada, False en caso contrario.
        output:
            bool: estado de la cortadora
        '''

        return self.activada

    def movimiento(self) -> None:
        
        '''
        Mueve la cortadora hacia la derecha si está activada.
        Actualiza su posición en la pantalla.
        '''
        
        if self.activada:
            self.x = self.x + self.velocidad
            self.rect.x = self.x

    def dibujar(self, ventana: pygame.Surface, offset_y: int = 0) -> None:
        
        '''
        dibuja la cortadora en la ventana en su posición actual.
        input:
            ventana: superficie de pygame donde se dibuja la cortadora
            offset_y: desplazamiento vertical para el dibujo
        '''
        
        self.rect.topleft = (self.x, self.y + offset_y)
        if self.imagen:
            ventana.blit(self.imagen, self.rect)
        else:
            pygame.draw.rect(ventana, (100, 0, 0), self.rect)

    def puede_reproducir_sonido(self) -> bool:

        '''
        Devuelve True si la cortadora puede reproducir sonido, False en caso contrario.
        output:
            bool: True si la cortadora está activada y aún no ha sonado, False en caso contrario.
        '''
        
        if self.activada and not self.ya_sono:
            self.ya_sono = True
            return True
        return False
