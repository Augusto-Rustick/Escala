class CarregarCedulasUseCase:
    def __init__(self, inventoryRepository, notificacaoService):
        self.inventoryRepository = inventoryRepository
        self.notificacaoService = notificacaoService

    def execute(self, cedulas: dict):
        inventario = self.inventoryRepository.getInventory()
        for denom, qtd in cedulas.items():
            inventario.adicionarCedula(denom, qtd)
        self.inventoryRepository.updateInventory(inventario)
        self.notificacaoService.notify(f"Carregar cédulas: {cedulas}")
        return True
