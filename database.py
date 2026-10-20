import sqlite3

connection = sqlite3.connect('database.db')
cursor = connection.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS agendamentos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT,
                    email TEXT,
                    telefone TEXT,
                    placa TEXT,
                    data TEXT,
                    hora TEXT,
                    servico TEXT
                )""")

cursor.execute("""CREATE TABLE IF NOT EXISTS usuarios (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    usuario TEXT NOT NULL UNIQUE,
                    senha_hash TEXT NOT NULL
                )""")

connection.commit()
connection.close()

print("Banco pronto.")