# src/config.py
import os

# Configurações do banco de dados
# É altamente recomendado usar variáveis de ambiente em vez de hardcoding
DB_NAME = os.environ.get("DB_NAME", "postgres")
DB_USER = os.environ.get("DB_USER", "postgres")
# !!! Substitua pela sua senha ou use variável de ambiente !!!
# Garante que a variável de ambiente tem prioridade, com fallback se não estiver definida
DB_PASSWORD = os.environ.get("DB_PASSWORD") # Agora lê apenas da variável de ambiente
DB_HOST = os.environ.get("DB_HOST", "localhost")
DB_PORT = os.environ.get("DB_PORT", "5432")

# Constantes do jogo
HAND_SIZE = 5

# Verifica se a senha do banco de dados está configurada
if DB_PASSWORD is None:
    print("ERRO: A senha do banco de dados (DB_PASSWORD) não está configurada nas variáveis de ambiente.")
    print("Por favor, defina a variável de ambiente DB_PASSWORD antes de executar o jogo.")
    # Em um jogo real, você pode querer encerrar aqui ou mostrar um erro na GUI.
    # Por enquanto, o jogo tentará continuar, mas as operações de DB falharão.