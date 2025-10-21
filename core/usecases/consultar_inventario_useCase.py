class ConsultarInventarioUseCase:
    def __init__(self, inventoryRepository):
        self.inventoryRepository = inventoryRepository

    def execute(self):
        inventario = self.inventoryRepository.getInventory()
        return inventario.getMapaDisponivel()
