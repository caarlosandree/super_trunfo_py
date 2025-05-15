# Super Trunfo de Cidades Brasileiras

[![Linguagem](https://img.shields.io/badge/Linguagem-Python-blue.svg)](https://www.python.org/)
[![Biblioteca GUI](https://img.shields.io/badge/GUI-Pygame-brightgreen.svg)](https://www.pygame.org/)
[![Banco de Dados](https://img.shields.io/badge/Banco%20de%20Dados-PostgreSQL-blue.svg)](https://www.postgresql.org/)

## Sobre o Projeto

Este projeto é uma implementação do clássico jogo de cartas Super Trunfo, focado em cidades brasileiras. Ele utiliza Python para a lógica do jogo e a biblioteca Pygame para a interface gráfica, interagindo com um banco de dados PostgreSQL para gerenciar as informações das cartas.

O objetivo é criar uma experiência visual interativa onde o jogador escolhe uma carta e um atributo para competir contra uma carta aleatória do computador, com base nos dados populacionais, econômicos e geográficos das cidades.

## Funcionalidades Implementadas

* **Interface Gráfica (GUI):** Desenvolvida com Pygame, apresentando diferentes estados de jogo (sorteio, escolha de carta, escolha de atributo, comparação).
* **Layout Responsivo:** A interface se adapta a diferentes tamanhos de janela, ajustando o posicionamento e tamanho dos elementos para uma melhor visualização.
* **Integração com Banco de Dados:** Carregamento dinâmico de cartas e seus atributos a partir de um banco de dados PostgreSQL.
* **Modularização:** O código é organizado em módulos e pacotes (`src/gui`, `src/db`, `src/game`) para melhor manutenção e escalabilidade.
* **Lógica de Carta:** Classe `Carta` para representar as cidades e seus atributos, incluindo indicadores calculados (PIB per Capita, Densidade Populacional).
* **Seleção de Cartas e Atributos:** O jogador pode interagir com a GUI para escolher sua carta e o atributo a ser comparado.
* **Comparação de Atributos:** Lógica inicial para comparar o atributo escolhido entre as cartas do jogador e do computador.

## Tecnologias Utilizadas

* **Python:** Linguagem de programação principal.
* **Pygame:** Biblioteca para desenvolvimento da interface gráfica e jogos 2D.
* **psycopg2:** Adaptador para conectar Python a um banco de dados PostgreSQL.
* **PostgreSQL:** Sistema de gerenciamento de banco de dados relacional para armazenar os dados das cidades.

## Como Configurar e Rodar

1.  **Clone o Repositório:**
    ```bash
    git clone [https://github.com/caarlosandree/super_trunfo_py.git](https://github.com/caarlosandree/super_trunfo_py.git)
    cd super_trunfo_py
    ```
2.  **Crie um Ambiente Virtual (Recomendado):**
    ```bash
    python -m venv .venv
    # No Windows:
    .venv\Scripts\activate
    # No macOS/Linux:
    source .venv/bin/activate
    ```
3.  **Instale as Dependências:**
    ```bash
    pip install pygame psycopg2-binary
    ```
4.  **Configure o Banco de Dados:**
    * Tenha uma instância do PostgreSQL rodando.
    * Crie um banco de dados (ex: `supertrunfo_db`).
    * Crie a tabela `infos_cidades` com a estrutura adequada (pode ser necessário um script SQL, se não tiver crie um arquivo como `db/schema.sql` e descreva a estrutura). Exemplo básico:
        ```sql
        CREATE TABLE infos_cidades (
            codigo VARCHAR(10) PRIMARY KEY,
            nome_cidade VARCHAR(100) NOT NULL,
            estado VARCHAR(2) NOT NULL,
            populacao BIGINT,
            area DECIMAL(10, 2),
            pib DECIMAL(20, 2), -- Ajuste o tipo e precisão conforme seus dados
            pontos_turisticos INT
            -- Adicione outras colunas conforme necessário
        );
        ```
    * Popule a tabela com os dados das cidades. Você pode usar um script Python, um cliente SQL ou importar de um arquivo (CSV, etc.).
5.  **Configure as Variáveis de Ambiente:**
    * Defina a variável de ambiente `DB_PASSWORD` com a senha do seu usuário do PostgreSQL.
    * **Importante:** Se estiver usando uma IDE como PyCharm, configure a variável de ambiente nas configurações de execução do script `src/main.py`. Se estiver usando o terminal, defina-a na sessão antes de executar (`export DB_PASSWORD='sua_senha'` no Linux/macOS ou `set DB_PASSWORD=sua_senha` no Windows).
    * Se você usou nomes ou portas diferentes para o DB, pode sobrescrever as variáveis `DB_NAME`, `DB_USER`, `DB_HOST`, `DB_PORT` da mesma forma.
6.  **Execute o Jogo:**
    A partir da raiz do projeto (`super_trunfo_py`), execute como um módulo:
    ```bash
    python -m src.main
    ```

## Estrutura do Projeto

super_trunfo_py/
├── src/
│ ├── init.py
│ ├── gui/
│ │ ├── init.py
│ │ ├── gui.py # Loop principal da GUI, estados, eventos
│ │ ├── drawing.py # Funções de desenho genéricas (texto, carta)
│ │ ├── layouts.py # Funções de desenho de layouts específicos (mão, comparação, seleção)
│ │ └── utils.py # Utilitários da GUI (dimensões, fontes, formatação)
│ ├── db/
│ │ ├── init.py
│ │ └── db.py # Conexão e operações de banco de dados
│ ├── game/
│ │ ├── init.py
│ │ ├── carta.py # Definição da classe Carta
│ │ ├── escolha_com.py # Lógica de escolha do computador
│ │ └── escolha_usuario.py # Lógica de sorteio de mão inicial
│ ├── config.py # Configurações globais (DB, tamanho da mão)
│ └── main.py # Ponto de entrada principal
├── fontes/ # Arquivos das fontes customizadas (.ttf)
└── README.md # Este arquivo!


## Próximos Passos (Sugestões de Melhoria)

* Implementar a lógica completa do jogo (turnos, adição de cartas ao vencedor, remoção de perdedor).
* Gerenciamento de placar e condição de vitória/derrota.
* Adicionar mais estados de jogo (tela inicial, fim de jogo, tela de placar).
* Incluir sons e músicas.
* Melhorar a apresentação visual (cartas mais detalhadas, animações).
* Adicionar a possibilidade de jogar contra outro jogador (local ou online).
* Expandir o banco de dados com mais cidades e atributos.
* Criar um script para facilitar a criação da tabela do banco de dados.