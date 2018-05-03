from PyQt5 import QtWidgets, uic
import os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QTextOption, QTextCursor, QFontMetrics
from PyQt5.QtGui import (QColor, QPainter, QFont, QSyntaxHighlighter, QTextFormat, QTextCharFormat)
import SintaxisEC

# --------------------------------
# Creacion del mundo de la tortuga
# --------------------------------
import turtle
import tkinter as tk
from Bloque import *
from Objeto import *

canvas_dimension = 400
bloques_cantidad = 10
bloque_dimension = int(canvas_dimension / bloques_cantidad)
canvas_color = "royal blue"
tortuga = None

# Creación del canvas
raiz = tk.Tk()
raiz.title("Tortuga")
raiz.resizable(width=False, height=False)
canvas = tk.Canvas(master = raiz, width = canvas_dimension, height = canvas_dimension, bd = 0, highlightthickness = 0)
canvas.pack()

# Crea tortuga para configurar mundo
tortuga = turtle.RawTurtle(canvas)
tortuga.hideturtle()
ventana = tortuga.getscreen()
ventana.bgcolor(canvas_color)

from gridOne import *
# --------------------------------

import sys
from Cuadruplo import *
from Simbolos import *
from Memoria import *
from Gramatica import *
from gridOne import *

# Diccionario de valores globales donde la llave es la direccion y el valor es el 'valor' almacenado en la direccion
memEjecucion = {}				# Mapa de Memoria [Dirección, Contenido]
pilaMemoriaLocal = [{}]			# Pila de diccionarios con memoria local a las funciones
listaCuadruplos = []			# Lista de cuadruplos
pilaApunCuadruplo = []			# Pila de apuntadores de cuadruplos
cuadruploActual = 0				# Apunta al cuadruplo al que se esta ejecutando
nivelAlcance = 0				# Nivel alcance local (0 = Global, 1 = Local)
directorioProc = {}				# Directorio de procedimientos
listaConstantes = None

# Globales de la Interface Grafica
# Globales
app = None 				# Aplicación
ui = None 				# Elementos de la interface
cursor = None 			# Cursor
scrollbar = None 		# Barra de navegación vertical del area de codigo
tamanoFuente = 10		# Tamaño actual de la fuente de texto del codigo
numeroLinea = 0			# Numero de linea actual
nombreArchivo = None 	# Nombre del archivo de lectura/escritura
cargoArchivo = False	# Bandera que indica si se abrio un archivo


# Termina la ejecucion del programa y muestra un mensaje
def finalizar(mensaje):
	print(mensaje)
	return
	#sys.exit()

# Retorna la direccion correcta en la que se le debe almacenar un valor
def encontrarDireccionAbs(numDireccion, alcanceFuncion):
    #Se verifica si es una direccion indirecta
    if numDireccion < -1:
        #Se obtiene el valor de la verdadera direccion que almacena esta indirecta
        return getValorMemoria(abs(numDireccion), alcanceFuncion)
    else: return int(numDireccion)

#Recibe una direccion y nivel de alcance para retornar el valor de la estructura pertinente segun la misma direccion: memoria global o local
def getValorMemoria(numDireccion, alcanceFuncion = 0):
	#Se verifica si es una direccion indirecta
	if numDireccion < -1:
		# Se obtiene la verdadera direccion invocandose a si mismo
		numDireccion = getValorMemoria(abs(numDireccion), alcanceFuncion)

	# Verificar si es una direccion local o global
	# Direccion global
	if numDireccion < posInicial['intLocal'] or numDireccion > posLimite['booleanTemp']:
		# Verificar que la direccion de memoria existe
		if numDireccion in memEjecucion:
			# Regresa el valor de dicho espacio de memoria
			tipoDato = getTipo(numDireccion)
			if tipoDato == code['int']: valor = int(memEjecucion[numDireccion])
			elif tipoDato == code['dec']: valor = float(memEjecucion[numDireccion])
			elif tipoDato == code['boolean']: valor = bool(memEjecucion[numDireccion])
			else: valor = str(memEjecucion[numDireccion][1:-1])
			return valor
		# Si no esta inicializada, inicializar a valor default y regresar dicho valor
		else:
			if getTipo(numDireccion) == code['int']:
				memEjecucion[numDireccion] = 0
				return 0
			elif getTipo(numDireccion) == code['dec']:
				memEjecucion[numDireccion] = 0.0
				return 0.0
			elif getTipo(numDireccion) == code['boolean']:
				memEjecucion[numDireccion] = False
				return False
			else:
				memEjecucion[numDireccion] = ""
				return ""
	# Direccion local/temporal
	else:
		# Verificar que la direccion local este dentro de la memoria local de la función
		if numDireccion in pilaMemoriaLocal[alcanceFuncion]:
			# Regresa el valor de dicho espacio de memoria
			
			tipoDato = getTipo(numDireccion)
			if tipoDato == code['int']: valor = int(pilaMemoriaLocal[alcanceFuncion][numDireccion])
			elif tipoDato == code['dec']: valor = float(pilaMemoriaLocal[alcanceFuncion][numDireccion])
			elif tipoDato == code['boolean']: valor = bool(pilaMemoriaLocal[alcanceFuncion][numDireccion])
			else: valor = str(pilaMemoriaLocal[alcanceFuncion][numDireccion][1:-1])

			print(valor)
			return valor
		# Si no esta inicializada, inicializar a valor default y regresar dicho valor
		else:
			if getTipo(numDireccion) == code['int']:
				pilaMemoriaLocal[alcanceFuncion][numDireccion] = 0
				return 0
			elif getTipo(numDireccion) == code['dec']:
				pilaMemoriaLocal[alcanceFuncion][numDireccion] = 0.0
				return 0.0
			elif getTipo(numDireccion) == code['boolean']:
				pilaMemoriaLocal[alcanceFuncion][numDireccion] = False
				return False
			else:
				pilaMemoriaLocal[alcanceFuncion][numDireccion] = ""
				return ""

