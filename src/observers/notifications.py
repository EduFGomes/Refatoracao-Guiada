from abc import ABC, abstractmethod
from src.models.order import Order

class IOrderObserver(ABC):
    @abstractmethod
    def update(self, order: Order, evento: str) -> None:
        pass

class EmailNotifier(IOrderObserver):
    def update(self, order: Order, evento: str) -> None:
        if evento == "criado":
            print(f"Email enviado para {order.cliente}: Pedido recebido!")
        elif evento == "aprovado":
            print(f"Email enviado para {order.cliente}: Pedido aprovado!")
        elif evento == "enviado":
            print(f"Email enviado para {order.cliente}: Pedido enviado")
        elif evento == "entregue":
            print(f"Email enviado para {order.cliente}: Pedido entregue!")

class SMSNotifier(IOrderObserver):
    def update(self, order: Order, evento: str) -> None:
        if order.get_tipo() == "vip":
            if evento == "criado":
                print(f"SMS enviado para {order.cliente}: Pedido VIP recebido!")
            elif evento == "aprovado":
                print(f"SMS enviado para {order.cliente}: Pedido aprovado!")

class ManagerNotifier(IOrderObserver):
    def update(self, order: Order, evento: str) -> None:
        if order.get_tipo() == "corporativo" and evento == "criado":
            print(f"Notificacao enviada ao gerente de conta de {order.cliente}")

class WhatsAppNotifier(IOrderObserver):
    def update(self, order: Order, evento: str) -> None:
        # Nova Extensao OCP: Notificacao para todos via WhatsApp
        if evento == "aprovado":
            print(f"WhatsApp enviado para {order.cliente}: Seu pedido foi aprovado e esta sendo preparado!")
