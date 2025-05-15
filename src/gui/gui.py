# src/gui/gui.py

import pygame
import sys
import random
import os

# Importações dos subpacotes src
from src.game.escolha_usuario import sortear_mao_usuario
from src.game.escolha_com import escolher_carta_computador
from src.game.carta import Carta
from src.config import HAND_SIZE

# Importa funções e variáveis dos módulos locais do gui
from . import utils # Importa o módulo utils
from .layouts import desenha_mao_jogador, desenha_area_comparacao, desenha_selecao_atributo
# Adiciona desenha_carta à importação de drawing
from .drawing import desenha_texto, desenha_carta # <<< Adicionado desenha_carta aqui

# --- Configurações Iniciais da Janela ---
largura_tela_inicial = 1000
altura_tela_inicial = 700
titulo_jogo = "Jogo de Cartas de Cidades"

# Cores (podem ser importadas de um arquivo de constantes globais, se houver)
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
VERMELHO = (255, 0, 0) # Usada em game over
VERDE = (0, 255, 0) # Usada para o retângulo de teste no estado 'dealing'


# --- Função que inicia a interface gráfica do jogo ---

def run_game_gui():
    pygame.init()

    screen = pygame.display.set_mode((largura_tela_inicial, altura_tela_inicial), pygame.RESIZABLE)
    pygame.display.set_caption(titulo_jogo)

    largura_atual, altura_atual = screen.get_size()
    utils.calcular_dimensoes(largura_atual, altura_atual)

    # --- Variáveis de Estado do Jogo ---
    mao_jogador = []
    carta_pc = None
    carta_usuario_selecionada = None
    atributo_usuario_selecionado_nome = None
    valor_usuario_selecionado = None
    valor_pc_selecionado = None
    resultado_rodada_texto = ""

    game_state = 'dealing'

    card_rects_na_mao = []
    attribute_rects_na_selecao = []


    running = True
    while running:
        largura_atual, altura_atual = screen.get_size()

        # --- Event Handling ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            if event.type == pygame.VIDEORESIZE:
                largura_atual, altura_atual = event.size
                screen = pygame.display.set_mode((largura_atual, altura_atual), pygame.RESIZABLE)
                utils.calcular_dimensoes(largura_atual, altura_atual)

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos

                if game_state == 'choose_card':
                    for rect, carta in card_rects_na_mao:
                        if rect.collidepoint(mouse_pos):
                            carta_usuario_selecionada = carta
                            carta_pc = escolher_carta_computador(mao_jogador)
                            if carta_pc:
                                game_state = 'choose_attribute'
                                card_rects_na_mao = []
                            else:
                                print("Erro ao sortear carta do computador. Fim do jogo.")
                                game_state = 'game_over'
                            break

                elif game_state == 'choose_attribute':
                     for rect, attr_nome in attribute_rects_na_selecao:
                         if rect.collidepoint(mouse_pos):
                             atributo_usuario_selecionado_nome = attr_nome
                             valor_usuario_selecionado = carta_usuario_selecionada.get_atributo(atributo_usuario_selecionado_nome)
                             valor_pc_selecionado = carta_pc.get_atributo(atributo_usuario_selecionado_nome)

                             if valor_usuario_selecionado is None or valor_pc_selecionado is None:
                                  resultado_rodada_texto = "Dados inválidos para comparação. Empate técnico."
                             elif atributo_usuario_selecionado_nome == 'pontos_turisticos':
                                  if (valor_usuario_selecionado is not None and valor_pc_selecionado is not None):
                                       if valor_usuario_selecionado < valor_pc_selecionado:
                                           resultado_rodada_texto = "🎉 Você venceu a rodada! (Menos pontos turísticos)"
                                       elif valor_usuario_selecionado > valor_pc_selecionado:
                                           resultado_rodada_texto = "💻 O computador venceu a rodada. (Mais pontos turísticos)"
                                       else:
                                           resultado_rodada_texto = "🤝 Empate!"
                                  else:
                                       resultado_rodada_texto = "Dados de pontos turísticos inválidos. Empate técnico."
                             else:
                                 if (valor_usuario_selecionado is not None and valor_pc_selecionado is not None):
                                      if valor_usuario_selecionado > valor_pc_selecionado:
                                          resultado_rodada_texto = "🎉 Você venceu a rodada!"
                                      elif valor_usuario_selecionado < valor_pc_selecionado:
                                          resultado_rodada_texto = "💻 O computador venceu a rodada."
                                      else:
                                          resultado_rodada_texto = "🤝 Empate!"
                                 else:
                                      resultado_rodada_texto = "Dados para comparação inválidos. Empate técnico."

                             game_state = 'comparing'
                             attribute_rects_na_selecao = []
                             break

                elif game_state == 'round_end':
                    print("Clicou na tela no fim da rodada. Implementar lógica de pontuação e próxima rodada/fim de jogo.")
                    # TODO: Implementar lógica real
                    mao_jogador = []
                    carta_pc = None
                    carta_usuario_selecionada = None
                    atributo_usuario_selecionado_nome = None
                    valor_usuario_selecionado = None
                    valor_pc_selecionado = None
                    resultado_rodada_texto = ""
                    game_state = 'dealing'


        # --- Game State Logic / Updates ---
        if game_state == 'dealing':
            mao_jogador = sortear_mao_usuario()
            if mao_jogador:
                carta_pc = escolher_carta_computador(mao_jogador)
                if carta_pc:
                    game_state = 'choose_card'
                else:
                    print("Erro ao sortear carta do computador. Fim do jogo.")
                    game_state = 'game_over'
            else:
                print("Não há cartas suficientes no banco de dados para iniciar o jogo.")
                game_state = 'game_over'

        elif game_state == 'comparing':
             game_state = 'round_end'

        elif game_state == 'game_over':
            pass


        # --- Drawing ---
        screen.fill(BRANCO) # Limpa a tela com branco

        if game_state == 'dealing':
            # --- DEBUG PRINT ---
            # Mantenha este print para confirmar que ainda estamos no estado dealing
            print(f"DEBUG: Desenhando no estado 'dealing'.")
            # --- FIM DEBUG PRINT ---

            # --- Desenho de Teste ---
            # DESCOMENTE A LINHA ABAIXO PARA VOLTAR A DESENHAR O TEXTO
            # desenha_texto(screen, "Sorteando cartas...", utils.font_large, largura_atual // 2, altura_atual // 2 - 20, alinhamento="center")
            # Remova ou comente as 3 linhas abaixo para remover o retângulo de teste
            test_rect_size = 100
            test_rect = pygame.Rect(largura_atual // 2 - test_rect_size // 2, altura_atual // 2 - test_rect_size // 2, test_rect_size, test_rect_size)
            pygame.draw.rect(screen, VERDE, test_rect)
            # --- Fim Desenho de Teste ---


        elif game_state == 'choose_card':
            # Desenhar carta do computador virada para baixo no topo
            # Acessa as dimensões de utils e usa a função desenha_carta importada
            rect_pc_virada = pygame.Rect(largura_atual // 2 - utils.carta_largura // 2, utils.margem * 2, utils.carta_largura, utils.carta_altura)
            desenha_carta(screen, None, rect_pc_virada, face_up=False) # Passa None para carta, só desenha o verso

            # Desenha a mão do jogador na parte inferior (passando dimensões atuais)
            # Usa as funções e variáveis importadas (layouts e utils)
            card_rects_na_mao = desenha_mao_jogador(screen, mao_jogador, largura_atual, altura_atual, selected_card=carta_usuario_selecionada)

            # Mensagem de instrução
            # Calcula a posição Y da mensagem baseada na parte inferior da carta do PC
            # Usa as variáveis calculadas globalmente e a variável de fonte importada
            pos_y_instrucao = rect_pc_virada.bottom + utils.margem * 2 # Posiciona 2 margens abaixo da carta do PC
            # Garante que a mensagem não sobreponha a área da mão do jogador
            # A área da mão começa em altura_atual - altura_mao_jogador
            # Deixa espaço para a altura da linha de texto acima da área da mão
            # Usa as variáveis calculadas globalmente e de fonte
            espaco_para_texto = (utils.font_medium.get_linesize() if utils.font_medium else 20) + utils.margem # Altura do texto + margem de segurança
            pos_y_instrucao = min(pos_y_instrucao, altura_atual - utils.altura_mao_jogador - espaco_para_texto)

            # Usa a função desenha_texto importada
            desenha_texto(screen, "Clique em uma carta da sua mão para jogar", utils.font_medium, largura_atual // 2, pos_y_instrucao, alinhamento="center")


        elif game_state == 'choose_attribute':
            # Desenha a área de seleção de atributo, incluindo a carta do PC
            # Passa a carta do PC para a função de desenho do layout
            # Usa as variáveis calculadas globalmente
            attribute_rects_na_selecao = desenha_selecao_atributo(screen, carta_usuario_selecionada, carta_pc, largura_atual, altura_atual)


        elif game_state == 'comparing' or game_state == 'round_end':
             # Desenha a área de comparação
             # Passa todas as informações relevantes para a função de desenho do layout
             # Usa as variáveis calculadas globalmente
             desenha_area_comparacao(screen, carta_usuario_selecionada, carta_pc,
                                     atributo_usuario_selecionado_nome, valor_usuario_selecionado, valor_pc_selecionado,
                                     resultado_rodada_texto if game_state == 'round_end' else "", # Só exibe o resultado no fim da rodada
                                     largura_atual, altura_atual)
             if game_state == 'round_end':
                 # Desenha a mensagem "Clique para continuar..." na parte inferior da tela, acima da área da mão (se houver espaço)
                 # Usa as variáveis calculadas globalmente e a variável de fonte importada
                 pos_y_continuar = altura_atual - utils.margem * 2
                 # Calcula a base Y da área de comparação para evitar sobreposição
                 # Base da área de comparação = altura_atual - altura_mao_jogador
                 base_area_comparacao = altura_atual - utils.altura_mao_jogador
                 limite_superior_continuar = base_area_comparacao + utils.margem # Um pouco acima da área da mão


                 pos_y_continuar = max(limite_superior_continuar, pos_y_continuar - (utils.font_small.get_linesize() if utils.font_small else 15)) # Ajusta para cima se necessário, deixando espaço para o texto

                 # Usa a função desenha_texto importada
                 desenha_texto(screen, "Clique para continuar...", utils.font_small, largura_atual // 2, pos_y_continuar, alinhamento="midtop")


        elif game_state == 'game_over':
             # Desenha a tela de Game Over
             # Usa as variáveis de fonte importadas
             desenha_texto(screen, "Fim do Jogo", utils.font_large, largura_atual // 2, altura_atual // 2 - 20, VERMELHO, alinhamento="center")
             desenha_texto(screen, "Verifique o console para mais informações.", utils.font_medium, largura_atual // 2, altura_atual // 2 + 20, PRETO, alinhamento="center")


        # --- Atualiza a tela ---
        pygame.display.flip()


    pygame.quit()
    # Não chame sys.exit() aqui.