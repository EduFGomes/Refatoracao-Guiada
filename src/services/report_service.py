from src.repositories.interfaces import IOrderRepository
from src.strategies.discount import IDiscountStrategy, NoDiscount

class ReportService:
    def __init__(self, repository: IOrderRepository):
        self.repository = repository

    def gerar_relatorio_vendas(self, discount_strategy: IDiscountStrategy = None) -> None:
        if discount_strategy is None:
            discount_strategy = NoDiscount()
            
        orders = self.repository.get_all()
        print("=== RELATORIO DE VENDAS ===")
        tot_g = 0.0
        for r in orders:
            total_final = discount_strategy.apply_discount(r.get_total_base(), r.itens)
            print(f"Pedido #{r.id} Cliente: {r.cliente} Total: R${total_final:.2f} Status: {r.status}")
            tot_g += total_final
        print(f"Total Geral: R${tot_g:.2f}")
        with open('rel_vendas.txt', 'w') as f:
            f.write(f"Total de vendas: {tot_g}")

    def gerar_relatorio_clientes(self) -> None:
        orders = self.repository.get_all()
        print("=== RELATORIO DE CLIENTES ===")
        
        # Agrupa por cliente
        clientes = {}
        for r in orders:
            if r.cliente not in clientes:
                clientes[r.cliente] = {"tp": r.get_tipo(), "tot": 0.0}
            clientes[r.cliente]["tot"] += r.get_total_base()
            
        for cli, data in clientes.items():
            print(f"Cliente: {cli} ({data['tp']}) Total gasto base: R${data['tot']:.2f}")
            
        with open('rel_clientes.txt', 'w') as f:
            for cli, data in clientes.items():
                f.write(f"{cli}, {data['tp']}\n")
