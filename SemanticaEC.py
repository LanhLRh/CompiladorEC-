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

# Cubo semantico
cubo = Cubo()

def p_imprimir(p):
	'imprimir : '
	print(dirProcedimientos)
	print(pilaOperadores)
	print(pilaOperandos)
	imprimir()

def imprimir():
	for index, cuadruplo in enumerate(cuadruplos):
		print("{} -\t{},\t{},\t{},\t{}".format(index, simbol(cuadruplo.ope), cuadruplo.op1, cuadruplo.op2, cuadruplo.reg))
	print("--------------------")

# Crea el directorio de procedimientos y variables
def p_NP1_DirProced(p):
	'NP1_DirProced : '
	global dirProcedimientos
	dirProcedimientos = {'funciones': {}, 'variables': {}}

# Guarda la funcion
def p_NP2_NombreFunc(p):
	'NP2_NombreFunc : '
	global numParametros, funcionActual
	numParametros = 1
	resetFuncMems()
	# Guardar nombre y tipo de la funcion
	tipoFuncion = p[-2]
	funcionActual = p[-1]

	# Comprobar que no sea nombre de una funcion
	if funcionActual in dirProcedimientos['funciones']:
		finalizar("Linea " + str(lineaActual) + " -> La función" + str(funcionActual) + " está repetida")

	memFunc = None
	# Para las funciones con valor de retorno, se crea una variable global
	if tipoFuncion != 'void':
		memFunc = getEspacioMemoria(tipoFuncion, 'Global')
		dirProcedimientos['variables'] = {'nombre': funcionActual, 'tipo' : tipoFuncion, 'mem': memFunc}

	# Agregar funcion al directorio	
	dirProcedimientos['funciones'][funcionActual] = {'retorno' : tipoFuncion, 'variables' : {}, 'mem': memFunc, 'parametros' : {}}

def p_NP7_Inicio(p):
	'NP7_Inicio : '
	global funcionActual
	# Comprobar que no haya otro inicio
	funcionActual = 'inicio'

	if funcionActual in dirProcedimientos['funciones']:
		finalizar("Linea " + str(lineaActual) + " -> El inicio ya fue declarado en otra parte")

	# Agregar funcion al directorio	
	dirProcedimientos['funciones']['inicio'] = {'retorno' : 'void', 'variables' : {}, 'parametros' : {}}

def p_NP3_Parametros(p):
	'NP3_Parametros : '
	global tipoActual, tamanoActual, numParametros
	nombreParametro = p[-1] # Guardar nombre del parametro

	tipoParametro = [-2]	

	# Verificar que no se repita el parametro
	if nombreParametro in dirProcedimientos['funciones'][funcionActual]:
		finalizar("Linea " + str(lineaActual) + " -> Nombre ya usado por otro parametro")

	if tipoParametro != '&':
		tipoParametro = 'valor'
		# Agregar el parametro como variable a su función correspondiente en la tabla
		dirProcedimientos['funciones'][funcionActual]['variables'][nombreParametro] = {'tipo' : tipoActual, 'mem': getEspacioMemoria(tipoActual, 'Var'), 'tamano' : tamanoActual}
	else:
		tipoParametro = 'referencia'
		# Agregar el parametro como variable a su función correspondiente en la tabla
		dirProcedimientos['funciones'][funcionActual]['variables'][nombreParametro] = {'tipo' : tipoActual, 'mem': -1, 'tamano' : tamanoActual}

	# Agregar el parametro a su función correspondiente en la tabla
	dirProcedimientos['funciones'][funcionActual]['parametros'][numParametros] = {'nombre': nombreParametro, 'tipo': tipoActual, 'tamano': tamanoActual, 'tipoParametro': tipoParametro}


	numParametros += 1

def p_NP4_Variable(p):
	'NP4_Variable : '
	global tipoActual, tamanoActual # Tipo actual se actualiza desde la gramatica
	tamanoActual = 0
	nombreVariable = p[-1] # Nombre de la variable (valor de ID)

	# Comprobar que no sea nombre de variable
	if existeVariable(nombreVariable):
		finalizar("Linea " + str(lineaActual) + " -> La variable " + str(nombreVariable) + " ya fue declarada")
 	
	# Si estamos dentro de una funcion (variable local)
	if funcionActual != '':
		# Se mete la variable al directorio
		dirProcedimientos['funciones'][funcionActual]['variables'][nombreVariable] = {'tipo': tipoActual, 'tamano': 0, 'mem': getEspacioMemoria(tipoActual, 'Var')}
	# Si la variable es global
	else:
		dirProcedimientos['variables'][nombreVariable] = {'tipo': tipoActual, 'tamano': 0, 'mem': getEspacioMemoria(tipoActual, 'Global')}

