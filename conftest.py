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


# ATENCAO: a data abaixo esta fixa. Em 2027 ela vira passado e o teste
# quebra sozinho, sem bug nenhum no sistema. Melhoria pendente:
# calcular uma data futura em dia util com datetime + timedelta.
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
