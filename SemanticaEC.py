import sys
from Cuadruplo import *
from Simbolos import *
from Memoria import *
from Cubo import *

# SEMANTICA ===================================================================================================
# Directorio de procedimientos
dirProcedimientos = {}
lineaActual = 1

def setLineaActual(num):
	global lineaActual
	lineaActual = num
def getLineaActual():
	global lineaActual
	return lineaActual

# Guarda el ultimo tipo de dato parseado. Su valor es el ultimo tipo de dato declarado
tipoActual = ''
tipoFuncion = ''
# Guarda la funcion actual que se esta parseando. Su valor se actualiza si se entra a parsear una nueva funcion
funcionActual = ''
funcionInvocada = ''
# Pila que guarda los operadores pendientes por resolver
pilaOperadores = []
# Pila que guardar las direcciones de los operandos pendientes por resolver
pilaOperandos = []
# Pila de saltos que garda cuadruplos pendientes por llenar
pilaSaltos = []
# Lista que almacena todos los cuadruplos generados
cuadruplos = []

numParametros = 1 # Numero de parametros
tamanoActual = 0  # Tamaño del arreglo
ERROR = False

# Cubo semantico
cubo = Cubo()

def p_procFinal(p):
	'procFinal : '
	#print(dirProcedimientos)
	print(pilaOperadores)
	print(pilaOperandos)
	print(pilaSaltos)
	imprimir()
	#finalizar("Compilación Exitosa")

def regresaDirProcedimientos():
	return dirProcedimientos

def imprimir():
	for index, cuadruplo in enumerate(cuadruplos):
		print("{} -\t{},\t{},\t{},\t{}".format(index, simbol(cuadruplo.ope), cuadruplo.op1, cuadruplo.op2, cuadruplo.reg))
	print("--------------------")

# Crea el directorio de procedimientos y variables
def p_NP1_DirProced(p):
	'NP1_DirProced : '
	global dirProcedimientos
	# Inicializar el directorio de procedimientos con los espacios para funciones y variables
	dirProcedimientos = {'funciones': {}, 'variables': {}}

# Proc que guarda las funciones en el directorio de funciones
def p_NP2_NombreFunc(p):
	'NP2_NombreFunc : '
	global numParametros, funcionActual
	numParametros = 1 						# Inicializar el contador de parametros
	resetFuncMems()							# Reiniciar las temporales
	# Guardar nombre y tipo de la funcion
	tipoFuncion = p[-2]						# Tipo de la función
	funcionActual = p[-1]					# Nombre de la función

	# Comprobar que no sea nombre de una funcion
	if funcionActual in dirProcedimientos['funciones']:
		finalizar("Linea " + str(lineaActual) + " -> La función" + str(funcionActual) + " está repetida")
	
	# Comprobar que no haya una variable con el nombre de la funcion
	if funcionActual in dirProcedimientos['variables']:
		finalizar("Linea " + str(lineaActual) + " -> El nombre " + str(funcionActual) + " ya esta siendo usado por una variable")

	memFunc = None
	# Para las funciones con valor de retorno, se crea una variable global
	if tipoFuncion != 'void':
		memFunc = getEspacioMemoria(tipoFuncion, 'Global')
		dirProcedimientos['variables'] = {'nombre': funcionActual, 'tipo' : tipoFuncion, 'mem': memFunc}

	# Agregar funcion al directorio	de funciones
	crearCuadruplo(code['inicioFunc'], None, None, funcionActual)
	dirProcedimientos['funciones'][funcionActual] = {'retorno' : tipoFuncion, 'variables' : {}, 'mem': memFunc, 'cuadruplo': len(cuadruplos), 'parametros' : {}}

# Procedimiento que agrega la funcion de inicio al directorio
def p_NP7_Inicio(p):
	'NP7_Inicio : '
	global funcionActual
	# Comprobar que no haya otro inicio
	funcionActual = 'inicio'

	# Comprobar que el inicio no este declarado ya
	if funcionActual in dirProcedimientos['funciones']:
		finalizar("Linea " + str(lineaActual) + " -> El inicio ya fue declarado en otra parte")
		return

	# Agregar funcion al directorio	
	dirProcedimientos['funciones']['inicio'] = {'retorno' : 'void', 'variables' : {}, 'cuadruplo': len(cuadruplos), 'parametros' : {}}
	cuadruplos[0].llenar(dirProcedimientos['funciones']['inicio']['cuadruplo'])
	crearCuadruplo(code['inicioFunc'], None, None, funcionActual)

