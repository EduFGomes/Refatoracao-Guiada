import pytest
import os
import sqlite3
from src.models.item import Item
from src.factory.order_factory import OrderFactory
from src.repositories.sqlite_repo import SQLiteOrderRepository
from src.services.order_service import OrderService
from src.services.report_service import ReportService
from src.strategies.payment import CreditCardPayment, PixPayment, BoletoPayment, CryptoPaymentStrategy
from src.strategies.discount import NoDiscount, PercentageDiscount, VIPDiscount, CorporateDiscount, VolumeDiscountStrategy
from src.observers.notifications import EmailNotifier, SMSNotifier, ManagerNotifier, WhatsAppNotifier

@pytest.fixture
def test_db():
    db_path = 'test_loja.db'
    if os.path.exists(db_path):
        os.remove(db_path)
    
    repo = SQLiteOrderRepository(db_path)
    yield repo
    
    if os.path.exists(db_path):
        os.remove(db_path)

def test_golden_master_create_and_pay_order(test_db):
    repo = test_db
    service = OrderService(repo)
    
    service.add_observer(EmailNotifier())
    service.add_observer(WhatsAppNotifier())
    
    order = OrderFactory.create_order("normal", "Cliente Teste")
    order.add_item(Item("Prod A", 100.0, 2))
    
    order_id = service.create_order(order)
    assert order_id is not None
    assert order.status == "pendente"
    
    saved_order = repo.get(order_id)
    assert saved_order is not None
    assert saved_order.cliente == "Cliente Teste"
    assert saved_order.get_total_base() == 200.0
    
    # Processar Pagamento Cartão
    success = service.process_payment(order, CreditCardPayment(), 200.0, NoDiscount())
    assert success is True
    assert order.status == "aprovado"
    
    updated_order = repo.get(order_id)
    assert updated_order.status == "aprovado"

def test_factory_creates_correct_types():
    normal = OrderFactory.create_order("normal", "A")
    vip = OrderFactory.create_order("vip", "B")
    corp = OrderFactory.create_order("corporativo", "C")
    
    assert normal.get_tipo() == "normal"
    assert vip.get_tipo() == "vip"
    assert corp.get_tipo() == "corporativo"
    
    with pytest.raises(ValueError):
        OrderFactory.create_order("inexistente", "D")

def test_vip_and_crypto_payment(test_db):
    service = OrderService(test_db)
    service.add_observer(SMSNotifier())
    
    order = OrderFactory.create_order("vip", "VIP User")
    order.add_item(Item("Monitor", 1000.0, 1))
    
    service.create_order(order)
    
    # VIP discount = 5%. 1000 * 0.95 = 950. Cripto fee doesn't change amount requested internally.
    success = service.process_payment(order, CryptoPaymentStrategy(), 950.0, VIPDiscount())
    assert success is True
    
    # insufficient funds
    success_fail = service.process_payment(order, PixPayment(), 10.0, VIPDiscount())
    assert success_fail is False

def test_corporate_and_volume_discount(test_db):
    service = OrderService(test_db)
    service.add_observer(ManagerNotifier())
    
    order = OrderFactory.create_order("corporativo", "Corp")
    order.add_item(Item("Teclado", 100.0, 3)) # 300 base, with volume: 300 * 0.85 = 255
    
    service.create_order(order)
    success = service.process_payment(order, BoletoPayment(), 255.0, VolumeDiscountStrategy())
    assert success is True

def test_percentage_and_corporate_discount():
    corp_disc = CorporateDiscount()
    perc_disc = PercentageDiscount(0.10)
    
    itens = [Item("A", 100.0, 1)]
    assert corp_disc.apply_discount(100.0, itens) == 90.0
    assert perc_disc.apply_discount(100.0, itens) == 90.0

def test_update_status(test_db):
    service = OrderService(test_db)
    order = OrderFactory.create_order("normal", "X")
    order.add_item(Item("A", 10.0, 1))
    oid = service.create_order(order)
    
    service.update_status(oid, "enviado")
    assert test_db.get(oid).status == "enviado"
    
    # test get unknown
    assert test_db.get(999) is None

def test_report_service(test_db):
    service = OrderService(test_db)
    order = OrderFactory.create_order("normal", "Y")
    order.add_item(Item("A", 10.0, 1))
    service.create_order(order)
    
    report = ReportService(test_db)
    report.gerar_relatorio_vendas()
    report.gerar_relatorio_clientes()
    
    assert os.path.exists('rel_vendas.txt')
    assert os.path.exists('rel_clientes.txt')
