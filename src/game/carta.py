# src/game/carta.py

class Carta:
    """Representa uma carta de cidade com seus atributos e indicadores calculados."""

    def __init__(self, codigo, nome_cidade, estado, populacao, area, pib, pontos_turisticos):
        self.codigo = codigo
        self.nome_cidade = nome_cidade
        self.estado = estado
        self.populacao = populacao
        self.area = area
        self.pib = pib  # Assume que PIB já está em BRL bilhões ou na unidade correta do DB
        self.pontos_turisticos = pontos_turisticos

        # Calcula indicadores derivados ao inicializar
        self._calcula_indicadores()

    def _calcula_indicadores(self):
        """Calcula PIB per capita e densidade populacional."""
        self.pib_per_capita = None
        # Verifica se populacao e pib não são None e populacao > 0 antes de calcular
        if self.populacao is not None and self.populacao > 0 and self.pib is not None:
             # Converte PIB para BRL (se assumirmos que o PIB no DB está em BRL bilhões)
             # Se o PIB no DB já estiver em BRL, remova a multiplicação por 1e9
            try:
                self.pib_per_capita = (self.pib * 1_000_000_000) / self.populacao
            except (TypeError, ValueError):
                 self.pib_per_capita = None # Define como None se a operação falhar

        self.densidade = None
        # Verifica se populacao e area não são None e area > 0 antes de calcular
        if self.populacao is not None and self.area is not None and self.area > 0:
            try:
                self.densidade = self.populacao / self.area
            except (TypeError, ValueError):
                self.densidade = None # Define como None se a operação falhar


    def get_atributo(self, atributo_nome):
        """Retorna o valor de um atributo pelo seu nome."""
        atributos = {
            'codigo': self.codigo,
            'nome_cidade': self.nome_cidade,
            'estado': self.estado,
            'populacao': self.populacao,
            'area': self.area,
            'pib': self.pib,
            'pontos_turisticos': self.pontos_turisticos,
            'pib_per_capita': self.pib_per_capita,
            'densidade': self.densidade
        }
        return atributos.get(atributo_nome) # Usar .get() para retornar None se o atributo não existir

    def __str__(self):
        """Representação string da carta para exibição."""
        return f"{self.nome_cidade} ({self.codigo})"

    def __repr__(self):
        """Representação formal da carta (útil para depuração)."""
        return f"Carta(codigo='{self.codigo}', nome_cidade='{self.nome_cidade}')"