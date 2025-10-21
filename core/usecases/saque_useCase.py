from decimal import Decimal
from core.dominio.entidades.conta import Conta
from core.dominio.entidades.inventario_cedulas import InventarioCedulas
from core.dominio.excecoes import NaoPodeComporValorError, ContaNaoEncontradaError

class SaqueUseCase:
    def __init__(self, accountRepository, inventoryRepository, strategies: dict, notificacaoService):
        self.accountRepository = accountRepository
        self.inventoryRepository = inventoryRepository
        self.strategies = strategies
        self.notificacaoService = notificacaoService

    def get_saldo(self, contaId: str):
        conta = self.accountRepository.getById(contaId)
        if not conta:
            raise ContaNaoEncontradaError()
        return conta.saldo

    def execute(self, contaId: str, valor: Decimal, strategyNome='padrao'):
        # valor em reais (Decimal); convert to centavos int
        centavos = int((valor * 100).to_integral_value())
        conta = self.accountRepository.getById(contaId)
        if not conta:
            return {'success': False, 'message': 'Conta não encontrada'}

        if conta.saldo < valor:
            return {'success': False, 'message': 'Saldo insuficiente'}

        inventario = self.inventoryRepository.getInventory()
        mapa = inventario.getMapaDisponivel() 
        
        if centavos % 100 != 0:
            return {'success': False, 'message': 'Somente valores inteiros em reais são suportados nesta versão'}
        valor_reais = centavos // 100

        # select strategy
        strat_key = 'padrao' if strategyNome not in self.strategies else strategyNome
        strategy = self.strategies.get(strat_key)
        if strategy is None:
            strategy = list(self.strategies.values())[0]

        composition = strategy.compose(valor_reais, {k: v for k, v in mapa.items()})
        if composition is None:
            # tenta sugerir valores (simples): listar valores sacáveis menores próximos
            sugestoes = []
            # tentar decrementar até 5 tentativas
            for diff in range(1, 6):
                v_try = valor_reais - diff
                if v_try <= 0:
                    break
                if strategy.compose(v_try, {k: v for k, v in mapa.items()}) is not None:
                    sugestoes.append(v_try)
            return {'success': False, 'message': 'Não é possível compor o valor exato com o inventário atual', 'suggestions': sugestoes}

        # aplicar mudanças
        # remove notas do inventario e atualiza conta
        for denom, qtd in composition.items():
            inventario.removerCedula(denom, qtd)
        # persistir
        self.inventoryRepository.updateInventory(inventario)
        conta.sacar(valor)
        self.accountRepository.update(conta)
        # notificar
        self.notificacaoService.notify(f"Saque: conta={contaId}, valor=R${{valor}}, notas={composition}")
        return {'success': True, 'dispensed_notes': composition}
