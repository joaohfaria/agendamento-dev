import os
import psycopg
from dotenv import load_dotenv

load_dotenv()


def conectar():
    url = os.getenv('DATABASE_URL')

    if not url:
        raise RuntimeError("DATABASE_URL nao definida. Confira o .env (local) ou as variaveis de ambiente (Render).")

    return psycopg.connect(url)
