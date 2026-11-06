import sqlite3
import pytest
from werkzeug.security import generate_password_hash

USUARIO_TESTE = "pytest_user"
SENHA_TESTE = "senha_de_teste_123"


@pytest.fixture
def usuario_teste():
    senha_hash = generate_password_hash(SENHA_TESTE)

    db = sqlite3.connect('database.db')
    cursor = db.cursor()
    cursor.execute(
        "INSERT OR IGNORE INTO usuarios (usuario, senha_hash) VALUES (?, ?)",
        (USUARIO_TESTE, senha_hash)
    )
    db.commit()
    db.close()

    yield {"usuario": USUARIO_TESTE, "senha": SENHA_TESTE}

    db = sqlite3.connect('database.db')
    cursor = db.cursor()
    cursor.execute("DELETE FROM usuarios WHERE usuario = ?", (USUARIO_TESTE,))
    db.commit()
    db.close()