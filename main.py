from src.models.item import Item
from src.factory.order_factory import OrderFactory
from src.repositories.sqlite_repo import SQLiteOrderRepository
from src.observers.notifications import EmailNotifier, SMSNotifier, ManagerNotifier, WhatsAppNotifier
from src.strategies.payment import CreditCardPayment, CryptoPaymentStrategy, PixPayment
from src.strategies.discount import VolumeDiscountStrategy, VIPDiscount
from src.services.order_service import OrderService
from src.services.report_service import ReportService

def main() -> None:
    # 1. Configurando as Injeções de Dependência
    repo = SQLiteOrderRepository('loja_refatorada.db')
    order_service = OrderService(repo)
    report_service = ReportService(repo)

    # 2. Configurando Observers
    order_service.add_observer(EmailNotifier())
    order_service.add_observer(SMSNotifier())
    order_service.add_observer(ManagerNotifier())
    
    # EXTENSÃO OCP 1: WhatsApp Notifier
    order_service.add_observer(WhatsAppNotifier())

    print("\n--- TESTE 1: Pedido Normal com Desconto por Volume ---")
    # EXTENSÃO OCP 2: Desconto por Volume
    order1 = OrderFactory.create_order("normal", "Cliente Volume")
    # 3 itens iguais disparam o desconto de 15% apenas nesse subtotal
    order1.add_item(Item("Teclado Mecanico", 200.0, 3)) 
    order1.add_item(Item("Mousepad", 50.0, 1))

    order_id_1 = order_service.create_order(order1)
    print(f"Pedido Normal criado com ID {order_id_1}. Total Base: R${order1.get_total_base():.2f}")
    
    volume_discount = VolumeDiscountStrategy()
    # Paga com Cartao
    order_service.process_payment(order1, CreditCardPayment(), 600.0, discount_strategy=volume_discount)

    print("\n--- TESTE 2: Pedido VIP com Pagamento Cripto ---")
    order2 = OrderFactory.create_order("vip", "Cliente VIP Cripto")
    order2.add_item(Item("Monitor 4K", 2000.0, 1))
    
    order_id_2 = order_service.create_order(order2)
    print(f"Pedido VIP criado com ID {order_id_2}. Total Base: R${order2.get_total_base():.2f}")

    # EXTENSÃO OCP 3: Pagamento em Cripto (taxa 2%)
    crypto_payment = CryptoPaymentStrategy()
    vip_discount = VIPDiscount()
    # Total Base 2000. VIP = 1900. Cripto = 1900 * 1.02 = 1938. 
    # O valor passado tem que ser >= 1900.
    order_service.process_payment(order2, crypto_payment, 2000.0, discount_strategy=vip_discount)

    print("\n--- TESTE 3: Relatorios ---")
    report_service.gerar_relatorio_vendas()
    print()
    report_service.gerar_relatorio_clientes()

if __name__ == '__main__':
    main()
