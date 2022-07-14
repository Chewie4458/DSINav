import sqlite3

def criacaoBanco():
    con = sqlite3.connect('dados.bd')

    c = con.cursor()

    c.execute("""CREATE TABLE IF NOT EXISTS clientes(
                    id_cliente INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                    nome VARCHAR(50) NOT NULL,
                    usuario VARCHAR(15) NOT NULL,
                    senha VARCHAR(20) NOT NULL
                    );""")

    c.execute("""CREATE TABLE IF NOT EXISTS agendamentos(
                    id_agendamento INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                    cliente VARCHAR(50) NOT NULL,
                    dia VARCHAR(10) NOT NULL,
                    hora VARCHAR(5) NOT NULL,
                    servicos TEXT NOT NULL);""")

    con.commit()

    con.close()
