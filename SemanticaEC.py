import sys

# SEMANTICA ===================================================================================================
# Directorio de procedimientos
directorioProced = {}

# Guarda el ultimo tipo de dato parseado. Su valor es el ultimo tipo de dato declarado
tipoActual = ''
tipoFuncion = ''

# Guarda la funcion actual que se esta parseando. Su valor se actualiza si se entra a parsear una nueva funcion
funcionActual = ''
    
# Pila que guarda los operadores pendientes por resolver
pilaOperadores = []

# Pila que guardar las direcciones de los operandos pendientes por resolver
stackDirMem = []

# Pila de saltos que garda cuadruplos pendientes por llenar
pilaSaltos = []

numParametros = 1 # Numero de parametros
tamanoActual = 0  # Tamaño del arreglo

def p_imprimir(p):
    'imprimir : '
    print(directorioProced)

def p_NP1_DirProced(p):
	'NP1_DirProced : '
	global directorioProced
	directorioProced = {'funciones': {}, 'variables': {}}

	
def p_NP2_NombreFunc(p):
	'NP2_NombreFunc : '
	global numParametros, funcionActual
	numParametros = 1
	# Guardar nombre y tipo de la funcion
	tipoFuncion = p[-2]
	funcionActual = p[-1]

	# Comprobar que no sea nombre de una funcion
	if funcionActual in directorioProced['funciones']:
		finalizar("Nombre ya usado por otra funcion")

	# Agregar funcion al directorio	
	directorioProced['funciones'][funcionActual] = {'retorno' : tipoFuncion, 'variables' : {}, 'parametros' : {}}

def p_NP7_Inicio(p):
	'NP7_Inicio : '
	global funcionActual
	# Comprobar que no haya otro inicio
	funcionActual = 'inicio'

	if funcionActual in directorioProced['funciones']:
		finalizar("El inicio ya fue declarado en otra parte")

	# Agregar funcion al directorio	
	directorioProced['funciones']['inicio'] = {'retorno' : 'void', 'variables' : {}, 'parametros' : {}}

def p_NP3_Parametros(p):
	'NP3_Parametros : '
	global tipoActual, tamanoActual, numParametros
	nombreParametro = p[-1]

	if nombreParametro in directorioProced['funciones'][funcionActual]:
		finalizar("Nombre ya usado por otro parametro")
	directorioProced['funciones'][funcionActual]['parametros'][numParametros] = {'nombre' : nombreParametro, 'tipo' : tipoActual, 'tamano' : tamanoActual}

	numParametros += 1

def p_NP4_Variable(p):
	'NP4_Variable : '
	global tipoActual, tamanoActual

	tamanoActual = 0
	nombreVariable = p[-1] # Nombre de la variable (valor de ID)

	# Comprobar que no sea nombre de variable
	if existeVariable(nombreVariable):
		finalizar("Nombre de variable repetido")
 	
	# Si estamos dentro de una funcion (variable local)
	if funcionActual != '':
		# Se mete la variable al directorio
		directorioProced['funciones'][funcionActual]['variables'][nombreVariable] = {'tipo': tipoActual, 'tamano': 0}
	# Si estamos fuera de una funcion
	else:
		directorioProced['variables'][nombreVariable] = {'tipo': tipoActual, 'tamano': 0}

def p_sNP6_Lista(p):
	'NP6_Lista :'
	# Obtenemos el tamaño del arreglo
	tamanoArreglo = p[-1]

	# Si el tamaño es menor a 0
	if int(tamanoArreglo) < 0:
		finalizar("El tamaño del arreglo debe ser mayor o igual a 0")
	# Obtenemos el nombre del arreglo, ya fue declarado, solo hay que actualizar el tamano
	nombreVariable = p[-3]

	# Actualizar tamaño de la variable (arreglo)
	if funcionActual != "":
		directorioProced['funciones'][funcionActual]['variables'][nombreVariable]['tamano'] = tamanoArreglo
	else:
		directorioProced['variables'][nombreVariable]['tamano'] = tamanoArreglo

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

def existeVariable(nombreVariable):
    # Si estamos dentro de una funcion
    if funcionActual != '':
        # Si es una variable dentro de la funcion
        if nombreVariable in directorioProced['funciones'][funcionActual]['variables']:
            return True
    # Si es una variable de global
    if nombreVariable in directorioProced['variables']:
        return True
    return False

