import sqlite3

connection = sqlite3.connect('database.db')
cursor = connection.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS agendamentos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL UNIQUE,
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

cursor.execute("""CREATE TABLE IF NOT EXISTS servicos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL,
                    descricao TEXT,
                    preco REAL
                )""")


servicos = [
    ("Troca de óleo", "Serviço de troca de óleo do motor.", 150.00),
    ("Alinhamento e balanceamento", "Serviço de alinhamento e balanceamento das rodas.", 200.00),
    ("Revisão completa", "Serviço de revisão completa do veículo.", 500.00),
    ("Troca de pneus", "Serviço de troca de pneus do veículo.", 300.00),
    ("Lavagem completa", "Serviço de lavagem completa do veículo.", 100.00),
]

for servico in servicos:
    cursor.execute("INSERT OR IGNORE INTO servicos (nome, descricao, preco) VALUES (?, ?, ?)", servico)

connection.commit()
connection.close()

print("Banco pronto.")