# Procedimiento que guarda los parametros de una funcion dentro del directorio
def p_NP3_Parametros(p):
	'NP3_Parametros : '
	global tipoActual, tamanoActual, numParametros
	nombreParametro = p[-1] # Guardar nombre del parametro

	tipoParametro = [-2]	# Tipo de parametro

	# Verificar que no se repita el parametro
	if nombreParametro in dirProcedimientos['funciones'][funcionActual]:
		finalizar("Linea " + str(lineaActual) + " -> Nombre ya usado por otro parametro")

	# Si el parametro es por valor
	if tipoParametro != '&':
		tipoParametro = 'valor'
		# Agregar el parametro como variable a su función correspondiente en la tabla
		dirProcedimientos['funciones'][funcionActual]['variables'][nombreParametro] = {'tipo' : tipoActual, 'mem': getEspacioMemoria(tipoActual, 'Local'), 'tamano' : tamanoActual}
	else:
		tipoParametro = 'referencia'
		# Agregar el parametro como variable a su función correspondiente en la tabla
		dirProcedimientos['funciones'][funcionActual]['variables'][nombreParametro] = {'tipo' : tipoActual, 'mem': -1, 'tamano' : tamanoActual}

	# Agregar el parametro a su función correspondiente en la tabla
	dirProcedimientos['funciones'][funcionActual]['parametros'][numParametros] = {'nombre': nombreParametro, 'tipo': tipoActual, 'tamano': tamanoActual, 'tipoParametro': tipoParametro}

	numParametros += 1		# Aumentar contador de parametros

# Procedimiento que guarda las variables dentro de la tabla de variables
def p_NP4_Variable(p):
	'NP4_Variable : '
	global funcionActual, tipoActual, tamanoActual # Tipo actual se actualiza desde la gramatica
	tamanoActual = -1		# Tamaño de la variable		
	nombreVariable = p[-1]	# Nombre de la variable (valor de ID)

	# Si estamos dentro de una funcion (variable local)
	if funcionActual != '':
		# Comprobar que la variable no este declarada dentro de la funcion
		if nombreVariable in dirProcedimientos['funciones'][funcionActual]['variables']:
			finalizar("Linea " + str(lineaActual) + " -> La variable '" + str(nombreVariable) + "' ya fue declarada")
		# Se mete la variable al directorio
		dirProcedimientos['funciones'][funcionActual]['variables'][nombreVariable] = {'tipo': tipoActual, 'tamano': 0, 'mem': getEspacioMemoria(tipoActual, 'Local')}
	# Si la variable es global
	else:
		# Comprobar que la variable no este declarada 
		if nombreVariable in dirProcedimientos['variables']:
			finalizar("Linea " + str(lineaActual) + " -> La variable '" + str(nombreVariable) + "' ya fue declarada")
		dirProcedimientos['variables'][nombreVariable] = {'tipo': tipoActual, 'tamano': 0, 'mem': getEspacioMemoria(tipoActual, 'Global')}

# Procedimiento que guarda las listas en el directorio
def p_sNP6_Lista(p):
	'NP6_Lista :'
	tamanoArreglo = p[-1]		# Obtenemos el tamaño del arreglo

	# Si el tamaño es menor a 0
	if int(tamanoArreglo) < 0:
		finalizar("Linea " + str(lineaActual) + " -> El tamaño del arreglo debe ser mayor o igual a 0")
	# Obtenemos el nombre del arreglo, ya fue declarado, solo hay que actualizar el tamano
	nombreVariable = p[-3]
	tipoArreglo = tipoActual # Tipo del arreglo

	# Actualizar tamaño de la variable (arreglo)
	if funcionActual != "":
		dirProcedimientos['funciones'][funcionActual]['variables'][nombreVariable]['tamano'] = tamanoArreglo
		# Aumentar numero de registros segun el tamaño del arreglo
		registrosMem[contadorReg[tipoArreglo + 'Local']] += (int(tamanoArreglo) - 1) 
	else:
		# 
		dirProcedimientos['variables'][nombreVariable]['tamano'] = tamanoArreglo
		# Aumentar numero de registros segun el tamaño del arreglo
		registrosMem[contadorReg[tipoArreglo + 'Global']] += (int(tamanoArreglo) - 1)