#Recibe una direccion y determina si es de tipo global o local
def esGlobal(numDireccion):
	#Se verifica si es una direccion indirecta
	if numDireccion < -1:
		#Se obtiene la verdadera direccion invocando a findValueInMemory que identifica en que estructura esta segun el absoluto de la direccion
		numDireccion = getValorMemoria(abs(numDireccion), nivelAlcance)

	# Se trata de una direccion global
	if numDireccion < posInicial['intLocal'] or numDireccion > posLimite['booleanTemp']: return True
	# Se trata de una direccion local o temporal
	else: return False

# Indica si una direccion almacena valor numerico entero
def esNumero(numDireccion):
    # Se verifica si es una direccion indirecta
    if numDireccion < -1:
        #Se obtiene la verdadera direccion invocando a findValueInMemory que identifica en que estructura esta segun el absoluto de la direccion
        numDireccion = getValorMemoria(abs(numDireccion), nivelAlcance)

    if getTipo(numDireccion) == code['int']:
        return True
    return False

interfaceTortuga = False

def procesarCuadruplos():

	global cuadruploActual, pilaMemoriaLocal, listaCuadruplos, memEjecucion, nivelAlcance, interfaceTortuga, pilaApunCuadruplo

	cuadruploActual = 0
	pilaMemoriaLocal.clear()
	interfaceTortuga = False
	for contenido, direccion in listaConstantes.items():
		memEjecucion[int(direccion)] = contenido 		# Guardar (Direccion : Contenido)

	cantidadCuadruplos = len(listaCuadruplos)
	# Agregar Memoria local para la funcion principal
	pilaMemoriaLocal.append({})

	while cuadruploActual < cantidadCuadruplos:
		
		if interfaceTortuga == True:
			inicioMundo()

		# Operador del cuadruplo (primer elemento de este)
		operacionCuadruplo = listaCuadruplos[cuadruploActual].ope
		# Ejecutar el cuadruplo
		if code['goto'] == operacionCuadruplo:
			cuadDestino = listaCuadruplos[cuadruploActual].reg		# Cuadruplo a donde se hara el salto
			cuadruploActual = cuadDestino						# Actualizar el cuadruplo actual
			cuadruploActual -= 1			# Restar 1 porque al final del ciclo se aumenta 1

		elif code['gotof'] == operacionCuadruplo:
			    
			operando1 = listaCuadruplos[cuadruploActual].op1
			valor1 = getValorMemoria(operando1, nivelAlcance)

			if not valor1:
				cuadDestino = listaCuadruplos[cuadruploActual].reg
				cuadruploActual = cuadDestino
				cuadruploActual -= 1

		elif code['gosub'] == operacionCuadruplo:
			# Se mete el a la pila de apuntadores a cuadruplos el numero del siguiente cuadruplo que se dormira
			pilaApunCuadruplo.append(cuadruploActual + 1)
			
			# Se obtiene el numero de cuadruplo destino y se actualiza el mismo
			destino = listaCuadruplos[cuadruploActual].reg
			cuadruploActual = destino

			# Se incrementa el nuevo nivel de entorno de valores locales a uno mayor
			nivelAlcance = nivelAlcance + 1
			cuadruploActual -= 1

		elif code['ERA'] == operacionCuadruplo:
			# Se le agrega una nuevo entorno de variables locales para la funcion a ser invocada
			pilaMemoriaLocal.append({})

		elif code['finProc'] == operacionCuadruplo:
			# Se obtiene el apuntador a cuadruplo que se dejo dormido donde se invoco la rutina que acaba de terminar
			cuadruploActual = pilaApunCuadruplo.pop()
			
			# Se decrementa el nivel de entorno de los valores locales pero sin destruir el de la funcion recien terminada
			nivelAlcance -= 1
			cuadruploActual -= 1

			# Si el cuadruplo al que se regresa no tiene operaciones de referencia
			print(cuadruploActual)
			if listaCuadruplos[cuadruploActual].ope != "referencia":
				#Se 'destruye' toda la memoria de entorno local de la funcion que recien acaba de terminar pues ya no se requiere
				pilaMemoriaLocal.pop()

		# Aignación de lo que regreso la función
		elif code['retu'] == operacionCuadruplo:
			operando1 = listaCuadruplos[cuadruploActual].op1
			valor1 = getValorMemoria(operando1, nivelAlcance)

			#Se obtiene la direccion absoluta en caso de que sea una direccion indirecta
			direccionAlmacenar = encontrarDireccionAbs(listaCuadruplos[cuadruploActual].reg, nivelAlcance)

			if esGlobal(direccionAlmacenar):
				# Se checa si la direccion a asignar valor es entera para almacenar solo la parte entera
				if esNumero(direccionAlmacenar): memEjecucion[direccionAlmacenar] = int(valor1)
				else: memEjecucion[direccionAlmacenar] = valor1
			else:
				#Se checa si la direccion a asignar valor es entera para almacenar solo la parte entera
				if esNumero(direccionAlmacenar): pilaMemoriaLocal[nivelAlcance][direccionAlmacenar] = int(valor1)
				else: pilaMemoriaLocal[nivelAlcance][direccionAlmacenar] = valor1

		# 'Regresa' de la función
		elif code['regresa'] == operacionCuadruplo:
			operando1 = listaCuadruplos[cuadruploActual].op1
			valor1 = getValorMemoria(operando1, nivelAlcance)

			#Se obtiene la direccion absoluta en caso de que sea una direccion indirecta
			direccionAlmacenar = int(encontrarDireccionAbs(listaCuadruplos[cuadruploActual].reg, nivelAlcance))

			#Se checa si la direccion a asignar valor es entera para almacenar solo la parte entera
			if esNumero(direccionAlmacenar): memEjecucion[direccionAlmacenar] = int(valor1)
			else: memEjecucion[direccionAlmacenar] = valor1

		elif code['parametro'] == operacionCuadruplo:

			operando1 = listaCuadruplos[cuadruploActual].op1
			valor1 = getValorMemoria(operando1, nivelAlcance)

			#Se obtiene la direccion absoluta en caso de que sea una direccion indirecta
			direccionAlmacenar = encontrarDireccionAbs(listaCuadruplos[cuadruploActual].reg, nivelAlcance)

			# Se inicializa valor de la variable local en la funcion a ejecutarse
			pilaMemoriaLocal[nivelAlcance + 1][direccionAlmacenar] = valor1

		elif code['='] == operacionCuadruplo:
			
			operando1 = listaCuadruplos[cuadruploActual].op1
			valor1 = getValorMemoria(operando1, nivelAlcance)

			#Se obtiene la direccion absoluta en caso de que sea una direccion indirecta
			direccionAlmacenar = int(encontrarDireccionAbs(listaCuadruplos[cuadruploActual].reg, nivelAlcance))

			if direccionAlmacenar in memEjecucion: memEjecucion[direccionAlmacenar] = valorOp1 * valorOp2
			else: pilaMemoriaLocal[nivelAlcance][direccionAlmacenar] = valor1

		elif code['*'] == operacionCuadruplo:
			op1 = listaCuadruplos[cuadruploActual].op1 		# Direaccion del Operando 1
			op2 = listaCuadruplos[cuadruploActual].op2 		# Direccion del Operando 2
			valorOp1 = getValorMemoria(op1, nivelAlcance)	# Obtener el valor del Operando 1
			valorOp2 = getValorMemoria(op2, nivelAlcance)	# Obtener el valor del Operando 2

			# Direccion donde se almacenara el resultado de la operacion
			direccionAlmacenar = encontrarDireccionAbs(listaCuadruplos[cuadruploActual].reg, nivelAlcance)
			# Se almacena valor global dentro de la estructura que maneja almacenamiento global
			if direccionAlmacenar in memEjecucion: memEjecucion[direccionAlmacenar] = valorOp1 * valorOp2
			#Se almacena valor local dentro de la estructura que maneja almacenamiento local
			else: pilaMemoriaLocal[nivelAlcance][direccionAlmacenar] = valorOp1 * valorOp2

		elif code['/'] == operacionCuadruplo:
			op1 = listaCuadruplos[cuadruploActual].op1 		# Direaccion del Operando 1
			op2 = listaCuadruplos[cuadruploActual].op2 		# Direccion del Operando 2
			valorOp1 = getValorMemoria(op1, nivelAlcance)	# Obtener el valor del Operando 1
			valorOp2 = getValorMemoria(op2, nivelAlcance)	# Obtener el valor del Operando 2
			
			# Direccion donde se almacenara el resultado de la operacion
			direccionAlmacenar = encontrarDireccionAbs(listaCuadruplos[cuadruploActual].reg, nivelAlcance)
			# Se almacena valor global dentro de la estructura que maneja almacenamiento global
			if direccionAlmacenar in memEjecucion: memEjecucion[direccionAlmacenar] = valorOp1 / valorOp2
			#Se almacena valor local dentro de la estructura que maneja almacenamiento local
			else: pilaMemoriaLocal[nivelAlcance][direccionAlmacenar] = valorOp1 / valorOp2

		elif code['-'] == operacionCuadruplo:
			op1 = listaCuadruplos[cuadruploActual].op1 		# Direaccion del Operando 1
			op2 = listaCuadruplos[cuadruploActual].op2 		# Direccion del Operando 2
			valorOp1 = getValorMemoria(op1, nivelAlcance)	# Obtener el valor del Operando 1
			valorOp2 = getValorMemoria(op2, nivelAlcance)	# Obtener el valor del Operando 2
			
			# Direccion donde se almacenara el resultado de la operacion
			direccionAlmacenar = encontrarDireccionAbs(listaCuadruplos[cuadruploActual].reg, nivelAlcance)
			# Se almacena valor global dentro de la estructura que maneja almacenamiento global
			if direccionAlmacenar in memEjecucion: memEjecucion[direccionAlmacenar] = valorOp1 - valorOp2
			#Se almacena valor local dentro de la estructura que maneja almacenamiento local
			else: pilaMemoriaLocal[nivelAlcance][direccionAlmacenar] = valorOp1 - valorOp2

		elif code['-'] == operacionCuadruplo:
			op1 = listaCuadruplos[cuadruploActual].op1 		# Direaccion del Operando 1
			op2 = listaCuadruplos[cuadruploActual].op2 		# Direccion del Operando 2
			valorOp1 = getValorMemoria(op1, nivelAlcance)	# Obtener el valor del Operando 1
			valorOp2 = getValorMemoria(op2, nivelAlcance)	# Obtener el valor del Operando 2
			
			# Direccion donde se almacenara el resultado de la operacion
			direccionAlmacenar = encontrarDireccionAbs(listaCuadruplos[cuadruploActual].reg, nivelAlcance)
			# Se almacena valor global dentro de la estructura que maneja almacenamiento global
			if direccionAlmacenar in memEjecucion: memEjecucion[direccionAlmacenar] = valorOp1 - valorOp2
			#Se almacena valor local dentro de la estructura que maneja almacenamiento local
			else: pilaMemoriaLocal[nivelAlcance][direccionAlmacenar] = valorOp1 - valorOp2

		elif code['+'] == operacionCuadruplo:
			op1 = listaCuadruplos[cuadruploActual].op1 		# Direaccion del Operando 1
			op2 = listaCuadruplos[cuadruploActual].op2 		# Direccion del Operando 2
			valorOp1 = getValorMemoria(op1, nivelAlcance)	# Obtener el valor del Operando 1
			valorOp2 = getValorMemoria(op2, nivelAlcance)	# Obtener el valor del Operando 2)

			# Direccion donde se almacenara el resultado de la operacion
			direccionAlmacenar = int(encontrarDireccionAbs(listaCuadruplos[cuadruploActual].reg, nivelAlcance))
			print(pilaMemoriaLocal)
			# Se almacena valor global dentro de la estructura que maneja almacenamiento global
			if esGlobal(direccionAlmacenar):
				
				memEjecucion[direccionAlmacenar] = valorOp1 + valorOp2
			# Se almacena valor local dentro de la estructura que maneja almacenamiento local
			else:
				pilaMemoriaLocal[nivelAlcance][direccionAlmacenar] = valorOp1 + valorOp2

		elif code['|'] == operacionCuadruplo:
			op1 = listaCuadruplos[cuadruploActual].op1 		# Direaccion del Operando 1
			op2 = listaCuadruplos[cuadruploActual].op2 		# Direccion del Operando 2
			valorOp1 = getValorMemoria(op1, nivelAlcance)	# Obtener el valor del Operando 1
			valorOp2 = getValorMemoria(op2, nivelAlcance)	# Obtener el valor del Operando 2
			
			# Direccion donde se almacenara el resultado de la operacion
			direccionAlmacenar = encontrarDireccionAbs(listaCuadruplos[cuadruploActual].reg, nivelAlcance)
			# Se almacena valor global dentro de la estructura que maneja almacenamiento global
			if direccionAlmacenar in memEjecucion: memEjecucion[direccionAlmacenar] = valorOp1 | valorOp2
			#Se almacena valor local dentro de la estructura que maneja almacenamiento local
			else: pilaMemoriaLocal[nivelAlcance][direccionAlmacenar] = valorOp1 | valorOp2

		elif code['&'] == operacionCuadruplo:
			op1 = listaCuadruplos[cuadruploActual].op1 		# Direaccion del Operando 1
			op2 = listaCuadruplos[cuadruploActual].op2 		# Direccion del Operando 2
			valorOp1 = getValorMemoria(op1, nivelAlcance)	# Obtener el valor del Operando 1
			valorOp2 = getValorMemoria(op2, nivelAlcance)	# Obtener el valor del Operando 2
			
			# Direccion donde se almacenara el resultado de la operacion
			direccionAlmacenar = encontrarDireccionAbs(listaCuadruplos[cuadruploActual].reg, nivelAlcance)
			# Se almacena valor global dentro de la estructura que maneja almacenamiento global
			if direccionAlmacenar in memEjecucion: memEjecucion[direccionAlmacenar] = valorOp1 & valorOp2
			#Se almacena valor local dentro de la estructura que maneja almacenamiento local
			else: pilaMemoriaLocal[nivelAlcance][direccionAlmacenar] = valorOp1 & valorOp2

		elif code['%'] == operacionCuadruplo:
			op1 = listaCuadruplos[cuadruploActual].op1 		# Direaccion del Operando 1
			op2 = listaCuadruplos[cuadruploActual].op2 		# Direccion del Operando 2
			valorOp1 = getValorMemoria(op1, nivelAlcance)	# Obtener el valor del Operando 1
			valorOp2 = getValorMemoria(op2, nivelAlcance)	# Obtener el valor del Operando 2
			
			# Direccion donde se almacenara el resultado de la operacion
			direccionAlmacenar = encontrarDireccionAbs(listaCuadruplos[cuadruploActual].reg, nivelAlcance)
			# Se almacena valor global dentro de la estructura que maneja almacenamiento global
			if direccionAlmacenar in memEjecucion: memEjecucion[direccionAlmacenar] = valorOp1 % valorOp2
			#Se almacena valor local dentro de la estructura que maneja almacenamiento local
			else: pilaMemoriaLocal[nivelAlcance][direccionAlmacenar] = valorOp1 % valorOp2

		elif code['*'] == operacionCuadruplo:
			op1 = listaCuadruplos[cuadruploActual].op1 		# Direaccion del Operando 1
			op2 = listaCuadruplos[cuadruploActual].op2 		# Direccion del Operando 2
			valorOp1 = getValorMemoria(op1, nivelAlcance)	# Obtener el valor del Operando 1
			valorOp2 = getValorMemoria(op2, nivelAlcance)	# Obtener el valor del Operando 2
			
			# Direccion donde se almacenara el resultado de la operacion
			direccionAlmacenar = encontrarDireccionAbs(listaCuadruplos[cuadruploActual].reg, nivelAlcance)
			# Se almacena valor global dentro de la estructura que maneja almacenamiento global
			if direccionAlmacenar in memEjecucion: memEjecucion[direccionAlmacenar] = valorOp1 * valorOp2
			#Se almacena valor local dentro de la estructura que maneja almacenamiento local
			else: pilaMemoriaLocal[nivelAlcance][direccionAlmacenar] = valorOp1 * valorOp2

		elif code['>'] == operacionCuadruplo:
			op1 = listaCuadruplos[cuadruploActual].op1 		# Direaccion del Operando 1
			op2 = listaCuadruplos[cuadruploActual].op2 		# Direccion del Operando 2
			valorOp1 = getValorMemoria(op1, nivelAlcance)	# Obtener el valor del Operando 1
			valorOp2 = getValorMemoria(op2, nivelAlcance)	# Obtener el valor del Operando 2
			
			# Direccion donde se almacenara el resultado de la operacion
			direccionAlmacenar = encontrarDireccionAbs(listaCuadruplos[cuadruploActual].reg, nivelAlcance)
			# Se almacena valor global dentro de la estructura que maneja almacenamiento global
			if direccionAlmacenar in memEjecucion: memEjecucion[direccionAlmacenar] = valorOp1 > valorOp2
			#Se almacena valor local dentro de la estructura que maneja almacenamiento local
			else: pilaMemoriaLocal[nivelAlcance][direccionAlmacenar] = valorOp1 > valorOp2

		elif code['<'] == operacionCuadruplo:
			op1 = listaCuadruplos[cuadruploActual].op1 		# Direaccion del Operando 1
			op2 = listaCuadruplos[cuadruploActual].op2 		# Direccion del Operando 2
			valorOp1 = getValorMemoria(op1, nivelAlcance)	# Obtener el valor del Operando 1
			valorOp2 = getValorMemoria(op2, nivelAlcance)	# Obtener el valor del Operando 2
			
			# Direccion donde se almacenara el resultado de la operacion
			direccionAlmacenar = encontrarDireccionAbs(listaCuadruplos[cuadruploActual].reg, nivelAlcance)
			# Se almacena valor global dentro de la estructura que maneja almacenamiento global
			if direccionAlmacenar in memEjecucion: memEjecucion[direccionAlmacenar] = valorOp1 < valorOp2
			#Se almacena valor local dentro de la estructura que maneja almacenamiento local
			else: pilaMemoriaLocal[nivelAlcance][direccionAlmacenar] = valorOp1 < valorOp2

		elif code['>='] == operacionCuadruplo:
			op1 = listaCuadruplos[cuadruploActual].op1 		# Direaccion del Operando 1
			op2 = listaCuadruplos[cuadruploActual].op2 		# Direccion del Operando 2
			valorOp1 = getValorMemoria(op1, nivelAlcance)	# Obtener el valor del Operando 1
			valorOp2 = getValorMemoria(op2, nivelAlcance)	# Obtener el valor del Operando 2
			
			# Direccion donde se almacenara el resultado de la operacion
			direccionAlmacenar = encontrarDireccionAbs(listaCuadruplos[cuadruploActual].reg, nivelAlcance)
			# Se almacena valor global dentro de la estructura que maneja almacenamiento global
			if direccionAlmacenar in memEjecucion: memEjecucion[direccionAlmacenar] = valorOp1 >= valorOp2
			#Se almacena valor local dentro de la estructura que maneja almacenamiento local
			else: pilaMemoriaLocal[nivelAlcance][direccionAlmacenar] = valorOp1 >= valorOp2

		elif code['<='] == operacionCuadruplo:
			op1 = listaCuadruplos[cuadruploActual].op1 		# Direaccion del Operando 1
			op2 = listaCuadruplos[cuadruploActual].op2 		# Direccion del Operando 2
			valorOp1 = getValorMemoria(op1, nivelAlcance)	# Obtener el valor del Operando 1
			valorOp2 = getValorMemoria(op2, nivelAlcance)	# Obtener el valor del Operando 2
			
			# Direccion donde se almacenara el resultado de la operacion
			direccionAlmacenar = encontrarDireccionAbs(listaCuadruplos[cuadruploActual].reg, nivelAlcance)
			# Se almacena valor global dentro de la estructura que maneja almacenamiento global
			if direccionAlmacenar in memEjecucion: memEjecucion[direccionAlmacenar] = valorOp1 <= valorOp2
			#Se almacena valor local dentro de la estructura que maneja almacenamiento local
			else: pilaMemoriaLocal[nivelAlcance][direccionAlmacenar] = valorOp1 <= valorOp2

		elif code['=='] == operacionCuadruplo:
			op1 = listaCuadruplos[cuadruploActual].op1 		# Direaccion del Operando 1
			op2 = listaCuadruplos[cuadruploActual].op2 		# Direccion del Operando 2
			valorOp1 = getValorMemoria(op1, nivelAlcance)	# Obtener el valor del Operando 1
			valorOp2 = getValorMemoria(op2, nivelAlcance)	# Obtener el valor del Operando 2
			
			# Direccion donde se almacenara el resultado de la operacion
			direccionAlmacenar = encontrarDireccionAbs(listaCuadruplos[cuadruploActual].reg, nivelAlcance)
			# Se almacena valor global dentro de la estructura que maneja almacenamiento global
			if direccionAlmacenar in memEjecucion: memEjecucion[direccionAlmacenar] = valorOp1 == valorOp2
			#Se almacena valor local dentro de la estructura que maneja almacenamiento local
			else: pilaMemoriaLocal[nivelAlcance][direccionAlmacenar] = valorOp1 == valorOp2

			print("Direccion Almacenar", direccionAlmacenar)
			print("Memoria EJecucion", memEjecucion)
			print("Mem Local", pilaMemoriaLocal)

		elif code['!='] == operacionCuadruplo:
			op1 = listaCuadruplos[cuadruploActual].op1 		# Direaccion del Operando 1
			op2 = listaCuadruplos[cuadruploActual].op2 		# Direccion del Operando 2
			valorOp1 = getValorMemoria(op1, nivelAlcance)	# Obtener el valor del Operando 1
			valorOp2 = getValorMemoria(op2, nivelAlcance)	# Obtener el valor del Operando 2
			
			# Direccion donde se almacenara el resultado de la operacion
			direccionAlmacenar = encontrarDireccionAbs(listaCuadruplos[cuadruploActual].reg, nivelAlcance)
			# Se almacena valor global dentro de la estructura que maneja almacenamiento global
			if direccionAlmacenar in memEjecucion: memEjecucion[direccionAlmacenar] = valorOp1 != valorOp2
			#Se almacena valor local dentro de la estructura que maneja almacenamiento local
			else: pilaMemoriaLocal[nivelAlcance][direccionAlmacenar] = valorOp1 != valorOp2

		elif code['escribir'] == operacionCuadruplo:

			escritoDir = listaCuadruplos[cuadruploActual].op1 		# Direccion de la temporal a imprimir
			print("Direccion a imprimir:", escritoDir)
			escrito = getValorMemoria(escritoDir, nivelAlcance)	# Obtener el valor de la direccion
			print("Valor escrito:", escrito)
			mostrarEnConsola(escrito)

		elif code['fin'] == operacionCuadruplo:
			return

		# ------------------------------------------

		elif code['colocarObjeto'] == operacionCuadruplo:
			v_1 = getValorMemoria(listaCuadruplos[cuadruploActual].op1, nivelAlcance)
			v_2 = getValorMemoria(listaCuadruplos[cuadruploActual+1].op1, nivelAlcance)
			v_3 = getValorMemoria(listaCuadruplos[cuadruploActual+2].op1, nivelAlcance)
			cuadruploActual = cuadruploActual + 2
			global tortuga
			tortuga = colocarObjeto(canvas, v_2, v_3)

		elif code['mover'] == operacionCuadruplo:
			v_1 = getValorMemoria(listaCuadruplos[cuadruploActual].op1, nivelAlcance)
			mover(tortuga, v_1)

		elif code['rotar'] == operacionCuadruplo:
			v_1 = getValorMemoria(listaCuadruplos[cuadruploActual].op1, nivelAlcance)
			rotar(tortuga, v_1)

		elif code['girarDerecha'] == operacionCuadruplo:
			girarDerecha(tortuga)
		
		elif code['girarIzquierda'] == operacionCuadruplo:
			girarIzquierda(tortuga)

		elif code['ocultar'] == operacionCuadruplo:
			v_1 = getValorMemoria(listaCuadruplos[cuadruploActual].op1, nivelAlcance)
			ocultar( tortuga, v_1)

		elif code['posicion'] == operacionCuadruplo:
			v_1 = getValorMemoria(listaCuadruplos[cuadruploActual].op1, nivelAlcance)
			v_2 = getValorMemoria(listaCuadruplos[cuadruploActual+1].op1, nivelAlcance)
			cuadruploActual = cuadruploActual + 1
			posicion(tortuga, v_1, v_2)

		elif code['color'] == operacionCuadruplo:
			v_1 = getValorMemoria(listaCuadruplos[cuadruploActual].op1, nivelAlcance)
			color(tortuga, v_1)

		elif code['trazo'] == operacionCuadruplo:
			v_1 = getValorMemoria(listaCuadruplos[cuadruploActual].op1, nivelAlcance)
			v_2 = getValorMemoria(listaCuadruplos[cuadruploActual+1].op1, nivelAlcance)
			cuadruploActual = cuadruploActual + 1
			trazo(tortuga, v_1, v_2)
		# ------------------------------------------

		elif code['leer'] == operacionCuadruplo:
			# Direccion donde se almacenara el resultado de la operacion
			direccionAlmacenar = listaCuadruplos[cuadruploActual].op1
			mensajeAMostrar = listaCuadruplos[cuadruploActual].op2

			respuestaUsuario = getTexto(mensajeAMostrar)
			#En caso de excepcion arrojada esta variable indica a que se trato de castear el valor de usuario
			tipoValor = 0
			try: 
				#Se identifica el tipo de direccion para saber al tipo de valor que se debe castear el valor ingresado por el usuario
				if getTipo(direccionAlmacenar) == code['int']:
					tipoValor = 0
					valor = int(respuestaUsuario)
				elif getTipo(direccionAlmacenar) == code['dec']:
					tipoValor = 1
					valor = float(respuestaUsuario)
				elif getTipo(direccionAlmacenar) == code['boolean']:
					tipoValor = 2
					if respuestaUsuario == 'verdadero': valor = True
					elif respuestaUsuario == 'falso': valor = False
					else:
						#No se puede castear a booleano
						mostrarEnConsola("Error de ejecución. No se puede convertir a boolean.")
						return
				else:
					tipoValor = 3
					# Se almacena un string directo
					valor = respuestaUsuario
			# Se lanzo una excepcion al tratar de castear el valor
			except:
				if tipoValor == 0:
					mostrarEnConsola("Error de ejecución. No se puede convertir a entero.")
				elif tipoValor == 1:
					mostrarEnConsola("Error de ejecución. No se puede convertir a decimal.")
				elif tipoValor == 2:
					mostrarEnConsola("Error de ejecución. No se puede convertir a boolean.")
				else:
					mostrarEnConsola("Error de ejecución. No se puede convertir a string.")
				return
		

		# Aumentar el contador de cuadruplos
		cuadruploActual += 1

