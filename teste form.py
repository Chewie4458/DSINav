from PyQt5 import uic, QtWidgets, QtGui
from PyQt5.QtWidgets import QMessageBox

app = QtWidgets.QApplication([])

tela = uic.loadUi("primeiraTela.ui")

tela.show()

app.exec()


# #C0284F