def p_sNP6_Lista(p):
	'NP6_Lista :'
	# Obtenemos el tamaño del arreglo
	tamanoArreglo = p[-1]

	# Si el tamaño es menor a 0
	if int(tamanoArreglo) < 0:
		finalizar("Linea " + str(lineaActual) + " -> El tamaño del arreglo debe ser mayor o igual a 0")
	# Obtenemos el nombre del arreglo, ya fue declarado, solo hay que actualizar el tamano
	nombreVariable = p[-3]

	# Actualizar tamaño de la variable (arreglo)
	if funcionActual != "":
		dirProcedimientos['funciones'][funcionActual]['variables'][nombreVariable]['tamano'] = tamanoArreglo
	else:
		dirProcedimientos['variables'][nombreVariable]['tamano'] = tamanoArreglo

# Argumentos de llamada de una función
def p_NP_Argumento(p):
	'NP_Argumento : '
	global numParametros
    # Verificamos que el numero de argumentos siga dentro del rango
	if numParametros in dirProcedimientos['funciones'][funcionActual]['parametros']:
		# Obtener la direccion del argumento
		argumDir = pilaOperandos.pop()
		# Obtenemos el nombre declarado del parametro, segun su posicion
		nombreParametro = dirProcedimientos['funciones'][funcionActual]['parametros'][numParametros]['nombre']

		# Obtener la direccion asignada a ese parametro para la generacion de cuadruplos
		dirVarParam = dirProcedimientos['funciones'][funcionActual]['variables'][nombreParametro]['mem']
		# Verificar que el argumento sea del mismo tipo que el parametro
		if cubo.revisar(getTipo(dirVarParam), getTipo(argumDir), code['=']) != 'error':

			# Si el parametro es un arreglo lo enviamos por referencia
	#		if int(dirProcedimientos['funciones'][funcionActual]['variables'][nombreParametro]['tamano']) > 0:
	#			hashRef[argumDir] = dirVarParam
	#			hashRefTam[argumDir] = dirProcedimientos['funciones'][funcionActual]['variables'][nombreParametro]['tamano']
	#		else:
			# Si el parametro es por valor, crear el cuadruplo
			crearCuadruplo(code['parametro'], argumDir, None, dirVarParam)
			numParametros += 1
		else:
			finalizar("Linea " + str(lineaActual) + " -> Error en los parametros de la función " + funcionActual)
	else:
		finalizar("Numero incorrecto de parametros en la funcion " + funcionActual)

def p_NP_ERA(p):
	'NP_ERA : '
	global numParametros, funcionActual
	nombreLlamada = p[-1]

	crearCuadruplo(code['ERA'], nombreLlamada, None, None)

def p_NP_Si_Expresion(p):
	'NP_Si_Expresion : '
	expresionIF = pilaOperandos.pop()
	if getTipo(expresionIF) == code['boolean']: # Revisar
		crearCuadruplo(code['gotof'], expresionIF, None, None)
		pilaSaltos.append(len(cuadruplos) - 1)
	else:
		print("Linea", lineaActual, "-> La expresion del estatuto SI debe ser boolean")

def p_NP_Sino(p):
	'NP_Sino : '
	crearCuadruplo(code['goto'], None, None, None)
	cuadruploFalso = pilaSaltos.pop()
	pilaSaltos.append(len(cuadruplos) - 1)
	cuadruplos[cuadruploFalso].llenar(cuadruploFalso)

def p_NP_Si_Cierre(p):
	'NP_Si_Cierre : '
	cuadruploFin = pilaSaltos.pop()
	cuadruplos[cuadruploFin].llenar(len(cuadruplos))

def p_NP_Ciclo_Inicio(p):
	'NP_Ciclo_Inicio : '
	pilaSaltos.append(len(cuadruplos))