def mainMaquinaVirtual():
	# Lectura de archivo
	global directorioProc, listaCuadruplos, listaConstantes

	directorioProc = getDirectorioProcedimientos()
	
	listaCuadruplos = getCuadruplos()
	
	listaConstantes = getDirConstantes()
	print("Inicializalizacion de Maquina Virtual")

	# e agregan a memoria constantes predefinidas booleanas
	memEjecucion[int(posInicial['booleanCTE'])] = False
	memEjecucion[int(posInicial['booleanCTE'])+1] = True

	procesarCuadruplos()
	print(memEjecucion)




# Función que compila el programa
def compilar():
	if not ui.txtCodigo.toPlainText() == "":
		archivo = open("archErroresCompilacion.txt", "w")
		archivo.close()
		codigo = ui.txtCodigo.toPlainText()
		resultado = parser.parse(codigo)
		#try: resultado = parser.parse(codigo)
		#except: pass
		mainMaquinaVirtual()
		mostrarEnConsola("")
	else:
		mensaje("No hay codigo", "Necesitas escribir codigo para poder compilar.")

def getTexto(mensaje):
	ex = QWidget()
	text, okPressed = QInputDialog.getText(ui.central_widget, "-",mensaje, QLineEdit.Normal, "")
	return text

# Ejecuta el input en la consola de comandos
def ejecutarInput():
	global ui
	comando = ui.lnInput.text()
	ui.lnInput.clear()
	mostrarEnConsola(comando)

