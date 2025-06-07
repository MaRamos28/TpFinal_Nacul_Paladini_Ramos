from funciones import *
from plantas import *

lista_zombis = []
lista_plantas = []
lista_proyectiles = []
lista_soles = []

cant_filas = 5
cant_columnas = 9
tamaño_celda = 100
ancho = cant_columnas * tamaño_celda
alto = cant_filas * tamaño_celda
barra_inferior_tamaño = 180
separacion_barra_grilla = 10
x = 0
y = 0

# NUEVO: barra arriba, offset para la grilla
barra_inferior_inicio = 0
offset_y_grilla = barra_inferior_tamaño + separacion_barra_grilla

tiempo_entre_zombis = 5  # Segundos
tiempo_ultimo_zombi = 0
cant_soles = 50
pygame.init()
pygame.mixer.init()

tamaño_ventana = (ancho, alto + barra_inferior_tamaño + separacion_barra_grilla)

color1 = (33, 150, 5)
color2 = (39, 223, 10)
color_background = (10, 223, 175)
borde = (0, 0, 0)

ventana = pygame.display.set_mode(tamaño_ventana)
pygame.display.set_caption("Plantas vs Zombies")

FPS = 60
reloj = pygame.time.Clock()

grilla = [[0 for _ in range(cant_columnas)] for _ in range(cant_filas)]
planta_seleccionada = "girasol"

# Cargar imágenes
img_girasol = cargar_imagen("Imagenes/girasol.png")
img_zombie_normal = cargar_imagen("Imagenes/zombie.png")
img_zombie_cono = cargar_imagen("Imagenes/zombie_cono.png")
img_zombie_balde = cargar_imagen("Imagenes/zombie_balde.png")
img_lanzaguisante = cargar_imagen("Imagenes/lanzaguisante.png")
img_nuez = cargar_imagen("Imagenes/nuez.png")
img_proyectil = cargar_imagen("Imagenes/Proyectil.png")
img_sol = cargar_imagen("Imagenes/sol.png")
img_pala = cargar_imagen("Imagenes/pala.png")

plantas_disponibles = [
    ("girasol", img_girasol, pygame.Rect(50, barra_inferior_inicio + 50, 100, 100)),
    ("lanzaguisante", img_lanzaguisante, pygame.Rect(200, barra_inferior_inicio + 50, 100, 100)),
    ("nuez", img_nuez, pygame.Rect(350, barra_inferior_inicio + 50, 100, 100)),
    ("pala", img_pala, pygame.Rect(500, barra_inferior_inicio + 50, 100, 100)),
]

zombis_disponibles = ("normal", "cono", "balde")

# Sonidos
sonido_principal = pygame.mixer.Sound("musica/musica.mp3")
sonido_principal.set_volume(0.4)
sonido_principal.play()
sonido_mordida = pygame.mixer.Sound("musica/efectos/mordida.mp3")
sonido_plantar = pygame.mixer.Sound("musica/efectos/plantar.mp3")
sonido_golpe = pygame.mixer.Sound("musica/efectos/golpe.mp3")
sonido_zombi_inicio = pygame.mixer.Sound("musica/efectos/zombies_are_coming.mp3")
sonido_zombi_inicio.play()
sonido_seleccionar = pygame.mixer.Sound("musica/efectos/seleccionar.mp3")

