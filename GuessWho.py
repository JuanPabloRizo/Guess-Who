import pygame
import json
import os

# Inicializar Pygame
pygame.init()
fondo = pygame.image.load("fondo2.jpg")
pagina_personajes = 0  # Página actual para la vista de personajes
# Configuración de pantalla
ANCHO = 800
ALTO = 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Adivina Quién - Los Simpson")
fondo = pygame.transform.scale(fondo, (ANCHO, ALTO))

# Fuente
fuente = pygame.font.SysFont(None, 32)
fuente_grande = pygame.font.SysFont(None, 48)

# Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
AZUL = (100, 149, 237)
ROJO = (220, 20, 60)
VERDE = (34, 139, 34)

# Cargar datos del JSON
with open("personajes.json", "r", encoding="utf-8") as archivo:
    datos = json.load(archivo)

personajes = datos["personajes"]
preguntas = datos["preguntas"]
mapeo_preguntas = datos["mapeo_preguntas"]

# Variables de estado
estado = "menu"
personajes_filtrados = personajes.copy()
pregunta_actual = 0
juego_terminado = False
personaje_final = None

# Categorías ya respondidas
categorias_respondidas = set()
descartar=True
# Mostrar texto centrado
def mostrar_texto(texto, y, fuente, color=NEGRO):
    render = fuente.render(texto, True, color)
    rect = render.get_rect(center=(ANCHO // 2, y))
    pantalla.blit(render, rect)

# Mostrar botón
def mostrar_boton(texto, x, y, ancho, alto, color):
    pygame.draw.rect(pantalla, color, (x, y, ancho, alto))
    render = fuente.render(texto, True, BLANCO)
    rect = render.get_rect(center=(x + ancho // 2, y + alto // 2))
    pantalla.blit(render, rect)
    return pygame.Rect(x, y, ancho, alto)

# Obtener siguiente pregunta válida
def obtener_pregunta_valida():
    global personajes_filtrados, pregunta_actual, categorias_respondidas, descartar
    while pregunta_actual < len(preguntas):
        pregunta = preguntas[pregunta_actual]
        clave = mapeo_preguntas.get(pregunta)
        
        valor_esperado = None

        if "cabello" in clave:
            if "azul" in pregunta:
                valor_esperado = "azul"
            elif "amarillo" in pregunta:
                valor_esperado = "amarillo"
            elif "cafe" in pregunta:
                valor_esperado = "cafe"
            elif "gris" in pregunta:
                valor_esperado = "gris"
            elif "rojo" in pregunta:
                valor_esperado = "rojo"
            elif "rubio" in pregunta:
                valor_esperado = "rubio"
        elif "edad" in clave:
            if "adulto" in pregunta:
                valor_esperado = "adulto"
            elif "joven" in pregunta:
                valor_esperado = "joven"
            elif "viejo" in pregunta:   
                valor_esperado = "viejo"  
        elif "color" in clave:
            if "amarillo" in pregunta:
                valor_esperado = "amarillo"
            elif "negro" in pregunta:
                valor_esperado = "negro"
            elif "blanco" in pregunta:   
                valor_esperado = "blanco"     
        elif "gafas" in clave:
            valor_esperado = "si" if "gafas" in pregunta else "no"
        elif "traje" in clave:
            valor_esperado = "si" if "traje" in pregunta else "no"
        elif "doctor" in clave:
            valor_esperado = "si" if "doctor" in pregunta else "no"
        elif "gordo" in clave:
            valor_esperado = "si" if "gordo" in pregunta else "no"
        elif "barba" in clave:
            valor_esperado = "si" if "barba" in pregunta else "no"
        elif "sacerdote" in clave:
            valor_esperado = "si" if "sacerdote" in pregunta else "no"
        elif "chef" in clave:
            valor_esperado = "si" if "chef" in pregunta else "no"
        elif "fuma" in clave:
            valor_esperado = "si" if "fuma" in pregunta else "no"
        elif "bailarin" in clave:
            valor_esperado = "si" if "bailarin" in pregunta else "no"
        elif "ropa" in clave:
            if "azul" in pregunta:
                valor_esperado = "azul"
            elif "rosa" in pregunta:
                valor_esperado = "rosa"
            elif "verde" in pregunta:
                valor_esperado = "verde"
            elif "blanca" in pregunta:
                valor_esperado = "blanca"
        elif "genero" in clave:
            valor_esperado = "masculino" if "hombre" in pregunta else "femenino"   
        
        descartar = any(p.get(clave) == valor_esperado for p in personajes_filtrados)
        if clave:
            categoria = clave.split("_")[0]
            if categoria in categorias_respondidas:
                pregunta_actual += 1
                continue
            elif descartar==False:
                pregunta_actual += 1
                continue
        return pregunta
    return None
def filtrar_personajes(respuesta):
    global personajes_filtrados, pregunta_actual, categorias_respondidas
    while pregunta_actual < len(preguntas):
        pregunta = preguntas[pregunta_actual]
        clave = mapeo_preguntas.get(pregunta)

        if not clave:
            pregunta_actual += 1
            continue

        categoria_base = clave.split("_")[0]

        # Si ya fue afirmativamente respondida antes, saltamos esta categoría
        if categoria_base in categorias_respondidas:
            pregunta_actual += 1
            continue

        valor_esperado = None

        if "cabello" in clave:
            if "azul" in pregunta:
                valor_esperado = "azul"
            elif "amarillo" in pregunta:
                valor_esperado = "amarillo"
            elif "cafe" in pregunta:
                valor_esperado = "cafe"
            elif "gris" in pregunta:
                valor_esperado = "gris"
            elif "rojo" in pregunta:
                valor_esperado = "rojo"
            elif "rubio" in pregunta:
                valor_esperado = "rubio"
        elif "edad" in clave:
            if "adulto" in pregunta:
                valor_esperado = "adulto"
            elif "joven" in pregunta:
                valor_esperado = "joven"
            elif "viejo" in pregunta:   
                valor_esperado = "viejo"  
        elif "color" in clave:
            if "amarillo" in pregunta:
                valor_esperado = "amarillo"
            elif "negro" in pregunta:
                valor_esperado = "negro"
            elif "blanco" in pregunta:   
                valor_esperado = "blanco"     
        elif "gafas" in clave:
            valor_esperado = "si" if "gafas" in pregunta else "no"
        elif "traje" in clave:
            valor_esperado = "si" if "traje" in pregunta else "no"
        elif "doctor" in clave:
            valor_esperado = "si" if "doctor" in pregunta else "no"
        elif "gordo" in clave:
            valor_esperado = "si" if "gordo" in pregunta else "no"
        elif "barba" in clave:
            valor_esperado = "si" if "barba" in pregunta else "no"
        elif "sacerdote" in clave:
            valor_esperado = "si" if "sacerdote" in pregunta else "no"
        elif "chef" in clave:
            valor_esperado = "si" if "chef" in pregunta else "no"
        elif "fuma" in clave:
            valor_esperado = "si" if "fuma" in pregunta else "no"
        elif "bailarin" in clave:
            valor_esperado = "si" if "bailarin" in pregunta else "no"
        elif "ropa" in clave:
            if "azul" in pregunta:
                valor_esperado = "azul"
            elif "rosa" in pregunta:
                valor_esperado = "rosa"
            elif "verde" in pregunta:
                valor_esperado = "verde"
            elif "blanca" in pregunta:
                valor_esperado = "blanca"
        elif "genero" in clave:
            valor_esperado = "masculino" if "hombre" in pregunta else "femenino"        


        if respuesta == "sí":
            personajes_filtrados = [p for p in personajes_filtrados if p.get(clave) == valor_esperado]
            # Solo se descarta la categoría si la respuesta fue afirmativa
            categorias_respondidas.add(categoria_base)
        else:
            personajes_filtrados = [p for p in personajes_filtrados if p.get(clave) != valor_esperado]

        pregunta_actual += 1
        break


# Reiniciar juego
def reiniciar_juego():
    global personajes_filtrados, pregunta_actual, juego_terminado, personaje_final, categorias_respondidas
    personajes_filtrados = personajes.copy()
    pregunta_actual = 0
    juego_terminado = False
    personaje_final = None
    categorias_respondidas.clear()

# Bucle principal
ejecutando = True
pagina_personajes = 0  # Página inicial
personajes_por_pagina = 8  # Número de personajes por página
fuente_pequena = pygame.font.Font(None, 20)  # Fuente más pequeña para los nombres

while ejecutando:
    pantalla.fill(BLANCO)
    pantalla.blit(fondo, (0, 0))

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False

        elif evento.type == pygame.MOUSEBUTTONDOWN:
            if estado == "menu":
                if boton_jugar.collidepoint(evento.pos):
                    reiniciar_juego()
                    estado = "juego"
                elif boton_ver.collidepoint(evento.pos):
                    estado = "ver_personajes"

            elif estado == "juego" and not juego_terminado:
                if boton_si.collidepoint(evento.pos):
                    filtrar_personajes("sí")
                elif boton_no.collidepoint(evento.pos):
                    filtrar_personajes("no")

            elif estado == "fin":
                if boton_menu.collidepoint(evento.pos):
                    estado = "menu"

            elif estado == "ver_personajes":
                if boton_menu.collidepoint(evento.pos):
                    estado = "menu"
                elif boton_anterior and boton_anterior.collidepoint(evento.pos):
                    pagina_personajes = max(0, pagina_personajes - 1)
                elif boton_siguiente and boton_siguiente.collidepoint(evento.pos):
                    pagina_personajes += 1

    if estado == "menu":
        mostrar_texto("Adivina Quién - Los Simpson", 100, fuente_grande)
        boton_jugar = mostrar_boton("Jugar", 300, 200, 200, 60, AZUL)
        boton_ver = mostrar_boton("Ver personajes", 300, 300, 200, 60, VERDE)

    elif estado == "ver_personajes":
        mostrar_texto("Personajes disponibles", 40, fuente_grande)
        boton_menu = mostrar_boton("Volver al menú", 600, 500, 160, 50, ROJO)
        
        # Paginación
        total_paginas = (len(personajes) + personajes_por_pagina - 1) // personajes_por_pagina
        personajes_actuales = personajes[pagina_personajes * personajes_por_pagina : (pagina_personajes + 1) * personajes_por_pagina]

        ancho_tarjeta = 150
        alto_tarjeta = 160
        margen = 20
        columnas = 4

        for i, personaje in enumerate(personajes_actuales):
            fila = i // columnas
            columna = i % columnas
            x = margen + columna * (ancho_tarjeta + margen)
            y = 100 + fila * (alto_tarjeta + margen)
            pygame.draw.rect(pantalla, (230, 230, 230), (x, y, ancho_tarjeta, alto_tarjeta), border_radius=10)
            imagen_path = personaje.get("imagen")
            if imagen_path and os.path.exists(imagen_path):
                imagen = pygame.image.load(imagen_path)
                imagen = pygame.transform.scale(imagen, (100, 100))
                pantalla.blit(imagen, (x + 25, y + 10))
            
            # Nombre del personaje con fuente más pequeña
            nombre = personaje.get("nombre", "Desconocido")
            nombre_render = fuente_pequena.render(nombre, True, NEGRO)
            nombre_rect = nombre_render.get_rect(center=(x + ancho_tarjeta // 2, y + 120))
            pantalla.blit(nombre_render, nombre_rect)

        # Botones de navegación
        if pagina_personajes > 0:
            boton_anterior = mostrar_boton("Anterior", 50, 500, 130, 50, AZUL)
        else:
            boton_anterior = None

        if pagina_personajes < total_paginas - 1:
            boton_siguiente = mostrar_boton("Siguiente", 200, 500, 130, 50, AZUL)
        else:
            boton_siguiente = None

    elif estado == "juego":
        if not juego_terminado:
            if len(personajes_filtrados) == 1:
                personaje_final = personajes_filtrados[0]
                juego_terminado = True
                estado = "fin"
            elif pregunta_actual >= len(preguntas):
                personaje_final = personajes_filtrados[0] if personajes_filtrados else None
                juego_terminado = True
                estado = "fin"
            else:
                pregunta_valida = obtener_pregunta_valida()
                if pregunta_valida:
                    mostrar_texto("Piensa en un personaje y responde:", 50, fuente)
                    mostrar_texto(pregunta_valida, 120, fuente_grande)
                    boton_si = mostrar_boton("Sí", 250, 300, 100, 50, AZUL)
                    boton_no = mostrar_boton("No", 450, 300, 100, 50, ROJO)
                else:
                    personaje_final = personajes_filtrados[0] if personajes_filtrados else None
                    juego_terminado = True
                    estado = "fin"

    elif estado == "fin":
        mostrar_texto("¡Ya lo tengo!", 50, fuente_grande, ROJO)
        if personaje_final:
            mostrar_texto(f"Tu personaje es: {personaje_final['nombre']}", 120, fuente_grande)
            imagen_path = personaje_final.get("imagen")
            if imagen_path and os.path.exists(imagen_path):
                imagen = pygame.image.load(imagen_path)
                imagen = pygame.transform.scale(imagen, (200, 200))
                pantalla.blit(imagen, (ANCHO // 2 - 100, 180))
        else:
            mostrar_texto("No pude adivinar tu personaje...", 120, fuente)
        boton_menu = mostrar_boton("Volver al menú", 300, 450, 200, 60, VERDE)

    pygame.display.flip()

pygame.quit()
