# Gramatica
import ply.lex as lex
import ply.yacc as yacc
import sys

# Bandera que indica si esta correcta la entrada
bCorrecto = True

# Tokens
tokens = [
    'MAS', 'MENOS', 'MULTI', 'DIV', 'MENOR', 'MAYOR', 'DIFERENTE', 'IGUAL', 'MENOR_IGUAL', 'MAYOR_IGUAL', 'ASIGNACION',
    'OP_Y', 'OP_O', 'RESIDUO', 'NEGACION',
    'DOSPUNTOS','PUNTOYCOMA', 'COMA', 'PAREN_IZQ','PAREN_DER', 'CORCHETE_IZQ', 'CORCHETE_DER',
    'LLAVE_IZQ', 'LLAVE_DER', 'ID', 'CTE_STRING', 'CTE_INT','CTE_DEC'
]

palabras_reservadas = {
    'int'   	        : 'VAR_INT',
    'dec' 	            : 'VAR_DEC',
    'boolean'           : 'VAR_BOOL',
    'string'            : 'VAR_STRING',
    'verdadero'         : 'BOOL_VERDADERO',
    'falso'             : 'BOOL_FALSO',
    'inicio' 	        : 'INICIO',
    'func'              : 'FUNC',
    'void'              : 'VOID',
    'imprimir' 	        : 'IMPRIMIR',
    'si'	            : 'SI',
    'sino'	            : 'SINO',
    'mientras'          : 'MIENTRAS',
    'repetir'           : 'REPETIR',
    'colocarObjeto'     : 'COLOCAR',
    'mover'             : 'MOVER',
    'rotar'             : 'ROTAR',
    'girarDerecha'      : 'GIRAR_DER',
    'girarIzquierda'    : 'GIRAR_IZQ',
    'caminoLibre'       : 'CAMINO_LIBRE',
    'deteccion'         : 'DETECCION',
    'ocultar'           : 'OCULTAR',
    'posicion'          : 'POSICION',
    'mapaCuadricula'    : 'MAPA_CUAD',
    'recogerObjeto'     : 'RECOGER_OBJ',
    'dejarObjeto'       : 'DEJAR_OBJ',
    'saltar'            : 'SALTAR',
    'matarEnemigo'      : 'MATAR_ENEMY',
    'color'             : 'COLOR',
    'trazo'             : 'TRAZO',
    'leer'              : 'LEER',
    'escribir'          : 'ESCRIBIR',
    'mostrarValor'      : 'MOSTRAR_VALOR',
    'fin'               : 'FIN'
}

# Tokens
t_MAS = r'\+'
t_MENOS = r'\-'
t_MULTI = r'\*'
t_DIV = r'\/'
t_MENOR = r'\<'
t_MAYOR = r'\>'
t_MAYOR_IGUAL = r'\>\='
t_MENOR_IGUAL = r'\<\='
t_DIFERENTE = r'\<\>'
t_IGUAL = r'\=\='
t_ASIGNACION = r'\='
t_NEGACION = r'\!'
t_OP_Y = r'\&'
t_OP_O = r'\|'
t_RESIDUO = r'\%'
t_DOSPUNTOS = r'\:'
t_PUNTOYCOMA = r'\;'
t_COMA = r'\,'
t_PAREN_IZQ = r'\('
t_PAREN_DER = r'\)'
t_LLAVE_IZQ = r'\{'
t_LLAVE_DER = r'\}'
t_CORCHETE_IZQ = r'\['
t_CORCHETE_DER = r'\]'
t_CTE_STRING = r'\"(\\.|[^"])*\"|\"\"'
t_CTE_INT = r'[0-9]+'
t_CTE_DEC = r'[0-9]+\.[0-9]+'

# Tokens + palabras reservadas
tokens = tokens + list(palabras_reservadas.values())

# ID's
def t_ID(t):
    r'[a-zA-Z]([a-zA-Z0-9]|\_)*'
    t.type = palabras_reservadas.get(t.value,'ID')
    return t

# Caracteres ignorados
t_ignore = ' \t\n'

# Caracteres invalidos
def t_error(t):
    global bCorrecto
    bCorrecto = False
    print("Caracter invalido '%s'" % t.value[0])
    t.lexer.skip(1)