jugando = True
tiempo_ultimo_sol = 0
intervalo_sol = 5

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
            sol_agarrado = False  # NUEVO: inicializo bandera

            for sol in lista_soles[:]:
                if sol.agarrar_sol(x, y, offset_y_grilla):
                    lista_soles.remove(sol)
                    cant_soles += 25

                    # AVISAR AL GIRASOL QUE SU SOL FUE AGARRADO
                    for planta in lista_plantas:
                        if isinstance(planta, Girasol) and planta.sol_activo == sol:
                            planta.tiempo_ultimo_sol = time.time()
                            planta.sol_activo = None
                            break

                    sol_agarrado = True
                    break

            if not sol_agarrado:
                if y < barra_inferior_tamaño:
                    for nombre, imagen, rect in plantas_disponibles:
                        if rect.collidepoint(x, y):
                            planta_seleccionada = nombre
                            print(f"Planta seleccionada: {planta_seleccionada}")
                            sonido_seleccionar.play()
                elif y >= offset_y_grilla:
                    fila = (y - offset_y_grilla) // tamaño_celda
                    columna = x // tamaño_celda
                    colocar_planta(fila, columna, planta_seleccionada, grilla, lista_plantas,
                                cant_filas, cant_columnas, img_girasol, img_lanzaguisante, img_nuez)
                    sonido_plantar.play()



    ventana.fill(color_background)

    dibujar_grilla(cant_filas, cant_columnas, tamaño_celda, color1, color2, borde, ventana, offset_y_grilla)

    for planta in lista_plantas:
        for zombi in lista_zombis:
            planta.dibujar(ventana, offset_y_grilla)
            if planta.devolver_coords()[1] == zombi.devolver_coords()[1]:
                if isinstance(planta, Lanzaguisantes):
                    if planta.puede_disparar():
                        proyectil = planta.disparar(img_proyectil)
                        lista_proyectiles.append(proyectil)

    for guisante in lista_proyectiles:
        guisante.mover()
        guisante.dibujar(ventana, offset_y_grilla)
        if guisante.x > ancho:
            lista_proyectiles.remove(guisante)
            continue
        for zombi in lista_zombis:
            if guisante.rect.colliderect(zombi.rect):
                murio = zombi.recibedaño()
                sonido_golpe.play()
                if murio:
                    lista_zombis.remove(zombi)
                if guisante in lista_proyectiles:
                    lista_proyectiles.remove(guisante)

    for zombi in lista_zombis:
        choco = False
        for planta in lista_plantas:
            if zombi.rect.colliderect(planta.rect):
                choco = True
                if zombi.ataque():
                    murio = planta.recibedaño()
                    sonido_mordida.play()
                    if murio:
                        lista_plantas.remove(planta)
                break
        if not choco:
            zombi.mover()
        zombi.dibujar(ventana, offset_y_grilla)

    for nombre, imagen, rect in plantas_disponibles:
        imagen_rect = imagen.get_rect(center=rect.center)
        ventana.blit(imagen, imagen_rect)
        color_borde = (255, 0, 0) if nombre == planta_seleccionada else (0, 0, 0)
        pygame.draw.rect(ventana, color_borde, rect, 2)

    if tiempo_actual - tiempo_ultimo_sol >= intervalo_sol:
        tiempo_ultimo_sol = tiempo_actual
        nueva_columna = random.randint(0, 9)
        lista_soles.append(Soles(nueva_columna, 0, img_sol, "cielo", 75, 75))

    for sol in lista_soles:
        sol.dibujar(ventana, offset_y_grilla)
        if sol.tipo == "cielo":
            sol.caida()

    # Eliminar soles que ya expiraron
    for sol in lista_soles[:]:
        if sol.expiro(tiempo_actual):
            lista_soles.remove(sol)

            # Si era de un girasol, avisarle que se expiró su sol
            for planta in lista_plantas:
                if isinstance(planta, Girasol) and planta.sol_activo == sol:
                    planta.tiempo_ultimo_sol = time.time()
                    planta.sol_activo = None
                    break


    img_sol_50 = pygame.transform.scale(img_sol, (50, 50))
    fuente = pygame.font.SysFont("Arial", 30)
    texto_sol = fuente.render(f"Soles: {cant_soles}", True, (255, 255, 0))
    ventana.blit(texto_sol, (10, 10))

    for girasol in lista_plantas:
        if isinstance(girasol, Girasol):
            if girasol.puede_generar():
                nuevo_sol = Soles(girasol.columna, girasol.fila, img_sol, "planta", 75, 75)
                lista_soles.append(nuevo_sol)
                girasol.sol_activo = nuevo_sol  



    ventana.blit(img_sol_50, (35, barra_inferior_inicio + 142))
    texto_valor_GP = fuente.render(f"50", True, (255, 255, 0))
    ventana.blit(texto_valor_GP, (90, barra_inferior_inicio + 149))

    ventana.blit(img_sol_50, (165, barra_inferior_inicio + 142))
    texto_valor_L = fuente.render(f"100", True, (255, 255, 0))
    ventana.blit(texto_valor_L, (210, barra_inferior_inicio + 149))

    ventana.blit(img_sol_50, (315, barra_inferior_inicio + 142, 50, 50))
    ventana.blit(texto_valor_GP, (365, barra_inferior_inicio + 149))

    pygame.display.update()

pygame.quit()
