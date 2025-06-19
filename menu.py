import pygame
import sys
import webbrowser

# Inicializamos Pygame
pygame.init()

# Dimensiones
ANCHO = 1152
ALTO = 768
ventana = pygame.display.set_mode((ANCHO, ALTO))

# Rectángulos de botones
rect_start = pygame.Rect(640, 115, 420, 100)
rect_tutorial = pygame.Rect(630, 280, 400, 100)
rect_exit = pygame.Rect(620, 412, 380, 95)

# pygame.image.load.()
menu = pygame.image.load("Imagenes/Menu_inicial.png").convert_alpha()


def mostrar_menu():
    while True:
        ventana.blit(menu, (0, 0))
        # pruebo dimensiones
        # pygame.draw.rect(ventana, (255, 0, 0), rect_start, 2)
        # pygame.draw.rect(ventana, (255, 0, 0), rect_tutorial, 2)
        # pygame.draw.rect(ventana, (255, 0, 0), rect_exit, 2)

        pygame.display.update()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if evento.type == pygame.MOUSEBUTTONDOWN:
                x, y = evento.pos
                if rect_start.collidepoint(x, y):
                    return  # Salimos del menú para arrancar el juego
                elif rect_tutorial.collidepoint(x, y):
                    webbrowser.open(
                        "https://www.youtube.com/"
                    )  # Poné acá tu link cuando tengas el video
                elif rect_exit.collidepoint(x, y):
                    pygame.quit()
                    sys.exit()
