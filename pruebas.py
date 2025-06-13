import pygame
import os

# Inicializar pygame
pygame.init()

# Tamaño ventana
ancho, alto = 800, 600
ventana = pygame.display.set_mode((ancho, alto))
pygame.display.set_caption("Prueba de Fuente PvZ")

# Colores
BLANCO = (255, 255, 255)
ROJO_SANGRE = (150, 0, 0)

# Ruta de la fuente
ruta_fuente_pvz = os.path.join("Letra", "ZOMBIE.TTF")

# Verificar que exista la fuente
if not os.path.exists(ruta_fuente_pvz):
    print("No se encontró la fuente en la ruta especificada.")
    pygame.quit()
    exit()

# Texto a mostrar
texto_principal = "OLEADA 3"

# FPS
clock = pygame.time.Clock()
FPS = 60

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    ventana.fill(BLANCO)

    # Cargar la fuente PvZ personalizada
    fuente = pygame.font.Font(ruta_fuente_pvz, 80)

    # Render texto en rojo sangre
    texto = fuente.render(texto_principal, True, ROJO_SANGRE)
    rect = texto.get_rect(center=(ancho//2, alto//2))
    ventana.blit(texto, rect)

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()