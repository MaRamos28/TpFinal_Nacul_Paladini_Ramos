def juego():
    # Immportamos las librerías necesarias
    from funciones import cargar_imagen, render_texto, generar_zombi, colocar_planta
    from plantas import Girasol, Lanzaguisantes, LanzaguisantesTriple, Nuez, Proyectiles
    from soles import Soles
    from zombies import Zombie
    from cortadora import cortadora
    from menu import mostrar_menu
    from EfectoGolpe import EfectoGolpe
    import pygame
    import time
    import random

    # Inicializamos Pygame, el reproductor de musica y mostramos el menú
    pygame.init()
    pygame.mixer.init()

    # Creamos las listas para almacenar los objetos del juego
    lista_zombis = []
    lista_plantas = []
    lista_proyectiles = []
    lista_soles = []
    lista_cortadoras = []
    lista_efectos = []

    # Variables del juego
    cant_filas = 5
    cant_columnas = 10
    tamaño_celda = 100
    margen_cortadora = 100
    ancho = margen_cortadora + (cant_columnas * tamaño_celda)
    alto = cant_filas * tamaño_celda
    barra_superior_tamaño = 180
    separacion_barra_grilla = 10
    x = 0
    y = 0
    cant_soles = 50

    pala_activa = False

    oleada_actual = 1
    mostrar_oleada = False
    tiempo_mostrar_oleada = 0
    duracion_cartel = 3000  # en milisegundos (3 segundos)

    pausar_generacion_zombis = True
    tiempo_reinicio = pygame.time.get_ticks()  # arranca pausado
    tiempo_pausa = 4000  # 4 segundos

    barra_inferior_inicio = 0
    offset_y_grilla = barra_superior_tamaño + separacion_barra_grilla
    tiempo_entre_zombis = 15  # Segundos
    tiempo_ultimo_zombi = 0
    puntuacion = 0

    tamaño_ventana = (ancho, alto + barra_superior_tamaño + separacion_barra_grilla)

    color_background = (10, 223, 175)

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
    img_impacto = cargar_imagen("Imagenes/impacto.png", tamaño=(40, 40))
    img_game_over = cargar_imagen("Imagenes/pantallas/pantalla_final.png", tamaño=tamaño_ventana)

    plantas_disponibles = [
        ("girasol", img_girasol, pygame.Rect(50, barra_inferior_inicio + 50, 100, 100)),
        ("lanzaguisante", img_lanzaguisante, pygame.Rect(200, barra_inferior_inicio + 50, 100, 100),),
        ("nuez", img_nuez, pygame.Rect(350, barra_inferior_inicio + 50, 100, 100)),
        ("lanzaguisanteTriple", img_tralladora, pygame.Rect(500, barra_inferior_inicio + 50, 100, 100),),
        ("pala", img_pala, pygame.Rect(650, barra_inferior_inicio + 50, 100, 100))
        ]

    cooldowns_plantas = {"girasol": 0, "lanzaguisante": 0, "lanzaguisanteTriple": 0, "nuez": 0}

    duracion_cooldown = {"girasol": 3, "lanzaguisante": 4, "lanzaguisanteTriple": 6, "nuez": 5}

    zombis_disponibles = ("normal", "cono", "balde")
    pesos = (1, 0, 0)

    # Sonidos
    sonido_principal = pygame.mixer.Sound("musica/musica.mp3")
    sonido_mordida = pygame.mixer.Sound("musica/efectos/mordida.mp3")
    sonido_plantar = pygame.mixer.Sound("musica/efectos/plantar.mp3")
    sonido_golpe = pygame.mixer.Sound("musica/efectos/golpe.mp3")
    sonido_zombi_inicio = pygame.mixer.Sound("musica/efectos/zombies_are_coming.mp3")
    sonido_game_over = pygame.mixer.Sound("musica/sonido game over.mp3")
    sonido_principal.play(-1)
    sonido_principal.set_volume(0.4)
    sonido_zombi_inicio.play()
    sonido_seleccionar = pygame.mixer.Sound("musica/efectos/seleccionar.mp3")
    sonido_disparo = pygame.mixer.Sound("musica/efectos/sonido disparo.mp3")
    sonido_sol = pygame.mixer.Sound("musica/efectos/sonido sol.mp3")
    sonido_cortadora = pygame.mixer.Sound("musica/efectos/cortadoraaa.mp3")


    jugando = True
    game_over = False

    tiempo_ultimo_sol = time.time()
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
                generar_zombi(lista_zombis, zombis_disponibles, pesos, img_zombie_normal, img_zombie_cono, img_zombie_balde)
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
                if evento.button == 1:
                    x, y = pygame.mouse.get_pos()
                    sol_agarrado = False  # inicializo bandera

                    # sonido mute
                    if rect_mute.collidepoint(x, y):
                        sonido_muteado = not sonido_muteado
                        print("muteado:", sonido_muteado)
                        if jugando:
                            if sonido_muteado:
                                ventana.blit(img_mute, rect_mute.topleft)
                                nuevo_volumen = 0.0
                            else:
                                ventana.blit(img_unmute, rect_mute.topleft)
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
                                        planta_seleccionada = None
                            else:
                                if columna < 10 and grilla[fila][columna] == 0:
                                    tiempo_actual = time.time()
                                    ultimo_tiempo = cooldowns_plantas.get(planta_seleccionada, 0)
                                    cooldown = duracion_cooldown.get(planta_seleccionada, 0)

                                    if tiempo_actual - ultimo_tiempo >= cooldown:
                                        # Verificamos cantidad soles y colocamos según planta
                                        if (planta_seleccionada == "girasol" and cant_soles >= 50):
                                            cant_soles -= 50
                                        elif (planta_seleccionada == "nuez" and cant_soles >= 50):
                                            cant_soles -= 50
                                        elif (planta_seleccionada == "lanzaguisante" and cant_soles >= 100):
                                            cant_soles -= 100
                                        elif (planta_seleccionada == "lanzaguisanteTriple" and cant_soles >= 300):
                                            cant_soles -= 300
                                        else:
                                            planta_seleccionada = None
                                            break  # No tenés suficientes soles, no se planta

                                        colocar_planta(fila, columna, planta_seleccionada, grilla, lista_plantas, cant_filas, cant_columnas, img_girasol, img_lanzaguisante, img_lanzaguisante_dispara, img_nuez, img_nuezmitad, img_nuezdañada, img_tralladora, img_tralladora_dispara)
                                        sonido_plantar.play()
                                        cooldowns_plantas[planta_seleccionada] = (tiempo_actual)
                                        planta_seleccionada = None
                                    else:
                                        planta_seleccionada = None
                                        print("Todavía está en cooldown esa planta.")

        # Oleadas
        if puntuacion >= 50 and oleada_actual != 7:
            pesos = (0, 0.25, 0.75)
            tiempo_entre_zombis = 2
            oleada_actual = 7
            mostrar_oleada = True
            tiempo_mostrar_oleada = pygame.time.get_ticks()
            pausar_generacion_zombis = True
            tiempo_reinicio = pygame.time.get_ticks()

        elif puntuacion >= 40 and oleada_actual != 6:
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
            tiempo_entre_zombis = 10
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
            ventana.blit(img_piso, (0, y))

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

            # Chequear si hay zombis en la misma fila
            hay_zombi_en_fila = any(zombi.devolver_coords()[1] == planta.devolver_coords()[1] for zombi in lista_zombis)

            if isinstance(planta, Lanzaguisantes):
                if hay_zombi_en_fila and planta.puede_disparar():
                    planta.preparar_disparo()

                if planta.actualizar_animacion():
                    proyectil = planta.disparar(img_proyectil)
                    lista_proyectiles.append(proyectil)
                    sonido_disparo.play()

            elif isinstance(planta, LanzaguisantesTriple):
                if not hay_zombi_en_fila:
                    planta.dejar_de_disparar()

                if hay_zombi_en_fila and planta.puede_disparar():
                    planta.preparar_disparo()

                proyectiles = planta.disparar(img_proyectil)
                for p in proyectiles:
                    lista_proyectiles.append(p)
                    sonido_disparo.play()

                if isinstance(planta, Lanzaguisantes):
                    if planta.actualizar_animacion():
                        proyectil = planta.disparar(img_proyectil)
                        lista_proyectiles.append(proyectil)
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
                    zombi.actualizar_imagen(img_zombie_normal, img_zombie_sin_brazo, img_zombie_cono_dañado, img_zombie_balde_dañado)
                    if murio:
                        lista_zombis.remove(zombi)
                        puntuacion += 1
                    if guisante in lista_proyectiles:
                        sonido_golpe.play()
                        efecto = EfectoGolpe(zombi.rect.centerx, zombi.rect.centery, img_impacto)
                        lista_efectos.append(efecto)
                        lista_proyectiles.remove(guisante)

        for zombi in lista_zombis:
            choco = False
            fila_zombi = zombi.y // tamaño_celda
            col_zombi = zombi.x // tamaño_celda
            for planta in lista_plantas:
                if fila_zombi == planta.fila and col_zombi == planta.columna:
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

                elif zombi.x < margen_cortadora - 30:
                    sonido_principal.stop()
                    sonido_mordida.play()
                    jugando = False
                    game_over = True

        for efecto in lista_efectos[:]:
            efecto.dibujar(ventana)
            if efecto.expiro():
                lista_efectos.remove(efecto)

        for nombre, imagen, rect in plantas_disponibles:
            for nombre, imagen, rect in plantas_disponibles:
                # Fondo de la celda
                pygame.draw.rect(ventana, (0, 0, 0), rect, 2)

                # Imagen centrada dentro del rect
                imagen_rect = imagen.get_rect(center=rect.center)
                ventana.blit(imagen, imagen_rect)

                # Cooldown (barra gris semitransparente desde arriba hacia abajo)
                if nombre in cooldowns_plantas:
                    tiempo_pasado = time.time() - cooldowns_plantas[nombre]
                    tiempo_total = duracion_cooldown[nombre]
                    if tiempo_pasado < tiempo_total:
                        fraccion_restante = 1 - (tiempo_pasado / tiempo_total)
                        altura_barra = int(rect.height * fraccion_restante)
                        sombra = pygame.Surface((rect.width, altura_barra), pygame.SRCALPHA)
                        sombra.fill((50, 50, 50, 160))  # RGBA: gris oscuro con transparencia
                        ventana.blit(sombra, (rect.left, rect.top))

                # Borde rojo si está seleccionada
                if nombre == planta_seleccionada:
                    pygame.draw.rect(ventana, (255, 0, 0), rect, 3)

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
                    nuevo_sol = Soles(girasol.columna, girasol.fila, img_sol, "planta", 75, 75)
                    lista_soles.append(nuevo_sol)
                    girasol.sol_activo = nuevo_sol

        # Girasol vale 50
        ventana.blit(img_sol_50, (35, barra_inferior_inicio + 142))
        texto_valor_GP = render_texto("50", 30, AMARILLO)
        ventana.blit(texto_valor_GP, (90, barra_inferior_inicio + 152))

        # Lanzaguisante vale 100
        ventana.blit(img_sol_50, (165, barra_inferior_inicio + 142))
        texto_valor_L = render_texto("100", 30, AMARILLO)
        ventana.blit(texto_valor_L, (210, barra_inferior_inicio + 152))

        # Nuez vale 50
        ventana.blit(img_sol_50, (315, barra_inferior_inicio + 142))
        ventana.blit(texto_valor_GP, (365, barra_inferior_inicio + 152))

        # Lanzaguisante triple vale 200
        ventana.blit(img_sol_50, (470, barra_inferior_inicio + 142))
        texto_valor_T = render_texto("300", 30, AMARILLO)
        ventana.blit(texto_valor_T, (515, barra_inferior_inicio + 152))

        texto_puntuacion = render_texto(f"Puntuacion {puntuacion}", 30, NEGRO)

        ventana.blit(texto_puntuacion, (ancho - 250, 140))

        texto_oleada = render_texto(f"Oleada {oleada_actual}", 30, NEGRO)
        ventana.blit(texto_oleada, (ancho - 250, 100))

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
                rect_cartel = img_cartel.get_rect(center=(ancho // 2, alto - offset_y_grilla // 2))
                ventana.blit(img_cartel, rect_cartel)

                # Luego el texto por encima
                texto_oleada_central = render_texto(f"Oleada {oleada_actual}", 80, BLANCO)
                rect_texto = texto_oleada_central.get_rect(center=(ancho // 2, alto - offset_y_grilla // 2))
                ventana.blit(texto_oleada_central, rect_texto)
            else:
                mostrar_oleada = False

        if pala_activa and planta_seleccionada == "pala":
            pos_mouse = pygame.mouse.get_pos()
            ventana.blit(img_pala, (pos_mouse[0] - 10, pos_mouse[1] - 90))

        pygame.display.update()

    # pantalla de game over
    rect_exit_to_map = pygame.Rect(280, 600, 200, 50)
    rect_retry = pygame.Rect(680, 600, 125, 50)
    if game_over:
        sonido_principal.stop()
        sonido_mordida.stop()
        sonido_cortadora.stop()
        sonido_game_over.play()
        while True:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_RETURN:
                        pygame.quit()
                        ventana.fill((0, 0, 0))
                
                if evento.type == pygame.MOUSEBUTTONDOWN:
                    if rect_exit_to_map.collidepoint(evento.pos):
                        sonido_game_over.stop()
                        return "menu"
                    elif rect_retry.collidepoint(evento.pos):
                        sonido_game_over.stop()
                        return "volver a jugar"
                        
            ventana.blit(img_game_over, (0, 0))

            pygame.display.flip()
            reloj.tick(FPS)
    pygame.quit()

if __name__ == "__main__":
    juego() #prueba individual del codigo