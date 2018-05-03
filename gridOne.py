import turtle

def colocarObjeto(canvas, x, y):
    tortuga = turtle.RawTurtle(canvas)
    tortuga.shape("turtle")
    tortuga.shapesize(1, 1, 1)
    tortuga.color("white")
    tortuga.setpos(x, y)
    return tortuga

def mover(tortuga, n):
    tortuga.forward(n)

def rotar(tortuga, n):
    tortuga.right(n)

def girarDerecha(tortuga):
    tortuga.right(90)

def girarIzquierda(tortuga):
    tortuga.left(90)

def ocultar(tortuga, bandera):
    if bandera:
        tortuga.showturtle()
    else:
        tortuga.hideturtle()

def posicion(tortuga, x, y):
    tortuga.setpos(x, y)

def color(tortuga, col):
    colores = {
        1: "yellow",
        2: "pink", 
        3: "purple",
        4: "blue",
        5: "orange",
        6: "green", 
        7: "white", 
        8: "gray", 
        9: "red",
        10: "black",      
    }
    tortuga.color(colores[col]);

def trazo(tortuga, bandera, tam):
    tortuga.width(tam)
    if bandera:
        tortuga.pendown()
    else:
        tortuga.penup()

def mostrarValor(tortuga, mensaje, tamano):
    tortuga.write(str(mensaje), True, align="center", font=("Arial", tamano, "normal"))

def colorFondo(ventana, col):
    colores = {
        1: "yellow",
        2: "pink", 
        3: "purple",
        4: "blue",
        5: "orange",
        6: "green", 
        7: "white", 
        8: "gray", 
        9: "red",
        10: "black",      
    }
    ventana.bgcolor(colores[col])

def dibujaCirculo(tortuga, radio):
    tortuga.circle(radio)

def rellenarForma(tortuga, bandera):
    if bandera:
        tortuga.begin_fill()
    else:
        tortuga.end_fill()