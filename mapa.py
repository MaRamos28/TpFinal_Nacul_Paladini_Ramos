import pygame
from zombies import Zombie
from plantas import Girasol, Lanzaguisantes, Nuez

# Tamaño de la grilla
cant_filas = 5
cant_columnas = 9
tamaño_celda = 100
ancho = cant_columnas * tamaño_celda
alto = cant_filas * tamaño_celda
tamaño_ventana = (ancho, alto + 200)

FPS = 120
reloj = pygame.time.Clock()

ventana = pygame.display.set_mode(tamaño_ventana)
pygame.display.set_caption("Plantas vs Zombies")

# Colores
color1 = (33, 150, 5)
color2 = (39, 223, 10)
color_background = (10 , 223 , 175)
borde = (0, 0, 0)

# Grilla lógica
grilla = [[0 for _ in range(cant_columnas)] for _ in range(cant_filas)]

# Cargar imágenes
def cargar_imagen(ruta, tamaño=(100, 100)):
    try:
        imagen = pygame.image.load(ruta)
        imagen = pygame.transform.scale(imagen, tamaño)
        return imagen    
    except:
        print("Error al cargar imagen:", ruta)
        return None

img_girasol = cargar_imagen("Imagenes/girasol.png")
img_zombie_normal = cargar_imagen("Imagenes/zombie.png")
img_zombie_cono = cargar_imagen("Imagenes/zombie_cono.png")
img_zombie_balde = cargar_imagen("Imagenes/zombie_balde.png")
img_lanzaguisante = cargar_imagen("Imagenes/lanzaguisante.png")
img_nuez = cargar_imagen("Imagenes/nuez.png")

# Listas de objetos
lista_zombis = []
lista_plantas = []

# Grilla visual
def dibujar_grilla():
    for fila in range(cant_filas):
        for columna in range(cant_columnas):
            color = color1 if (fila + columna) % 2 == 0 else color2
            x = columna * tamaño_celda
            y = fila * tamaño_celda
            rect = pygame.Rect(x, y, tamaño_celda, tamaño_celda)
            pygame.draw.rect(ventana, color, rect)
            pygame.draw.rect(ventana, borde, rect, 1)

# Bucle principal
jugando = True
clock = pygame.time.Clock()

# Plantar algo de prueba
lista_plantas.append(Girasol(0, 0, img_girasol))
lista_plantas.append(Lanzaguisantes(1, 0, img_lanzaguisante))
lista_plantas.append(Nuez(2, 0, img_nuez))

# Spawn de zombis de ejemplo
lista_zombis.append(Zombie(900, tipo="normal", imagen=img_zombie_normal))
lista_zombis.append(Zombie(900, tipo="cono", imagen=img_zombie_cono))
lista_zombis.append(Zombie(900, tipo="balde", imagen=img_zombie_balde))

while jugando:
    reloj.tick(FPS)
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            jugando = False
        if evento.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            fila = y // tamaño_celda
            columna = x // tamaño_celda
            print(f"Click en celda: fila {fila}, columna {columna}")

    ventana.fill(color_background)
    dibujar_grilla()

    for planta in lista_plantas:
        planta.dibujar(ventana)

    for z in lista_zombis:
        z.mover()
        z.dibujar(ventana)

    pygame.display.update()
    clock.tick(30)

pygame.quit()
