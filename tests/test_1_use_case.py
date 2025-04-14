from packeroo import services, dtos
from mock_db import MockDB
from abc import abstractmethod
from typing import List
from kink import inject, di

class MockPacker(services.OrderService):
    def __init__(self):
        self.__orders = []
        
    def new_order(self, _order):
        self.__orders.append(_order)
    
    def order_queue(self):
        return self.__orders
    
    def __iter__(self):
        return iter(self.order_queue())
    
class MockService:
    @abstractmethod
    def get_report_from_database_order_by_date(self, _selected_date):
        pass

    @abstractmethod
    def get_items(self):
        pass

    @abstractmethod
    def new_order(self, _order_data):
        pass

    @abstractmethod
    def list_of_orders(self):
        pass

    @abstractmethod
    def finish_order(self, _order_data):
        pass

    @abstractmethod
    def order_queue(self):
        pass

    @abstractmethod
    def all_orders_queue(self):
        pass   

    @abstractmethod
    def insert_data_to_database(self, _order_data , _order_date):
        pass

@inject
class MockPublisher:
    def __init__(self, _subscriber: List[services.OrderNotification]):
        self.subscriber = _subscriber

    def notify(self, _type, _order_data):
        for i in range(len(self.subscriber)):
            self.subscriber[i].notified(_type, _order_data)

@inject(alias=MockService)
class MockOrderService(MockService):
    # Terhubung ke Database
    def __init__(self, _order_db: MockDB, _publisher: MockPublisher):
        self.__order_db = _order_db
        self.__publisher = _publisher
        self.__order = []

    def initialize_new_database(self):
        return self.__order_db.initialize_database_packeroo()


    def get_report_from_database_order_by_date(self, _selected_date):
        return self.__order_db.get_reports(_selected_date)
    

    def get_items(self):
        return self.__order_db.get_items_data()


    def new_order(self, _order_data):
        self.__publisher.notify("NEW ORDER!", _order_data)
        self.__order.append(_order_data)

    def finish_order(self, _order_data):
        self.__publisher.notify("DONE", _order_data)
        if len(self.__order) == 1:
            self.__order.pop(0)
        elif self.__order != []:
            self.__order.pop(0)
        elif self.__order == []:
            print("No more order that can be done.\n")

    def order_queue(self):
        if len(self.__order) > 0:
            return self.__order[0]
        return self.__order

    def all_orders_queue(self):
        return self.__order     
    
    def insert_data_to_database(self, _order_data, _order_date):
        return self.__order_db.insert_data(_order_data, _order_date)

    def __iter__(self):
        return iter(self.order_queue())

def test_should_show_a_new_add_order_in_packer():
    # Before test
    packer = MockPacker()
    order = {
        "customer_name": "Nopal",
        "customer_address": "Kemayoran, Jakarta",
        "item": "Mouse",
        "item_qty": 2
    }
    
    # Test
    packer.new_order(order)

    # Expected result
    current = packer.order_queue()[0]
    expected = order
    
    assert current == expected, "Order was not added to packer queue."

def test_create_new_database():
    db = MockDB()
    publisher = MockPublisher()
    service = MockOrderService(db, publisher)

    current = service.initialize_new_database()
    expected = "Database Packeroo is created!"
    
    assert current == expected, "Database was not created."


def test_get_first_report_from_database_order_by_date():
    db = MockDB()
    publisher = MockPublisher()
    service = MockOrderService(db, publisher)

    result = service.get_report_from_database_order_by_date("12/17/2023")
    current = result[0].customer_name
    expected = "Nopal"

    assert current == expected, "Report was not shown" 


def test_get_items():
    db = MockDB()
    publisher = MockPublisher()
    service = MockOrderService(db, publisher)

    items = service.get_items()
    result = []
    for item in items:
        result.append(item.order_items)
    
    current = result
    expected = ["Lego", "Mouse", "Pencil", "Hat", "Hairpin"]

    assert current == expected, "Items was not shown"

def test_new_order():
    db = MockDB()
    publisher = MockPublisher()
    service = MockOrderService(db, publisher)

    order = {
        "customer_name": "Nopal",
        "customer_address": "Kemayoran, Jakarta",
        "item": "Mouse",
        "item_qty": 2
    }

    service.new_order(order)
    current = service.all_orders_queue()
    expected = [{
        "customer_name": "Nopal",
        "customer_address": "Kemayoran, Jakarta",
        "item": "Mouse",
        "item_qty": 2
    }]

    assert current == expected, "Order was not added to packer queue."

def test_finish_order():
    db = MockDB()
    publisher = MockPublisher()
    service = MockOrderService(db, publisher)

    order = {
        "customer_name": "Nopal",
        "customer_address": "Kemayoran, Jakarta",
        "item": "Mouse",
        "item_qty": 2
    }

    service.new_order(order)
    service.finish_order(order)
    current = service.all_orders_queue()
    expected = []

    assert current == expected, "Order was not finished."

def test_order_queue():
    db = MockDB()
    publisher = MockPublisher()
    service = MockOrderService(db, publisher)

    order1 = {
        "customer_name": "Nopal",
        "customer_address": "Kemayoran, Jakarta",
        "item": "Mouse",
        "item_qty": 2
    }

    order2 = {
        "customer_name": "Cute Girl",
        "customer_address": "Surabaya",
        "item": "Lego",
        "item_qty": 1
    }

    service.new_order(order1)
    service.new_order(order2)
    current = service.order_queue()
    expected = service.all_orders_queue()[0]

    assert current == expected, "Order was not added to packer queue."

def test_insert_data_to_database():
    db = MockDB()
    publisher = MockPublisher()
    service = MockOrderService(db, publisher)

    order = {
        "customer_name": "Nopal",
        "customer_address": "Kemayoran, Jakarta",
        "item": "Mouse",
        "item_qty": 2
    }

    service.new_order(order)
    current = service.insert_data_to_database(order, "12/17/2023")
    expected = "Data is inserted to database!"

    assert current == expected, "Data was not inserted to database."













