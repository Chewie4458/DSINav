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

def entrar():
    try:
        usuario = loginCliente.edtUsuarioCliente.text()
        senha = loginCliente.edtSenhaCliente.text()

        # verifica se o usuario está cadastrado
        c.execute("""SELECT EXISTS (SELECT * FROM clientes WHERE usuario = ?);""", [usuario])
        infoGet = c.fetchone()
        existe = infoGet[0]

        if existe == 1:
            c.execute("""SELECT senha FROM clientes WHERE usuario = ?;""", [usuario])
            infoGet = c.fetchone()
            senhaCadastrada = infoGet[0]

            if str(senhaCadastrada) == str(senha):
                menuCliente.show()
                loginCliente.close()

                c.execute("""SELECT nome FROM clientes WHERE usuario = ?;""", [usuario])
                infoGet = c.fetchone()
                menuCliente.lblLogadoComo.setText('Logado como ' + str(infoGet[0]))
                novoAgendamento.lblNome.setText(str(infoGet[0]))

            else:
                avisoErro('Usuário e/ou senha incorretos.')

        else:
            avisoErro('Usuário e/ou senha incorretos.')

    except Exception as e:
        erro = str(e)
        avisoErro(erro)

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

'''Ações tela menu cliente'''
# volta da tela menu cliente para login
def voltarMenuLogin():
    loginCliente.show()
    menuCliente.close()

    loginCliente.edtUsuarioCliente.setText('')
    loginCliente.edtSenhaCliente.setText('')

def abrirNovoAgendamento():
    novoAgendamento.show()
    menuCliente.close()

'''Ações tela novo agendamento'''
def voltarNovoMenu():
    menuCliente.show()
    novoAgendamento.close()

def adicionarServico():
    servico = novoAgendamento.cbServico.currentText()
    novoAgendamento.tbServicos.append(servico)

def concluirAgendamento():
    try:
        cliente = novoAgendamento.lblNome.text()
        servicos = novoAgendamento.tbServicos.toPlainText()
        servicos = tirarN(list(servicos))
        data = str(novoAgendamento.edtData.date().day()) + '/' + str(novoAgendamento.edtData.date().month()) + '/' \
               + str(novoAgendamento.edtData.date().year())
        minuto = novoAgendamento.edtHora.time().minute()
        if minuto < 10:
            hora = str(novoAgendamento.edtHora.time().hour()) + ':0' + str(novoAgendamento.edtHora.time().minute())
        else:
            hora = str(novoAgendamento.edtHora.time().hour()) + ':' + str(novoAgendamento.edtHora.time().minute())

        c.execute("""INSERT INTO agendamentos (cliente, dia, hora, servicos) VALUES (?, ?, ?, ?);""", (cliente, data, hora, servicos))

        con.commit()

        avisoSucesso('Agendamento realizado com sucesso!\nDia ' + data + ' às ' + hora)

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

def tirarN(lista):
    for c in range(len(lista)):
        if lista[c] == '\n':
            lista[c] = ', '

    result = ''.join(lista)

    return result

app = QtWidgets.QApplication([])

criacaoBanco()

con = sqlite3.connect('dados.bd')
c = con.cursor()

# load dos forms
telaInicial = uic.loadUi("formPrimeiraTela.ui")
loginCliente = uic.loadUi("formLoginCliente.ui")
cadastroCliente = uic.loadUi("formCadastroCliente.ui")
menuCliente = uic.loadUi("formMenuCliente.ui")
novoAgendamento = uic.loadUi("formNovoAgendamento.ui")

# botoes forms
# tela inicial
telaInicial.btnAreaCliente.clicked.connect(abrirLoginCliente)

# login cliente
loginCliente.btnVoltar.clicked.connect(voltarLoginClienteInicio)
loginCliente.btnCadastre.clicked.connect(abrirTelaCadastro)
loginCliente.btnEntrar.clicked.connect(entrar)

# cadastro cliente
cadastroCliente.btnVoltar.clicked.connect(voltarCadastroLogin)
cadastroCliente.btnCadastrar.clicked.connect(cadastrar)

# menu cliente
menuCliente.btnVoltar.clicked.connect(voltarMenuLogin)
menuCliente.btnNovoAgendamento.clicked.connect(abrirNovoAgendamento)

#novo agendamento
novoAgendamento.btnVoltar.clicked.connect(voltarNovoMenu)
novoAgendamento.btnAdicionar.clicked.connect(adicionarServico)
novoAgendamento.btnConcluir.clicked.connect(concluirAgendamento)

telaInicial.show()

app.exec()
