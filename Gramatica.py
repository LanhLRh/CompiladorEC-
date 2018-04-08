# Gramatica
import ply.yacc as yacc
from Tokens import tokens
from SemanticaEC import *

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
	crearCuadruplo(code["finProc"], None, None, None)
def p_funcionP(p):
	'''funcionP : VOID cuerpo_funcion
                | tipo cuerpo_funcion REGRESA expresion'''
	setFuncionActual('') # Se acabo la funcion
    
def p_cuerpo_funcion(p):
    'cuerpo_funcion : ID NP2_NombreFunc PAREN_IZQ parametro PAREN_DER LLAVE_IZQ instruccion LLAVE_DER'
def p_parametro(p):
    '''parametro : tipo tipoParametro ID NP3_Parametros otroParametro
				| empty'''
def p_otroParametro(p):
	'''otroParametro : COMA parametro otroParametro
    				| empty'''
def p_tipoParametro(p):
	'''tipoParametro : OP_Y
						| empty'''
    
def p_declaracion(p):
	'declaracion : tipo declaracionP'
def p_declaracionP(p):
    'declaracionP : ID NP4_Variable declaracionPPP declaracionPP'
def p_declaracionPP(p):
	'''declaracionPP : COMA declaracionP
    					| empty'''
def p_declaracionPPP(p):
	'''declaracionPPP : ASIGNACION NP_VariableAPila expresion NP_Asignacion
    					| declaracion_lista NP6_Lista
    					| empty'''
    
# MODIFICACION: Se cambio la declaracion de lista
def p_declaracion_lista(p):
	'''declaracion_lista : ASIGNACION lista
    					| CORCHETE_IZQ CTE_INT CORCHETE_DER'''
	p[0] = p[2]
    
# MODIFICION: Se cambio la asignacion a una lista
def p_asignacion(p):
    'asignacion : ID asignacionP ASIGNACION NP_VariableAPila expresion NP_Asignacion'
def p_asignacionP(p):
	'''asignacionP : CORCHETE_IZQ expresion CORCHETE_DER
    				| empty'''

def p_condicion(p):
    'condicion : SI PAREN_IZQ expresion PAREN_DER NP_Si_Expresion LLAVE_IZQ instruccion LLAVE_DER condicionP'
def p_condicionP(p):
	'''condicionP : SINO NP_Sino condicionPP
    				| empty'''
def p_condicionPP(p):
	'''condicionPP : LLAVE_IZQ instruccion LLAVE_DER NP_Si_Cierre
    				| condicion'''

# MODIFICACION: repetir puede usar una variable entera o una constante entera
def p_ciclo(p):
	'''ciclo : MIENTRAS NP_Ciclo_Inicio PAREN_IZQ expresion NP_Ciclo PAREN_DER LLAVE_IZQ instruccion LLAVE_DER NP_Ciclo_Cierre
             | REPETIR NP_Ciclo_Inicio expresion NP_Ciclo LLAVE_IZQ instruccion LLAVE_DER NP_Ciclo_Cierre'''

def p_llamada(p):
	'''llamada : funcionEspecial 
				| ID NP_ERA LLAVE_IZQ llamadaP LLAVE_DER'''
def p_llamadaP(p):
	'''llamadaP : expresion NP_Argumento llamadaPP
    			| empty'''
def p_llamadaPP(p):
	'''llamadaPP : COMA llamadaP
    			| empty'''
    
def p_expresion(p):
	'expresion : subExp NP_OpLogicosPendientes NP_OpLogicosPendientes expresionP'
def p_expresionP(p):
	'''expresionP : opLogico expresion
				  | empty'''
def p_opLogico(p):
	'''opLogico : OP_Y 
				| OP_O'''
	pushPilaOperadores(p[1])
    
def p_subExp(p):
	'subExp : subExpP exp NP_OpRelacionalesPendientes subExpPP'
def p_subExpP(p):
	'''subExpP : NEGACION
				| empty'''
def p_subExpPP(p):
	'''subExpPP : comparador subExp
    			| empty'''
    
def p_exp(p):
	'exp : termino NP_SumResPendientes otroExp'
def p_otroExp(p):
	'''otroExp : opAritmetico exp
    			| empty'''
def p_opAritmetico(p):
	'''opAritmetico : MAS
    				| MENOS'''
	pushPilaOperadores(p[1])

