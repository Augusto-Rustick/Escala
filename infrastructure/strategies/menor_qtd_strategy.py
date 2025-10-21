from .composition_strategy import CompositionStrategy

class MenorQtdStrategy(CompositionStrategy):
    def compose(self, valor_reais: int, cedulasDisponiveis: dict):
        # Greedy por notas maiores -> tenta minimizar quantidade
        # cedulasDisponiveis: {denom_reais: qtd}
        notas = sorted(cedulasDisponiveis.keys(), reverse=True)
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
        # se greedy falhar, tenta backtracking simples (recursivo)
        # limitar profundidade: tenta combinações reduzindo uso da maior nota
        def backtrack(index, restante, current):
            if restante == 0:
                return current.copy()
            if index >= len(notas):
                return None
            n = notas[index]
            max_use = min(cedulasDisponiveis.get(n,0), restante // n)
            for u in range(max_use, -1, -1):
                if u > 0:
                    current[n] = u
                elif n in current:
                    current.pop(n)
                res = backtrack(index+1, restante - n*u, current)
                if res is not None:
                    return res
            return None
        return backtrack(0, valor_reais, {})
