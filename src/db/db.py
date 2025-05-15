# src/db/db.py
import psycopg2
import contextlib
# Importa do arquivo de configuração na raiz de src
from src.config import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT
import os # Importa os para depuração da variável de ambiente

# REMOVA ESTA LINHA DE DEBUG APÓS CONFIGURAR A SENHA CORRETAMENTE
print(f"DEBUG: Valor de DB_PASSWORD lido em db.py: {DB_PASSWORD}")

def get_db_connection():
    """Estabelece uma conexão com o banco de dados."""
    # Verifica se a senha foi lida corretamente antes de tentar conectar
    if DB_PASSWORD is None:
        print("Erro: Não foi possível conectar ao banco de dados. DB_PASSWORD não está definida.")
        return None # Retorna None se a senha não estiver definida

    try:
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD, # Usa o valor lido de config
            host=DB_HOST,
            port=DB_PORT
        )
        return conn
    except Exception as e:
        print(f"Erro no banco de dados: {e}")
        return None # Retorna None em caso de erro de conexão


@contextlib.contextmanager
def cursor_context():
    """Fornece um cursor de banco de dados usando um gerenciador de contexto."""
    conn = None
    cur = None
    try:
        conn = get_db_connection()
        if conn is None: # Verifica se a conexão foi bem sucedida
            yield None # Retorna None para o cursor se a conexão falhou
            return # Sai do contexto sem tentar commit/rollback

        cur = conn.cursor()
        yield cur
        conn.commit() # Confirma as alterações se houver
    except Exception as e:
        if conn:
            conn.rollback() # Reverte em caso de erro
        print(f"Erro no banco de dados durante a operação: {e}")
        # NUNCA LANCE A EXCEÇÃO NOVAMENTE EM AMBIENTE DE PRODUÇÃO SE QUISER QUE O JOGO CONTINUE
        # Removendo o raise aqui para evitar que um erro de DB crashe a GUI imediatamente
        # raise # Re-lança a exceção para ser tratada externamente se necessário (removido)
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()