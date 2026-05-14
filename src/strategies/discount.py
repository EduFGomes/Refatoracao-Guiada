from abc import ABC, abstractmethod
from typing import List
from src.models.item import Item

class IDiscountStrategy(ABC):
    @abstractmethod
    def apply_discount(self, total_base: float, itens: List[Item]) -> float:
        pass

class NoDiscount(IDiscountStrategy):
    def apply_discount(self, total_base: float, itens: List[Item]) -> float:
        return total_base

class PercentageDiscount(IDiscountStrategy):
    def __init__(self, percent: float):
        self.percent = percent

    def apply_discount(self, total_base: float, itens: List[Item]) -> float:
        return total_base * (1.0 - self.percent)

class VIPDiscount(IDiscountStrategy):
    def apply_discount(self, total_base: float, itens: List[Item]) -> float:
        return total_base * 0.95

class CorporateDiscount(IDiscountStrategy):
    def apply_discount(self, total_base: float, itens: List[Item]) -> float:
        return total_base * 0.90

class VolumeDiscountStrategy(IDiscountStrategy):
    def apply_discount(self, total_base: float, itens: List[Item]) -> float:
        # Nova Extensao OCP: 15% de desconto adicional para 3 ou mais unidades do mesmo item.
        # Desconto em cima do valor do item específico ou do total base?
        # A regra diz: "15% de desconto adicional para 3 ou mais unidades do mesmo item."
        # Assumindo que o desconto é aplicado ao subtotal desse item.
        
        novo_total = 0.0
        for item in itens:
            subtotal = item.preco * item.quantidade
            if item.quantidade >= 3:
                subtotal *= 0.85
            novo_total += subtotal
        
        return novo_total
