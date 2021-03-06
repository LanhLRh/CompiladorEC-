code = {
    # Error
    'error': 0,

    # Tipos de datos
    'int': 1,
    'dec': 2,
    'boolean': 3,
    'string': 4,

    # Operadores
    # Op aritmeticos
    '+': 12,
    '-': 13,
    '*': 14,
    '/': 15,
    '%': 16,
    # Op Asignación
    '=': 20,
    # Op relacionales
    '>': 22,
    '<': 23,
    '>=': 24,
    '<=': 25,
    '==': 26,
    '!=': 27,
    # Op logicos
    '|': 28,
    '&': 29,
    # Op agrupación
    '(': 30,
    ')': 31,

    # Saltos
    'goto': 50,
    'gotof': 51,

    # Funciones especiales
    'mostrar': 55,
    'leer' : 56,
    'inicio' 	        : 57,
    'regresa'			: 58,
    'colocarObjeto'     : 59,
    'mover'             : 60,
    'rotar'             : 61,
    'girarDerecha'      : 62,
    'girarIzquierda'    : 63,
    'caminoLibre'       : 64,
    'deteccion'         : 65,
    'ocultar'           : 66,
    'posicion'          : 67,
    'dibujar_cuadricula': 68,
    'recogerObjeto'     : 69,
    'dejarObjeto'       : 70,
    'saltar'            : 71,
    'matarEnemigo'      : 72,
    'color'             : 73,
    'trazo'             : 74,
    'leer'              : 75,
    'escribir'          : 76,
    'mostrarValor'      : 77,
    'fin'               : 78,
    'colorFondo'        : 79, 
    'dibujaCirculo'     : 80,
    'rellenarForma'     : 81,

    # Valor nulo
    'nulo' : 90,
    # Negación
    '!': 91,
    'verdadero': 92,
    'falso': 93,

    # Otros
    'finProc': 100,
    'ERA': 101,
    'parametro' : 102,
    'inicioFunc' : 103,
    'retu' : 104,
    'gosub': 105,
    'ver'  : 106
}

simb = {

}

def simbol(codigo):
    return list(code.keys())[list(code.values()).index(codigo)]

# Posiciones de memoria a asignar
# Posicion inicial
posInicial = {
    # Funciones
    'intGlobal': 100,
    'decGlobal': 1100,
    'stringGlobal': 2100,
    'booleanGlobal': 3100,

    # Funciones
    'intLocal': 4100,
    'decLocal': 5100,
    'stringLocal': 6100,
    'booleanLocal': 7100,
    
    # Registros termporales
    'intTemp': 8100,
    'decTemp': 9100,
    'stringTemp': 10100,
    'booleanTemp': 11100,
    
    # Constantes
    'intCTE': 12100,
    'decCTE': 13100,
    'stringCTE': 14100,
    'booleanCTE': 15100,

}

# Posicion final
posLimite = {
   
    'intGlobal': 1099,
    'decGlobal': 2099,
    'stringGlobal': 3099,
    'booleanGlobal': 4099,

    'intLocal': 5099,
    'decLocal': 6099,
    'stringLocal': 7099,
    'booleanLocal': 8099,
    
    'intTemp': 9099,
    'decTemp': 10099,
    'stringTemp': 11099,
    'booleanTemp': 12099,
    
    'intCTE': 13099,
    'decCTE': 14099,
    'stringCTE': 15099,
    'booleanCTE': 16099
}

# Contador de registros por variable
contadorReg = {
    
    'intGlobal': 0,
    'decGlobal': 1,
    'stringGlobal': 2,
    'booleanGlobal': 3,
    
    'intTemp': 4,
    'decTemp': 5,
    'stringTemp': 6,
    'booleanTemp': 7,
    
    'intCTE': 8,
    'decCTE': 9,
    'stringCTE': 10,
    'booleanCTE': 11,

    'intLocal': 12,
    'decLocal': 13,
    'stringLocal': 14,
    'booleanLocal': 15,
}