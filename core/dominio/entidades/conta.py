from decimal import Decimal

class Conta:
    def __init__(self, id: str, saldo: Decimal):
        self.id = id
        self.saldo = saldo

    def sacar(self, valor: Decimal):
        if valor > self.saldo:
            raise ValueError('Saldo insuficiente')
        self.saldo -= valor

    def depositar(self, valor: Decimal):
        self.saldo += valor