# Construcion del lexer
lex.lex()

# Reglas
def p_programa(t):
    'programa : definicion INICIO LLAVE_IZQ instruccion LLAVE_DER definicion'

def p_definicion(t):
    '''definicion :  definicionP
                   | empty'''
def p_definicionP(t):
    '''definicionP : funcion definicion
                    | declaracion definicion'''

def p_instruccion(t):
    'instruccion : instruccionP PUNTOYCOMA instruccionP'
def p_instruccionP(t):
    '''instruccionP : declaracion | asignacion | condicion | ciclo | llamada | empty'''

def p_funcion(t):
    'funcion : FUNC funcionP LLAVE_DER'
def p_funcionP(t):
    '''funcionP : tipo cuerpo_funcion REGRESA expresion
                | VOID cuerpo_funcion'''
    
def p_cuerpo_funcion(t):
    'cuerpo_funcion : ID PAREN_IZQ cfP PAREN_DER LLAVE_IZQ instruccion LLAVE_DER'
def p_cfP(t):
    '''cfP : tipo ID cfPP | empty'''
def p_cfPP(t):
    '''cfPP : COMA cfPPP | empty'''
def p_cfPPP(t):
    '''cfPPP : cfP | ID cfPP'''
    
def p_declaracion(t):
    'declaracion : tipo declaracionP'
def p_declaracionP(t):
    'declaracionP : ID declaracionPPP declaracionPP'
def p_declaracionPP(t):
    '''declaracionPP : COMA declaracionP | empty'''
def p_declaracionPPP(t):
    '''declaracionPPP : expresion | declaracion_lista | empty'''
    
def p_declaracion_lista(t):
    '''declaracion : ASIGNACION lista | CORCHETE_IZQ INT CORCHETE_DER'''
    
def p_asignacion(t):
    'asignacion : ID asignacionP ASIGNACION expresion'
def p_asignacionP(t):
    '''asignacionP : CORCHETE_IZQ INT CORCHETE_DER | empty'''

def p_condicion(t):
    'condicion : SI PAREN_IZQ expresion PAREN_DER LLAVE_IZQ instrucion condicionP'
def p_condicionP(t):
    '''condicionP : SINO condicionPP | empty'''
def p_condicionPP(t):
    '''condicionPP : LLAVE_IZQ instruccion LLAVE_DER | condicion'''

# MODIFICACION: repetir puede usar una variable entera o una constante entera
def p_ciclo(t):
    '''ciclo : MIENTRAS PAREN_IZQ expresion PAREN_DER LLAVE_IZQ instruccion LLAVE_DER
                | REPETIR repetir LLAVE_IZQ instruccion LLAVE_DER'''
def p_repetir(t):
    '''repetir : CTE_INT | ID'''

def p_llamada(t):
    'llamada : id LLAVE_IZQ llamadaP LLAVE_DER'
def p_llamadaP(t):
    '''llamadaP : expresion llamadaPP | empty'''
def p_llamadaPP(t):
    '''llamadaPP : COMA llamadaP | empty'''
    
def p_expresion(t):
    'expresion : subExp expresionP'
def p_expresionP(t):
    '''expresionP : OP_Y expresion | OP_O expresion | empty'''
    
def p_subExp(t):
    'subExp : subExpP exp subExpPP'
def p_subExpP(t):
    '''subExp : NEGACION | empty'''
def p_subExpPP(t):
    '''subExpPPP : comparador exp | empty'''

# Vacio (epsilon)
def p_empty(t):
    'empty :'

# Error de sintaxis 
def p_error(t):
    global bCorrecto
    bCorrecto = False
    print("Error de sintaxis en '%s'" % t.value)
    sys.exit()

# Creacion del parser
parser = yacc.yacc()

# Lectura de archivo
nombreArchivo = raw_input("Nombre del archivo: ")
archivo = open(nombreArchivo, 'r')
contenidoArch = archivo.read()
parser.parse(contenidoArch)    

# Notificar si el archivo esta correcto o no
if bCorrecto == True:
    print("Archivo correcto")
else: 
    print("Archivo incorrecto")
raw_input()
sys.exit()
