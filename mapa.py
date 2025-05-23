from funciones import *

lista_zombis = []
lista_plantas = []

cant_filas = 5
cant_columnas = 9
tamaño_celda = 100
ancho = cant_columnas * tamaño_celda
alto = cant_filas * tamaño_celda
barra_inferior_tamaño = 200
separacion_barra_grilla = 10
barra_inferior_inicio = alto + separacion_barra_grilla
tiempo_entre_zombis = 5 #Segundos
tiempo_ultimo_zombi = 0

tamaño_ventana = (ancho, alto + barra_inferior_tamaño + separacion_barra_grilla)

color1 = (33, 150, 5)
color2 = (39, 223, 10)
color_background = (10, 223, 175)
borde = (0, 0, 0)

ventana = pygame.display.set_mode(tamaño_ventana)
pygame.display.set_caption("Plantas vs Zombies")

FPS = 120
reloj = pygame.time.Clock()

grilla = [[0 for _ in range(cant_columnas)] for _ in range(cant_filas)]
planta_seleccionada = "girasol"  #por defecto

img_girasol = cargar_imagen("Imagenes/girasol.png")
img_zombie_normal = cargar_imagen("Imagenes/zombie.png")
img_zombie_cono = cargar_imagen("Imagenes/zombie_cono.png")
img_zombie_balde = cargar_imagen("Imagenes/zombie_balde.png")
img_lanzaguisante = cargar_imagen("Imagenes/lanzaguisante.png")
img_nuez = cargar_imagen("Imagenes/nuez.png")

plantas_disponibles = [
    ("girasol", img_girasol, pygame.Rect(50, barra_inferior_inicio + 50, 100, 100)),
    ("lanzaguisante", img_lanzaguisante, pygame.Rect(200, barra_inferior_inicio + 50, 100, 100)),
    ("nuez", img_nuez, pygame.Rect(350, barra_inferior_inicio + 50, 100, 100))
]

zombis_disponibles = ("normal", "cono", "balde")

jugando = True

while jugando:
    reloj.tick(FPS)
    tiempo_actual = time.time()
    if tiempo_actual - tiempo_ultimo_zombi >= tiempo_entre_zombis:
        tiempo_ultimo_zombi = tiempo_actual
        generar_zombi(lista_zombis, zombis_disponibles, img_zombie_normal, img_zombie_cono, img_zombie_balde)
    
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
                colocar_planta(fila, columna, planta_seleccionada, grilla, lista_plantas, cant_filas, cant_columnas, img_girasol, img_lanzaguisante, img_nuez)

    ventana.fill(color_background)
    dibujar_grilla(cant_filas, cant_columnas, tamaño_celda, color1, color2, borde, ventana)

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
