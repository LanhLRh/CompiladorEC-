import sys
from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QColor, QTextCharFormat, QFont, QSyntaxHighlighter

# Regresa un QTextCharFormat con los atributos dados
def format(color, estilo=''):
    _color = QColor()
    if type(color) is not str:
        _color.setRgb(color[0], color[1], color[2])
    else:
        _color.setNamedColor(color)

    _format = QTextCharFormat()
    _format.setForeground(_color)
    if 'bold' in estilo:
        _format.setFontWeight(QFont.Bold)
    if 'italic' in estilo:
        _format.setFontItalic(True)

    return _format


# Estilos de sintaxis
ESTILOS = {
    'keyword': format([200, 120, 50], 'bold'),
    'operador': format([150, 150, 150]),
    'llave': format('darkGray'),
    'funcDefini': format([220, 220, 255], 'bold'),
    'string': format([20, 110, 100]),
    'comentario': format([128, 128, 128]),
    'numeros': format([100, 150, 190]),
    'variables': format([229, 103, 103]),
}

# Resaltador de Sintaxis del EC++
class ResaltadorLineas(QSyntaxHighlighter):

    # Palabras clave
    keywords = [
        'func','repetir', 'si', 'sino',
        'regresa', 'mientras',
        'Nulo', 'verdadero', 'falso',
    ]

    # Variables
    variables = [
        'int', 'dec', 'string', 'boolean', 'void'
    ]

    # Operadores
    operadores = [
        '=',
        # Comparación
        '==', '!=', '<', '<=', '>', '>=',
        # Aritmetico
        '\+', '-', '\*', '/', '\%', '\*\*',
        # Logicos
        '\^', '\|', '\&', '\!'
    ]

    # Brackets, Llaves y Parentesis
    llaves = [
        '\{', '\}', '\(', '\)', '\[', '\]',
    ]

    def __init__(self, document):
        QSyntaxHighlighter.__init__(self, document)

        reglas = []

        # Reglas de keyword, operadores, variables, llaves
        reglas += [(r'\b%s\b' % w, 0, ESTILOS['keyword'])
                  for w in ResaltadorLineas.keywords]
        reglas += [(r'\b%s\b' % v, 0, ESTILOS['variables'])
                  for v in ResaltadorLineas.variables]                  
        reglas += [(r'%s' % o, 0, ESTILOS['operador'])
                  for o in ResaltadorLineas.operadores]
        reglas += [(r'%s' % b, 0, ESTILOS['llave'])
                  for b in ResaltadorLineas.llaves]

        # Demas reglas
        reglas += [

            # String (delimitado por doble comilla)
            (r'"[^"\\]*(\\.[^"\\]*)*"', 0, ESTILOS['string']),

            # Funcion [func] seguido de un identificador
            (r'\bfunc\b\s*\bvoid\b\s*(\w+)', 1, ESTILOS['funcDefini']),
            (r'\bfunc\b\s*\bint\b\s*(\w+)', 1, ESTILOS['funcDefini']),
            (r'\bfunc\b\s*\bdec\b\s*(\w+)', 1, ESTILOS['funcDefini']),
            (r'\bfunc\b\s*\bstring\b\s*(\w+)', 1, ESTILOS['funcDefini']),
            (r'\bfunc\b\s*\bboolean\b\s*(\w+)', 1, ESTILOS['funcDefini']),

            # Llamadas a funciones (no funciona bien)
            #(r'[a-zA-Z]+\([^\)]*\)(\.[^\)]*\))?', 0, ESTILOS['funcDefini']),

            # Comentario (inicia con un #)
            (r'#[^\n]*', 0, ESTILOS['comentario']),

            # Numeros
            (r'\b[+-]?[0-9]+[lL]?\b', 0, ESTILOS['numeros']),
            (r'\b[+-]?0[xX][0-9A-Fa-f]+[lL]?\b', 0, ESTILOS['numeros']),
        ]

        # Crea un QRegExp para cada patron
        self.reglas = [(QRegExp(pat), index, fmt)
                      for (pat, index, fmt) in reglas]

    # Aplica el resaltado de sintaxis al bloque recibido de texto
    def highlightBlock(self, text):

        # Hacer el resto de formateo de sintaxis
        for expression, nth, format in self.reglas:
            index = expression.indexIn(text, 0)

            while index >= 0:
                # Queremos el index de el nth match
                index = expression.pos(nth)
                length = len(expression.cap(nth))
                self.setFormat(index, length, format)
                index = expression.indexIn(text, index + length)

        self.setCurrentBlockState(0)