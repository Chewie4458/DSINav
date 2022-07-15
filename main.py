import sqlite3

from PyQt5 import uic, QtWidgets, QtGui
from PyQt5.QtWidgets import QMessageBox

from banco import criacaoBanco

from datetime import date

dataAtual = date.today()

'''Ações tela inicial'''
def abrirLoginCliente():
    loginCliente.show()
    telaInicial.close()

def abrirLoginFunc():
    loginFunc.show()
    telaInicial.close()

'''Ações tela de login do cliente'''
# volta da tela de login para tela de inicio
def voltarLoginClienteInicio():
    telaInicial.show()
    loginCliente.close()

def abrirTelaCadastro():
    cadastroCliente.show()
    loginCliente.close()

def entrarCliente():
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
                agendamentos.lblNome.setText(str(infoGet[0]))

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

def abrirAgendamentos():
    agendamentos.show()
    menuCliente.close()

    try:
        usuario = agendamentos.lblNome.text()

        c.execute("""SELECT dia, hora, servicos FROM agendamentos WHERE dataCalculo >= current_date AND cliente = ? ORDER BY dataCalculo ASC;""", [usuario])

        infoGet = c.fetchall()
        agendamentos.tabFuturos.setRowCount(len(infoGet))
        agendamentos.tabFuturos.setColumnCount(3)

        for i in range(len(infoGet)):
            for j in range(3):
                agendamentos.tabFuturos.setItem(i, j, QtWidgets.QTableWidgetItem(str(infoGet[i][j])))

    except Exception as e:
        erro = str(e)
        avisoErro(erro)

def abrirHistorico():
    historico.show()
    menuCliente.close()

    try:
        cliente = agendamentos.lblNome.text()

        c.execute("""SELECT dia, hora, servicos FROM agendamentos WHERE dataCalculo < current_date AND cliente = ? ORDER BY dataCalculo ASC;""", [cliente])

        infoGet = c.fetchall()
        historico.tabHist.setRowCount(len(infoGet))
        historico.tabHist.setColumnCount(3)

        for i in range(len(infoGet)):
            for j in range(3):
                historico.tabHist.setItem(i, j, QtWidgets.QTableWidgetItem(str(infoGet[i][j])))

    except Exception as e:
        erro = str(e)
        avisoErro(erro)

'''Ações tela novo agendamento'''
# volta da tela de novo agendamento para o menu
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

        mes = str(novoAgendamento.edtData.date().month())
        if int(mes) < 10:
            mes = '0' + mes

        dia = str(novoAgendamento.edtData.date().day()) + '/' + mes + '/' \
               + str(novoAgendamento.edtData.date().year())
        # variavel para calculo de data
        dataCalculo = str(novoAgendamento.edtData.date().year()) + '-' + mes + '-' \
              + str(novoAgendamento.edtData.date().day())

        minuto = novoAgendamento.edtHora.time().minute()
        if minuto < 10:
            hora = str(novoAgendamento.edtHora.time().hour()) + ':0' + str(novoAgendamento.edtHora.time().minute())
        else:
            hora = str(novoAgendamento.edtHora.time().hour()) + ':' + str(novoAgendamento.edtHora.time().minute())

        c.execute("""INSERT INTO agendamentos (cliente, dia, dataCalculo, hora, servicos) VALUES (?, ?, ?, ?, ?);""", (cliente, dia, dataCalculo, hora, servicos))

        con.commit()

        avisoSucesso('Agendamento realizado com sucesso!\nDia ' + dia + ' às ' + hora)

        novoAgendamento.tbServicos.clear()

    except Exception as e:
        erro = str(e)
        avisoErro(erro)

def verificarAgendamentosSemana(dia, mes, ano):
    cliente = novoAgendamento.lblNome.text()
    aux = dia - 6
    dataAux = ano + '-' + mes + '-' + aux
    data = ano + '-' + mes + '-' + dia

    # anterior ao marcado agora
    c.execute("""SELECT id_agendamento, dataCalculo FROM agendamentos WHERE cliente = ? AND (data >= dia >= dataAux)""")

