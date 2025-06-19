from funciones import *
from plantas import *
from cortadora import *
from menu import *

mostrar_menu()

lista_zombis = []
lista_plantas = []
lista_proyectiles = []
lista_soles = []
lista_cortadoras = []

cant_filas = 5
cant_columnas = 10
tamaño_celda = 100
margen_cortadora = 100
margen_derecho = 200
ancho = margen_cortadora + (cant_columnas * tamaño_celda)
alto = cant_filas * tamaño_celda
barra_superior_tamaño = 180
separacion_barra_grilla = 10
x = 0
y = 0
vidas = 5
tiempo_invulnerabilidad = 2000
es_vulnerable = False

pala_activa = False

oleada_actual = 1  # arranca en 1, para que la primera vez entre
mostrar_oleada = False
tiempo_mostrar_oleada = 0
duracion_cartel = 3000  # en milisegundos (3 segundos)

pausar_generacion_zombis = True
tiempo_reinicio = pygame.time.get_ticks()  # arranca pausado
tiempo_pausa = 4000  # 4 segundos

barra_inferior_inicio = 0
offset_y_grilla = barra_superior_tamaño + separacion_barra_grilla
tiempo_entre_zombis = 10  # Segundos
tiempo_ultimo_zombi = 0
cant_soles = 50000
pygame.init()
pygame.mixer.init()
puntuacion = 0

tamaño_ventana = (ancho, alto + barra_superior_tamaño + separacion_barra_grilla)

color1 = (33, 150, 5)
color2 = (39, 223, 10)
color_background = (10, 223, 175)
borde = (0, 0, 0)

NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
AMARILLO = (255, 255, 0)


ventana = pygame.display.set_mode(tamaño_ventana)
pygame.display.set_caption("Plantas vs Zombies")

FPS = 60
reloj = pygame.time.Clock()

grilla = [[0 for _ in range(cant_columnas)] for _ in range(cant_filas)]
planta_seleccionada = "girasol"

# Cargar imágenes
img_girasol = cargar_imagen("Imagenes/girasol.png")
img_zombie_normal = cargar_imagen("Imagenes/zombie.png")
img_zombie_sin_brazo = cargar_imagen("Imagenes/zombie_sin_brazo.png")
img_zombie_cono = cargar_imagen("Imagenes/zombie_cono.png")
img_zombie_cono_dañado = cargar_imagen("Imagenes/caracono_dañado.png")
img_zombie_balde = cargar_imagen("Imagenes/zombie_balde.png")
img_zombie_balde_dañado = cargar_imagen("Imagenes/balde_dañado.png")
img_lanzaguisante = cargar_imagen("Imagenes/lanzaguisante.png")
img_lanzaguisante_dispara = cargar_imagen("Imagenes/lanzaguisanteDispara.png")
img_nuez = cargar_imagen("Imagenes/nuez.png")
img_nuezmitad = cargar_imagen("Imagenes/nuez mitad.png")
img_nuezdañada = cargar_imagen("Imagenes/nuez dañada.png")
img_proyectil = cargar_imagen("Imagenes/Proyectil.png")
img_sol = cargar_imagen("Imagenes/sol.png")
img_pala = cargar_imagen("Imagenes/pala.png")
img_cortadora = cargar_imagen("Imagenes/cortadora.png")
img_piso = cargar_imagen("Imagenes/piso.png")
img_fondo_grilla = cargar_imagen("Imagenes/imagenFondoGrilla.png", tamaño=(1000, 500))
img_cartel = cargar_imagen("Imagenes/cartel.png", tamaño=(600, 300))
img_mute = cargar_imagen("Imagenes/mutear.png", tamaño=(50, 50))
img_unmute = cargar_imagen("Imagenes/unmute.png", tamaño=(50, 50))
rect_mute = pygame.Rect(1000, 50, 50, 50)
img_tralladora = cargar_imagen("imagenes/GuisantralladoraPvz1.png")
img_tralladora_dispara = cargar_imagen("imagenes/tralladoraDispara.png")

