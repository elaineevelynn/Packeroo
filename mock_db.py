from kink import *
from packeroo.persistance import OrderDB
from packeroo.dtos import OrderItemsDTO, ReportDTO


@inject(alias=OrderDB)
class MockDB(OrderDB):
    def __init__(self):
        self.orders = [
            {"customer_name": "Nopal",
             "customer_address": "Kemayoran, Jakarta",
             "item": "Mouse",
             "item_qty": 2,
             "date": "12/17/2023"
            }
        ]

    def get_items_data(self):
        items_dtos = []
        items_data = ["Lego", "Mouse", "Pencil", "Hat", "Hairpin"]

        for item in items_data:
            items_dtos.append(OrderItemsDTO(item))

        return items_dtos
    
    def insert_data(self, _order_data, _order_date):
        _order_data["date"] = _order_date
        self.orders.append(_order_data)
        return "Data is inserted to database!"

    def get_reports(self, _order_date):
        reports_dtos_list = []

        for order in self.orders:
            if order["date"] == _order_date:
                customer_name = order["customer_name"]
                customer_address = order["customer_address"]
                item = order["item"]
                item_qty = order["item_qty"]

                new_dto = ReportDTO(customer_name, customer_address, item, item_qty)
                reports_dtos_list.append(new_dto)

        return reports_dtos_list
    
    def initialize_database_packeroo(self):
        return "Database Packeroo is created!"