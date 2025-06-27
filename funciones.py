import pygame
from zombies import Zombie
from plantas import Girasol, Lanzaguisantes, Nuez, Proyectiles, LanzaguisantesTriple
from soles import Soles
import random


def cargar_imagen(ruta: str, tamaño: tuple = (100, 100)) -> pygame.Surface:
    """
    Función para cargar una imagen y redimensionarla a un tamaño específico.

    input:
        ruta: str, ruta de la imagen a cargar
        tamaño: tuple, tamaño al que se redimensionará la imagen (ancho, alto)
    output:
        imagen: pygame.Surface, imagen cargada y redimensionada
    """

    try:  # En caso de que haya un error al cargar la imagen, se captura la excepción y se imprime un mensaje de error, evitando la detencion del programa.
        if not isinstance(ruta, str):
            print("La ruta debe ser una cadena de texto.")
            exit()
        if not ruta.endswith((".png", ".jpg", ".jpeg", ".bmp")):
            print(
                "La ruta debe terminar con una extensión de imagen válida (.png, .jpg, .jpeg, .bmp)."
            )
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


def render_texto(
    texto: str, tamaño: int, color: tuple, ruta_fuente_pvz: str = "Letra/ZOMBIE.TTF"
) -> pygame.Surface:
    """
    Función para renderizar texto en la pantalla usando la fuente especificada.

    input:
        texto: str, texto a renderizar
        tamaño: int, tamaño de la fuente
        color: tuple, color del texto (R, G, B)
        ruta_fuente_pvz: str, ruta de la fuente a utilizar
    output:
        superficie: pygame.Surface, superficie con el texto renderizado
    """

    try:
        if not isinstance(
            texto, str
        ):  # Se verifica que la variable "texto" sea una cadena de texto.
            print("El texto debe ser una cadena de texto.")
            exit()

        fuente = pygame.font.Font(ruta_fuente_pvz, tamaño)
        return fuente.render(texto, True, color)
    except:
        print("Error al cargar la fuente:", ruta_fuente_pvz)
        return None


def colocar_planta(
    fila: int,
    columna: int,
    planta_seleccionada: str,
    grilla: list,
    lista_plantas: list,
    cant_filas: int,
    cant_columnas: int,
    img_girasol: pygame.Surface,
    img_lanzaguisante: pygame.Surface,
    img_lanzaguisante_dispara: pygame.Surface,
    img_nuez: pygame.Surface,
    img_nuezmitad: pygame.Surface,
    img_nuezdañada: pygame.Surface,
    img_tralladora: pygame.Surface,
    img_tralladora_dispara: pygame.Surface,
) -> None:
    """
    Función para colocar una planta en la grilla del juego.

    input:
        fila: fila donde se desea colocar la planta
        columna: columna donde se desea colocar la planta
        planta_seleccionada: tipo de planta a colocar (girasol, lanzaguisante, nuez, lanzaguisanteTriple)
        grilla: grilla del juego donde se colocarán las plantas
        lista_plantas: lista que contiene las plantas colocadas
        cant_filas: cantidad de filas en la grilla
        cant_columnas: cantidad de columnas en la grilla
        img_girasol: imagen del girasol
        img_lanzaguisante: imagen del lanzaguisante
        img_lanzaguisante_dispara: imagen del lanzaguisante al disparar
        img_nuez: imagen de la nuez
        img_nuezmitad: imagen de la nuez a medio daño
        img_nuezdañada: imagen de la nuez dañada
        img_tralladora: imagen del lanzaguisante triple
        img_tralladora_dispara: imagen del lanzaguisante triple al disparar
    output:
        None
    """

    if (
        0 <= fila < cant_filas + 1 and 0 <= columna < cant_columnas
    ):  # Verifica que la fila y columna estén dentro de los límites de la grilla
        if grilla[fila][columna] == 0:  # Si no hay planta en esa posición
            nueva_planta = None  # Bandera para saber si se ha creado una planta nueva
            if planta_seleccionada == "girasol":
                nueva_planta = Girasol(
                    fila, columna, img_girasol
                )  # En caso de que la planta seleccionada sea un girasol, se crea un objeto de la clase Girasol
            elif planta_seleccionada == "lanzaguisante":
                nueva_planta = Lanzaguisantes(
                    fila, columna, img_lanzaguisante, img_lanzaguisante_dispara
                )  # En caso de que la planta seleccionada sea un lanzaguisante, se crea un objeto de la clase Lanzaguisantes
            elif planta_seleccionada == "nuez":
                nueva_planta = Nuez(
                    fila, columna, img_nuez, img_nuezmitad, img_nuezdañada
                )  # En caso de que la planta seleccionada sea una nuez, se crea un objeto de la clase Nuez
            elif planta_seleccionada == "lanzaguisanteTriple":
                nueva_planta = LanzaguisantesTriple(
                    fila, columna, img_tralladora, img_tralladora_dispara
                )  # En caso de que la planta seleccionada sea un lanzaguisante triple, se crea un objeto de la clase LanzaguisantesTriple

            if (
                nueva_planta is not None
            ):  # Si se ha creado una planta nueva, se procede a agregarla a la lista de plantas y a la grilla
                lista_plantas.append(nueva_planta)
                grilla[fila][columna] = nueva_planta
                print(
                    f"{planta_seleccionada} colocada en fila {fila}, columna {columna}"
                )
            else:
                print(f"Error: planta desconocida {planta_seleccionada}")