plantas_disponibles = [
    ("girasol", img_girasol, pygame.Rect(50, barra_inferior_inicio + 50, 100, 100)),
    (
        "lanzaguisante",
        img_lanzaguisante,
        pygame.Rect(200, barra_inferior_inicio + 50, 100, 100),
    ),
    ("nuez", img_nuez, pygame.Rect(350, barra_inferior_inicio + 50, 100, 100)),
    ("pala", img_pala, pygame.Rect(500, barra_inferior_inicio + 50, 100, 100)),
    (
        "lanzaguisanteTriple",
        img_tralladora,
        pygame.Rect(650, barra_inferior_inicio + 50, 100, 100),
    ),
]

zombis_disponibles = ("normal", "cono", "balde")
pesos = (0.7, 0.2, 0.1)


# Sonidos
sonido_principal = pygame.mixer.Sound("musica/musica.mp3")
sonido_mordida = pygame.mixer.Sound("musica/efectos/mordida.mp3")
sonido_plantar = pygame.mixer.Sound("musica/efectos/plantar.mp3")
sonido_golpe = pygame.mixer.Sound("musica/efectos/golpe.mp3")
sonido_zombi_inicio = pygame.mixer.Sound("musica/efectos/zombies_are_coming.mp3")

sonido_principal.play(-1)
sonido_principal.set_volume(0.4)
sonido_zombi_inicio.play()
sonido_seleccionar = pygame.mixer.Sound("musica/efectos/seleccionar.mp3")
sonido_disparo = pygame.mixer.Sound("musica/efectos/sonido disparo.mp3")
sonido_sol = pygame.mixer.Sound("musica/efectos/sonido sol.mp3")
sonido_cortadora = pygame.mixer.Sound("musica/efectos/cortadoraaa.mp3")


jugando = True
tiempo_ultimo_sol = 0
intervalo_sol = 5

# sonido
sonido_muteado = False
volumen_original = 0.4
for fila in range(cant_filas):
    lista_cortadoras.append(cortadora(fila, img_cortadora))

