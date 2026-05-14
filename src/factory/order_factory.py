from src.models.order import Order, NormalOrder, VIPOrder, CorporateOrder

class OrderFactory:
    @staticmethod
    def create_order(tipo: str, cliente: str) -> Order:
        if tipo == "normal":
            return NormalOrder(cliente)
        elif tipo == "vip":
            return VIPOrder(cliente)
        elif tipo == "corporativo":
            return CorporateOrder(cliente)
        else:
            raise ValueError(f"Tipo de pedido desconhecido: {tipo}")
