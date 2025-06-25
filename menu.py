import pygame
import sys
import webbrowser
from funciones import *

# Inicializamos Pygame
pygame.init()
pygame.mixer.init()
# Dimensiones

ANCHO = 1152
ALTO = 768
ventana = pygame.display.set_mode((ANCHO, ALTO))
sonido_seleccionar = pygame.mixer.Sound("musica/efectos/sonido seleccionar menu.mp3")
sonido_menu = pygame.mixer.Sound("musica/menu.mp3")
sonido_menu.set_volume(0.25)
# Rectángulos de botones
rect_start = pygame.Rect(640, 115, 420, 100)
rect_tutorial = pygame.Rect(630, 260, 400, 120)
rect_exit = pygame.Rect(620, 402, 380, 120)

menu = cargar_imagen("Imagenes/pantallas/Menu_inicial.png", (1152, 768))
menu_load = cargar_imagen("Imagenes/pantallas/menu load game.png", (1152, 768))
menu_tutorial = cargar_imagen("Imagenes/pantallas/menu tutorial.png", (1152, 768))
menu_exit = cargar_imagen("Imagenes/pantallas/menu exit.png", (1152, 768))


def mostrar_menu():
    imagen_actual = menu
    toco = False
    sonido_menu.play(-1)
    while True:
        pygame.display.update()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
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
                x, y = evento.pos
                if rect_start.collidepoint(x, y):
                    sonido_menu.stop()
                    return 
                elif rect_tutorial.collidepoint(x, y):
                    webbrowser.open(
                        "https://www.youtube.com/"
                    )  
                elif rect_exit.collidepoint(x, y):
                    sonido_menu.stop()
                    pygame.quit()
                    sys.exit()
        ventana.blit(imagen_actual, (0, 0))
        pygame.display.update()