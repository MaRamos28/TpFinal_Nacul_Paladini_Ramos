import pygame
import webbrowser
from funciones import *

# Inicializamos Pygame
pygame.init()
pygame.mixer.init()
# Dimensiones

ANCHO = 1100
ALTO = 690
ventana = pygame.display.set_mode((ANCHO, ALTO))
sonido_seleccionar = pygame.mixer.Sound("musica/efectos/sonido seleccionar menu.mp3")
sonido_menu = pygame.mixer.Sound("musica/menu.mp3")
sonido_menu.set_volume(0.25)
# Rectángulos de botones
rect_start = pygame.Rect(600, 115, 420, 100)
rect_tutorial = pygame.Rect(605, 250, 400, 100)
rect_exit = pygame.Rect(590, 380, 380, 100)

menu = cargar_imagen("Imagenes/pantallas/Menu_inicial.png", (ANCHO, ALTO))
menu_load = cargar_imagen("Imagenes/pantallas/menu load game.png", (ANCHO, ALTO))
menu_tutorial = cargar_imagen("Imagenes/pantallas/menu tutorial.png", (ANCHO, ALTO))
menu_exit = cargar_imagen("Imagenes/pantallas/menu exit.png", (ANCHO, ALTO))


def mostrar_menu():
    imagen_actual = menu
    toco = False
    sonido_menu.play(-1)
    while True:
        pygame.display.update()
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
            
            if evento.type == pygame.MOUSEMOTION:
                if rect_start.collidepoint(evento.pos):
                    imagen_actual = menu_load
                    if rect_start.collidepoint(evento.pos) and not toco:
                        imagen_actual = menu_load
                        sonido_seleccionar.play()
                        toco = True

                elif rect_exit.collidepoint(evento.pos):
                    imagen_actual = menu_exit
                    if rect_exit.collidepoint(evento.pos) and not toco:
                        imagen_actual = menu_exit
                        sonido_seleccionar.play()
                        toco = True
    
                elif rect_tutorial.collidepoint(evento.pos):
                    imagen_actual = menu_tutorial
                    if rect_tutorial.collidepoint(evento.pos) and not toco:
                        imagen_actual = menu_tutorial
                        sonido_seleccionar.play()
                        toco = True

                else:
                    imagen_actual = menu
                    toco = False
                pygame.display.update()

            if evento.type == pygame.MOUSEBUTTONDOWN:
                evento.pos  
                if rect_start.collidepoint(evento.pos):
                    sonido_menu.stop()
                    return 
                elif rect_tutorial.collidepoint(evento.pos):
                    webbrowser.open("https://www.youtube.com/watch?v=A4ebxSGXFyc")  
                elif rect_exit.collidepoint(evento.pos):
                    sonido_menu.stop()
                    pygame.quit()
        
        ventana.blit(imagen_actual, (0, 0))
        pygame.display.update()
        
if __name__ == "__main__":
    mostrar_menu() # Prueba individual