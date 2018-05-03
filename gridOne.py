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
    if col == 1:
        tortuga.color("green");

def trazo(tortuga, bandera, tam):
    tortuga.width(tam)
    if bandera:
        tortuga.pendown()
    else:
        tortuga.penup()
