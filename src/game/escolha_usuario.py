# src/game/escolha_usuario.py

import random
# Importa do subpacote db dentro de src
from src.db.db import cursor_context
# Importa a classe Carta do mesmo subpacote game (importação relativa)
from .carta import Carta
# Importa a constante do arquivo de configuração na raiz de src
from src.config import HAND_SIZE

def sortear_mao_usuario():
    """Sorteia a mão inicial de cartas para o usuário."""
    todas_cartas = []
    try:
        with cursor_context() as cur:
            if cur is None: # Verifica se o cursor foi obtido com sucesso (conexão falhou)
                print("Não foi possível conectar ao banco de dados para sortear a mão do usuário.")
                return []

            cur.execute("SELECT codigo, nome_cidade, estado, populacao, area, pib, pontos_turisticos FROM public.infos_cidades;")
            rows = cur.fetchall()
            # Converte as tuplas do DB em objetos Carta
            todas_cartas = [Carta(*row) for row in rows]

        if len(todas_cartas) < HAND_SIZE:
            print(f"Não há cartas suficientes no banco de dados para formar uma mão de {HAND_SIZE} cartas.")
            return []

        # Embaralhar e pegar HAND_SIZE cartas aleatórias (objetos Carta)
        mao = random.sample(todas_cartas, HAND_SIZE)
        return mao

    except Exception as e:
        print(f"Erro ao sortear mão do usuário: {e}")
        return []

# As funções escolher_carta_da_mao e escolher_atributo_usuario são apenas para a versão de console
# e não são usadas pela GUI. Podem ser mantidas, mas não afetam a GUI.

# def escolher_carta_da_mao(mao: list[Carta]):
#     """Permite ao usuário escolher uma carta da sua mão."""
#     # ... (código da função) ...

# def escolher_atributo_usuario(carta: Carta):
#     """Permite ao usuário escolher um atributo para jogar."""
#     # ... (código da função) ...