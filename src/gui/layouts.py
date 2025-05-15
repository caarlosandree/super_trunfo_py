# src/gui/layouts.py

import pygame
from src.game.carta import Carta
# Importa funções do drawing e o módulo utils
from .drawing import desenha_carta, desenha_texto
# Importa o módulo utils para acessar as variáveis de fonte e dimensão
# Remove a importação direta das variáveis globais
from . import utils # <<< Importa o módulo utils

# Cores (podem ser importadas de um arquivo de constantes globais, se houver)
PRETO = (0, 0, 0)
AZUL_CLARO = (173, 216, 230)
AZUL_ESCURO = (70, 130, 180)
VERDE = (0, 255, 0)
VERMELHO = (255, 0, 0)
CINZA_MEDIO = (150, 150, 150)


def desenha_mao_jogador(surface, mao: list[Carta], largura_atual, altura_atual, selected_card: Carta = None):
    """Desenha a mão de cartas do jogador na parte inferior da tela, responsivamente."""
    # Usa as dimensões calculadas globalmente (gerenciadas em utils)
    current_carta_largura = utils.carta_largura
    current_carta_altura = utils.carta_altura
    current_margem = utils.margem
    current_espaco_entre_cartas = utils.espaco_entre_cartas
    current_altura_mao_jogador = utils.altura_mao_jogador

    largura_total_necessaria = len(mao) * current_carta_largura + (max(0, len(mao) - 1)) * current_espaco_entre_cartas
    largura_disponivel_para_mao = largura_atual - current_margem * 2

    if largura_total_necessaria > largura_disponivel_para_mao:
        if len(mao) > 0:
            largura_para_carta_ajustada = (largura_disponivel_para_mao - (max(0, len(mao) - 1)) * utils.MIN_ESPACO_ENTRE_CARTAS) // len(mao)
            current_carta_largura = max(utils.MIN_CARTA_LARGURA, min(current_carta_largura, largura_para_carta_ajustada))
            current_carta_altura = max(utils.MIN_CARTA_ALTURA, int(current_carta_largura * (utils.carta_altura / max(1, utils.carta_largura))))
            current_espaco_entre_cartas = utils.MIN_ESPACO_ENTRE_CARTAS
        else:
            current_carta_largura = utils.MIN_CARTA_LARGURA
            current_carta_altura = utils.MIN_CARTA_ALTURA
            current_espaco_entre_cartas = utils.MIN_ESPACO_ENTRE_CARTAS


        largura_total_necessaria = len(mao) * current_carta_largura + (max(0, len(mao) - 1)) * current_espaco_entre_cartas


    card_x_start = (largura_atual - largura_total_necessaria) // 2
    card_y = altura_atual - current_altura_mao_jogador + current_margem

    card_rects = []
    for i, carta in enumerate(mao):
        rect = pygame.Rect(card_x_start + i * (current_carta_largura + current_espaco_entre_cartas), card_y, current_carta_largura, current_carta_altura)
        desenha_carta(surface, carta, rect, face_up=True, selecionada=(carta == selected_card))
        card_rects.append((rect, carta))

    mao_area_rect = pygame.Rect(0, altura_atual - current_altura_mao_jogador, largura_atual, current_altura_mao_jogador)
    s = pygame.Surface((mao_area_rect.width, mao_area_rect.height), pygame.SRCALPHA)
    s.fill((0, 0, 0, 30))
    surface.blit(s, (mao_area_rect.x, mao_area_rect.y))

    # Usa utils.font_medium aqui
    desenha_texto(surface, "Sua Mão:", utils.font_medium, current_margem, altura_atual - current_altura_mao_jogador + current_margem, PRETO)

    return card_rects

