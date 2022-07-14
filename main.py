import sqlite3

from PyQt5 import uic, QtWidgets, QtGui
from PyQt5.QtWidgets import QMessageBox

from banco import criacaoBanco

'''Ações tela inicial'''
def abrirLoginCliente():
    loginCliente.show()
    telaInicial.close()

'''Ações tela de login do cliente'''
# volta da tela de login para tela de inicio
def voltarLoginClienteInicio():
    telaInicial.show()
    loginCliente.close()

def abrirTelaCadastro():
    cadastroCliente.show()
    loginCliente.close()

'''Ações tela cadastro cliente'''
# volta da tela de cadastro para tela de login
def voltarCadastroLogin():
    loginCliente.show()
    cadastroCliente.close()

def cadastrar():
    try:
        nome = cadastroCliente.edtNomeCadastro.text()
        usuario = cadastroCliente.edtUsuarioCadastro.text()
        senha = cadastroCliente.edtSenhaCadastro.text()

        c.execute("""INSERT INTO clientes(nome, usuario, senha) VALUES (?, ?, ?)""", (str(nome), str(usuario), str(senha)))

        con.commit()

        cadastroCliente.edtNomeCadastro.setText('')
        cadastroCliente.edtUsuarioCadastro.setText('')
        cadastroCliente.edtSenhaCadastro.setText('')

        avisoSucesso('Cadastro realizado com sucesso!')

    except Exception as e:
        erro = str(e)
        avisoErro(erro)

'''Mais'''
def avisoErro(e):
    aviso = QMessageBox()
    aviso.setIcon(QMessageBox.Warning)
    aviso.setText(e)
    aviso.setWindowTitle('ERRO!')
    aviso.addButton('Ok', 0)
    aviso.setWindowIcon(QtGui.QIcon('imagens/erro icon.png'))

    retorno = aviso.exec()

def avisoSucesso(op):
    avisoFoi = QMessageBox()
    avisoFoi.setIcon(QMessageBox.Information)
    avisoFoi.setText(op)
    avisoFoi.setWindowTitle('SUCESSO!')
    avisoFoi.addButton('Ok', 0)
    avisoFoi.setWindowIcon(QtGui.QIcon('imagens/sucesso icon.png'))

    avisoFoi.exec()

app = QtWidgets.QApplication([])

criacaoBanco()

con = sqlite3.connect('dados.bd')
c = con.cursor()

# load dos forms
telaInicial = uic.loadUi("formPrimeiraTela.ui")
loginCliente = uic.loadUi("formLoginCliente.ui")
cadastroCliente = uic.loadUi("formCadastroCliente.ui")

# botoes forms
# tela inicial
telaInicial.btnAreaCliente.clicked.connect(abrirLoginCliente)

# login cliente
loginCliente.btnVoltar.clicked.connect(voltarLoginClienteInicio)
loginCliente.btnCadastre.clicked.connect(abrirTelaCadastro)

#cadastro cliente
cadastroCliente.btnVoltar.clicked.connect(voltarCadastroLogin)
cadastroCliente.btnCadastrar.clicked.connect(cadastrar)

telaInicial.show()

app.exec()