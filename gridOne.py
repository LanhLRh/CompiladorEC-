import turtle
import tkinter as tk
from Bloque import *
from Objeto import *

# ------------------------------------------------
# Funciones para crear objetos y mundo
# ------------------------------------------------
def define_cuadricula(canvas_dimension, cantidad_bloques, bloque_dimension):
    # Crea la matriz para almacenar las posiciones en la cuadricula
    cuadricula = [[Bloque() for j in range(cantidad_bloques)] for i in range(cantidad_bloques)]

    x = 0
    y = 0

    # Actualiza la información de cada bloque
    for i in range(0, cantidad_bloques):
        for j in range(0, cantidad_bloques):
            cuadricula[i][j].x = x - canvas_dimension / 2
            cuadricula[i][j].y = y - canvas_dimension / 2
            cuadricula[i][j].dimension = bloque_dimension
            x = x + bloque_dimension
        y = y + bloque_dimension
        x = 0

    return cuadricula

def dibujar_cuadricula(canvas_dimension, bloque_dimension, color):
    # Dibuja lineas horizontales
    x_i = 0 - canvas_dimension
    x_f = canvas_dimension
    for i in range(-int(canvas_dimension / 2), canvas_dimension, bloque_dimension):
        y_i = i
        y_f = i
        canvas.create_line(x_i, y_i, x_f, y_f, fill=color)

    # Dibuja lineas verticales
    y_i = 0 - canvas_dimension
    y_f = canvas_dimension
    for i in range(-int(canvas_dimension / 2), canvas_dimension, bloque_dimension):
        x_i = i
        x_f = i
        canvas.create_line(x_i, y_i, x_f, y_f, fill=color)

def dibujar_bloque(renglon, columna, tipo):
    # Define el color del bloque
    color = None
    if tipo == 1:
        # suelo
        color = "forest green"
    elif tipo == 2:
        # meta
        color = "gold"
    elif tipo == 3:
        # obstaculo
        color = "saddle brown"

    # Obtiene la información del bloque
    bloque = cuadricula[renglon][columna]
    dimension = bloque.dimension
    x = bloque.x
    y = bloque.y
    
    # Dibuja el bloque
    canvas.create_rectangle(x, y, x + dimension, y + dimension, fill=color, width=0)

    # Actualiza el tipo del bloque
    bloque.tipo = tipo

def dibujar_objeto(renglon, columna, tipo, orientacion):
    # Define el color y forma del objeto
    color = None
    forma = None
    if tipo == 1:
        # personaje
        color = "white"
        forma = "turtle"
    elif tipo == 2:
        # enemigo
        color = "orange red"
        forma = "turtle"
    elif tipo == 3:
        # coleccionable
        color = "orange"
        forma = "circle"

    # Define un objeto
    objeto = turtle.RawTurtle(canvas)
    objeto.hideturtle()
    objeto.penup()
    objeto.shape(forma)
    objeto.shapesize(1, 1, 1)
    objeto.color(color)
    objeto.right(orientacion * 90)

    # Obtiene la información del bloque
    bloque = cuadricula[bloques_cantidad - 1 - renglon][columna]
    x = bloque.x
    y = bloque.y
    dimension = bloque.dimension
    objeto.goto(x + dimension / 2.0, y + dimension / 2.0)
    objeto.showturtle()

    # Actualiza el objeto
    cuadricula[renglon][columna].objeto = tipo
    cuadricula[renglon][columna].elemento = objeto

    # Crea el objeto de retorno
    objeto_creado = Objeto()
    objeto_creado.renglon = renglon
    objeto_creado.columna = columna
    objeto_creado.orientacion = orientacion
    objeto_creado.tipo = tipo
    objeto_creado.objeto = objeto

    return objeto_creado