def p_NP_ListaCont(p):
	'NP_ListaCont :'
	global tipoActual

	if p[-1] != tipoActual:
		finalizar("Linea " + str(lineaActual) + " -> Error de tipos en la declaración del arreglo")
		return

# Argumentos de llamada de una función
def p_NP_Argumento(p):
	'NP_Argumento : '
	global numParametros, funcionInvocada

	# Verificamos que el numero de argumentos siga dentro del rango
	if numParametros in dirProcedimientos['funciones'][funcionInvocada]['parametros']:
		# Obtener la direccion del argumento
		argumDir = pilaOperandos.pop()
		# Obtenemos el nombre declarado del parametro, segun su posicion
		nombreParametro = dirProcedimientos['funciones'][funcionInvocada]['parametros'][numParametros]['nombre']

		# Obtener la direccion asignada a ese parametro para la generacion de cuadruplos
		dirVarParam = dirProcedimientos['funciones'][funcionInvocada]['variables'][nombreParametro]['mem']
		# Verificar que el argumento sea del mismo tipo que el parametro
		if cubo.revisar(getTipo(dirVarParam), getTipo(argumDir), code['=']) != 'error':

			# Si el parametro es un arreglo lo enviamos por referencia
	#		if int(dirProcedimientos['funciones'][funcionInvocada]['variables'][nombreParametro]['tamano']) > 0:
	#			hashRef[argumDir] = dirVarParam
	#			hashRefTam[argumDir] = dirProcedimientos['funciones'][funcionInvocada]['variables'][nombreParametro]['tamano']
	#		else:
			# Si el parametro es por valor, crear el cuadruplo
			crearCuadruplo(code['parametro'], argumDir, None, dirVarParam)
			numParametros += 1
		else:
			finalizar("Linea " + str(lineaActual) + " -> Error en los parametros de la función " + funcionInvocada)
	else:
		finalizar("Linea " + str(lineaActual) + " -> Numero incorrecto de parametros en la funcion " + funcionInvocada)

# Proc que crea el cuadruplo ERA de una llamada
def p_NP_ERA(p):
	'NP_ERA : '
	global numParametros, funcionInvocada
	funcionInvocada = p[-1] # Guardar el nombre de la función invocada
	numParametros = 1	   # Inicializar el contador de parametros

	# Comprobar que la función este declarada
	if funcionInvocada in dirProcedimientos['funciones']:
		crearCuadruplo(code['ERA'], funcionInvocada, None, dirProcedimientos['funciones'][funcionInvocada]['cuadruplo'])
	# Informar que la función no fue declarada
	else:
		finalizar("Linea " + str(lineaActual) + " -> La funcion " + funcionInvocada + " no esta declarada")

# Proc que crea los cuadruplos de un condicion
def p_NP_Si_Expresion(p):
	'NP_Si_Expresion : '
	expresionIF = pilaOperandos.pop()

	# Comprobar que dentro del if hay un booleano
	if getTipo(expresionIF) == code['boolean']: # Revisar
		# Crear cuadruplo gotof
		crearCuadruplo(code['gotof'], expresionIF, None, None)
		pilaSaltos.append(len(cuadruplos) - 1) # Guardar la posición del salto
	else:
		print("Linea", lineaActual, "-> La expresion del estatuto SI debe ser boolean")

