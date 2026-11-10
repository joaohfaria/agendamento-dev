import sqlite3
import pytest
from werkzeug.security import generate_password_hash
from conexao import conectar

USUARIO_TESTE = "pytest_user"
SENHA_TESTE = "senha_de_teste_123"


@pytest.fixture
def usuario_teste():
    senha_hash = generate_password_hash(SENHA_TESTE)

    db = conectar()
    cursor = db.cursor()
    cursor.execute(
        "INSERT OR IGNORE INTO usuarios (usuario, senha_hash) VALUES (?, ?)",
        (USUARIO_TESTE, senha_hash)
    )
    db.commit()
    db.close()

    yield {"usuario": USUARIO_TESTE, "senha": SENHA_TESTE}

    db = conectar()
    cursor = db.cursor()
    cursor.execute("DELETE FROM usuarios WHERE usuario = ?", (USUARIO_TESTE,))
    db.commit()
    db.close()

AGENDAMENTO_TESTE = {
    "nome": "PYTEST_AGENDAMENTO",
    "email": "pytest@example.com",
    "telefone": "35999999999",
    "placa": "TST0001",
    "data": "2026-12-14",
    "hora": "09:00",
    "servico": "Troca de óleo",
}


def apagar_agendamento_teste():
    db = conectar()
    cursor = db.cursor()
    cursor.execute(
        "DELETE FROM agendamentos WHERE nome = ? AND data = ? AND hora = ?",
        (AGENDAMENTO_TESTE["nome"], AGENDAMENTO_TESTE["data"], AGENDAMENTO_TESTE["hora"])
    )
    db.commit()
    db.close()


@pytest.fixture
def agendamento_teste():
    apagar_agendamento_teste()
    yield AGENDAMENTO_TESTE
    apagar_agendamento_teste()