# ------------------------------------------------
# Funciones para interactuar con el agente
# ------------------------------------------------
def mover(objeto, posiciones):
    renglon = objeto.renglon
    columna = objeto.columna
    orientacion = objeto.orientacion
    tipo = objeto.tipo
    obj = objeto.objeto

    n_renglon = renglon
    n_columna = columna
    
    cuadricula_renglon = n_renglon
    cuadricula_columna = n_columna

    if orientacion == 0:
        n_columna = columna + posiciones
        cuadricula_columna = n_columna
    elif orientacion == 1:
        n_renglon = renglon + posiciones
        cuadricula_renglon = renglon - posiciones
    elif orientacion == 2:
        n_columna = columna - posiciones
        cuadricula_columna = n_columna
    elif orientacion == 3:
        n_renglon = renglon - posiciones
        cuadricula_renglon = renglon + posiciones

    # Actualiza el objeto
    objeto.renglon = n_renglon
    objeto.columna = n_columna

    # Mueve al objeto
    x = cuadricula[cuadricula_renglon][cuadricula_columna].x
    y = cuadricula[cuadricula_renglon][cuadricula_columna].y
    dimension = cuadricula[cuadricula_renglon][cuadricula_columna].dimension

    obj.speed("slowest")
    obj.goto(x + dimension / 2, y - dimension / 2)

    # Elimina el objeto en la posicion previa
    cuadricula[bloques_cantidad - 1 - renglon][cuadricula_columna].objeto = None

def saltar(objeto):
    mover(objeto, 2)

def posicionar(objeto, renglon, columna):
    # Obtiene los datos del objeto
    obj_renglon = objeto.renglon
    obj_columna = objeto.columna
    tipo = objeto.tipo

    # Obtener los datos de la cuadricula en donde se situara
    x = cuadricula[bloques_cantidad - 1 - renglon][columna].x
    y = cuadricula[bloques_cantidad - 1 - renglon][columna].y
    dimension = cuadricula[bloques_cantidad - 1 - renglon][columna].dimension

    # Mueve el objeto
    objeto.objeto.goto(x + dimension / 2, y + dimension / 2)

    # Acualiza la posicion del objeto
    objeto.renglon = renglon
    objeto.columna = columna

    # Elimina el objeto en la posicion previa
    cuadricula[bloques_cantidad - 1 - obj_renglon][obj_columna].objeto = None

def girar_derecha(objeto):
    obj = objeto.objeto
    orientacion = objeto.orientacion
    n_orientacion = None

    if orientacion == 3:
        n_orientacion = 0
    else:
        n_orientacion = orientacion + 1

    # Actualiza la orientacion del objeto
    objeto.orientacion = n_orientacion
    obj.right(90)

def girar_izquierda(objeto):
    obj = objeto.objeto
    orientacion = objeto.orientacion
    n_orientacion = None
    
    if orientacion == 0:
        n_orientacion = 3
    else:
        n_orientacion = orientacion - 1
    
    # Actualiza la orientacion del objeto
    objeto.orientacion = n_orientacion
    obj.left(90)

def ocultar(objeto, bandera):
    if bandera:
        objeto.objeto.hideturtle()
    else:
        objeto.objeto.showturtle()

def camino_libre(objeto):
    # Obtener la informacion del objeto
    orientacion = objeto.orientacion
    renglon = objeto.renglon
    columna = objeto.columna

    # Obtener la informacion del bloque de enfrente
    renglon_bloque = renglon
    columna_bloque = columna

    if orientacion == 0:
        columna_bloque = columna_bloque + 1
    elif orientacion == 1:
        renglon_bloque = renglon_bloque + 1
    elif orientacion == 2:
        columna_bloque = columna_bloque - 1
    elif orientacion == 3:
        renglon_bloque = renglon_bloque - 1

    tipo = cuadricula[renglon_bloque][columna_bloque].tipo
    obj = cuadricula[renglon_bloque][columna_bloque].objeto

    if obj == None and (tipo == 1 or tipo == 2):
        return True
    return False

def deteccion_objeto(objeto):
    # Obtener la informacion del objeto
    orientacion = objeto.orientacion
    renglon = objeto.renglon
    columna = objeto.columna

    # Obtener la informacion del bloque de enfrente
    renglon_bloque = renglon
    columna_bloque = columna

    if orientacion == 0:
        columna_bloque = columna_bloque + 1
    elif orientacion == 1:
        renglon_bloque = renglon_bloque + 1
    elif orientacion == 2:
        columna_bloque = columna_bloque - 1
    elif orientacion == 3:
        renglon_bloque = renglon_bloque - 1

    tipo = cuadricula[renglon_bloque][columna_bloque].tipo
    obj = cuadricula[renglon_bloque][columna_bloque].objeto

    if obj == 2:
        # enemigo
        return 1
    elif obj == 3:
        # coleccionable
        return 2

