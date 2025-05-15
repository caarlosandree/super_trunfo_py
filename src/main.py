# src/main.py

# Importar a função que inicia a interface gráfica do subpacote gui
from src.gui.gui import run_game_gui
import sys # Importar sys para sair corretamente

# Opcional: Você pode adicionar aqui alguma lógica de configuração
# antes de iniciar a GUI, como carregar configurações de arquivo,
# analisar argumentos de linha de comando, etc.
# Ex: print("Preparando para iniciar o jogo...")

if __name__ == "__main__":
    # Este bloco só roda quando main.py é executado diretamente
    try:
        run_game_gui() # Inicia a interface gráfica do jogo
    except Exception as e:
        print(f"Um erro inesperado ocorreu durante a execução da GUI: {e}")
    finally:
        # Certifique-se de que o script termina corretamente após o Pygame fechar
        sys.exit()