# Gramatica
import ply.yacc as yacc
from Tokens import tokens
from SemanticaEC import *
import Stack

# Bandera que indica si esta correcta la entrada
bCorrecto = True

# Regla Inicial
def p_programa(p):
    'programa : NP1_DirProced definicion INICIO NP7_Inicio LLAVE_IZQ instruccion LLAVE_DER definicion imprimir'

def p_definicion(p):
    '''definicion :  definicionP
                   | empty'''
def p_definicionP(p):
    '''definicionP : funcion definicion
                    | declaracion definicion'''

def p_instruccion(p):
    '''instruccion : declaracion PUNTOYCOMA instruccion
    				| llamada PUNTOYCOMA instruccion
				    | asignacion PUNTOYCOMA instruccion
				    | condicion instruccion
				    | ciclo instruccion
				    | empty'''

def p_funcion(p):
    'funcion : FUNC funcionP'
def p_funcionP(p):
	'''funcionP : VOID cuerpo_funcion
                | tipo cuerpo_funcion REGRESA expresion'''
	setFuncionActual('') # Se acabo la funcion
    
def p_cuerpo_funcion(p):
    'cuerpo_funcion : ID NP2_NombreFunc PAREN_IZQ parametro PAREN_DER LLAVE_IZQ instruccion LLAVE_DER'
def p_parametro(p):
    '''parametro : tipo ID NP3_Parametros otroParametro
				| empty'''
def p_otroParametro(p):
	'''otroParametro : COMA parametro otroParametro
    				| empty'''
    
def p_declaracion(p):
    'declaracion : tipo declaracionP'
def p_declaracionP(p):
    'declaracionP : ID NP4_Variable declaracionPPP declaracionPP'
def p_declaracionPP(p):
	'''declaracionPP : COMA declaracionP
    					| empty'''
def p_declaracionPPP(p):
	'''declaracionPPP : ASIGNACION expresion
    					| declaracion_lista NP6_Lista
    					| empty'''
    
# MODIFICACION: Se cambio la declaracion de lista
def p_declaracion_lista(p):
	'''declaracion_lista : ASIGNACION lista
    					| CORCHETE_IZQ CTE_INT CORCHETE_DER'''
	p[0] = p[2]
    
# MODIFICION: Se cambio la asignacion a una lista
def p_asignacion(p):
    'asignacion : ID asignacionP ASIGNACION expresion'
def p_asignacionP(p):
	'''asignacionP : CORCHETE_IZQ expresion CORCHETE_DER
    				| empty'''

def p_condicion(p):
    'condicion : SI PAREN_IZQ expresion PAREN_DER LLAVE_IZQ instruccion LLAVE_DER condicionP'
def p_condicionP(p):
	'''condicionP : SINO condicionPP
    				| empty'''
def p_condicionPP(p):
	'''condicionPP : LLAVE_IZQ instruccion LLAVE_DER
    				| condicion'''

# MODIFICACION: repetir puede usar una variable entera o una constante entera
def p_ciclo(p):
	'''ciclo : MIENTRAS PAREN_IZQ expresion PAREN_DER LLAVE_IZQ instruccion LLAVE_DER
                | REPETIR repetir LLAVE_IZQ instruccion LLAVE_DER'''
def p_repetir(p):
	'''repetir : expresion'''

def p_llamada(p):
	'''llamada : funcionEspecial
				| ID LLAVE_IZQ llamadaP LLAVE_DER'''
def p_llamadaP(p):
	'''llamadaP : expresion llamadaPP
    			| empty'''
def p_llamadaPP(p):
	'''llamadaPP : COMA llamadaP
    			| empty'''
    
def p_expresion(p):
	'expresion : subExp expresionP'
def p_expresionP(p):
	'''expresionP : OP_Y expresion
					| OP_O expresion
					| empty'''
    
def p_subExp(p):
	'subExp : subExpP exp subExpPP'
def p_subExpP(p):
	'''subExpP : NEGACION
				| empty'''
def p_subExpPP(p):
	'''subExpPP : comparador exp
    			| empty'''
    
def p_exp(p):
	'exp : termino expP'
def p_expP(p):
	'''expP : MAS termino
    		| MENOS termino
    		| empty'''

