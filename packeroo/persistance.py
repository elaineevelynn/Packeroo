# Database Layer
from abc import ABC, abstractmethod
from kink import inject
from packeroo.dtos import OrderItemsDTO, ReportDTO
import sqlite3
from sqlite3 import *

# Interface untuk DB
class OrderDB:
    @abstractmethod
    # Menampilkan choices of items yang bisa dipilih
    def get_items_data(self):
        pass
    
    # Insert item yang terpilih ke dalam database
    @abstractmethod
    def insert_data(self, _order_data, _order_date):
        pass
    
    # Menampilkan data dari DB berdasarkan date
    @abstractmethod
    def get_reports(self, _order_date):
        pass

# Database
@inject(alias=OrderDB)
class OrderDatabase(OrderDB):
     # Establish a connection to a database and create a cursor for data retrieval
    # Untuk initialize database
    def __init__(self, _db_setting):
        self.conn = self.connection(_db_setting)
        # self.create_table()
        if self.conn is not None:
            self.c = self.conn.cursor()

    # Untuk connect ke db
    def connection(self, db_file):
        self.conn = None
        try:
            self.conn = sqlite3.connect(db_file)
        except Error as e:
            print(e)

        return self.conn
    
    # def create_table(self):
    #     pass

    # Untuk ambil data dari db
    def get_items_data(self):
        items_dtos = []
        query = "SELECT * FROM items"
        self.c.execute(query)

        items_data = self.c.fetchall()
        for id, item in items_data:
            items_dtos.append(OrderItemsDTO(item))

        return items_dtos
        
    # Untuk insert data ke db
    def insert_data(self, _order_data, _order_date):
        self.c.execute("begin")
        item = _order_data['item']
        self.c.execute("""SELECT item_id FROM items WHERE item_name=?""", (item,))
        item_id = self.c.fetchall()[0][0]
        
        
        self.c.execute("INSERT INTO reports VALUES (:no, :customer_name, :customer_address, :item_id, :item_qty, :date)",
                       {'no': None, 
                        'customer_name': _order_data['customer_name'],
                        'customer_address': _order_data['customer_address'],
                        'item_id': item_id, 
                        'item_qty': _order_data['item_qty'], 
                        'date': _order_date
                        })
        self.c.execute("commit")

    # Untuk ambil data dari db berdasarkan date
    def get_reports(self, _order_date):
        reports_dtos_list = []
        self.c.execute("""SELECT customer_name, customer_address, item_id, item_qty FROM reports WHERE DATE=?""", (_order_date,))
        order_reports = self.c.fetchall()

        for order in order_reports:
            customer_name = order[0]
            customer_address = order[1]
            item_id = order[2]
            item_qty = order[3]

            self.c.execute("SELECT item_name FROM items WHERE item_id=?", (item_id,))
            item = self.c.fetchall()[0]


            new_dto = ReportDTO(customer_name, customer_address, item, item_qty)
            reports_dtos_list.append(new_dto)

        return reports_dtos_list

    # Untuk initialize database
    def initialize_database_packeroo(self):
        self.c.execute("begin")
        self.c.execute("""
            CREATE TABLE IF NOT EXISTS reports (
                no INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_name TEXT,
                customer_address TEXT,
                item_id INTEGER,
                item_qty INTEGER,
                date TEXT,
                
                FOREIGN KEY (item_id) REFERENCES items(item_id)
            )
        """)

        self.c.execute("""
            CREATE TABLE IF NOT EXISTS items (
                item_id TEXT PRIMARY KEY,
                item_name TEXT
            )
        """)

        self.c.execute("INSERT OR REPLACE INTO items VALUES (:item_id, :item_name)",
                       {'item_id' : 'I001',
                        'item_name' : 'Lego'
                        })
        
        self.c.execute("INSERT OR REPLACE INTO items VALUES (:item_id, :item_name)",
                       {'item_id' : 'I002',
                        'item_name' : 'Mouse'
                        })
        
        self.c.execute("INSERT OR REPLACE INTO items VALUES (:item_id, :item_name)",
                       {'item_id' : 'I003',
                        'item_name' : 'Pencil'
                        })
        
        self.c.execute("INSERT OR REPLACE INTO items VALUES (:item_id, :item_name)",
                       {'item_id' : 'I004',
                        'item_name' : 'Hat'
                        })        
        
        self.c.execute("INSERT OR REPLACE INTO items VALUES (:item_id, :item_name)",
                       {'item_id' : 'I005',
                        'item_name' : 'Hairpin'
                        })

        self.c.execute("commit")