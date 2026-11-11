from conexao import conectar


def criar_tabelas():
    connection = conectar()
    cursor = connection.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS agendamentos (
                    id INTEGER PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
                    nome TEXT NOT NULL,
                    email TEXT,
                    telefone TEXT,
                    placa TEXT,
                    data TEXT,
                    hora TEXT,
                    servico TEXT NOT NULL,
                    status TEXT NOT NULL DEFAULT 'Aguardando'
                )""")

    cursor.execute("""CREATE TABLE IF NOT EXISTS usuarios (
                    id INTEGER PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
                    usuario TEXT NOT NULL UNIQUE,
                    senha_hash TEXT NOT NULL
                )""")

    cursor.execute("""CREATE TABLE IF NOT EXISTS servicos (
                    id INTEGER PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
                    nome TEXT NOT NULL UNIQUE,
                    descricao TEXT,
                    preco NUMERIC(10, 2) NOT NULL
                )""")

    servicos = [
        ("Troca de óleo", "Serviço de troca de óleo do motor.", 150.00),
        ("Alinhamento e balanceamento", "Serviço de alinhamento e balanceamento das rodas.", 200.00),
        ("Revisão completa", "Serviço de revisão completa do veículo.", 500.00),
        ("Troca de pneus", "Serviço de troca de pneus do veículo.", 300.00),
        ("Lavagem completa", "Serviço de lavagem completa do veículo.", 100.00),
    ]

    for servico in servicos:
        cursor.execute(
            "INSERT INTO servicos (nome, descricao, preco) VALUES (%s, %s, %s) ON CONFLICT (nome) DO NOTHING",
            servico
        )

    connection.commit()
    connection.close()

    print("Banco pronto.")


if __name__ == "__main__":
    criar_tabelas()
