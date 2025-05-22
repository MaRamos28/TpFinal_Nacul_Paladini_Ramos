import pygame

cant_filas = 5
cant_columnas = 9
tamaño_celda = 100
ancho = cant_columnas * tamaño_celda
alto = cant_filas * tamaño_celda
FPS = 120

tamaño_ventana = (ancho, alto)

#Lista con los enemigos y plantas
lista_enemigos = []
lista_plantas = []

reloj = pygame.time.Clock()

ventana = pygame.display.set_mode(tamaño_ventana)
pygame.display.set_caption("Plantas vs Zombies")

color1 = (33, 150, 5)
color2 = (39, 223, 10)
borde = (0, 0, 0)

grilla = [[0 for _ in range(cant_columnas)] for _ in range(cant_filas)]

def dibujar_grilla():
    for fila in range(cant_filas):
        for columna in range(cant_columnas):
            # Alternar color por celda (estilo damero)
            color_celda = color1 if (fila + columna) % 2 == 0 else color2
            x = columna * tamaño_celda
            y = fila * tamaño_celda
            rect = pygame.Rect(x, y, tamaño_celda, tamaño_celda)
            pygame.draw.rect(ventana, color_celda, rect)
            pygame.draw.rect(ventana, borde, rect, 1)  # borde negro fino

def dibujar_objeto_en_celda(fila, columna, imagen):
    centro_x = columna * tamaño_celda + tamaño_celda // 2
    centro_y = fila * tamaño_celda + tamaño_celda // 2

    # Obtener rectángulo de la imagen y moverlo al centro de la celda
    rect = imagen.get_rect(center=(centro_x, centro_y))
    ventana.blit(imagen, rect)
    
def cargar_imagen(ruta, tamaño=(60, 60)):
    try:
        imagen = pygame.image.load(ruta).convert_alpha()
        imagen = pygame.transform.scale(imagen, tamaño)
        return imagen    
    except:
        print ("Hubo un error cargando la imagen")
        quit()
        
#carga de imagenes
img_girasol = cargar_imagen(r"Imagenes\girasol.png")
img_zombie_normal = cargar_imagen(r"Imagenes\zombie.png")
img_lanzaguisante = cargar_imagen(r"Imagenes\lanzaguisante.png")
img_zombie_cono = cargar_imagen(r"Imagenes\zombie_cono.png")
img_zombie_balde = cargar_imagen(r"Imagenes\zombie_balde.png") #Actualizar xq se ve mal
img_sol = cargar_imagen(r"Imagenes\sol.png")


jugando = True
while jugando:
    pygame.display.update()
    reloj.tick(FPS)
    dibujar_objeto_en_celda(0, 0, img_girasol)    
    dibujar_objeto_en_celda(0, 1, img_zombie_normal)
    dibujar_objeto_en_celda(0, 2, img_zombie_cono)
    dibujar_objeto_en_celda(0, 3, img_zombie_balde)
    dibujar_objeto_en_celda(0, 4, img_sol)
    dibujar_objeto_en_celda(0, 5, img_lanzaguisante)    
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            jugando = False
            print("Juego cerrado")
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            fila = y
            columna = x
            print(x, y)
        dibujar_grilla()