# Función que actualiza el tamaño del tab deacuerdo al tamaño de font
def actualizarTab():
	font = QFont('Consolas', tamanoFuente)		# Font usada en el editor
	anchoFont = QFontMetrics(font).width(" ")	# Medida en pixeles de un espacio
	ui.txtCodigo.setTabStopWidth(4 * anchoFont) # Actualizar tamaño de tab

# Aumenta el tamaño de la letra del codigo
def aumentarLetra():
	global ui, tamanoFuente
	if tamanoFuente < 50:
		tamanoFuente += 1
		ui.txtCodigo.setFont(QFont("Consolas", tamanoFuente))
		actualizarTab()

# Disminuye el tamaño de la letra del codigo
def disminuirLetra():
	global ui, tamanoFuente
	if tamanoFuente > 4:
		tamanoFuente -= 1
		ui.txtCodigo.setFont(QFont("Consolas", tamanoFuente))
		actualizarTab()

# Coloca la salida de la consola en el cuadro de texto
def mostrarEnConsola(salida = ""):
	if salida == "":
		global ui, app, cursor, scrollbar, numeroLinea
		# Mover el cursor al final
		cursor.movePosition(QTextCursor.End)
		ui.txtCmd.setTextCursor(cursor)

		# Insertar errores de compilación en la cmd
		archivo = open("archErroresCompilacion.txt", "r") 
		contenidoArch = archivo.read()
		if contenidoArch != "":
			ui.txtCmd.insertPlainText(str(numeroLinea) + "> " + contenidoArch + '\n')
			numeroLinea += 1	# Aumentar contador

		# Mover scrollbar
		scrollbar.setValue(scrollbar.maximum())
	else:
		# Muestra mensaje recibido como parametro
		mensajeSalida = str(str(numeroLinea) + "> " + str(salida) + "\n")
		ui.txtCmd.insertPlainText(mensajeSalida)
		numeroLinea += 1	# Aumentar contador

