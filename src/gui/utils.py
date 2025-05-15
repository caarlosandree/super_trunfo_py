# src/gui/utils.py

import pygame
import os
from src.game.carta import Carta # Precisa importar Carta para type hinting e acesso aos atributos

# --- Definição de Tamanhos Mínimos (Movidos para cá) ---
MIN_LARGURA_TELA = 700
MIN_ALTURA_TELA = 500
MIN_CARTA_LARGURA = 90
MIN_CARTA_ALTURA = 160
MIN_MARGEM = 8
MIN_ESPACO_ENTRE_CARTAS = 5
MIN_ALTURA_MAO_JOGADOR = 120
MIN_FONT_SMALL_SIZE = 10
MIN_FONT_MEDIUM_SIZE = 12
MIN_FONT_LARGE_SIZE = 20

# Variáveis globais para as dimensões calculadas (Gerenciadas por esta função)
carta_largura = 0
carta_altura = 0
margem = 0
espaco_entre_cartas = 0
altura_mao_jogador = 0

# Variáveis globais para as fontes (Gerenciadas por esta função)
font_small = None
font_medium = None
font_large = None

# Fontes (caminho relativo agora a src/gui/)
# Sobe dois níveis (de src/gui/) para a raiz do projeto SuperTrunfo/ e entra em fontes/
FONTE_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "fontes")
FONTE_REGULAR_FILE = "IntelbrasSans-Regular.ttf"
FONTE_MEDIUM_FILE = "IntelbrasSans-Medium.ttf"


def calcular_dimensoes(largura_atual, altura_atual):
    """Calcula as dimensões e posições dos elementos com base no tamanho atual da tela, respeitando mínimos."""
    global carta_largura, carta_altura, margem, espaco_entre_cartas, altura_mao_jogador

    # Dimensões baseadas em percentuais da tela atual, respeitando mínimos
    carta_largura = max(MIN_CARTA_LARGURA, int(largura_atual * 0.14))
    carta_altura = max(MIN_CARTA_ALTURA, int(altura_atual * 0.28))
    margem = max(MIN_MARGEM, int(min(largura_atual, altura_atual) * 0.02)) # Margem baseada na menor dimensão
    espaco_entre_cartas = max(MIN_ESPACO_ENTRE_CARTAS, int(largura_atual * 0.03))
    altura_mao_jogador = max(MIN_ALTURA_MAO_JOGADOR, int(altura_atual * 0.3))

    # As fontes são recalculadas na função carregar_fontes
    carregar_fontes(altura_atual)


def carregar_fontes(altura_atual):
    """Carrega ou recalcula os tamanhos das fontes com base na altura atual, respeitando mínimos."""
    global font_small, font_medium, font_large

    try:
        caminho_fonte_regular = os.path.join(FONTE_DIR, FONTE_REGULAR_FILE)
        # caminho_fonte_medium_file = os.path.join(FONTE_DIR, FONTE_MEDIUM_FILE)

        # Usa max() para garantir o tamanho mínimo da fonte
        # Baseado na altura atual da tela
        font_small = pygame.font.Font(caminho_fonte_regular, max(MIN_FONT_SMALL_SIZE, int(altura_atual * 0.02)))
        font_medium = pygame.font.Font(caminho_fonte_regular, max(MIN_FONT_MEDIUM_SIZE, int(altura_atual * 0.025)))
        font_large = pygame.font.Font(caminho_fonte_regular, max(MIN_FONT_LARGE_SIZE, int(altura_atual * 0.04)))

        # Se quiser usar a variação Medium para 'font_medium', descomente abaixo:
        # font_medium = pygame.font.Font(caminho_fonte_medium_file, max(MIN_FONT_MEDIUM_SIZE, int(altura_atual * 0.025)))


    except (pygame.error, FileNotFoundError) as e:
        print(f"Não foi possível carregar a fonte customizada: {e}. Usando fonte padrão.")
        font_small = pygame.font.SysFont("arial", max(MIN_FONT_SMALL_SIZE, int(altura_atual * 0.02)))
        font_medium = pygame.font.SysFont("arial", max(MIN_FONT_MEDIUM_SIZE, int(altura_atual * 0.025)))
        font_large = pygame.font.SysFont("arial", max(MIN_FONT_LARGE_SIZE, int(altura_atual * 0.04)))


    # --- DEBUG PRINT ---
    # Verifica se as fontes foram carregadas (não são None) antes de imprimir
    small_status = "OK" if font_small else "Failed"
    medium_status = "OK" if font_medium else "Failed"
    large_status = "OK" if font_large else "Failed"
    print(f"DEBUG: Fontes carregadas/recalculadas. small={small_status}, medium={medium_status}, large={large_status}")
    # --- FIM DEBUG PRINT ---


def formatar_valor_numerico(valor):
    """Formata valores numéricos para exibição curta (K, M) ou com vírgula/ponto."""
    if isinstance(valor, (int, float)) and valor is not None:
         if abs(valor) >= 1_000_000:
              return f"{valor / 1_000_000:,.1f}M".replace(',', 'X').replace('.', ',').replace('X', '.')
         elif abs(valor) >= 1000:
              return f"{valor / 1000:,.1f}K".replace(',', 'X').replace('.', ',').replace('X', '.')
         elif isinstance(valor, float):
            if valor == int(valor):
                return f"{int(valor):,}".replace(',', '.')
            else:
                return f"{valor:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
         else:
             return f"{int(valor):,}".replace(',', '.')
    elif valor is not None:
         return str(valor)
    return 'N/A'