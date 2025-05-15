# src/gui/drawing.py

import pygame
from src.game.carta import Carta
# Importa o módulo utils para acessar as variáveis de fonte e dimensão
# Remove a importação direta das variáveis globais
from . import utils # <<< Importa o módulo utils

# Cores (podem ser importadas de um arquivo de constantes globais, se houver)
PRETO = (0, 0, 0)
AZUL_ESCURO = (70, 130, 180)
CINZA_CLARO = (220, 220, 220)
AMARELO_SELECAO = (255, 255, 102)
BRANCO = (255, 255, 255)


def desenha_texto(surface, texto, fonte: pygame.font.Font, x, y, cor=PRETO, alinhamento="topleft", max_width=None):
    # --- DEBUG PRINT ---
    # Mantém este print para verificar a fonte recebida
    print(f"DEBUG: desenha_texto chamada para '{texto}'. Fonte recebida: {fonte}")
    # --- FIM DEBUG PRINT ---

    if fonte is None:
        # print(f"Erro: Fonte não carregada para renderizar texto: '{texto}'") # Evitar spam excessivo
        return pygame.Rect(x, y, 0, 0)
    try:
        texto_str = str(texto)

        if max_width is not None and max_width > 0:
            texto_surface_temp = fonte.render(texto_str, True, cor)
            if texto_surface_temp.get_width() > max_width:
                truncated_text = texto_str
                while fonte.render(truncated_text + "...", True, cor).get_width() > max_width and len(truncated_text) > 0:
                    truncated_text = truncated_text[:-1]
                texto_str = truncated_text + "..." if len(truncated_text) < len(texto_str) else truncated_text
            if fonte.render(texto_str, True, cor).get_width() > max_width:
                 while fonte.render(texto_str, True, cor).get_width() > max_width and len(texto_str) > 0:
                      texto_str = texto_str[:-1]


        texto_surface = fonte.render(texto_str, True, cor)
        texto_rect = texto_surface.get_rect()
        if alinhamento == "topleft": texto_rect.topleft = (x, y)
        elif alinhamento == "midtop": texto_rect.midtop = (x, y)
        elif alinhamento == "center": texto_rect.center = (x, y)
        elif alinhamento == "topright": texto_rect.topright = (x, y)
        elif alinhamento == "midleft": texto_rect.midleft = (x,y)
        elif alinhamento == "midright": texto_rect.midright = (x,y)


        surface.blit(texto_surface, texto_rect)
        return texto_rect
    except pygame.error as e:
        print(f"Erro ao renderizar texto: {e} com fonte {fonte} e texto '{texto}'")
        return pygame.Rect(x, y, 0, 0)


def desenha_carta(surface, carta: Carta, rect, face_up=True, selecionada=False):
    current_card_width = rect.width
    current_card_height = rect.height
    current_margem_interna = max(3, int(min(current_card_width, current_card_height) * 0.08))

    if selecionada:
        rect_borda = rect.copy()
        rect_borda.y -= max(5, int(current_card_height * 0.05))
        borda_espessura = max(1, int(min(current_card_width, current_card_height) * 0.01))
        borda_radius = max(5, int(min(current_card_width, current_card_height) * 0.05))
        pygame.draw.rect(surface, (255, 223, 0), rect_borda, borda_espessura, border_radius=borda_radius)


    fundo_cor = AMARELO_SELECAO if selecionada else CINZA_CLARO
    borda_preta_espessura = max(1, int(min(current_card_width, current_card_height) * 0.005))
    borda_radius = max(5, int(min(current_card_width, current_card_height) * 0.05))
    pygame.draw.rect(surface, fundo_cor, rect, border_radius=borda_radius)
    pygame.draw.rect(surface, PRETO, rect, borda_preta_espessura, border_radius=borda_radius)

    if face_up and carta:
        titulo_altura = max(20, int(current_card_height * 0.15))
        titulo_rect = pygame.Rect(rect.x, rect.y, current_card_width, titulo_altura)
        pygame.draw.rect(surface, AZUL_ESCURO, titulo_rect, border_top_left_radius=borda_radius, border_top_right_radius=borda_radius)
        # Usa utils.font_medium aqui
        desenha_texto(surface, carta.nome_cidade, utils.font_medium, titulo_rect.centerx, titulo_rect.centery, BRANCO, alinhamento="center", max_width=current_card_width - current_margem_interna * 2)
        pygame.draw.line(surface, PRETO, (rect.x, rect.y + titulo_altura), (rect.x + current_card_width, rect.y + titulo_altura), borda_preta_espessura)

        attr_y_start = rect.y + titulo_altura + current_margem_interna
        attr_x_nome = rect.x + current_margem_interna
        attr_x_valor = rect.right - current_margem_interna
        # Usa utils.font_small aqui
        line_height = int(utils.font_small.get_linesize() * 1.2) if utils.font_small else 18

        atributos = ['populacao', 'area', 'pib', 'pontos_turisticos', 'pib_per_capita', 'densidade']

        for attr_nome in atributos:
            if attr_y_start + line_height > rect.bottom - current_margem_interna:
                break

            valor = carta.get_atributo(attr_nome)
            valor_formatado = utils.formatar_valor_numerico(valor)

            max_width_attr_name = int(current_card_width * 0.5)
            max_width_attr_value = int(current_card_width * 0.4)

            # Usa utils.font_small aqui
            desenha_texto(surface, f"{attr_nome.replace('_', ' ').title()}:", utils.font_small, attr_x_nome, attr_y_start, PRETO, alinhamento="topleft", max_width=max_width_attr_name)
            desenha_texto(surface, valor_formatado, utils.font_small, attr_x_valor, attr_y_start, PRETO, alinhamento="topright", max_width=max_width_attr_value)
            attr_y_start += line_height


    else:
        # Usa utils.font_large aqui
        if utils.font_large:
            desenha_texto(surface, "Top", utils.font_large, rect.centerx, rect.centery - max(10, int(current_card_height * 0.08)), PRETO, alinhamento="center")
            desenha_texto(surface, "Trunfo", utils.font_large, rect.centerx, rect.centery + max(10, int(current_card_height * 0.08)), PRETO, alinhamento="center")