# Muetra un mensaje como ventana emergente
def mensaje(titulo="Advertencia", mensaje=""):
	QMessageBox.information(None, titulo, mensaje)

# Guarda el codigo actual en un archivo
def guardarArchivo():
	global nombreArchivo, cargoArchivo
	# Si hay un archivo cargado, lo sobreescribe
	if cargoArchivo == True:
		print('Archivo Guardado')
		with open(nombreArchivo[0], 'w') as archivo:
				codigo = ui.txtCodigo.toPlainText()
				archivo.write(codigo)
	# Si no, crea uno nuevo
	else:
		# Seleccionar donde guarda y como llamar al archivo
		nombreArchivo = QFileDialog.getSaveFileName(ui.central_widget, 'Guardar', os.getenv('HOME'))
		# Verificar que se selecciono archivo
		if nombreArchivo != ('', ''):
			with open(nombreArchivo[0], 'w') as archivo:
				codigo = ui.txtCodigo.toPlainText()
				archivo.write(codigo)
	# Informar que se guardo el archivo
	mostrarEnConsola("Archivo Guardado")

# Carga el contenido de un archivo en el area de codigo
def abrirArchivo():
	global nombreArchivo, cargoArchivo
	# Buscar archivo a abrir
	nombreArchivo = QFileDialog.getOpenFileName(ui.central_widget, 'Abrir', os.getenv('HOME'))

	# Si si se selecciono un archivo, cargarlo
	if nombreArchivo != ('', ''):
		cargoArchivo = True
		print('Cargo archivo', cargoArchivo)
		with open(nombreArchivo[0], 'r') as archivo:
			codigo = archivo.read()
			ui.txtCodigo.setPlainText(codigo)

