import pygame
import sys
import webbrowser

# Inicializamos Pygame
pygame.init()

# Dimensiones
ANCHO = 1152
ALTO = 768
ventana = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Plantas vs Zombies - Menú de Inicio")

# Colores
VERDE_FONDO = (80, 200, 120)
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
GRIS = (200, 200, 200)
MARRON_MACETA = (160, 82, 45)

# Fuente
fuente_titulo = pygame.font.SysFont("comicsansms", 80)
fuente_boton = pygame.font.SysFont("comicsansms", 40)
fuente_macetas = pygame.font.SysFont("comicsansms", 30)

# Rectángulos de botones
rect_start = pygame.Rect(450, 300, 250, 70)
rect_tutorial = pygame.Rect(450, 400, 250, 70)
rect_exit = pygame.Rect(450, 500, 250, 70)

def mostrar_menu():
    while True:
        ventana.fill(VERDE_FONDO)

        # Título
        texto_titulo = fuente_titulo.render("Plantas vs Zombies", True, NEGRO)
        ventana.blit(texto_titulo, (ANCHO // 2 - texto_titulo.get_width() // 2, 100))

        # Botones
        pygame.draw.rect(ventana, GRIS, rect_start)
        pygame.draw.rect(ventana, GRIS, rect_tutorial)
        pygame.draw.rect(ventana, GRIS, rect_exit)

        ventana.blit(fuente_boton.render("Start", True, NEGRO), (rect_start.x + 70, rect_start.y + 15))
        ventana.blit(fuente_boton.render("Tutorial", True, NEGRO), (rect_tutorial.x + 45, rect_tutorial.y + 15))
        ventana.blit(fuente_boton.render("Exit", True, NEGRO), (rect_exit.x + 80, rect_exit.y + 15))

        # Macetas con nombres
        posiciones_macetas = [330, 530, 730]
        nombres = ["Nacul", "Paladini", "Ramos"]
        for i in range(3):
            pygame.draw.rect(ventana, MARRON_MACETA, (posiciones_macetas[i], 650, 80, 80))
            texto_nombre = fuente_macetas.render(nombres[i], True, BLANCO)
            ventana.blit(texto_nombre, (posiciones_macetas[i] + 10, 660))

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
                    webbrowser.open("https://www.youtube.com/")  # Poné acá tu link cuando tengas el video
                elif rect_exit.collidepoint(x, y):
                    pygame.quit()
                    sys.exit()
