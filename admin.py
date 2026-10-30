import os
import sqlite3
from werkzeug.security import generate_password_hash


def criar_admin():
    usuario = os.getenv('ADMIN_USUARIO')
    senha = os.getenv('ADMIN_SENHA')

    if not usuario or not senha:
        print("ADMIN_USUARIO ou ADMIN_SENHA nao definidos. Usuario admin nao criado.")
        return

    senha_hash = generate_password_hash(senha)

    db = sqlite3.connect('database.db')
    cursor = db.cursor()

    cursor.execute(
        "INSERT OR IGNORE INTO usuarios (usuario, senha_hash) VALUES (?, ?)",
        (usuario, senha_hash)
    )

    db.commit()
    db.close()

    print(f"Usuario admin '{usuario}' verificado.")
