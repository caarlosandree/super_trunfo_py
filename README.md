# Super Trunfo de Cidades Brasileiras

[![Linguagem](https://img.shields.io/badge/Linguagem-Python-blue.svg)](https://www.python.org/)
[![Biblioteca GUI](https://img.shields.io/badge/GUI-Pygame-brightgreen.svg)](https://www.pygame.org/)
[![Banco de Dados](https://img.shields.io/badge/Banco%20de%20Dados-PostgreSQL-blue.svg)](https://www.postgresql.org/)
[![Licença](https://img.shields.io/badge/Licença-MIT-green.svg)](LICENSE)

## Índice

- [Sobre o Projeto](#sobre-o-projeto)
- [Funcionalidades Implementadas](#funcionalidades-implementadas)
- [Tecnologias Utilizadas](#tecnologias-utilizadas)
- [Como Configurar e Rodar](#como-configurar-e-rodar)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Próximos Passos (Sugestões de Melhoria)](#próximos-passos-sugestões-de-melhoria)

## Sobre o Projeto

Este projeto é uma implementação do clássico jogo de cartas Super Trunfo, focado em cidades brasileiras. Ele utiliza Python para a lógica do jogo e a biblioteca Pygame para a interface gráfica, interagindo com um banco de dados PostgreSQL para gerenciar as informações das cartas.

O objetivo é criar uma experiência visual interativa onde o jogador escolhe uma carta e um atributo para competir contra uma carta aleatória do computador, com base nos dados populacionais, econômicos e geográficos das cidades.

## Funcionalidades Implementadas

- **Interface Gráfica (GUI):** Desenvolvida com Pygame, apresentando diferentes estados de jogo (sorteio, escolha de carta, escolha de atributo, comparação).
- **Layout Responsivo:** A interface se adapta a diferentes tamanhos de janela, ajustando o posicionamento e tamanho dos elementos para uma melhor visualização.
- **Integração com Banco de Dados:** Carregamento dinâmico de cartas e seus atributos a partir de um banco de dados PostgreSQL.
- **Modularização:** O código é organizado em módulos e pacotes (`src/gui`, `src/db`, `src/game`) para melhor manutenção e escalabilidade.
- **Lógica de Carta:** Classe `Carta` para representar as cidades e seus atributos, incluindo indicadores calculados (PIB per Capita, Densidade Populacional).
- **Seleção de Cartas e Atributos:** O jogador pode interagir com a GUI para escolher sua carta e o atributo a ser comparado.
- **Comparação de Atributos:** Lógica inicial para comparar o atributo escolhido entre as cartas do jogador e do computador.

## Tecnologias Utilizadas

- **Python:** Linguagem de programação principal.
- **Pygame:** Biblioteca para desenvolvimento da interface gráfica e jogos 2D.
- **psycopg2:** Adaptador para conectar Python a um banco de dados PostgreSQL.
- **PostgreSQL:** Sistema de gerenciamento de banco de dados relacional para armazenar os dados das cidades.

## Como Configurar e Rodar

1. **Clone o Repositório:**
    ```bash
    git clone https://github.com/caarlosandree/super_trunfo_py.git
    cd super_trunfo_py
    ```

2. **Crie um Ambiente Virtual (Recomendado):**
    ```bash
    python -m venv .venv
    # No Windows:
    .venv\Scripts\activate
    # No macOS/Linux:
    source .venv/bin/activate
    ```

3. **Instale as Dependências:**
    ```bash
    pip install pygame psycopg2-binary
    ```

4. **Configure o Banco de Dados:**
    - Tenha uma instância do PostgreSQL rodando.
    - Crie um banco de dados (ex: `supertrunfo_db`).
    - Crie a tabela `infos_cidades` com a estrutura adequada. Exemplo básico:
        ```sql
        CREATE TABLE infos_cidades (
            codigo VARCHAR(10) PRIMARY KEY,
            nome_cidade VARCHAR(100) NOT NULL,
            estado VARCHAR(2) NOT NULL,
            populacao BIGINT,
            area DECIMAL(10, 2),
            pib DECIMAL(20, 2),
            pontos_turisticos INT
            -- Adicione outras colunas conforme necessário
        );
        ```
    - Popule a tabela com os dados das cidades via script, importação de CSV ou cliente SQL.

5. **Configure as Variáveis de Ambiente:**
    - Defina a variável `DB_PASSWORD` com a senha do PostgreSQL.
    - Também é possível definir `DB_NAME`, `DB_USER`, `DB_HOST`, `DB_PORT` conforme sua configuração.
    - Exemplo:
        - Linux/macOS:
          ```bash
          export DB_PASSWORD='sua_senha'
          ```
        - Windows:
          ```cmd
          set DB_PASSWORD=sua_senha
          ```

6. **Execute o Jogo:**
    ```bash
    python -m src.main
    ```

## Estrutura do Projeto

```text
super_trunfo_py/
├── src/
│   ├── __init__.py
│   ├── gui/
│   │   ├── __init__.py
│   │   ├── gui.py            # Loop principal da GUI, estados, eventos
│   │   ├── drawing.py        # Funções de desenho genéricas (texto, carta)
│   │   ├── layouts.py        # Funções de desenho de layouts específicos (mão, comparação, seleção)
│   │   └── utils.py          # Utilitários da GUI (dimensões, fontes, formatação)
│   ├── db/
│   │   ├── __init__.py
│   │   └── db.py             # Conexão e operações de banco de dados
│   ├── game/
│   │   ├── __init__.py
│   │   ├── carta.py          # Definição da classe Carta
│   │   ├── escolha_com.py    # Lógica de escolha do computador
│   │   └── escolha_usuario.py # Lógica de sorteio de mão inicial
│   ├── config.py             # Configurações globais (DB, tamanho da mão)
│   └── main.py               # Ponto de entrada principal
├── fontes/                   # Arquivos das fontes customizadas (.ttf)
└── README.md                 # Documentação do projeto