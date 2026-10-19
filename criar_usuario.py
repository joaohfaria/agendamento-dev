import sqlite3
from werkzeug.security import generate_password_hash

def criar_usuario(usuario, senha):
    if not usuario or not senha:
        print("Nome de usuário e senha não podem estar vazios.")
        return

    senha_hash = generate_password_hash(senha)
    connection = None # Inicializa para evitar erro no bloco finally se o connect falhar

    try:
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()

        # CORREÇÃO: Garante que a tabela 'usuarios' existe antes de fazer o INSERT
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS usuarios (
                usuario TEXT PRIMARY KEY,
                senha_hash TEXT NOT NULL
            )
        ''')

        sql = "INSERT INTO usuarios (usuario, senha_hash) VALUES (?, ?)"
        cursor.execute(sql, (usuario, senha_hash))

        connection.commit()
        print(f"Usuário '{usuario}' criado com sucesso.")

    except sqlite3.IntegrityError:
        print(f"Erro: O usuário '{usuario}' já existe. Escolha outro nome de usuário.")
    except Exception as e:
        print(f"Ocorreu um erro ao criar o usuário: {e}")
    finally:
        if connection:
            connection.close()

if __name__ == "__main__":
    usuario = input("Digite o nome de usuário: ").strip()
    senha = input("Digite a senha: ")

    if usuario and senha:
        criar_usuario(usuario, senha)
    else:
        print("Erro: Usuário e senha não podem ser vazios.")
