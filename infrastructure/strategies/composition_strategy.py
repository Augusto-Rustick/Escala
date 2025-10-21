from abc import ABC, abstractmethod

class CompositionStrategy(ABC):
    @abstractmethod
    def compose(self, valor_reais: int, cedulasDisponiveis: dict):
        pass
