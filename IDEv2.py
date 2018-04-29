from PyQt5 import QtWidgets, uic
import os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QTextOption, QTextCursor, QFontMetrics
from PyQt5.QtGui import (QColor, QPainter, QFont, QSyntaxHighlighter, QTextFormat, QTextCharFormat)
import EditorCodigo
import SintaxisEC
import Gramatica

# Globales
app = None 				# Aplicación
ui = None 				# Elementos de la interface
cursor = None 			# Cursor
scrollbar = None 		# Barra de navegación vertical del area de codigo
tamanoFuente = 10		# Tamaño actual de la fuente de texto del codigo
numeroLinea = 0			# Numero de linea actual
nombreArchivo = None 	# Nombre del archivo de lectura/escritura
cargoArchivo = False	# Bandera que indica si se abrio un archivo

# Función que compila el programa
def compilar():
	if not ui.txtCodigo.toPlainText() == "":
		codigo = ui.txtCodigo.toPlainText()
		try:
			resultado = Gramatica.parser.parse(codigo)
		except:
			print('Fin del procedimiento')
		mostrarEnConsola()
	else:
		mensaje("No hay codigo", "Necesitas escribir codigo para poder compilar.")


# Ejecuta el input en la consola de comandos
def ejecutarInput():
	global ui
	comando = ui.lnInput.text()
	ui.lnInput.clear()
	mostrarEnConsola(comando)

# Función que actualiza el tamaño del tab deacuerdo al tamaño de font
def actualizarTab():
	font = QFont('Consolas', tamanoFuente)		# Font usada en el editor
	anchoFont = QFontMetrics(font).width(" ")	# Medida en pixeles de un espacio
	ui.txtCodigo.setTabStopWidth(4 * anchoFont) # Actualizar tamaño de tab

# Aumenta el tamaño de la letra del codigo
def aumentarLetra():
	global ui, tamanoFuente
	if tamanoFuente < 50:
		tamanoFuente += 1
		ui.txtCodigo.setFont(QFont("Consolas", tamanoFuente))
		actualizarTab()

# Disminuye el tamaño de la letra del codigo
def disminuirLetra():
	global ui, tamanoFuente
	if tamanoFuente > 4:
		tamanoFuente -= 1
		ui.txtCodigo.setFont(QFont("Consolas", tamanoFuente))
		actualizarTab()

# Coloca la salida de la consola en el cuadro de texto
def mostrarEnConsola(salida = ""):
	if salida == "":
		global ui, app, cursor, scrollbar, numeroLinea
		# Mover el cursor al final
		cursor.movePosition(QTextCursor.End)
		ui.txtCmd.setTextCursor(cursor)

		# Insertar errores de compilación en la cmd
		archivo = open("archErroresCompilacion.txt", "r") 
		contenidoArch = archivo.read() 
		ui.txtCmd.insertPlainText(str(numeroLinea) + "> " + contenidoArch + '\n')
		numeroLinea += 1

		# Mover scrollbar
		scrollbar.setValue(scrollbar.maximum())
	else:
		ui.txtCmd.insertPlainText(str(numeroLinea) + "> " + salida + '\n')

# Muetra un mensaje como ventana emergente
def mensaje(titulo="Advertencia", mensaje=""):
	QMessageBox.information(None, titulo, mensaje)

# Guarda el codigo actual en un archivo
def guardarArchivo():
	global nombreArchivo, cargoArchivo
	# Si hay un archivo cargado, lo sobreescribe
	if cargoArchivo == True:
		print('Archivo Guardado')
		with open(nombreArchivo[0], 'w') as archivo:
				codigo = ui.txtCodigo.toPlainText()
				archivo.write(codigo)
	# Si no, crea uno nuevo
	else:
		# Seleccionar donde guarda y como llamar al archivo
		nombreArchivo = QFileDialog.getSaveFileName(ui.central_widget, 'Guardar', os.getenv('HOME'))
		# Verificar que se selecciono archivo
		if nombreArchivo != ('', ''):
			with open(nombreArchivo[0], 'w') as archivo:
				codigo = ui.txtCodigo.toPlainText()
				archivo.write(codigo)
	# Informar que se guardo el archivo
	mostrarEnConsola("Archivo Guardado")

