# src/game/escolha_com.py
import random
# Importa do subpacote db dentro de src
from src.db.db import cursor_context
# Importa a classe Carta do mesmo subpacote game (importação relativa)
from .carta import Carta

def escolher_carta_computador(mao_usuario: list[Carta]):
    """Escolhe uma carta aleatória para o computador, excluindo as da mão do usuário."""
    todas_cartas = []
    codigos_usuario = [carta.codigo for carta in mao_usuario] # Obtém códigos dos objetos Carta

    try:
        with cursor_context() as cur:
            if cur is None: # Verifica se o cursor foi obtido com sucesso (conexão falhou)
                 print("Não foi possível conectar ao banco de dados para escolher carta do computador.")
                 return None

            cur.execute("SELECT codigo, nome_cidade, estado, populacao, area, pib, pontos_turisticos FROM public.infos_cidades;")
            rows = cur.fetchall()
            # Converte as tuplas do DB em objetos Carta
            todas_cartas = [Carta(*row) for row in rows]

        # Filtrar cartas (objetos Carta) que NÃO estão na mão do usuário
        cartas_validas = [c for c in todas_cartas if c.codigo not in codigos_usuario]

        if not cartas_validas:
            print("Não há cartas disponíveis para o computador (após excluir as do usuário).")
            return None

        carta_pc = random.choice(cartas_validas) # Escolhe um objeto Carta
        return carta_pc

    except Exception as e:
        print(f"Erro ao escolher carta do computador: {e}")
        return None