def desenha_area_comparacao(surface, carta_usuario: Carta, carta_pc: Carta, selected_attribute_name: str, valor_usuario, valor_pc, resultado_texto: str, largura_atual, altura_atual):
    """Desenha as cartas selecionadas e os detalhes da comparação no centro da tela, responsivamente."""
    current_carta_largura = utils.carta_largura
    current_carta_altura = utils.carta_altura
    current_margem = utils.margem
    current_altura_mao_jogador = utils.altura_mao_jogador

    center_x = largura_atual // 2
    area_y_start = int(altura_atual * 0.15)
    comparacao_fundo_rect = pygame.Rect(
        current_margem * 2, area_y_start - current_margem,
        largura_atual - current_margem * 4,
        altura_atual - current_altura_mao_jogador - area_y_start + current_margem
    )
    comparacao_fundo_radius = max(5, int(min(comparacao_fundo_rect.width, comparacao_fundo_rect.height) * 0.02))
    comparacao_fundo_borda = max(1, int(min(comparacao_fundo_rect.width, comparacao_fundo_rect.height) * 0.005))
    pygame.draw.rect(surface, AZUL_CLARO, comparacao_fundo_rect, border_radius=comparacao_fundo_radius)
    pygame.draw.rect(surface, AZUL_ESCURO, comparacao_fundo_rect, comparacao_fundo_borda, border_radius=comparacao_fundo_radius)

    spacing_cards = int(largura_atual * 0.1)
    pos_y_cartas_comparacao = comparacao_fundo_rect.y + current_margem * 2
    if pos_y_cartas_comparacao + current_carta_altura > comparacao_fundo_rect.bottom - current_margem:
         pos_y_cartas_comparacao = comparacao_fundo_rect.bottom - current_carta_altura - current_margem


    rect_usuario = pygame.Rect(center_x - current_carta_largura - spacing_cards // 2, pos_y_cartas_comparacao, current_carta_largura, current_carta_altura)
    desenha_carta(surface, carta_usuario, rect_usuario, face_up=True)

    rect_pc = pygame.Rect(center_x + spacing_cards // 2, pos_y_cartas_comparacao, current_carta_largura, current_carta_altura)
    desenha_carta(surface, carta_pc, rect_pc, face_up=True)

    text_area_y_start = rect_usuario.bottom + max(10, int(altura_atual * 0.03))
    text_x_usuario = rect_usuario.centerx
    text_x_pc = rect_pc.centerx
    text_x_atributo_nome = center_x

    if selected_attribute_name:
        max_width_attr_name_comp = comparacao_fundo_rect.width - current_margem * 2
        pos_y_attr_name_comp = text_area_y_start
        # Usa utils.font_medium aqui
        if pos_y_attr_name_comp + (utils.font_medium.get_linesize() if utils.font_medium else 20) > comparacao_fundo_rect.bottom - current_margem:
             pos_y_attr_name_comp = comparacao_fundo_rect.bottom - current_margem - (utils.font_medium.get_linesize() if utils.font_medium else 20)


        # Usa utils.font_medium aqui
        desenha_texto(surface, f"Atributo: {selected_attribute_name.replace('_', ' ').title()}:", utils.font_medium, text_x_atributo_nome, pos_y_attr_name_comp, PRETO, alinhamento="midtop", max_width=max_width_attr_name_comp)

        # Usa utils.font_medium aqui
        value_display_y = pos_y_attr_name_comp + max(5, int(altura_atual * 0.02)) + (utils.font_medium.get_linesize() if utils.font_medium else 20)
        # Usa utils.font_medium aqui
        line_height_values = int(utils.font_medium.get_linesize() * 1.2) if utils.font_medium else 25

        max_width_valor_comp = (comparacao_fundo_rect.width / 2) - (spacing_cards / 2) - current_margem

        if value_display_y + line_height_values * 2 < comparacao_fundo_rect.bottom - current_margem:
            # Usa utils.font_small e utils.font_medium aqui
            desenha_texto(surface, "Seu Valor:", utils.font_small, text_x_usuario, value_display_y, PRETO, alinhamento="midtop", max_width=max_width_valor_comp)
            desenha_texto(surface, utils.formatar_valor_numerico(valor_usuario), utils.font_medium, text_x_usuario, value_display_y + int(line_height_values * 0.8), VERDE, alinhamento="midtop", max_width=max_width_valor_comp)

            # Usa utils.font_small e utils.font_medium aqui
            desenha_texto(surface, "Valor PC:", utils.font_small, text_x_pc, value_display_y, PRETO, alinhamento="midtop", max_width=max_width_valor_comp)
            desenha_texto(surface, utils.formatar_valor_numerico(valor_pc), utils.font_medium, text_x_pc, value_display_y + int(line_height_values * 0.8), VERMELHO, alinhamento="midtop", max_width=max_width_valor_comp)


    if resultado_texto:
        resultado_y = comparacao_fundo_rect.bottom - current_margem * 3
        max_width_resultado = comparacao_fundo_rect.width - current_margem * 2
        min_y_resultado = (value_display_y + line_height_values * 2 + current_margem) if selected_attribute_name else (comparacao_fundo_rect.y + current_margem)
        if resultado_y > min_y_resultado:
            # Usa utils.font_large aqui
            desenha_texto(surface, resultado_texto, utils.font_large, center_x, resultado_y, AZUL_ESCURO, alinhamento="center", max_width=max_width_resultado)


def desenha_selecao_atributo(surface, carta_usuario: Carta, carta_pc: Carta, largura_atual, altura_atual):
     """Desenha a carta selecionada, a carta do PC (virada para baixo) e os atributos clicáveis, responsivamente."""
     current_carta_largura = utils.carta_largura
     current_carta_altura = utils.carta_altura
     current_margem = utils.margem
     current_altura_mao_jogador = utils.altura_mao_jogador

     center_x = largura_atual // 2
     area_y_start = current_margem * 2
     selecao_fundo_rect = pygame.Rect(current_margem * 2, area_y_start - current_margem, largura_atual - current_margem * 4, altura_atual - current_altura_mao_jogador - area_y_start + current_margem)
     selecao_fundo_radius = max(5, int(min(selecao_fundo_rect.width, selecao_fundo_rect.height) * 0.02))
     selecao_fundo_borda = max(1, int(min(selecao_fundo_rect.width, selecao_fundo_rect.height) * 0.005))
     pygame.draw.rect(surface, AZUL_CLARO, selecao_fundo_rect, border_radius=selecao_fundo_radius)
     pygame.draw.rect(surface, AZUL_ESCURO, selecao_fundo_rect, selecao_fundo_borda, border_radius=selecao_fundo_radius)


     # Posição da carta selecionada na área de seleção (à esquerda)
     selected_card_x = selecao_fundo_rect.x + current_margem * 2
     selected_card_y = selecao_fundo_rect.y + current_margem * 2
     selected_card_rect = pygame.Rect(selected_card_x, selected_card_y, current_carta_largura, current_carta_altura)
     desenha_carta(surface, carta_usuario, selected_card_rect, face_up=True)


     # Desenha os atributos como botões (à direita da carta do usuário)
     atributos_disponiveis = [
        'populacao', 'area', 'pib', 'pontos_turisticos', 'pib_per_capita', 'densidade'
     ]

     attribute_rects = []
     coluna_botoes_x_start = selected_card_rect.right + current_margem * 3
     coluna_botoes_y_start = selecao_fundo_rect.y + current_margem * 2

     # Usa utils.font_medium aqui
     desenha_texto(surface, "Escolha um atributo:", utils.font_medium, coluna_botoes_x_start, coluna_botoes_y_start - max(10, int(current_margem * 1.5)), PRETO)

     largura_disponivel_total = selecao_fundo_rect.right - current_margem * 2 - coluna_botoes_x_start
     percentual_largura_botoes = 0.6
     largura_disponivel_apenas_botoes = int(largura_disponivel_total * percentual_largura_botoes)
     largura_disponivel_apenas_botoes = max(150, largura_disponivel_apenas_botoes)


     button_width = max(100, int(largura_disponivel_apenas_botoes * 0.9))
     button_height = max(25, int(altura_atual * 0.04))
     button_spacing = max(5, int(altura_atual * 0.015))

     max_width_texto_botao = button_width - max(5, int(current_margem * 0.5))


     for i, attr_nome in enumerate(atributos_disponiveis):
         valor = carta_usuario.get_atributo(attr_nome)
         texto_atributo = f"{attr_nome.replace('_', ' ').title()}: {utils.formatar_valor_numerico(valor)}"

         button_rect = pygame.Rect(coluna_botoes_x_start, coluna_botoes_y_start + i * (button_height + button_spacing), button_width, button_height)

         if button_rect.bottom > selecao_fundo_rect.bottom - current_margem:
              break


         pygame.draw.rect(surface, CINZA_MEDIO, button_rect, border_radius=5)
         pygame.draw.rect(surface, PRETO, button_rect, 1, border_radius=5)

         # Usa utils.font_small aqui
         desenha_texto(surface, texto_atributo, utils.font_small, button_rect.midleft[0] + max(3, int(current_margem * 0.5)), button_rect.centery, PRETO, alinhamento="midleft", max_width=max_width_texto_botao)


         attribute_rects.append((button_rect, attr_nome))


     # Desenha a carta do computador virada para baixo
     # Posição: À direita da coluna de botões de atributo
     if carta_pc:
         rect_pc_virada_x = coluna_botoes_x_start + largura_disponivel_apenas_botoes + current_margem * 2
         rect_pc_virada_y = coluna_botoes_y_start # Alinha verticalmente com o topo dos botões


         if rect_pc_virada_x + current_carta_largura <= selecao_fundo_rect.right - current_margem:
              if rect_pc_virada_y + current_carta_altura <= selecao_fundo_rect.bottom - current_margem:
                   rect_pc_virada = pygame.Rect(rect_pc_virada_x, rect_pc_virada_y, current_carta_largura, current_carta_altura)
                   desenha_carta(surface, None, rect_pc_virada, face_up=False)
              # else:
                  # print(f"DEBUG: Carta do PC muito baixa para caber na área de seleção de atributo. Y={rect_pc_virada_y}") # Debugging
         # else:
             # print(f"DEBUG: Carta do PC muito à direita para caber na área de seleção de atributo. X={rect_pc_virada_x}") # Debugging


     return attribute_rects