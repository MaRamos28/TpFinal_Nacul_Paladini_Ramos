import pygame
from zombies import Zombie
from plantas import Girasol, Lanzaguisantes, Nuez, Proyectiles, LanzaguisantesTriple
from soles import Soles

import time
import random


def cargar_imagen(ruta: str, tamaño:tuple=(100, 100)) -> pygame.Surface:
    '''
    Función para cargar una imagen y redimensionarla a un tamaño específico.
    
    input: 
        ruta: str, ruta de la imagen a cargar
        tamaño: tuple, tamaño al que se redimensionará la imagen (ancho, alto)
    output:
        imagen: pygame.Surface, imagen cargada y redimensionada
    '''
    
    try: #En caso de que haya un error al cargar la imagen, se captura la excepción y se imprime un mensaje de error, evitando la detencion del programa.
        if not isinstance(ruta, str):
            print("La ruta debe ser una cadena de texto.")
            exit()
        if not ruta.endswith(('.png', '.jpg', '.jpeg', '.bmp')):
            print("La ruta debe terminar con una extensión de imagen válida (.png, .jpg, .jpeg, .bmp).")
            exit()
        if not isinstance(tamaño, tuple) or len(tamaño) != 2:
            print("El tamaño debe ser una tupla con dos elementos (ancho, alto).")
            exit()

        imagen = pygame.image.load(ruta)
        imagen = pygame.transform.scale(imagen, tamaño)
        return imagen
    except:
        print("Error al cargar imagen:", ruta)
        return None


def render_texto(texto:str, tamaño:int, color:tuple, ruta_fuente_pvz:str="Letra/ZOMBIE.TTF") -> pygame.Surface:
    '''
    Función para renderizar texto en la pantalla usando la fuente especificada.
    
    input:
        texto: str, texto a renderizar
        tamaño: int, tamaño de la fuente
        color: tuple, color del texto (R, G, B)
        ruta_fuente_pvz: str, ruta de la fuente a utilizar
    output:
        superficie: pygame.Surface, superficie con el texto renderizado
    '''
    
    fuente = pygame.font.Font(ruta_fuente_pvz, tamaño)
    return fuente.render(texto, True, color)


def colocar_planta(fila,columna,planta_seleccionada,grilla,lista_plantas,cant_filas,cant_columnas,img_girasol,img_lanzaguisante,img_lanzaguisante_dispara,img_nuez,img_nuezmitad,img_nuezdañada,img_tralladora,img_tralladora_dispara):
    if 0 <= fila < cant_filas + 1 and 0 <= columna < cant_columnas:
        if grilla[fila][columna] == 0:
            nueva_planta = None
            if planta_seleccionada == "girasol":
                nueva_planta = Girasol(fila, columna, img_girasol)
            elif planta_seleccionada == "lanzaguisante":
                nueva_planta = Lanzaguisantes(
                    fila, columna, img_lanzaguisante, img_lanzaguisante_dispara
                )
            elif planta_seleccionada == "nuez":
                nueva_planta = Nuez(
                    fila, columna, img_nuez, img_nuezmitad, img_nuezdañada
                )
            elif planta_seleccionada == "lanzaguisanteTriple":
                nueva_planta = LanzaguisantesTriple(fila, columna, img_tralladora, img_tralladora_dispara)

            if nueva_planta is not None:
                lista_plantas.append(nueva_planta)
                grilla[fila][columna] = nueva_planta
                print(f"{planta_seleccionada} colocada en fila {fila}, columna {columna}")
            else:
                print(f"Error: planta desconocida {planta_seleccionada}")



def generar_zombi(
    lista_zombis,
    zombis_disponibles,
    pesos,
    img_zombie_normal,
    img_zombie_cono,
    img_zombie_balde,
):
    tipo_zombi = random.choices(zombis_disponibles, weights=pesos)[0]

    if tipo_zombi == "normal":
        imagen = img_zombie_normal
    elif tipo_zombi == "cono":
        imagen = img_zombie_cono
    elif tipo_zombi == "balde":
        imagen = img_zombie_balde

    lista_zombis.append(Zombie(tipo_zombi, imagen))


def generar_proyectil(lista_proyectiles, img_proyectil, x, y):
    lista_proyectiles.append(Proyectiles(x, y, img_proyectil))


def generar_soles(lista_soles, imagen, columna, fila):
    nuevo_sol = Soles(columna, fila, imagen, "planta", 75, 75)
    lista_soles.append(nuevo_sol)
