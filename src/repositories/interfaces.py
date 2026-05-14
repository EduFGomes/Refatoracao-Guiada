from abc import ABC, abstractmethod
from typing import List, Optional
from src.models.order import Order

class IOrderRepository(ABC):
    @abstractmethod
    def save(self, order: Order) -> int:
        pass

    @abstractmethod
    def get(self, order_id: int) -> Optional[Order]:
        pass

    @abstractmethod
    def get_all(self) -> List[Order]:
        pass

    @abstractmethod
    def update_status(self, order_id: int, status: str) -> None:
        pass