def deteccion_bloque(objeto):
     # Obtener la informacion del objeto
    orientacion = objeto.orientacion
    renglon = objeto.renglon
    columna = objeto.columna

    # Obtener la informacion del bloque de enfrente
    renglon_bloque = renglon
    columna_bloque = columna

    if orientacion == 0:
        columna_bloque = columna_bloque + 1
    elif orientacion == 1:
        renglon_bloque = renglon_bloque + 1
    elif orientacion == 2:
        columna_bloque = columna_bloque - 1
    elif orientacion == 3:
        renglon_bloque = renglon_bloque - 1

    tipo = cuadricula[renglon_bloque][columna_bloque].tipo
    obj = cuadricula[renglon_bloque][columna_bloque].objeto

    if tipo == 1:
        # suelo
        return 1
    elif tipo == 2:
        # meta
        return 2
    elif tipo== 3:
        # obstaculo
        return 3
    else:
        # agua
        return 4

def eliminar_enemigo(objeto):
    # Obtener la informacion del objeto
    orientacion = objeto.orientacion
    renglon = objeto.renglon
    columna = objeto.columna

    # Obtener la informacion del bloque de enfrente
    renglon_bloque = renglon
    columna_bloque = columna

    if orientacion == 0:
        columna_bloque = columna_bloque + 1
    elif orientacion == 1:
        renglon_bloque = renglon_bloque + 1
    elif orientacion == 2:
        columna_bloque = columna_bloque - 1
    elif orientacion == 3:
        renglon_bloque = renglon_bloque - 1

    obj = cuadricula[renglon_bloque][columna_bloque].objeto
    elemento = cuadricula[renglon_bloque][columna_bloque].elemento

    if obj == 2:
        cuadricula[renglon_bloque][columna_bloque].objeto = None
        elemento.hideturtle()

def recoger_objeto(objeto):
    # Obtener la informacion del objeto
    orientacion = objeto.orientacion
    renglon = objeto.renglon
    columna = objeto.columna

    # Obtener la informacion del bloque actual
    renglon_bloque = renglon
    columna_bloque = columna

    obj = cuadricula[renglon_bloque][columna_bloque].objeto
    elemento = cuadricula[renglon_bloque][columna_bloque].elemento
    
    if obj == 3:
        cuadricula[renglon_bloque][columna_bloque].objeto = None
        elemento.hideturtle()
        return True
    return False

def dejar_objeto(objeto, lleva_objeto):
    # Obtener la informacion del objeto
    orientacion = objeto.orientacion
    renglon = objeto.renglon
    columna = objeto.columna

    # Obtener la informacion del bloque actual
    renglon_bloque = renglon
    columna_bloque = columna

    obj = cuadricula[renglon_bloque][columna_bloque].objeto
    elemento = cuadricula[renglon_bloque][columna_bloque].elemento

    if lleva_objeto:
        dibujar_objeto(renglon_bloque, columna_bloque, 3, 0)
    
    return False

# ------------------------------------------------
# Funciones de trazo
# ------------------------------------------------
def crear_tortuga(color):
    tortuga = turtle.RawTurtle(canvas)
    tortuga.shape("turtle")
    tortuga.shapesize(1, 1, 1)
    tortuga.color(color)
    return tortuga

def rotar_derecha(tortuga, grados):
    tortuga.right(grados)

def rotar_izquierda(tortuga, grados):
    tortuga.left(grados)

def trazo(tortuga, dibujar, tamano):
    if dibujar:
        tortuga.pendown()
    else:
        tortuga.penup()

    tortuga.pensize(tamano)

def color(tortuga, color):
    tortuga.color(color)

def avanzar(tortuga, distancia):
    tortuga.forward(distancia)

def colocar(tortuga, x, y):
    tortuga.setposition(x, y)

def velocidad(tortuga, velocidad):
    tortuga.speed(velocidad)

def mostrar_valor(tortuga, mensaje, tamano):
    tortuga.write(str(mensaje), True, align="center", font=("Arial", tamano, "normal"))

# ------------------------------------------------
# Creacion del canvas
# ------------------------------------------------

canvas_dimension = None
bloques_cantidad = None
canvas_color = None
bloque_dimension = None
raiz = None
canvas = None
tortuga = None
ventana = None

