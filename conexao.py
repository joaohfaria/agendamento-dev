import sqlite3

CAMINHO_DATABASE = 'database.db'

def conectar():
    return sqlite3.connect(CAMINHO_DATABASE)