import sqlite3
import json
from typing import List, Optional
from src.models.order import Order
from src.models.item import Item
from src.factory.order_factory import OrderFactory
from src.repositories.interfaces import IOrderRepository

class SQLiteOrderRepository(IOrderRepository):
    def __init__(self, db_path: str = 'loja.db'):
        self.db_path = db_path
        self._init_db()

    def _init_db(self) -> None:
        db = sqlite3.connect(self.db_path)
        try:
            c = db.cursor()
            c.execute('''CREATE TABLE IF NOT EXISTS ped (
                id INTEGER PRIMARY KEY, cli TEXT, itens TEXT,
                tot REAL, st TEXT, dt TEXT, tp TEXT)''')
            db.commit()
        finally:
            db.close()

    def save(self, order: Order) -> int:
        db = sqlite3.connect(self.db_path)
        try:
            c = db.cursor()
            itens_str = json.dumps([{"nome": i.nome, "p": i.preco, "q": i.quantidade} for i in order.itens])
            c.execute("INSERT INTO ped (cli, itens, tot, st, dt, tp) VALUES (?, ?, ?, ?, ?, ?)",
                      (order.cliente, itens_str, order.get_total_base(), order.status, order.data_criacao, order.get_tipo()))
            db.commit()
            order.id = c.lastrowid
            assert order.id is not None
            return order.id
        finally:
            db.close()

    def get(self, order_id: int) -> Optional[Order]:
        db = sqlite3.connect(self.db_path)
        try:
            c = db.cursor()
            c.execute("SELECT * FROM ped WHERE id=?", (order_id,))
            r = c.fetchone()
            if not r:
                return None
            
            order = OrderFactory.create_order(tipo=r[6], cliente=r[1])
            order.id = r[0]
            order.status = r[4]
            order.data_criacao = r[5]
            
            itens_data = json.loads(r[2])
            for i_data in itens_data:
                order.add_item(Item(nome=i_data['nome'], preco=i_data['p'], quantidade=i_data['q']))
            
            return order
        finally:
            db.close()

    def get_all(self) -> List[Order]:
        orders = []
        db = sqlite3.connect(self.db_path)
        try:
            c = db.cursor()
            c.execute("SELECT * FROM ped")
            rows = c.fetchall()
            for r in rows:
                order = OrderFactory.create_order(tipo=r[6], cliente=r[1])
                order.id = r[0]
                order.status = r[4]
                order.data_criacao = r[5]
                itens_data = json.loads(r[2])
                for i_data in itens_data:
                    order.add_item(Item(nome=i_data['nome'], preco=i_data['p'], quantidade=i_data['q']))
                orders.append(order)
            return orders
        finally:
            db.close()

    def update_status(self, order_id: int, status: str) -> None:
        db = sqlite3.connect(self.db_path)
        try:
            c = db.cursor()
            c.execute("UPDATE ped SET st=? WHERE id=?", (status, order_id))
            db.commit()
        finally:
            db.close()