# Procedimiento que crea el cuadruplo de retorno
def p_NP_Retorno(p):
	'NP_Retorno :'
	if funcionActual == "":
		finalizar("Linea", lineaActual, "-> Retorno fuera de función")
		
	# Obtenemos la direccion del valor de retorno
	memRetorno = pilaOperandos.pop()

	# El tipo de expresion debe coincidir con el tipo de retorno
	tipoFuncion = dirProcedimientos['funciones'][funcionActual]['retorno']
		
	if tipoFuncion == "void":
		finalizar("Linea", lineaActual, "-> La función", funcionActual, "no debe retornar valor")
	# Direccion de la funcion global que almacena el retorno
	dirRetornoGlobal = dirProcedimientos['funciones'][funcionActual]['mem']
		
	if code[tipoFuncion] == getTipo(memRetorno):
		# Crear el cuadruplo de retorno
		crearCuadruplo(code["regresa"], memRetorno, -1, dirRetornoGlobal)
		crearCuadruplo(code["finProc"], -1, -1, -1)
	else:
		finalizar("Linea", lineaActual, "-> Tipo incorrecto de retorno en la funcion")

# Llamada dedes p_valor
def p_NP_FinInvocacion(p):
	'NP_FinInvocacion :'
	global numParametros, funcionInvocada



	if len(dirProcedimientos['funciones'][funcionInvocada]['parametros']) == numParametros - 1:
	   
		crearCuadruplo(code['gosub'], None, None, dirProcedimientos['funciones'][funcionInvocada]['cuadruplo'])
		
		dirRetorno = dirProcedimientos['funciones'][funcionInvocada]['mem']
		if  dirRetorno == None: return

		print("DirRetorno", dirRetorno)
		# Crear el cuadruplo que guarda el valor de retorno
		if dirRetorno != -1:
			tipoRetorno = simbol(getTipo(dirRetorno))
			nuevaTemporal = memConts[memCont[tipoRetorno + 'Temp']]
			crearCuadruplo(code['retu'], dirRetorno, -1, nuevaTemporal)
			pilaOperandos.append(nuevaTemporal)
			registrosMem[contadorReg[tipoRetorno + 'Temp']] += 1
		
	else:
		terminate("Numero incorrecto de argumentos en la llamada")

cantSinoSi = 0

# Proc que crea los cuadruplos de un else
def p_NP_Sino(p):
	'NP_Sino : '
	crearCuadruplo(code['goto'], None, None, None)		# Crear cuadruplo goto del else
	cuadruploFalso = pilaSaltos.pop() 					# Sacar la posición de el gotof correspondiente al if de este else
	pilaSaltos.append(len(cuadruplos) - 1)				# Guardar posición del salto
	cuadruplos[cuadruploFalso].llenar(len(cuadruplos))	# Rellenar cuadruplo gotof correspondiente

# Proc que actualiza el cuadruplo gotof de la condicion
def p_NP_Si_Cierre(p):
	'NP_Si_Cierre : '
	global cantSinoSi

	cuadruploFin = pilaSaltos.pop()
	cuadruplos[cuadruploFin].llenar(len(cuadruplos))	# Rellenar cuadruplo
	cantSinoSi -= 1

# Proc que guarda la posicion inicial de la condicion de un ciclo
def p_NP_Ciclo_Inicio(p):
	'NP_Ciclo_Inicio : '
	pilaSaltos.append(len(cuadruplos))

# Proc que crea los cuadruplos de un ciclo
def p_NP_Ciclo(p):
	'NP_Ciclo : '
	expresionCiclo = pilaOperandos.pop()
	# Ciclo repeter
	if p[-1] == 'repetir':
		if getTipo(expresionCiclo) != code['int']: # Revisar que haya un numero para repetir el ciclo
			finalizar("Linea " + str(lineaActual) + " -> La expresión del estatuto REPETIR debe ser un valor entero")
	# Ciclo mientras
	else:
		if getTipo(expresionCiclo) != code['boolean']:	# Revisar la condición sea booleana
			finalizar("Linea " + str(lineaActual) + " -> La expresión del estatuto MIENTRAS debe ser un boolean")
		
	# Crear cuadruplo gotof del ciclo
	crearCuadruplo(code['gotof'], expresionCiclo, None, None)
	pilaSaltos.append(len(cuadruplos) - 1) 				# Guardar la posición del salto

