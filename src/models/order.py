from abc import ABC, abstractmethod
from typing import List, Optional
from src.models.item import Item
import json

class Order(ABC):
    def __init__(self, cliente: str):
        self.id: Optional[int] = None
        self.cliente = cliente
        self.itens: List[Item] = []
        self.status = "pendente"
        self.data_criacao = ""
    
    def add_item(self, item: Item) -> None:
        self.itens.append(item)
        
    def get_total_base(self) -> float:
        return sum(item.preco * item.quantidade for item in self.itens)

    @abstractmethod
    def get_tipo(self) -> str:
        pass

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "cli": self.cliente,
            "itens": [{"nome": i.nome, "p": i.preco, "q": i.quantidade} for i in self.itens],
            "st": self.status,
            "dt": self.data_criacao,
            "tp": self.get_tipo()
        }

class NormalOrder(Order):
    def get_tipo(self) -> str:
        return "normal"

class VIPOrder(Order):
    def get_tipo(self) -> str:
        return "vip"

class CorporateOrder(Order):
    def get_tipo(self) -> str:
        return "corporativo"
