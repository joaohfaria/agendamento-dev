import pytest
from werkzeug.security import generate_password_hash
from conexao import conectar
from datetime import date, timedelta

USUARIO_TESTE = "pytest_user"
SENHA_TESTE = "senha_de_teste_123"

def proximo_dia_util(dias_para_somar: int = 7) -> str:
    data_alvo = date.today() + timedelta(days=dias_para_somar)

    while data_alvo.weekday() >= 5:
        data_alvo += timedelta(days=1)

    return data_alvo.strftime("%Y-%m-%d")

@pytest.fixture
def usuario_teste():
    senha_hash = generate_password_hash(SENHA_TESTE)

    db = conectar()
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO usuarios (usuario, senha_hash) VALUES (%s, %s) ON CONFLICT (usuario) DO NOTHING",
        (USUARIO_TESTE, senha_hash)
    )
    db.commit()
    db.close()

    yield {"usuario": USUARIO_TESTE, "senha": SENHA_TESTE}

    db = conectar()
    cursor = db.cursor()
    cursor.execute("DELETE FROM usuarios WHERE usuario = %s", (USUARIO_TESTE,))
    db.commit()
    db.close()

AGENDAMENTO_TESTE = {
    "nome": "PYTEST_AGENDAMENTO",
    "email": "pytest@example.com",
    "telefone": "35999999999",
    "placa": "TST0001",
    "data": proximo_dia_util(),
    "hora": "09:00",
    "servico": "Troca de óleo",
}


def apagar_agendamento_teste():
    db = conectar()
    cursor = db.cursor()
    cursor.execute(
        "DELETE FROM agendamentos WHERE nome = %s AND data = %s AND hora = %s",
        (AGENDAMENTO_TESTE["nome"], AGENDAMENTO_TESTE["data"], AGENDAMENTO_TESTE["hora"])
    )
    db.commit()
    db.close()


@pytest.fixture
def agendamento_teste():
    apagar_agendamento_teste()
    yield AGENDAMENTO_TESTE
    apagar_agendamento_teste()