# Proc que crea el cuadruplo goto de un ciclo
def p_NP_Ciclo_Cierre(p):
	'NP_Ciclo_Cierre : '
	cuadruploFin = pilaSaltos.pop()
	retorno = pilaSaltos.pop()
	crearCuadruplo(code['goto'], None, None, retorno)
	cuadruplos[cuadruploFin].llenar(len(cuadruplos))

# Proc que crea los cuadruplos de sumas y restas
def p_NP_SumResPendientes(p):
	'NP_SumResPendientes :'
	# pregunto si tengo sumas o restas pendientes por resolver
	if len(pilaOperadores) > 0 and (pilaOperadores[-1] == code['+'] or pilaOperadores[-1] == code['-']):
		
		# obtengo direcciones de memoria de los valores a sumar/restar
		opDir2 = pilaOperandos.pop()	# Operando 1
		opDir1 = pilaOperandos.pop()	# Operando 2
		opTypeCode1 = getTipo(opDir1)	# Tipo operando 1
		opTypeCode2 = getTipo(opDir2)	# Tipo operando 2
		opeCode = pilaOperadores.pop()	# Operador

		# Obtener el tipo de registro temporal
		tipoRegistro = cubo.revisar(abs(opTypeCode1), abs(opTypeCode2), opeCode) 

		# Si la operación es posible, se agrega el cuadruplo
		if tipoRegistro != 'error':
			# Al tipo de registro se le agrega Temp al final para crear el registro temporal de ese tipo
			tipoRegistro += "Temp"

			pilaOperandos.append(registrosMem[contadorReg[tipoRegistro]])
			crearCuadruplo(opeCode, opDir1, opDir2, registrosMem[contadorReg[tipoRegistro]])
			registrosMem[contadorReg[tipoRegistro]] += 1
		else:
			finalizar("Linea " + str(lineaActual) + " -> Error de tipos")

# Proc que crea los cuadruplos de multiplicaciones, divisiones y residuos
def p_NP_MulDivResPendientes(p):
	'NP_MulDivResPendientes :'
	# pregunto si tengo sumas o restas pendientes por resolver
	if len(pilaOperadores) > 0 and (pilaOperadores[-1] == code['*'] or pilaOperadores[-1] == code['/'] or pilaOperadores[-1] == code['%']):
		
		# obtengo direcciones de memoria de los valores a sumar/restar
		opDir2 = pilaOperandos.pop()	# Operando 1
		opDir1 = pilaOperandos.pop()	# Operando 2
		opTypeCode1 = getTipo(opDir1)	# Tipo operando 1
		opTypeCode2 = getTipo(opDir2)	# Tipo operando 2
		opeCode = pilaOperadores.pop()	# Operador

		# Obtener el tipo de registro temporal
		tipoRegistro = cubo.revisar(abs(opTypeCode1), abs(opTypeCode2), opeCode) 

		# Si la operación es posible, se agrega el cuadruplo
		if tipoRegistro != 'error':
			# Al tipo de registro se le agrega Temp al final para crear el registro temporal de ese tipo
			tipoRegistro += "Temp"

			pilaOperandos.append(registrosMem[contadorReg[tipoRegistro]])
			crearCuadruplo(opeCode, opDir1, opDir2, registrosMem[contadorReg[tipoRegistro]])
			registrosMem[contadorReg[tipoRegistro]] += 1
		else:
			finalizar("Linea " + str(lineaActual) + " -> Error de tipos")

