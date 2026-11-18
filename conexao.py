import os
import time
import psycopg
from dotenv import load_dotenv

load_dotenv()


def conectar():
    url = os.getenv('DATABASE_URL')

    if not url:
        raise RuntimeError("DATABASE_URL nao definida. Confira o .env (local) ou as variaveis de ambiente (Render).")

    inicio = time.perf_counter()
    
    try:
        conn = psycopg.connect(url, connect_timeout=10)
        
        tempo_decorrido = time.perf_counter() - inicio
        
        return conn
    
    except psycopg.OperationalError as e:
        tempo_decorrido = time.perf_counter() - inicio
        raise
