class CaixaService:
    def __init__(self, saqueUseCase, carregarCedulasUseCase, consultarInventarioUseCase):
        self.saqueUseCase = saqueUseCase
        self.carregarCedulasUseCase = carregarCedulasUseCase
        self.consultarInventarioUseCase = consultarInventarioUseCase

    def getSaldo(self, contaId):
        # delega ao usecase de saque para obter saldo via repos
        return self.saqueUseCase.get_saldo(contaId)

    def realizarSaque(self, contaId, valor, strategyNome='padrao'):
        return self.saqueUseCase.execute(contaId, valor, strategyNome)

    def carregarCedulas(self, cedulas):
        return self.carregarCedulasUseCase.execute(cedulas)

    def consultarInventario(self):
        return self.consultarInventarioUseCase.execute()
