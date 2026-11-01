import sqlite3

conexao = sqlite3.connect("database.db")
cursor = conexao.cursor()

print("--- colunas da tabela agendamentos ---")
cursor.execute("PRAGMA table_info(agendamentos)")
for coluna in cursor.fetchall():
    print(coluna[1], "-", coluna[2])

print()
print("--- agendamentos ---")
cursor.execute("SELECT id, nome, data, hora, servico, status FROM agendamentos")
for linha in cursor.fetchall():
    print(linha)

conexao.close()