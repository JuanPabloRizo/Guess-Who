import pygame
import json
import os

# Inicializar Pygame
pygame.init()
fondo = pygame.image.load("fondo2.jpg")

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
estado = "menu"  # Puede ser: "menu", "juego", "ver_personajes", "fin"
personajes_filtrados = []
pregunta_actual = 0
juego_terminado = False
personaje_final = None

# Función para mostrar texto centrado
def mostrar_texto(texto, y, fuente, color=NEGRO):
    render = fuente.render(texto, True, color)
    rect = render.get_rect(center=(ANCHO // 2, y))
    pantalla.blit(render, rect)

# Función para mostrar botones
def mostrar_boton(texto, x, y, ancho, alto, color):
    pygame.draw.rect(pantalla, color, (x, y, ancho, alto))
    render = fuente.render(texto, True, BLANCO)
    rect = render.get_rect(center=(x + ancho // 2, y + alto // 2))
    pantalla.blit(render, rect)
    return pygame.Rect(x, y, ancho, alto)

# Función para filtrar personajes según la respuesta
def filtrar_personajes(respuesta):
    global personajes_filtrados, pregunta_actual

    pregunta = preguntas[pregunta_actual]
    clave = mapeo_preguntas.get(pregunta)

    if clave:
        valor_esperado = None
        for valor_posible in ["azul", "amarillo", "calvo", "cafe", "si", "no", "masculino", "femenino"]:
            if valor_posible in pregunta.lower():
                valor_esperado = valor_posible
                break

        if valor_esperado:
            if respuesta == "sí":
                personajes_filtrados = [p for p in personajes_filtrados if p.get(clave, "").lower() == valor_esperado]
            else:
                personajes_filtrados = [p for p in personajes_filtrados if p.get(clave, "").lower() != valor_esperado]
        else:
            if respuesta == "sí":
                personajes_filtrados = [p for p in personajes_filtrados if p.get(clave, "").lower() in ["sí", "masculino"]]
            else:
                personajes_filtrados = [p for p in personajes_filtrados if p.get(clave, "").lower() not in ["sí", "masculino"]]

    pregunta_actual += 1

# Función para reiniciar el juego
def reiniciar_juego():
    global personajes_filtrados, pregunta_actual, juego_terminado, personaje_final
    personajes_filtrados = personajes.copy()
    pregunta_actual = 0
    juego_terminado = False
    personaje_final = None

# Bucle principal
ejecutando = True
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

    # Menú principal
    if estado == "menu":
        mostrar_texto("Adivina Quién - Los Simpson", 100, fuente_grande)
        boton_jugar = mostrar_boton("Jugar", 300, 200, 200, 60, AZUL)
        boton_ver = mostrar_boton("Ver personajes", 300, 300, 200, 60, VERDE)

    # Mostrar personajes
    elif estado == "ver_personajes":
        mostrar_texto("Personajes disponibles", 40, fuente_grande)
        boton_menu = mostrar_boton("Volver al menú", 600, 500, 160, 50, ROJO)

        # Dimensiones para cada personaje
        ancho_tarjeta = 150
        alto_tarjeta = 160
        margen = 20
        columnas = 4  # Puedes cambiar esto si quieres más o menos por fila

        for i, personaje in enumerate(personajes):
            fila = i // columnas
            columna = i % columnas
            x = margen + columna * (ancho_tarjeta + margen)
            y = 100 + fila * (alto_tarjeta + margen)

            # Dibujar rectángulo de fondo (opcional)
            pygame.draw.rect(pantalla, (230, 230, 230), (x, y, ancho_tarjeta, alto_tarjeta), border_radius=10)

            # Mostrar imagen
            imagen_path = personaje.get("imagen")
            if imagen_path and os.path.exists(imagen_path):
                imagen = pygame.image.load(imagen_path)
                imagen = pygame.transform.scale(imagen, (100, 100))
                pantalla.blit(imagen, (x + 25, y + 10))

            # Mostrar nombre
            nombre = personaje.get("nombre", "Desconocido")
            nombre_render = fuente.render(nombre, True, NEGRO)
            nombre_rect = nombre_render.get_rect(center=(x + ancho_tarjeta // 2, y + 120))
            pantalla.blit(nombre_render, nombre_rect)


    # Juego en progreso
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
                mostrar_texto("Piensa en un personaje y responde:", 50, fuente)
                mostrar_texto(preguntas[pregunta_actual], 120, fuente_grande)
                boton_si = mostrar_boton("Sí", 250, 300, 100, 50, AZUL)
                boton_no = mostrar_boton("No", 450, 300, 100, 50, ROJO)

    # Fin del juego
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