'''Ações tela agendamentos'''
# volta da tela de agendamentos para o menu
def voltarAgendamentosMenu():
    menuCliente.show()
    agendamentos.close()

'''Ações tela historico'''
def voltarHistoricoMenu():
    menuCliente.show()
    historico.close()

# op
'''Tela login op'''
def voltarLoginOpInicio():
    telaInicial.show()
    loginFunc.close()

def entrarOp():
    try:
        usuario = loginFunc.edtUsuarioFunc.text()
        senha = loginFunc.edtSenhaFunc.text()

        # verifica se o usuario está cadastrado
        c.execute("""SELECT EXISTS (SELECT * FROM opAcesso WHERE usuario = ?);""", [usuario])
        infoGet = c.fetchone()
        existe = infoGet[0]

        if existe == 1:
            c.execute("""SELECT senha FROM opAcesso WHERE usuario = ?;""", [usuario])
            infoGet = c.fetchone()
            senhaCadastrada = infoGet[0]

            if str(senhaCadastrada) == str(senha):
                agendamentosOp.show()
                loginFunc.close()

                c.execute("""SELECT cliente, dia, hora, servicos FROM agendamentos WHERE dataCalculo >= current_date
                ORDER BY dataCalculo ASC, hora ASC;""")

                infoGet = c.fetchall()
                agendamentosOp.tabAgenda.setRowCount(len(infoGet))
                agendamentosOp.tabAgenda.setColumnCount(4)

                for i in range(len(infoGet)):
                    for j in range(4):
                        agendamentosOp.tabAgenda.setItem(i, j, QtWidgets.QTableWidgetItem(str(infoGet[i][j])))

            else:
                avisoErro('Usuário e/ou senha incorretos.')

        else:
            avisoErro('Usuário e/ou senha incorretos.')

    except Exception as e:
        erro = str(e)
        avisoErro(erro)

'''Tela agendamentos op'''
def voltarAgendamentosOpLogin():
    loginFunc.show()
    agendamentosOp.close()

    loginFunc.edtUsuarioFunc.setText('')
    loginFunc.edtSenhaFunc.setText('')

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
agendamentos = uic.loadUi("formFuturos.ui")
historico = uic.loadUi("formHistorico.ui")
loginFunc = uic.loadUi("formloginFunc.ui")
agendamentosOp = uic.loadUi("formAgendamentosOp.ui")

# botoes forms
# tela inicial
telaInicial.btnAreaCliente.clicked.connect(abrirLoginCliente)
telaInicial.btnAreaOp.clicked.connect(abrirLoginFunc)

# login cliente
loginCliente.btnVoltar.clicked.connect(voltarLoginClienteInicio)
loginCliente.btnCadastre.clicked.connect(abrirTelaCadastro)
loginCliente.btnEntrar.clicked.connect(entrarCliente)

# cadastro cliente
cadastroCliente.btnVoltar.clicked.connect(voltarCadastroLogin)
cadastroCliente.btnCadastrar.clicked.connect(cadastrar)

# menu cliente
menuCliente.btnVoltar.clicked.connect(voltarMenuLogin)
menuCliente.btnNovoAgendamento.clicked.connect(abrirNovoAgendamento)
menuCliente.btnFuturos.clicked.connect(abrirAgendamentos)
menuCliente.btnHistorico.clicked.connect(abrirHistorico)

#novo agendamento
novoAgendamento.btnVoltar.clicked.connect(voltarNovoMenu)
novoAgendamento.btnAdicionar.clicked.connect(adicionarServico)
novoAgendamento.btnConcluir.clicked.connect(concluirAgendamento)

# agendamentos
agendamentos.btnVoltar.clicked.connect(voltarAgendamentosMenu)

# historico
historico.btnVoltar.clicked.connect(voltarHistoricoMenu)

# op
# login op
loginFunc.btnVoltar.clicked.connect(voltarLoginOpInicio)
loginFunc.btnEntrar.clicked.connect(entrarOp)

# agendamentos op
agendamentosOp.btnVoltar.clicked.connect(voltarAgendamentosOpLogin)

telaInicial.show()

app.exec()