# Carga el contenido de un archivo en el area de codigo
def abrirArchivo():
	global nombreArchivo, cargoArchivo
	# Buscar archivo a abrir
	nombreArchivo = QFileDialog.getOpenFileName(ui.central_widget, 'Abrir', os.getenv('HOME'))

	# Si si se selecciono un archivo, cargarlo
	if nombreArchivo != ('', ''):
		cargoArchivo = True
		print('Cargo archivo', cargoArchivo)
		with open(nombreArchivo[0], 'r') as archivo:
			codigo = archivo.read()
			ui.txtCodigo.setPlainText(codigo)

# Limpia la pantalla y cierra el archivo actual
def nuevoArchivo():
	global nombreArchivo, cargoArchivo

	nombreArchivo = None
	cargoArchivo = False
	limpiarTexto(ui)
	mostrarEnConsola("Nuevo archivo abierto")



# Limpia el contenido de la caja de texto
def limpiarTexto(self):
    self.txtCodigo.clear()

# Cambia el area de codigo (no funciona actualmente)
def substituirCodigo():
	# Substituir la txtCodigo
	ui.mainLayout.removeWidget(ui.txtCodigo)
	ui.txtCodigo.deleteLater()
	ui.txtCodigo = None

	# Editor con lineas de texto (falta integrar)
	txtCodigo = EditorCodigo.QCodeEditor(DISPLAY_LINE_NUMBERS=True, 
                     HIGHLIGHT_CURRENT_LINE=True,
                     SyntaxHighlighter=SintaxisEC.ResaltadorLineas)
	ui.mainLayout.insertWidget(1, txtCodigo)


# Metodo main - Inicializa todos los elementos en pantalla
def main():
	global ui, app, cursor, scrollbar
    #sys.exit(app.exec_())
    # Inicialización de aplicación
	#app = QtWidgets.QApplication([])
	app = QApplication([])
	# Inicializar ventana y elementos
	ui = uic.loadUi("IDE2.ui")
	
	# Configurar colores de txtCodigo
	ui.txtCodigo.setStyleSheet("""QPlainTextEdit{ 
		color: #ccc; 
		background-color: #2b2b2b;}""")

	# Tamaño del tab
	actualizarTab()

	# Resaltar palabras de la gramatica
	highlight = SintaxisEC.ResaltadorLineas(ui.txtCodigo.document())

	# Comportamiento de los botones
	ui.btnCompilar.clicked.connect(compilar)
	ui.btnMas.clicked.connect(aumentarLetra)
	ui.btnMenos.clicked.connect(disminuirLetra)
	ui.btnGuardar.clicked.connect(guardarArchivo)
	ui.btnAbrir.clicked.connect(abrirArchivo)
	ui.btnNuevo.clicked.connect(nuevoArchivo)

	# Propiedades de la consola
	ui.txtCmd.setReadOnly(True)								# Solo lectura
	ui.txtCodigo.document().setMaximumBlockCount(500)
	ui.txtCmd.setWordWrapMode(QTextOption.WrapAnywhere)

	# Controles
	cursor = ui.txtCmd.textCursor()
	scrollbar = ui.txtCmd.verticalScrollBar()

	# Interpretación de señales (teclas)
	ui.lnInput.returnPressed.connect(ejecutarInput)

	#substituirCodigo() # Hay problemas con esto
	#manejoArchivo = Archivo()

	# Mostrar interface
	ui.show()
	# Ejecutar aplicación
	app.exec()


# Llamada al main
if __name__ == "__main__":
    main()