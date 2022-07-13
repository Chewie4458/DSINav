from PyQt5 import uic, QtWidgets, QtGui
from PyQt5.QtWidgets import QMessageBox

def abrirLoginCliente():
    loginCliente.show()
    telaInicial.close()

# volta da tela de login para tela de inicio
def voltarLoginClienteInicio():
    telaInicial.show()
    loginCliente.close()

app = QtWidgets.QApplication([])

# load dos forms
telaInicial = uic.loadUi("formPrimeiraTela.ui")
loginCliente = uic.loadUi("formLoginCliente.ui")

# botoes forms
# tela inicial
telaInicial.btnAreaCliente.clicked.connect(abrirLoginCliente)

# login cliente
loginCliente.btnVoltar.clicked.connect(voltarLoginClienteInicio)

telaInicial.show()

app.exec()