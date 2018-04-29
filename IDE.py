from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QTextOption, QTextCursor
import SintaxisEC

window = None;

# Funciones
def compilar():
	global window
	if not window.ui.txtCodigo.toPlainText() == "":
		codigo = window.ui.txtCodigo.toPlainText()
		window.mostrarEnConsola('Compilación Exitosa')
	else:
		mensaje("No hay codigo", "Necesitar escribir codigo para poder compilar.")


# Consola de comandos
class MainWindow:

	def __init__(self):

		# Inicializar ventana y elementos
		self.ui = uic.loadUi("IDE2.ui")
		
		# Configurar colores de txtCodigo
		self.ui.txtCodigo.setStyleSheet("""QPlainTextEdit{
			font-family:'Consolas'; 
			color: #ccc; 
			background-color: #2b2b2b;}""")
		highlight = SintaxisEC.ResaltadorLineas(self.ui.txtCodigo.document())

		# Botones
		self.ui.btnCompilar.clicked.connect(compilar)

		self.ui.txtCmd.setReadOnly(True)

		# Propiedades de la consola
		self.ui.txtCodigo.document().setMaximumBlockCount(500)
		self.ui.txtCmd.setWordWrapMode(QTextOption.WrapAnywhere)

		# Controles
		self.cursor = self.ui.txtCmd.textCursor()
		self.scrollbar = self.ui.txtCmd.verticalScrollBar()

		# Interpreter Signals
		self.ui.lnInput.returnPressed.connect(self.ejecutarInput)
		self.ui.show()


	# Ejecuta el input en la consola de comandos
	def ejecutarInput(self):

		comando = self.ui.lnInput.text()
		self.ui.lnInput.clear()
		self.mostrarEnConsola(comando)


    # Coloca la salida de la consola en el cuadro de texto
	def mostrarEnConsola(self, salida):
		# Mover el cursor al final
		self.cursor.movePosition(QTextCursor.End)
		self.ui.txtCmd.setTextCursor(self.cursor)

		# Insertar texto en el cuadro
		self.ui.txtCmd.insertPlainText(salida + '\n')

		# Mover scrollbar
		self.scrollbar.setValue(self.scrollbar.maximum())

	def mensaje(titulo="Advertencia", mensaje=""):
		QMessageBox.information(None, titulo, mensaje)


#-------------------------------------

# Metodo main
def main():
	global window
    #sys.exit(app.exec_())
    # Inicialización de aplicación
	#app = QtWidgets.QApplication([])
	app = QApplication([])
	window = MainWindow()

	app.exec()

# Llamada al main
if __name__ == "__main__":
    main()