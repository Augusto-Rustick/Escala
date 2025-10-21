from decimal import Decimal
from core.domino.excecoes import ContaNaoEncontradaError
import time

class CaixaController:
    def __init__(self, caixaService):
        self.caixaService = caixaService

    def iniciar(self):
        while True:
            print("\n=== CAIXA ELETRÔNICO ===")
            print("1. Consultar saldo")
            print("2. Realizar saque")
            print("3. Consultar inventário")
            print("4. Carregar cédulas (admin)")
            print("0. Sair")

            opcao = input("Escolha uma opção: ").strip()

            if opcao == "1":
                self.consultarSaldo()
            elif opcao == "2":
                self.realizarSaque()
            elif opcao == "3":
                self.consultarInventario()
            elif opcao == "4":
                self.carregarCedulas()
            elif opcao == "0":
                print("Encerrando o sistema...")
                break
            else:
                print("Opção inválida!")

    def consultarSaldo(self):
        contaId = input("Informe o ID da conta: ").strip()
        try:
            saldo = self.caixaService.getSaldo(contaId)
            print(f"Saldo atual: R${{saldo}}".replace('Decimal', ''))
        except Exception as e:
            print('Erro ao consultar saldo:', e)

    def realizarSaque(self):
        contaId = input("Informe o ID da conta: ").strip()
        try:
            valor = Decimal(input("Informe o valor do saque: ").strip())
        except Exception:
            print('Valor inválido')
            return
        strategy = input("Estratégia (padrao/alternativa): ").strip().lower()
        resultado = self.caixaService.realizarSaque(contaId, valor, strategy)
        if resultado.get('success'):
            print("Saque realizado com sucesso!")
            print("Cédulas entregues:", resultado.get('dispensed_notes'))
        else:
            print(f"Erro: {resultado.get('message')}")
            if resultado.get('suggestions'):
                print("Sugestões possíveis:", resultado.get('suggestions'))

    def consultarInventario(self):
        inventario = self.caixaService.consultarInventario()
        print("Inventário atual:")
        for valor, qtd in inventario.items():
            print(f"R${{valor}}: {{qtd}} unidades")

    def carregarCedulas(self):
        try:
            valor = int(input("Informe o valor da cédula (ex: 50): ").strip())
            qtd = int(input("Informe a quantidade a adicionar: ").strip())
        except Exception:
            print('Entrada inválida')
            return
        self.caixaService.carregarCedulas({valor: qtd})
        print("Cédulas adicionadas com sucesso.")
