from typing import List, Optional
from datetime import datetime

from src.models.order import Order
from src.models.item import Item
from src.repositories.interfaces import IOrderRepository
from src.observers.notifications import IOrderObserver
from src.strategies.payment import IPaymentStrategy
from src.strategies.discount import IDiscountStrategy, NoDiscount

class OrderService:
    def __init__(self, repository: IOrderRepository):
        self.repository = repository
        self.observers: List[IOrderObserver] = []

    def add_observer(self, observer: IOrderObserver) -> None:
        self.observers.append(observer)

    def _notify(self, order: Order, evento: str) -> None:
        for obs in self.observers:
            obs.update(order, evento)

    def create_order(self, order: Order, discount_strategy: Optional[IDiscountStrategy] = None) -> int:
        if discount_strategy is None:
            discount_strategy = NoDiscount()
        
        # O cálculo final do total poderia ser armazenado na Order, 
        # mas por simplicidade e para não alterar a interface legada fortemente,
        # assumimos que as estratégias dão o valor final se precisarmos expor isso.
        
        order.data_criacao = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        order_id = self.repository.save(order)
        self._notify(order, "criado")
        return order_id

    def process_payment(self, order: Order, payment_strategy: IPaymentStrategy, amount_paid: float, discount_strategy: Optional[IDiscountStrategy] = None) -> bool:
        if discount_strategy is None:
            discount_strategy = NoDiscount()

        total_base = order.get_total_base()
        total_final = discount_strategy.apply_discount(total_base, order.itens)

        if amount_paid < total_final:
            print("Valor insuficiente!")
            return False

        success = payment_strategy.process_payment(total_final)
        if success:
            assert order.id is not None
            self.repository.update_status(order.id, "aprovado")
            order.status = "aprovado"
            self._notify(order, "aprovado")
        return success

    def update_status(self, order_id: int, status: str) -> None:
        order = self.repository.get(order_id)
        if order:
            self.repository.update_status(order_id, status)
            order.status = status
            self._notify(order, status)