# Limpia la pantalla y cierra el archivo actual
def nuevoArchivo():
	global nombreArchivo, cargoArchivo

	nombreArchivo = None
	cargoArchivo = False
	limpiarTexto(ui)
	mostrarEnConsola("Nuevo archivo abierto")

# Limpia el contenido de la caja de texto
def limpiarTexto(self):
    self.txtCodigo.clear()

# Cambia el area de codigo (no funciona actualmente)
def substituirCodigo():
	# Substituir la txtCodigo
	ui.mainLayout.removeWidget(ui.txtCodigo)
	ui.txtCodigo.deleteLater()
	ui.txtCodigo = None

	# Editor con lineas de texto (falta integrar)
	txtCodigo = EditorCodigo.QCodeEditor(DISPLAY_LINE_NUMBERS=True, 
                     HIGHLIGHT_CURRENT_LINE=True,
                     SyntaxHighlighter=SintaxisEC.ResaltadorLineas)
	ui.mainLayout.insertWidget(1, txtCodigo)


# Metodo main - Inicializa todos los elementos en pantalla
def main():
	global ui, app, cursor, scrollbar
    #sys.exit(app.exec_())
    # Inicialización de aplicación
	#app = QtWidgets.QApplication([])
	app = QApplication([])
	# Inicializar ventana y elementos
	ui = uic.loadUi("IDE2.ui")
	
	# Configurar colores de txtCodigo
	ui.txtCodigo.setStyleSheet("""QPlainTextEdit{ 
		color: #ccc; 
		background-color: #2b2b2b;}""")

	# Tamaño del tab
	actualizarTab()

	# Resaltar palabras de la gramatica
	highlight = SintaxisEC.ResaltadorLineas(ui.txtCodigo.document())

	# Comportamiento de los botones
	ui.btnCompilar.clicked.connect(compilar)
	ui.btnMas.clicked.connect(aumentarLetra)
	ui.btnMenos.clicked.connect(disminuirLetra)
	ui.btnGuardar.clicked.connect(guardarArchivo)
	ui.btnAbrir.clicked.connect(abrirArchivo)
	ui.btnNuevo.clicked.connect(nuevoArchivo)

	# Propiedades de la consola
	ui.txtCmd.setReadOnly(True)								# Solo lectura
	ui.txtCodigo.document().setMaximumBlockCount(500)
	ui.txtCmd.setWordWrapMode(QTextOption.WrapAnywhere)

	# Controles
	cursor = ui.txtCmd.textCursor()
	scrollbar = ui.txtCmd.verticalScrollBar()

	# Interpretación de señales (teclas)
	ui.lnInput.returnPressed.connect(ejecutarInput)

	#substituirCodigo() # Hay problemas con esto
	#manejoArchivo = Archivo()

	# Mostrar interface
	ui.show()
	# Ejecutar aplicación
	app.exec()


# Llamada al main
if __name__ == "__main__":
    main()

raiz.mainloop()
# ---------------