# Proc que crea los cuadruplos de los operadores logicos
def p_NP_OpLogicosPendientes(p):
	'NP_OpLogicosPendientes :'
	# pregunto si tengo sumas o restas pendientes por resolver
	if len(pilaOperadores) > 0 and (pilaOperadores[-1] == code['&'] or pilaOperadores[-1] == code['|']):
		
		# obtengo direcciones de memoria de los valores a sumar/restar
		opDir2 = pilaOperandos.pop()	# Operando 1
		opDir1 = pilaOperandos.pop()	# Operando 2
		opTypeCode1 = getTipo(opDir1)	# Tipo operando 1
		opTypeCode2 = getTipo(opDir2)	# Tipo operando 2
		opeCode = pilaOperadores.pop()	# Operador

		# Obtener el tipo de registro temporal
		tipoRegistro = cubo.revisar(abs(opTypeCode1), abs(opTypeCode2), opeCode) 

		# Si la operación es posible, se agrega el cuadruplo
		if tipoRegistro != 'error':
			# Al tipo de registro se le agrega Temp al final para crear el registro temporal de ese tipo
			tipoRegistro += "Temp"

			pilaOperandos.append(registrosMem[contadorReg[tipoRegistro]])
			crearCuadruplo(opeCode, opDir1, opDir2, registrosMem[contadorReg[tipoRegistro]])
			registrosMem[contadorReg[tipoRegistro]] += 1
		else:
			finalizar("Linea " + str(lineaActual) + " -> Error de tipo")

# Proc que crea los cuadruplos de los operadores relacionales
def p_NP_OpRelacionalesPendientes(p):
	'NP_OpRelacionalesPendientes :'
	# pregunto si tengo sumas o restas pendientes por resolver
	if len(pilaOperadores) > 0 and (pilaOperadores[-1] == code['>'] or pilaOperadores[-1] == code['<'] or pilaOperadores[-1] == code['>='] or pilaOperadores[-1] == code['<='] or pilaOperadores[-1] == code['=='] or pilaOperadores[-1] == code['!=']):
		
		# obtengo direcciones de memoria de los valores a sumar/restar
		opDir2 = pilaOperandos.pop()	# Operando 1
		opDir1 = pilaOperandos.pop()	# Operando 2
		opTypeCode1 = getTipo(opDir1)	# Tipo operando 1
		opTypeCode2 = getTipo(opDir2)	# Tipo operando 2
		opeCode = pilaOperadores.pop()	# Operador

		# Obtener el tipo de registro temporal
		tipoRegistro = cubo.revisar(abs(opTypeCode1), abs(opTypeCode2), opeCode) 

		# Si la operación es posible, se agrega el cuadruplo
		if tipoRegistro != 'error':
			# Al tipo de registro se le agrega Temp al final para crear el registro temporal de ese tipo
			tipoRegistro += "Temp"
			# Meter a operandos el nuevo temporal
			pilaOperandos.append(registrosMem[contadorReg[tipoRegistro]])
			# Crear cuadruplo con el nuevo temporal y los operandos extraidos de la pila
			crearCuadruplo(opeCode, opDir1, opDir2, registrosMem[contadorReg[tipoRegistro]])
			# Aumentar la direccion de memoria para el siguiente registro
			registrosMem[contadorReg[tipoRegistro]] += 1
		else:
			finalizar("Linea " + str(lineaActual) + " -> Error de tipo")

# Operadores de asignación pendientes
def p_NP_Asignacion(p):
	'NP_Asignacion :'
	resultDir = pilaOperandos.pop()
	varDir = pilaOperandos.pop()

	if cubo.revisar(getTipo(resultDir), getTipo(varDir), code['=']) != 'error':
		crearCuadruplo(code['='], resultDir, None, varDir)
	else:
		finalizar("Linea " + str(lineaActual) + " -> Error de tipos en la asignación")

# Valida que existe la variable y meterla a la pila
def p_NP_VariableAPila(p):
	'NP_VariableAPila :'
	validarIDSemantica(p[-3])

# Agregar parentesis izq (fondo falso) a la pila
def p_NP_AgrupacionAbre(p):
	'NP_AgrupacionAbre : '
	pushPilaOperadores('(')

def p_NP_AgrupacionCierra(p):
	'NP_AgrupacionCierra : '
	# Al finalizar la agrupacion, debe haber un parentesis que abre
	if pilaOperadores.pop() != code['(']:
		finalizar("Linea " + str(lineaActual) + " -> Error en los parentesis")

# Asignación de memoria a CONSTANTES ----------------------------------------------
# Nueva constante entera
def p_NP_IntCTE(p):
	'NP_IntCTE :'
	# Crear la direccion de mem si no existe
	if not p[-1] in dirConstantes:
		registrarReg(p[-1], 'intCTE')
	# Agregar a la pila de operadores
	pilaOperandos.append(dirConstantes[p[-1]])