def p_termino(p):
	'termino : factor terminoP'
def p_terminoP(p):
	'''terminoP : MULTI termino
    			| DIV termino
    			| RESIDUO termino
				| empty'''
    
def p_comparador(p):
	'''comparador :   MENOR
    				| MAYOR
    				| IGUAL
    				| DIFERENTE
    				| MENOR_IGUAL
    				| MAYOR_IGUAL'''
    
def p_constante(p):
	'''constante :    NULO
    				| CTE_INT
    				| CTE_DEC
    				| CTE_STRING
    				| boolean'''
    
def p_factor(p):
	'''factor : PAREN_IZQ expresion PAREN_DER
    			| opAritmetico valor'''
def p_opAritmetico(p):
	'''opAritmetico : MAS
    				| MENOS
    				| empty'''
    
def p_lista(p):
	'lista : CORCHETE_IZQ listaVacia CORCHETE_DER'
	p[0] = getTamanoActual()
def p_listaP(p):
	'''listaP :   COMA expresion listaP
    			| empty'''
	setTamanoActual(getTamanoActual()+1)
def p_listaVacia(p):
	'''listaVacia : expresion listaP
				| empty'''

def p_valor(p):
	'''valor :    llamada
    			| ID
    			| constante'''

def p_tipo(p):
	'''tipo : VAR_INT
			| VAR_DEC
			| VAR_STRING
			| VAR_BOOL'''
	# if t[1] == 'int':
	# 	print("tipo INT")
	# elif t[1] == 'dec':
	# 	print("tipo DEC")
	# elif t[1] == 'string':
	# 	print("tipo STRING")
	# elif t[1] == 'boolean':
	# 	print("tipo BOOLEAN")
	p[0] = p[1]
	setTipoActual(p[1])
    
def p_boolean(p):
	'''boolean :  VERDADERO
    			| FALSO'''

    
# Funciones especiales
def p_funcionEspecial(p):
	'''funcionEspecial : COLOCAR PAREN_IZQ expresion COMA expresion COMA expresion PAREN_DER
						| MOVER PAREN_IZQ expresion PAREN_DER
						| ROTAR PAREN_IZQ expresion PAREN_DER
						| GIRAR_DER PAREN_IZQ PAREN_DER
						| GIRAR_IZQ PAREN_IZQ PAREN_DER
						| CAMINO_LIBRE PAREN_IZQ PAREN_DER
						| DETECCION PAREN_IZQ PAREN_DER
						| OCULTAR PAREN_IZQ expresion PAREN_DER
						| POSICION PAREN_IZQ expresion COMA expresion PAREN_DER
						| MAPA_CUAD PAREN_IZQ expresion PAREN_DER
						| RECOGER_OBJ PAREN_IZQ PAREN_DER
						| DEJAR_OBJ PAREN_IZQ PAREN_DER
						| SALTAR PAREN_IZQ PAREN_DER
						| MATAR_ENEMY PAREN_IZQ PAREN_DER
						| COLOR PAREN_IZQ expresion PAREN_DER
						| TRAZO PAREN_IZQ expresion COMA expresion PAREN_DER
						| LEER PAREN_IZQ leerP PAREN_DER
						| ESCRIBIR PAREN_IZQ expresion PAREN_DER
						| MOSTRAR_VALOR PAREN_IZQ expresion PAREN_DER
						| FIN PAREN_IZQ PAREN_DER
						'''

def p_leerP(p):
	'''leerP : expresion
    			| empty'''
    
# Vacio (epsilon)
def p_empty(p):
    'empty :'
    pass

# Error de sintaxis 
def p_error(p):
    global bCorrecto
    bCorrecto = False
    print("Error de sintaxis en '", p.value, "' en la linea ", str(p.lineno))
    sys.exit()

# Creacion del parser
parser = yacc.yacc()

# Lectura de archivo
nombreArchivo = input("Nombre del archivo: ")
archivo = open(nombreArchivo, 'r')
contenidoArch = archivo.read()
resultado = parser.parse(contenidoArch)
#print(resultado)

# Notificar si el archivo esta correcto o no
if bCorrecto == True:
    print("Archivo correcto")
else: 
    print("Archivo incorrecto")
input()
sys.exit()