def p_NP_Ciclo(p):
	'NP_Ciclo : '
	expresionCiclo = pilaOperandos.pop()
	if p[-1] == 'repetir':
		if getTipo(expresionCiclo) != code['int']: # Revisar
			finalizar("Linea " + str(lineaActual) + " -> La expresión del estatuto REPETIR debe ser un valor entero")
	else:
		if getTipo(expresionCiclo) != code['boolean']: # Revisar
			finalizar("Linea " + str(lineaActual) + " -> La expresión del estatuto MIENTRAS debe ser un boolean")
		
	crearCuadruplo(code['gotof'], expresionCiclo, None, None)
	pilaSaltos.append(len(cuadruplos) - 1)
			
def p_NP_Ciclo_Cierre(p):
	'NP_Ciclo_Cierre : '
	cuadruploFin = pilaSaltos.pop()
	retorno = pilaSaltos.pop()
	crearCuadruplo(code['goto'], None, None, retorno)
	cuadruplos[cuadruploFin].llenar(len(cuadruplos))

# Llamada desde 
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

# Llamada desde 
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

# Llamada desde 
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

# Llamada desde 
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

# Validar que existe la variable y meterla a la pila
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

# 
def p_NP_FuncSinArgs(p):
    'NP_FuncSinArgs :'
    # Crear cuadruplo de la funcion
    crearCuadruplo(code[p[-3]], None, None, None)

# 
def p_NP_FuncUnArg(p):
	'NP_FuncUnArg :'
	global funcionInvocada
	funcionInvocada = code[p[-4]]
	# Crear cuadruplo de la funcion obteniendo su argumento de la pila
	crearCuadruplo(funcionInvocada, pilaOperandos.pop(), None, None)

# 
def p_NP_FuncOtroArg1(p):
    'NP_FuncOtroArg1 :'
    # Crear cuadruplo de la funcion obteniendo su argumento de la pila
    crearCuadruplo(code[p[-7]], pilaOperandos.pop(), None, None)

def p_NP_FuncOtroArg2(p):
    'NP_FuncOtroArg2 :'
    # Crear cuadruplo de la funcion obteniendo su argumento de la pila
    crearCuadruplo(code[p[-8]], pilaOperandos.pop(), None, None)

# Nueva constante string
def p_NP_LeerSinArgs(p):
	'NP_LeerSinArgs :'
	pass
    # Crear la direccion de mem si no existe
    ##crearCuadruplo(code[p[-3]], None, None, None)

#==============================================================================================
# Agrega un registro a la memoria
def registrarReg(dato, tipo):
	dirConstantes[dato] = registrosMem[contadorReg[tipo]] # Guardar el dato con su direccion de memoria
	registrosMem[contadorReg[tipo]] += 1 # Mover el contador a siguiente direccion de memoria

# Termina la ejecucion del programa y muestra un mensaje
def finalizar(mensaje):
    print(mensaje)
    sys.exit()

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
	if valBool == 'verdadero': pilaOperandos.append(registrosMem[contadorReg['booleanCTE']] + 1)
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

def validarIDSemantica(IDNombreActual):
	# Validar que existe la variable
	if not existeVariable(IDNombreActual):
		finalizar("Linea " + str(lineaActual) + " -> La variable " + IDNombreActual + " no está declarada")

	# Si variable existe, insertarla en la pila de operandos
	if funcionActual == '' or IDNombreActual in dirProcedimientos['funciones'][funcionActual]['variables']:
		# las variables locales no tienen privilegios
		pilaOperandos.append(dirProcedimientos['funciones'][funcionActual]['variables'][IDNombreActual]['mem'])

	elif IDNombreActual in dirProcedimientos['variables']:
		# Estan siendo utilizadas dentro de su contexto, no ocupo privilegios
		pilaOperandos.append(dirProcedimientos['variables'][IDNombreActual]['mem'])
	# Borrar este else
	else:
		finalizar("Linea " + str(lineaActual) + " -> La variable " + IDNombreActual + " no fue encontrada")

def getEspacioMemoria(tipoVariable, scope):
    tipoMemoria = tipoVariable + scope                # Tipo de dato para saber donde guardar
    registrosMem[contadorReg[tipoMemoria]] += 1       # Aumentar el contador de ese tipo de dato
    return registrosMem[contadorReg[tipoMemoria]] - 1 # Regresar la posicion de memoria en que se guardo