def p_termino(p):
	'termino : factor NP_MulDivResPendientes terminoP'
def p_terminoP(p):
	'''terminoP : opMulDivRes termino
				| empty'''
def p_opMulDivRes(p):
	'''opMulDivRes :  MULTI
    				| DIV 
    				| RESIDUO'''
	pushPilaOperadores(p[1])
    
def p_comparador(p):
	'''comparador :   MENOR
    				| MAYOR
    				| IGUAL
    				| DIFERENTE
    				| MENOR_IGUAL
    				| MAYOR_IGUAL'''
	pushPilaOperadores(p[1])
    
def p_constante(p):
	'''constante : NULO
				 | CTE_INT NP_IntCTE
				 | CTE_DEC NP_DecimalCTE
				 | CTE_STRING NP_StringCTE
				 | boolean'''
    
def p_factor(p):
	'''factor : PAREN_IZQ NP_AgrupacionAbre expresion PAREN_DER NP_AgrupacionCierra
    			| valor'''
    
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
    			| identificador
    			| constante'''

def p_tipo(p):
	'''tipo : VAR_INT
			| VAR_DEC
			| VAR_STRING
			| VAR_BOOL'''
	p[0] = p[1]
	setTipoActual(p[1])
    
def p_boolean(p):
	'''boolean :  VERDADERO
    			| FALSO'''
	nuevaBoolCTE(p[1])

def p_identificar(p):
	'identificador : ID'
	validarIDSemantica(p[1])
	p[0] = p[1]

# Funciones especiales
def p_funcionEspecial(p):
	'''funcionEspecial : COLOCAR NP_ERA PAREN_IZQ expresion NP_FuncUnArg COMA expresion NP_FuncOtroArg1 COMA expresion NP_FuncOtroArg2 PAREN_DER
						| MOVER NP_ERA PAREN_IZQ expresion NP_FuncUnArg PAREN_DER
						| ROTAR NP_ERA PAREN_IZQ expresion NP_FuncUnArg PAREN_DER
						| GIRAR_DER NP_ERA PAREN_IZQ PAREN_DER NP_FuncSinArgs
						| GIRAR_IZQ NP_ERA PAREN_IZQ PAREN_DER NP_FuncSinArgs
						| CAMINO_LIBRE NP_ERA PAREN_IZQ PAREN_DER NP_FuncSinArgs
						| DETECCION NP_ERA PAREN_IZQ PAREN_DER NP_FuncSinArgs
						| OCULTAR NP_ERA PAREN_IZQ expresion NP_FuncUnArg PAREN_DER
						| POSICION NP_ERA PAREN_IZQ expresion NP_FuncUnArg COMA expresion NP_FuncOtroArg1 PAREN_DER
						| MAPA_CUAD NP_ERA PAREN_IZQ expresion NP_FuncUnArg PAREN_DER
						| RECOGER_OBJ NP_ERA PAREN_IZQ PAREN_DER NP_FuncSinArgs
						| DEJAR_OBJ NP_ERA PAREN_IZQ PAREN_DER NP_FuncSinArgs
						| SALTAR NP_ERA PAREN_IZQ PAREN_DER NP_FuncSinArgs
						| MATAR_ENEMY NP_ERA PAREN_IZQ PAREN_DER NP_FuncSinArgs
						| COLOR NP_ERA PAREN_IZQ expresion NP_FuncUnArg PAREN_DER
						| TRAZO NP_ERA PAREN_IZQ expresion NP_FuncUnArg COMA expresion NP_FuncOtroArg1 PAREN_DER
						| LEER NP_ERA PAREN_IZQ leerP PAREN_DER NP_LeerSinArgs
						| ESCRIBIR NP_ERA PAREN_IZQ expresion NP_FuncUnArg PAREN_DER
						| MOSTRAR_VALOR NP_ERA PAREN_IZQ expresion NP_FuncUnArg PAREN_DER
						| FIN NP_ERA PAREN_IZQ PAREN_DER NP_FuncSinArgs
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
    print("Error de sintaxis en '" + str(p.value) + "' en la linea ", str(p.lineno))
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
if bCorrecto == True: print("Archivo correcto")
else: print("Archivo incorrecto")
input()
sys.exit()