def inicioMundo():
    global canvas_dimension, bloques_cantidad, canvas_color, bloque_dimension, raiz, canvas, tortuga, ventana

    # Definición de propiedades del canvas
    canvas_dimension = 400
    bloques_cantidad = 10
    canvas_color = "royal blue"
    bloque_dimension = int(canvas_dimension / bloques_cantidad)

    # Creación del canvas
    raiz = tk.Tk()
    raiz.title("IDE EC++")
    raiz.resizable(width=False, height=False)
    canvas = tk.Canvas(master = raiz, width = canvas_dimension, height = canvas_dimension, bd = 0, highlightthickness = 0)
    canvas.pack()

    # Crea tortuga para configurar mundo
    tortuga = turtle.RawTurtle(canvas)
    tortuga.hideturtle()
    ventana = tortuga.getscreen()
    ventana.bgcolor(canvas_color)

    # Dibuja personaje
    personaje = dibujar_objeto(5, 5, 1, 2)
    raiz.mainloop()



# **********************************************
# Prueba
# Define cuadricula
# cuadricula = define_cuadricula(canvas_dimension, bloques_cantidad, bloque_dimension)

# Creación de cuadricula
# color_lineas = "white"
# dibujar_cuadricula(canvas_dimension, bloque_dimension, color_lineas)


# print("personaje: " + str(personaje.renglon) + " - " + str(personaje.columna) + " - " + str(personaje.orientacion))

# Prueba 1
# saltar(personaje)
# print("personaje: " + str(personaje.renglon) + " - " + str(personaje.columna) + " - " + str(personaje.orientacion))

# Prueba 2
# posicionar(personaje, 9, 9)
# print("personaje: " + str(personaje.renglon) + " - " + str(personaje.columna) + " - " + str(personaje.orientacion))

# Prueba 3
# girar_derecha(personaje)
# girar_izquierda(personaje)

# Prueba 4
# ocultar(personaje, True)

# Prueba 5
#dibujar_bloque(4, 5, 3)
#dibujar_bloque(5, 4, 1)
#dibujar_bloque(5, 6, 2)
#resp = camino_libre(personaje)
#if resp:
    #print("camino libre")
#else:
    #print("camino no libre")

# Prueba 6
# dibujar_bloque(4, 5, 3)
# dibujar_bloque(5, 4, 1)
# dibujar_bloque(5, 6, 2)
# resp = deteccion(personaje)
# print(resp)

# Prueba 7
#dibujar_bloque(5, 4, 1)
#dibujar_objeto(5, 4, 2, 0)
#resp = camino_libre(personaje)
#if resp:
    #print("camino libre")
#else:
    #print("camino no libre")
#eliminar_enemigo(personaje)
#resp = camino_libre(personaje)
#if resp:
    #print("camino libre")
#else:
    #print("camino no libre")

# Prueba 8
#personaje = crear_tortuga("white")
#color(personaje, "yellow")
#rotar_derecha(personaje, 225)
#trazo(personaje, True, 5);

#avanzar(personaje, 50)
#rotar_derecha(personaje, 90)

#avanzar(personaje, 50)
#rotar_derecha(personaje, 90)

#avanzar(personaje, 50)
#rotar_derecha(personaje, 90)

#avanzar(personaje, 50)
#rotar_derecha(personaje, 90)

# Prueba 9
#personaje = crear_tortuga("white")
#color(personaje, "yellow")
#mostrar_valor(personaje, "hola", 20)
#avanzar(personaje, 20)

#velocidad(tortuga, 0)

#for i in range(180):
    #avanzar(personaje, 100)
    #rotar_derecha(personaje, 30)
    #avanzar(personaje, 20)
    #rotar_izquierda(personaje, 60)
    #avanzar(personaje, 50)
    #rotar_derecha(personaje, 30)

    #trazo(personaje, False, 1)
    #colocar(personaje, 0, 0)
    #trazo(personaje, True, 1)

    #rotar_derecha(personaje, 2)

# Prueba 10
# dibujar_objeto(5, 4, 3, 0)
# resp = deteccion_objeto(personaje)
# print(resp)
# resp = deteccion_bloque(personaje)
# print(resp)
# mover(personaje, 1)
# recoger = recoger_objeto(personaje)
# saltar(personaje)
# recoger = dejar_objeto(personaje, recoger)
# mover(personaje, 1)

# **********************************************

