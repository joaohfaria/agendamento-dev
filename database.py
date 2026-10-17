import sqlite3

connection = sqlite3.connect('database.db')
cursor = connection.cursor()

cursor.execute("""DROP TABLE IF EXISTS agendamentos""")

cursor.execute("""CREATE TABLE agendamentos (
                    
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT,
                    email TEXT,
                    telefone TEXT,
                    placa TEXT,
                    data TEXT,
                    hora TEXT,
                    servico TEXT
                    )""")

               

connection.commit()
connection.close()