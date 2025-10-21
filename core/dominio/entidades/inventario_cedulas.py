from decimal import Decimal

class InventarioCedulas:
    def __init__(self, mapa=None):
        # mapa: {denominacao_int: quantidade_int}
        self.cedulas = mapa or {}

    def getValorTotal(self):
        total = 0
        for denom, qtd in self.cedulas.items():
            total += denom * qtd
        return total / 100  # retorna em reais

    def adicionarCedula(self, denominacao, quantidade: int):
        self.cedulas[denominacao] = self.cedulas.get(denominacao, 0) + quantidade

    def removerCedula(self, denominacao, quantidade: int):
        atual = self.cedulas.get(denominacao, 0)
        if quantidade > atual:
            raise ValueError('Quantidade insuficiente no inventário')
        self.cedulas[denominacao] = atual - quantidade
        if self.cedulas[denominacao] == 0:
            del self.cedulas[denominacao]

    def getMapaDisponivel(self):
        return dict(self.cedulas)
