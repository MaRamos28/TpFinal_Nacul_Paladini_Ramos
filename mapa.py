import pygame
from zombies import Zombie
from plantas import Girasol, Lanzaguisantes, Nuez
import time
import random

pygame.init()

cant_filas = 5
cant_columnas = 9
tamaño_celda = 100
ancho = cant_columnas * tamaño_celda
alto = cant_filas * tamaño_celda
barra_inferior_tamaño = 200
separacion_barra_grilla = 10
barra_inferior_inicio = alto + separacion_barra_grilla

tiempo_entre_zombis = 5 #Segundos
tiempo_ulitmo_zombi = 0


tamaño_ventana = (ancho, alto + barra_inferior_tamaño + separacion_barra_grilla)

ventana = pygame.display.set_mode(tamaño_ventana)
pygame.display.set_caption("Plantas vs Zombies")

FPS = 120
reloj = pygame.time.Clock()

color1 = (33, 150, 5)
color2 = (39, 223, 10)
color_background = (10, 223, 175)
borde = (0, 0, 0)

grilla = [[0 for _ in range(cant_columnas)] for _ in range(cant_filas)]
lista_zombis = []
lista_plantas = []
planta_seleccionada = "girasol"  # Valor por defecto


def cargar_imagen(ruta, tamaño=(100, 100)):
    try:
        imagen = pygame.image.load(ruta)
        imagen = pygame.transform.scale(imagen, tamaño)
        return imagen    
    except:
        print("Error al cargar imagen:", ruta)
        return None

def dibujar_grilla():
    for fila in range(cant_filas):
        for columna in range(cant_columnas):
            color = color1 if (fila + columna) % 2 == 0 else color2
            x = columna * tamaño_celda
            y = fila * tamaño_celda
            rect = pygame.Rect(x, y, tamaño_celda, tamaño_celda)
            pygame.draw.rect(ventana, color, rect)
            pygame.draw.rect(ventana, borde, rect, 1)

def colocar_planta(fila, columna, planta_seleccionada):
    if 0 <= fila < cant_filas and 0 <= columna < cant_columnas:
        if grilla[fila][columna] == 0:
            if planta_seleccionada == "girasol":
                nueva_planta = Girasol(fila, columna, img_girasol)
            elif planta_seleccionada == "lanzaguisante":
                nueva_planta = Lanzaguisantes(fila, columna, img_lanzaguisante)
            elif planta_seleccionada == "nuez":
                nueva_planta = Nuez(fila, columna, img_nuez)

            lista_plantas.append(nueva_planta)
            grilla[fila][columna] = nueva_planta
            print(f"{planta_seleccionada} colocada en fila {fila}, columna {columna}")

img_girasol = cargar_imagen("Imagenes/girasol.png")
img_zombie_normal = cargar_imagen("Imagenes/zombie.png")
img_zombie_cono = cargar_imagen("Imagenes/zombie_cono.png")
img_zombie_balde = cargar_imagen("Imagenes/zombie_balde.png")
img_lanzaguisante = cargar_imagen("Imagenes/lanzaguisante.png")
img_nuez = cargar_imagen("Imagenes/nuez.png")

plantas_disponibles = [
    ("girasol", img_girasol, pygame.Rect(50, barra_inferior_inicio + 50, 60, 60)),
    ("lanzaguisante", img_lanzaguisante, pygame.Rect(150, barra_inferior_inicio + 50, 60, 60)),
    ("nuez", img_nuez, pygame.Rect(250, barra_inferior_inicio + 50, 60, 60))
]

zombis_disponibles = ("normal", "cono", "balde")

jugando = True

while jugando:
    reloj.tick(FPS)
    
    #Genero zombis cada 1 segundo    
    tiempo_actual = time.time()
    
    if tiempo_actual - tiempo_ulitmo_zombi >= tiempo_entre_zombis:
        tiempo_ulitmo_zombi = tiempo_actual
        
        tipo_zombi = random.choice(zombis_disponibles)
        
        if tipo_zombi == "normal":
            imagen = img_zombie_normal
        elif tipo_zombi == "cono":
            imagen = img_zombie_cono
        elif tipo_zombi == "balde":
            imagen = img_zombie_balde
            
        lista_zombis.append(Zombie(tipo_zombi, imagen))
        
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            jugando = False

        if evento.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()

            # Si clickeás en la barra de selección
            if y > barra_inferior_inicio:
                for nombre, imagen, rect in plantas_disponibles:
                    if rect.collidepoint(x, y):
                        planta_seleccionada = nombre
                        print(f"Planta seleccionada: {planta_seleccionada}")
            else:
                fila = y // tamaño_celda
                columna = x // tamaño_celda
                colocar_planta(fila, columna, planta_seleccionada)

    ventana.fill(color_background)
    dibujar_grilla()

    # Dibujar plantas
    for planta in lista_plantas:
        planta.dibujar(ventana)

    # Dibujar zombis
    for zombi in lista_zombis:
        zombi.mover()
        zombi.dibujar(ventana)

    for nombre, imagen, rect in plantas_disponibles:
        imagen_rect = imagen.get_rect(center=rect.center)
        ventana.blit(imagen, imagen_rect)
        
        color_borde = (255, 0, 0) if nombre == planta_seleccionada else (0, 0, 0)
        pygame.draw.rect(ventana, color_borde, rect, 2)


    pygame.display.update()

pygame.quit()
