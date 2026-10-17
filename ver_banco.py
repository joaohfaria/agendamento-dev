import sqlite3

conexao = sqlite3.connect("database.db")
cursor = conexao.cursor()

cursor.execute("SELECT * FROM agendamentos")
print(cursor.fetchall())

conexao.close()

import sqlite3

conexao = sqlite3.connect("database.db")
cursor = conexao.cursor()

cursor.execute("PRAGMA table_info(agendamentos)")

for coluna in cursor.fetchall():
    print(coluna[1], "-", coluna[2])

conexao.close()