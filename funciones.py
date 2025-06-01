import pygame
from zombies import Zombie
from plantas import Girasol, Lanzaguisantes, Nuez, Proyectiles
import time
import random


def cargar_imagen(ruta, tamaño=(100, 100)):
    try:
        imagen = pygame.image.load(ruta)
        imagen = pygame.transform.scale(imagen, tamaño)
        return imagen
    except:
        print("Error al cargar imagen:", ruta)
        return None


def dibujar_grilla(
    cant_filas, cant_columnas, tamaño_celda, color1, color2, borde, ventana
):
    for fila in range(cant_filas):
        for columna in range(cant_columnas):
            color = color1 if (fila + columna) % 2 == 0 else color2
            x = columna * tamaño_celda
            y = fila * tamaño_celda
            rect = pygame.Rect(x, y, tamaño_celda, tamaño_celda)
            pygame.draw.rect(ventana, color, rect)
            pygame.draw.rect(ventana, borde, rect, 1)


def colocar_planta(
    fila,
    columna,
    planta_seleccionada,
    grilla,
    lista_plantas,
    cant_filas,
    cant_columnas,
    img_girasol,
    img_lanzaguisante,
    img_nuez,
):
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


def generar_zombi(
    lista_zombis,
    zombis_disponibles,
    img_zombie_normal,
    img_zombie_cono,
    img_zombie_balde,
):
    tipo_zombi = random.choice(zombis_disponibles)

    if tipo_zombi == "normal":
        imagen = img_zombie_normal
    elif tipo_zombi == "cono":
        imagen = img_zombie_cono
    elif tipo_zombi == "balde":
        imagen = img_zombie_balde

    lista_zombis.append(Zombie(tipo_zombi, imagen))


def generar_proyectil(lista_proyectiles, img_proyectil, x, y):
    lista_proyectiles.append(Proyectiles(x, y, img_proyectil))

