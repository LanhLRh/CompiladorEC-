from Simbolos import *

listaConstantes = []
listaCuadruplos = []
pilaMemoriaLocal = []
memEjecucion = {}
pilaApunCuadruplo = []

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
		print("Memoria Local:", pilaMemoriaLocal)
		if interfaceTortuga == True:
			#inicioMundo()
			pass

		# Operador del cuadruplo (primer elemento de este)
		operacionCuadruplo = listaCuadruplos[cuadruploActual].ope

		elif code['ver'] == operacionCuadruplo:
			operando1 = listaCuadruplos[cuadruploActual].op1
			limiteInf = listaCuadruplos[cuadruploActual].op2
			limiteSup = listaCuadruplos[cuadruploActual].reg

			offset = getValorMemoria(operando1, nivelAlcance)
			print("Offset:", offset)

			# Se verifica si el valor de indexacion al arreglo esta dentro de los limites posibles
			if offset < limiteInf or offset > limiteSup:
				finalizar("Indice fuera de rango")
				return

		elif code['finProc'] == operacionCuadruplo:
			# Se obtiene el apuntador a cuadruplo que se dejo dormido donde se invoco la rutina que acaba de terminar
			cuadruploActual = pilaApunCuadruplo.pop()
			
			# Se decrementa el nivel de entorno de los valores locales pero sin destruir el de la funcion recien terminada
			nivelAlcance -= 1
			cuadruploActual -= 1

			# Si el cuadruplo al que se regresa no tiene operaciones de referencia
			if listaCuadruplos[cuadruploActual].ope != "referencia":
				#Se 'destruye' toda la memoria de entorno local de la funcion que recien acaba de terminar pues ya no se requiere
				pilaMemoriaLocal.pop()

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
			direccionAlmacenar = encontrarDireccionAbs(listaCuadruplos[cuadruploActual].reg, nivelAlcance)
			print("DireccionAlmacenar:", direccionAlmacenar)
			print("Valor:", valor1)

			if direccionAlmacenar in memEjecucion: memEjecucion[direccionAlmacenar] = valor1
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

			#Se valida que la division sea valida
			if valorOp2 == 0:
				finalizar("ERROR: División entre cero")
				return
			
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

		elif code['+'] == operacionCuadruplo:
			op1 = listaCuadruplos[cuadruploActual].op1 		# Direaccion del Operando 1
			op2 = listaCuadruplos[cuadruploActual].op2 		# Direccion del Operando 2
			valorOp1 = getValorMemoria(op1, nivelAlcance)	# Obtener el valor del Operando 1
			valorOp2 = getValorMemoria(op2, nivelAlcance)	# Obtener el valor del Operando 2)

			# Direccion donde se almacenara el resultado de la operacion
			direccionAlmacenar = int(encontrarDireccionAbs(listaCuadruplos[cuadruploActual].reg, nivelAlcance))
			print("Suma:",valorOp1 + valorOp2)
			#print("Constante:",memEjecucion[op1])

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
			escrito = getValorMemoria(escritoDir, nivelAlcance)	# Obtener el valor de la direccion
			print("escribir", escrito)
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
