import sqlite3

conexao = sqlite3.connect("database.db")
cursor = conexao.cursor()

cursor.execute("SELECT * FROM servicos")

for linha in cursor.fetchall():
    print(linha)

conexao.close()