def generar_zombi(
    lista_zombis: list,
    zombis_disponibles: list,
    pesos: list,
    img_zombie_normal: pygame.Surface,
    img_zombie_cono: pygame.Surface,
    img_zombie_balde: pygame.Surface,
) -> None:
    """
    Genera un zombi segun los distintos pesos asigandos y lo agrega a la lista de zombis.

    input:
        lista_zombis: lista donde se agregará el zombi generado
        zombis_disponibles: lista de tipos de zombis disponibles
        pesos: lista de pesos para cada tipo de zombi
        img_zombie_normal: imagen del zombi normal
        img_zombie_cono: imagen del zombi con cono
        img_zombie_balde: imagen del zombi con balde

    output:
        None
    """
    tipo_zombi = random.choices(zombis_disponibles, weights=pesos)[0]

    if tipo_zombi == "normal":
        imagen = img_zombie_normal  # Si el tipo de zombi es normal, se asigna la imagen y el tipo del zombi normal
    elif tipo_zombi == "cono":
        imagen = img_zombie_cono  # Si el tipo de zombi es cono, se asigna la imagen y el tipo del zombi con cono
    elif tipo_zombi == "balde":
        imagen = img_zombie_balde  # Si el tipo de zombi es balde, se asigna la imagen y el tipo del zombi con balde

    lista_zombis.append(
        Zombie(tipo_zombi, imagen)
    )  # Se crea un nuevo objeto Zombie con el tipo y la imagen seleccionada y se agrega a la lista de zombis


def generar_proyectil(
    lista_proyectiles: list, img_proyectil: pygame.Surface, x: int, y: int
) -> None:
    """
    Genera un proyectil y lo agrega a la lista de proyectiles.
    input:
        lista_proyectiles: lista donde se agregará el proyectil generado
        img_proyectil: imagen del proyectil
        x: coordenada x donde se generará el proyectil
        y: coordenada y donde se generará el proyectil
    output:
        None
    """

    lista_proyectiles.append(
        Proyectiles(x, y, img_proyectil)
    )  # Crea un nuevo proyectil y lo agrega a la lista de proyectiles


def generar_soles(
    lista_soles: list, imagen: pygame.Surface, columna: int, fila: int
) -> None:
    """
    Genera un sol y lo agrega a la lista de soles.
    input:
        lista_soles: lista donde se agregará el sol generado
        imagen: imagen del sol
        columna: columna donde se generará el sol
        fila: fila donde se generará el sol
    output:
        None
    """
    nuevo_sol = Soles(
        columna, fila, imagen, "planta", 75, 75
    )  # Crea un nuevo sol con la imagen, columna y fila especificadas
    lista_soles.append(nuevo_sol)  # Agrega el nuevo sol a la lista de soles