# Nueva constante dec
def p_NP_DecimalCTE(p):
	'NP_DecimalCTE :'
	# Crear la direccion de mem si no existe
	if not p[-1] in dirConstantes:
		registrarReg(p[-1], 'decCTE')
	# Agregar a la pila de operadores
	pilaOperandos.append(dirConstantes[p[-1]])

# Nueva constante string
def p_NP_StringCTE(p):
	'NP_StringCTE :'
	# Crear la direccion de mem si no existe
	if not p[-1] in dirConstantes:
		registrarReg(p[-1], 'stringCTE')
	# Agregar a la pila de operadores
	pilaOperandos.append(dirConstantes[p[-1]])
#------------------------------------------------------------------------------------------

# Global que mantiene el nombre de la funcion especial invocada
funcionEspecial = None

# Crea el cuadruplo de invocación de una función especial sin parametros
def p_NP_FuncEsp(p):
	'NP_FuncEsp :'
	global funcionEspecial
	funcionEspecial = code[p[-1]]
	# Crear cuadruplo de la funcion
	crearCuadruplo(funcionEspecial, None, None, None)

# Crea el primer cuadruplo de invocación de una función especial con parametros
def p_NP_FuncEspParam(p):
	'NP_FuncEspParam :'
	global funcionEspecial
	funcionEspecial = code[p[-1]]

# Crea el cuadruplo de una funcion especial que tiene argumentos
def p_NP_ArgFunEsp(p):
	'NP_ArgFunEsp :'
	# Crear cuadruplo de la funcion obteniendo su argumento de la pila
	crearCuadruplo(funcionEspecial, pilaOperandos.pop(), None, None)

def p_NP_Leer1(p):
	'NP_Leer1 :'
	validarIDSemantica(p[-1])

def p_NP_Leer2(p):
	'NP_Leer2 :'
	crearCuadruplo(funcionEspecial, pilaOperandos.pop(), pilaOperandos.pop(), None)


#==============================================================================================
# Agrega un registro a la memoria
def registrarReg(dato, tipo):
	dirConstantes[dato] = registrosMem[contadorReg[tipo]] # Guardar el dato con su direccion de memoria
	registrosMem[contadorReg[tipo]] += 1 # Mover el contador a siguiente direccion de memoria

# Termina la ejecucion del programa y muestra un mensaje
def finalizar(mensaje):
	print(mensaje)
	file = open("archErroresCompilacion.txt","w") 
	file.write(mensaje) 
	file.close()
	return
	#sys.exit()

# Actualiza el el tipo actal de variable
def setTipoActual(nuevoTipo):
	global tipoActual
	tipoActual = nuevoTipo

# Actualiza el tipo actual de variable
def setFuncionActual(nuevaFuncion):
	global funcionActual
	funcionActual = nuevaFuncion

# Actualiza el tamaño actual de variable
def setTamanoActual(nuevoTamano):
	global tamanoActual
	tamanoActual = nuevoTamano

# Regresa el tamaño actual de variable
def getTamanoActual():
	global tamanoActual
	return tamanoActual

# Funcion que verifica que una variable exista ya sea global o localmente
def existeVariable(nombreVariable):
	# Si estamos dentro de una funcion
	if funcionActual != '':
		# Si es una variable dentro de la funcion
		if nombreVariable in dirProcedimientos['funciones'][funcionActual]['variables']:
			return True
	# Si es una variable global
	if nombreVariable in dirProcedimientos['variables']:
		return True
	return False

# Funcion que verifica que una variable exista ya sea global o localmente
def existeFuncion(nombreFuncion):
	# Verifica que la funcion este dentro del directorio de funciones
	if nombreFuncion in dirProcedimientos['funciones']:
		return True
	return False

# ======================================================================================

# Agrega el operador recibido a la pila de operadores
def pushPilaOperadores(operador):
	global pilaOperadores
	pilaOperadores.append(code[operador])

# Agrega el operando recibido a la pila de operandos
def pushPilaOperandos(operando):
	global pilaOperadores
	pilaOperandos.append(code[operando])

