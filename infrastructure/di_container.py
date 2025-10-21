import os
from core.services.caixa_service import CaixaService
from core.usecases.saque_useCase import SaqueUseCase
from core.usecases.carregar_cedulas_useCase import CarregarCedulasUseCase
from core.usecases.consultar_inventario_useCase import ConsultarInventarioUseCase
from infrastructure.persistence.postgres_account_repository import PostgresAccountRepository
from infrastructure.persistence.postgres_inventory_repository import PostgresInventoryRepository
from infrastructure.strategies.menor_qtd_strategy import MenorQtdStrategy
from infrastructure.strategies.preservar_altos_strategy import PreservarAltosStrategy
from infrastructure.notifications.file_notifier import FileNotifier
from core.services.notificacao_service import NotificacaoService
from interface.cli.caixa_controller import CaixaController

class DIContainer:
    def __init__(self):
        database_url = os.environ.get('DATABASE_URL')
        if not database_url:
            raise RuntimeError('DATABASE_URL não definido')
        # repositories
        self.accountRepository = PostgresAccountRepository(database_url)
        self.inventoryRepository = PostgresInventoryRepository(database_url)
        # strategies factory simple
        self.strategies = {
            'padrao': MenorQtdStrategy(),
            'alternativa': PreservarAltosStrategy()
        }
        # notification service
        self.notificacaoService = NotificacaoService()
        self.notificacaoService.registrarNotifier(FileNotifier('logs/atm_events.log'))
        # use cases
        self.saqueUseCase = SaqueUseCase(self.accountRepository, self.inventoryRepository, self.strategies, self.notificacaoService)
        self.carregarCedulasUseCase = CarregarCedulasUseCase(self.inventoryRepository, self.notificacaoService)
        self.consultarInventarioUseCase = ConsultarInventarioUseCase(self.inventoryRepository)
        # service and controller
        self.caixaService = CaixaService(self.saqueUseCase, self.carregarCedulasUseCase, self.consultarInventarioUseCase)
        self.caixaController = CaixaController(self.caixaService)

    def get_caixa_controller(self):
        return self.caixaController
