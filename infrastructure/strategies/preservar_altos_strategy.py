from .composition_strategy import CompositionStrategy

class PreservarAltosStrategy(CompositionStrategy):
    def compose(self, valor_reais: int, cedulasDisponiveis: dict):
        # Tenta preservar notas altas: usa mais notas pequenas primeiro.
        notas = sorted(cedulasDisponiveis.keys())
        restante = valor_reais
        resultado = {}
        for n in notas:
            if restante <= 0:
                break
            max_usable = min(cedulasDisponiveis.get(n,0), restante // n)
            if max_usable > 0:
                resultado[n] = max_usable
                restante -= n * max_usable
        if restante == 0:
            return resultado
        # fallback: tentar combinações com heurística simples
        notas_desc = sorted(cedulasDisponiveis.keys(), reverse=True)
        restante = valor_reais
        resultado = {}
        for n in notas_desc:
            max_usable = min(cedulasDisponiveis.get(n,0), restante // n)
            if max_usable > 0:
                resultado[n] = max_usable
                restante -= n * max_usable
        if restante == 0:
            return resultado
        return None
