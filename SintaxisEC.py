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


# Syntax styles that can be shared by all languages
STYLES = {
    'keyword': format([200, 120, 50], 'bold'),
    'operador': format([150, 150, 150]),
    'llave': format('darkGray'),
    'defclass': format([220, 220, 255], 'bold'),
    'string': format([20, 110, 100]),
    'comentario': format([128, 128, 128]),
    'numeros': format([100, 150, 190]),
    'variables': format([150,120,140])
}

# Syntax highlighter for the Python language
class ResaltadorLineas(QSyntaxHighlighter):

    # Palabras clave
    keywords = [
        'def','repetir', 'si', 'sino',
        'regresar', 'mientras',
        'Nulo', 'Verdadero', 'Falso',
    ]

    # Variables
    variables = [
        'int', 'dec', 'string', 'boolean'
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
        reglas += [(r'\b%s\b' % w, 0, STYLES['keyword'])
                  for w in ResaltadorLineas.keywords]
        reglas += [(r'\b%s\b' % v, 0, STYLES['variables'])
                  for v in ResaltadorLineas.variables]                  
        reglas += [(r'%s' % o, 0, STYLES['operador'])
                  for o in ResaltadorLineas.operadores]
        reglas += [(r'%s' % b, 0, STYLES['llave'])
                  for b in ResaltadorLineas.llaves]

        # Demas reglas
        reglas += [

            # String (delimitado por doble comilla)
            (r'"[^"\\]*(\\.[^"\\]*)*"', 0, STYLES['string']),

            # Funcion [def] seguido de un identificador
            (r'\bdef\b\s*(\w+)', 1, STYLES['defclass']),

            # Comentario (inicia con un #)
            (r'#[^\n]*', 0, STYLES['comentario']),

            # Numeros
            (r'\b[+-]?[0-9]+[lL]?\b', 0, STYLES['numeros']),
            (r'\b[+-]?0[xX][0-9A-Fa-f]+[lL]?\b', 0, STYLES['numeros']),
        ]

        # Crea un QRegExp para cada patron
        self.reglas = [(QRegExp(pat), index, fmt)
                      for (pat, index, fmt) in reglas]

    # Aplica el resaltado de sintaxis al bloque recibido de texto
    def highlightBlock(self, text):

        # Do other syntax formatting
        for expression, nth, format in self.reglas:
            index = expression.indexIn(text, 0)

            while index >= 0:
                # Queremos el index de el nth match
                index = expression.pos(nth)
                length = len(expression.cap(nth))
                self.setFormat(index, length, format)
                index = expression.indexIn(text, index + length)

        self.setCurrentBlockState(0)