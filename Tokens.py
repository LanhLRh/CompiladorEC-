import ply.lex as lex
from SemanticaEC import setLineaActual
from SemanticaEC import getLineaActual

# Tokens
tokens = [
    'MAS', 'MENOS', 'MULTI', 'DIV', 'MENOR', 'MAYOR', 'DIFERENTE', 'IGUAL', 'MENOR_IGUAL', 'MAYOR_IGUAL',
    'ASIGNACION', 'OP_Y', 'OP_O', 'RESIDUO', 'NEGACION',
    'PUNTOYCOMA', 'COMA', 'PAREN_IZQ','PAREN_DER', 'CORCHETE_IZQ', 'CORCHETE_DER',
    'LLAVE_IZQ', 'LLAVE_DER', 'ID', 'CTE_STRING', 'CTE_INT','CTE_DEC'
]

palabras_reservadas = {
    'int'   	        : 'VAR_INT',
    'dec' 	            : 'VAR_DEC',
    'boolean'           : 'VAR_BOOL',
    'string'            : 'VAR_STRING',
    'verdadero'         : 'VERDADERO',
    'falso'             : 'FALSO',
    'inicio' 	        : 'INICIO',
    'regresa'			: 'REGRESA',
    'func'              : 'FUNC',
    'void'              : 'VOID',
    'nulo'              : 'NULO',
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
    'dibujar_cuadricula'    : 'MAPA_CUAD',
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
t_DIFERENTE = r'\!\='
t_IGUAL = r'\=\='
t_ASIGNACION = r'\='
t_NEGACION = r'\!'
t_OP_Y = r'\&'
t_OP_O = r'\|'
t_RESIDUO = r'\%'
t_PUNTOYCOMA = r'\;'
t_COMA = r'\,'
t_PAREN_IZQ = r'\('
t_PAREN_DER = r'\)'
t_LLAVE_IZQ = r'\{'
t_LLAVE_DER = r'\}'
t_CORCHETE_IZQ = r'\['
t_CORCHETE_DER = r'\]'
t_CTE_STRING = r'\"(\\.|[^"])*\"|\"\"'
t_CTE_INT = r'\-?[0-9]+'
t_CTE_DEC = r'\-?[0-9]+\.[0-9]+'

# Tokens + palabras reservadas
tokens = tokens + list(palabras_reservadas.values())

# ID's
def t_ID(p):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    p.type = palabras_reservadas.get(p.value,'ID')
    return p

# Caracteres ignorados
t_ignore = ' \t'

# Comentarios
def t_COMENTARIO(p):
	r'\#.*'
	pass

# Comentarios
def t_newline(p):
    r'\n+'
    p.lexer.lineno += len(p.value)
    setLineaActual(getLineaActual() + len(p.value))

class LexerError(Exception): pass

# Caracteres invalidos
def t_error(p):
    global bCorrecto
    bCorrecto = False
    raise LexerError("Caracter ilegal '%s'" % p.value[0])
    #print("Caracter ilegal '%s'" % p.value[0])
    #p.lexer.skip(1)

# Construcion del lexer
lex.lex()