# Agrega el operando recibido a la pila de operandos
def nuevaBoolCTE(valBool):
	global pilaOperadores
	if valBool == 'verdadero':
		pilaOperandos.append(registrosMem[contadorReg['booleanCTE']] + 1)
		#print(registrosMem[contadorReg['booleanCTE']] + 1)
	else: pilaOperandos.append(registrosMem[contadorReg['booleanCTE']])

# Crea un cuadruplo
def crearCuadruplo(operador, op1, op2, registro):
	global cuadruplos
	# Agrega el cuadruplo a la lista de cuadruplos
	cuadruplos.append(Cuadruplo())
	# Actualiza los valores del cuadruplo agregado
	cuadruplos[-1].ope = operador
	cuadruplos[-1].op1 = op1
	cuadruplos[-1].op2 = op2
	cuadruplos[-1].reg = registro

def validarIDSemantica(IDNombreActual, arreglo=""):
	# Validar que existe la variable
	if not existeVariable(IDNombreActual):
		finalizar("Linea " + str(lineaActual) + " -> La variable " + str(IDNombreActual) + " no está declarada")

	# Si variable existe, insertarla en la pila de operandos
	if funcionActual != '' and IDNombreActual in dirProcedimientos['funciones'][funcionActual]['variables']:
		pilaOperandos.append(dirProcedimientos['funciones'][funcionActual]['variables'][IDNombreActual]['mem'])

	elif IDNombreActual in dirProcedimientos['variables']:
		pilaOperandos.append(dirProcedimientos['variables'][IDNombreActual]['mem'])
	# Borrar este else
	else:
		finalizar("Linea " + str(lineaActual) + " -> La variable " + str(IDNombreActual) + " no fue encontrada")

def getEspacioMemoria(tipoVariable, scope):
	tipoMemoria = tipoVariable + scope				# Tipo de dato para saber donde guardar
	registrosMem[contadorReg[tipoMemoria]] += 1	   # Aumentar el contador de ese tipo de dato
	return registrosMem[contadorReg[tipoMemoria]] - 1 # Regresar la posicion de memoria en que se guardo


def accesoArreglo(IDNombreActual):
	# Expresion de indexamiento
	indexMem = pilaOperandos.pop()

	# Si el indice no es un entero, finaliza ejecución
	if getTipo(indexMem) != code['int']:
		finalizar("Linea " + str(lineaActual) + " -> El indice de una lista debe ser un valor entero")
		
	# Variables auxiliares
	limiteArreglo = 0
	tipoArreglo = 0
	nuevaTemporal = 0
	dirBase = 0
		
	# Encontrar donde esta declarado el arreglo para obtener datos
	if funcionActual != "" and IDNombreActual in dirProcedimientos['funciones'][funcionActual]['variables']:
		# Arreglo local a una funcion
		limiteArreglo = dirProcedimientos['funciones'][funcionActual]['variables'][IDNombreActual]['tamano']
		dirBase = dirProcedimientos['funciones'][funcionActual]['variables'][IDNombreActual]['mem']
	else:
		# Arreglo global
		limiteArreglo = dirProcedimientos['variables'][IDNombreActual]['tamano']
		dirBase = dirProcedimientos['variables'][IDNombreActual]['mem']

	# Generar cuadruplos del arreglo
	tipoArreglo = getTipo(dirBase)
	nuevaTemporal = getEspacioMemoria(simbol(tipoArreglo), 'Temp')				
	crearCuadruplo(code['ver'], indexMem, 0, int(limiteArreglo) - 1)
	dirBase = int(dirBase)

	# Verificación de existencia de constante (posiblemente innecesaria)
	if not dirBase in dirConstantes:
		dirConstantes[dirBase] = memConts[memCont['intCTE']]
		registrosMem[contadorReg['intCTE']] += 1
	crearCuadruplo(code['+'], dirConstantes[dirBase], indexMem, nuevaTemporal)
	pilaOperandos.append(nuevaTemporal * -1)

crearCuadruplo(code['goto'], 'inicio', None, None) 