while jugando:
    reloj.tick(FPS)
    tiempo_actual = time.time()
    tiempo = pygame.time.get_ticks()

    if not pausar_generacion_zombis:
        if tiempo_actual - tiempo_ultimo_zombi >= tiempo_entre_zombis:
            tiempo_ultimo_zombi = tiempo_actual
            generar_zombi(
                lista_zombis,
                zombis_disponibles,
                pesos,
                img_zombie_normal,
                img_zombie_cono,
                img_zombie_balde,
            )
    else:
        if pygame.time.get_ticks() - tiempo_reinicio >= tiempo_pausa:
            pausar_generacion_zombis = False

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            jugando = False
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_ESCAPE:
                planta_seleccionada = None

        if evento.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            sol_agarrado = False  # NUEVO: inicializo bandera

            # sonido mute
            if rect_mute.collidepoint(x, y):
                sonido_muteado = not sonido_muteado
                print("muteado:", sonido_muteado)
                if sonido_muteado:

                    nuevo_volumen = 0.0
                else:
                    nuevo_volumen = volumen_original

                sonido_principal.set_volume(nuevo_volumen)
                sonido_mordida.set_volume(nuevo_volumen)
                sonido_plantar.set_volume(nuevo_volumen)
                sonido_golpe.set_volume(nuevo_volumen)
                sonido_zombi_inicio.set_volume(nuevo_volumen)
                sonido_seleccionar.set_volume(nuevo_volumen)
                sonido_disparo.set_volume(nuevo_volumen)
                sonido_sol.set_volume(nuevo_volumen)
                sonido_cortadora.set_volume(nuevo_volumen)

            for sol in lista_soles[:]:
                if sol.agarrar_sol(x, y, offset_y_grilla):
                    lista_soles.remove(sol)
                    cant_soles += 25
                    sonido_sol.play()

                    for planta in lista_plantas:
                        if isinstance(planta, Girasol) and planta.sol_activo == sol:
                            planta.tiempo_ultimo_sol = time.time()
                            planta.sol_activo = None
                            break

                    sol_agarrado = True
                    break

            if not sol_agarrado:
                if y < barra_superior_tamaño:
                    for nombre, imagen, rect in plantas_disponibles:
                        if rect.collidepoint(x, y):
                            planta_seleccionada = nombre
                            print(f"Planta seleccionada: {planta_seleccionada}")
                            sonido_seleccionar.play()

                            if planta_seleccionada == "pala":
                                pala_activa = True
                            else:
                                pala_activa = False

                elif y >= offset_y_grilla and x >= margen_cortadora:
                    fila = (y - offset_y_grilla) // tamaño_celda
                    columna = x // tamaño_celda

                    if planta_seleccionada == "pala":
                        for planta in lista_plantas:
                            if planta.fila == fila and planta.columna == columna:
                                lista_plantas.remove(planta)
                                grilla[fila][columna] = 0
                                planta_seleccionada = (None)  # Reinicia la planta seleccionada
                    else:
                        if columna < 10:
                            if (
                                planta_seleccionada == "girasol"
                                or planta_seleccionada == "nuez"
                            ) and cant_soles >= 50:
                                if grilla[fila][columna] != 0:
                                    continue
                                else:
                                    cant_soles -= 50
                                    colocar_planta(fila, columna, planta_seleccionada, grilla, lista_plantas, cant_filas, cant_columnas, img_girasol, img_lanzaguisante, img_lanzaguisante_dispara, img_nuez, img_nuezmitad, img_nuezdañada, img_tralladora, img_tralladora_dispara)
                                    sonido_plantar.play()
                                    planta_seleccionada = (None)  # Reinicia la planta seleccionada

                            elif (
                                planta_seleccionada == "lanzaguisante"
                                and cant_soles >= 100
                            ):
                                if grilla[fila][columna] != 0:
                                    continue
                                else:
                                    cant_soles -= 100
                                    colocar_planta(fila, columna, planta_seleccionada, grilla, lista_plantas, cant_filas, cant_columnas, img_girasol, img_lanzaguisante, img_lanzaguisante_dispara, img_nuez, img_nuezmitad, img_nuezdañada, img_tralladora, img_tralladora_dispara)
                                    sonido_plantar.play()
                                    planta_seleccionada = (None)  # Reinicia la planta seleccionada
                                    
                            elif (planta_seleccionada == "lanzaguisanteTriple" and cant_soles >= 200):
                                if grilla[fila][columna] != 0:
                                    continue
                                else:
                                    cant_soles -= 200
                                    colocar_planta(fila, columna, planta_seleccionada, grilla, lista_plantas, cant_filas, cant_columnas, img_girasol, img_lanzaguisante, img_lanzaguisante_dispara, img_nuez, img_nuezmitad, img_nuezdañada, img_tralladora, img_tralladora_dispara)
                                    sonido_plantar.play()
                                    planta_seleccionada = (None)  # Reinicia la planta seleccionada

    # Oleadas
    if puntuacion >= 40 and oleada_actual != 6:
        pesos = (0, 0.50, 0.50)
        tiempo_entre_zombis = 3
        oleada_actual = 6
        mostrar_oleada = True
        tiempo_mostrar_oleada = pygame.time.get_ticks()
        pausar_generacion_zombis = True
        tiempo_reinicio = pygame.time.get_ticks()

    elif puntuacion >= 30 and puntuacion < 40 and oleada_actual != 5:
        pesos = (0.10, 0.45, 0.45)
        tiempo_entre_zombis = 4
        oleada_actual = 5
        mostrar_oleada = True
        tiempo_mostrar_oleada = pygame.time.get_ticks()
        pausar_generacion_zombis = True
        tiempo_reinicio = pygame.time.get_ticks()

    elif puntuacion >= 20 and puntuacion < 30 and oleada_actual != 4:
        pesos = (0.4, 0.35, 0.25)
        tiempo_entre_zombis = 5
        oleada_actual = 4
        mostrar_oleada = True
        tiempo_mostrar_oleada = pygame.time.get_ticks()
        pausar_generacion_zombis = True
        tiempo_reinicio = pygame.time.get_ticks()

    elif puntuacion >= 10 and puntuacion < 20 and oleada_actual != 3:
        pesos = (0.5, 0.3, 0.2)
        tiempo_entre_zombis = 7
        oleada_actual = 3
        mostrar_oleada = True
        tiempo_mostrar_oleada = pygame.time.get_ticks()
        pausar_generacion_zombis = True
        tiempo_reinicio = pygame.time.get_ticks()

    elif puntuacion >= 5 and puntuacion < 10 and oleada_actual != 2:
        pesos = (0.6, 0.25, 0.15)
        tiempo_entre_zombis = 5
        oleada_actual = 2
        mostrar_oleada = True
        tiempo_mostrar_oleada = pygame.time.get_ticks()
        pausar_generacion_zombis = True
        tiempo_reinicio = pygame.time.get_ticks()

    if mostrar_oleada:
        tiempo_actual = pygame.time.get_ticks()
        if tiempo_actual - tiempo_mostrar_oleada < duracion_cartel:
            fuente = pygame.font.SysFont("Arial", 50)
            texto = fuente.render(f"Oleada {oleada_actual}", True, (255, 0, 0))
            rect = texto.get_rect(center=(ancho // 2, alto // 2))
            ventana.blit(texto, rect)
        else:
            mostrar_oleada = False

    ventana.fill(color_background)

    ventana.blit(img_fondo_grilla, (margen_cortadora, offset_y_grilla))

    for fila in range(cant_filas):
        y = fila * tamaño_celda + offset_y_grilla
        x_piso = margen_cortadora + (9 * tamaño_celda)
        ventana.blit(img_piso, (x_piso, y))

    for cortadora in lista_cortadoras:
        cortadora.movimiento()
        cortadora.dibujar(ventana, offset_y_grilla)

        if cortadora.esta_activada():
            if not cortadora.ya_sono:
                sonido_cortadora.play()
                cortadora.ya_sono = True

            for zombi in lista_zombis[:]:
                if cortadora.rect.colliderect(zombi):
                    lista_zombis.remove(zombi)

    for planta in lista_plantas:
        planta.dibujar(ventana, offset_y_grilla)

        for zombi in lista_zombis:
            if planta.devolver_coords()[1] == zombi.devolver_coords()[1]:

                if isinstance(planta, Lanzaguisantes):
                    if planta.puede_disparar():
                        planta.preparar_disparo()

                    if planta.actualizar_animacion():
                        proyectil = planta.disparar(img_proyectil)
                        lista_proyectiles.append(proyectil)
                        sonido_disparo.play()

                elif isinstance(planta, LanzaguisantesTriple):
                    if planta.puede_disparar():
                        planta.preparar_disparo()

                    proyectiles = planta.disparar(img_proyectil)
                    for p in proyectiles:
                        lista_proyectiles.append(p)
                        sonido_disparo.play()



    for guisante in lista_proyectiles:
        guisante.mover()
        guisante.dibujar(ventana, offset_y_grilla)
        if guisante.x > ancho:
            lista_proyectiles.remove(guisante)
            continue
        for zombi in lista_zombis:
            if guisante.rect.colliderect(zombi.rect):
                murio = zombi.recibedaño()
                zombi.actualizar_imagen(
                    img_zombie_normal,
                    img_zombie_sin_brazo,
                    img_zombie_cono_dañado,
                    img_zombie_balde_dañado,
                )
                sonido_golpe.play()
                if murio:
                    lista_zombis.remove(zombi)
                    puntuacion += 1
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
                        grilla[planta.fila][planta.columna] = 0
                break
        if not choco:
            zombi.mover()
        zombi.dibujar(ventana, offset_y_grilla)
        for cortadora in lista_cortadoras:
            if zombi.rect.colliderect(cortadora):
                cortadora.activar()
                if cortadora.rect.colliderect(zombi):
                    lista_zombis.remove(zombi)

    for nombre, imagen, rect in plantas_disponibles:
        imagen_rect = imagen.get_rect(center=rect.center)
        ventana.blit(imagen, imagen_rect)
        color_borde = (255, 0, 0) if nombre == planta_seleccionada else (0, 0, 0)
        pygame.draw.rect(ventana, color_borde, rect, 2)

    if tiempo_actual - tiempo_ultimo_sol >= intervalo_sol:
        tiempo_ultimo_sol = tiempo_actual
        nueva_columna = random.uniform(1.0, 9.0)
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
    texto_sol = render_texto(f"Soles {cant_soles}", 30, AMARILLO)
    ventana.blit(texto_sol, (10, 10))

    for girasol in lista_plantas:
        if isinstance(girasol, Girasol):
            if girasol.puede_generar():
                nuevo_sol = Soles(
                    girasol.columna, girasol.fila, img_sol, "planta", 75, 75
                )
                lista_soles.append(nuevo_sol)
                girasol.sol_activo = nuevo_sol

    ventana.blit(img_sol_50, (35, barra_inferior_inicio + 142))
    texto_valor_GP = render_texto("50", 30, AMARILLO)
    ventana.blit(texto_valor_GP, (90, barra_inferior_inicio + 149))

    ventana.blit(img_sol_50, (165, barra_inferior_inicio + 142))
    texto_valor_L = render_texto("100", 30, AMARILLO)
    ventana.blit(texto_valor_L, (210, barra_inferior_inicio + 149))
    texto_puntuacion = render_texto(f"Puntuacion {puntuacion}", 30, NEGRO)
    ventana.blit(img_sol_50, (315, barra_inferior_inicio + 142, 50, 50))
    ventana.blit(texto_valor_GP, (365, barra_inferior_inicio + 149))

    ventana.blit(texto_puntuacion, (700, barra_inferior_inicio + 142))

    texto_oleada = render_texto(f"Oleada {oleada_actual}", 30, NEGRO)
    ventana.blit(texto_oleada, (700, barra_inferior_inicio + 110))

    # Sonido
    if sonido_muteado:
        ventana.blit(img_mute, rect_mute.topleft)
    else:
        ventana.blit(img_unmute, rect_mute.topleft)
    rect_mute = pygame.Rect(1000, 50, 50, 50)

    # Dibujar la oleada actual
    if mostrar_oleada:
        if pygame.time.get_ticks() - tiempo_mostrar_oleada < duracion_cartel:
            # Primero dibujamos el cartel de fondo
            rect_cartel = img_cartel.get_rect(
                center=(ancho // 2, alto - offset_y_grilla // 2)
            )
            ventana.blit(img_cartel, rect_cartel)

            # Luego el texto por encima
            texto_oleada_central = render_texto(f"Oleada {oleada_actual}", 80, BLANCO)
            rect_texto = texto_oleada_central.get_rect(
                center=(ancho // 2, alto - offset_y_grilla // 2)
            )
            ventana.blit(texto_oleada_central, rect_texto)
        else:
            mostrar_oleada = False

    if pala_activa and planta_seleccionada == "pala":
        pos_mouse = pygame.mouse.get_pos()
        ventana.blit(img_pala, (pos_mouse[0] - 10, pos_mouse[1] - 90))

    pygame.display.update()

# pantalla de game over
if vidas <= 0:
    sonido_principal.stop()
    sonido_mordida.stop()
    game_over = True
    while game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    game_over = False
        s = pygame.Surface((1000, 1000))
        s.set_alpha(128)
        s.fill((0, 0, 0))
        imagen_final = cargar_imagen("Imagenes/pantallas/coso.png")
        ventana.blit(s, (0, 0))
        ventana.blit(imagen_final, (200, 100))
        pygame.display.flip()
        reloj.tick(FPS)

pygame.quit()
