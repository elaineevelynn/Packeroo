# Untuk mengatur logika bisnis dari aplikasi packeroo. 
# Terhubung ke database (line 102)
from abc import abstractmethod, ABC
from typing import List
from kink import inject
from packeroo.persistance import OrderDB
from mock_db import MockDB

@inject
class Service(ABC):
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
class OrderNotification:
    @abstractmethod
    def notified(self, _type, _order_data):
        pass

@inject(alias=OrderNotification)
class Customer(OrderNotification):
    def notified(self, _type, _order_data):
        if _type == "DONE":
            if _order_data != []:
                print()
                print("+"*40)
                print(f"Email sent to {_order_data['customer_name']}.")
                print(f"Order\t\t: {_order_data['item']}.")
                print(f"Quantity\t: {_order_data['item_qty']}.")
                print("+"*40, "\n\n")
            else:
                print("Email not sent")

@inject(alias=OrderNotification)
class Seller(OrderNotification):
    def notified(self, _type, _order_data):
        if _type == "DONE":
            if _order_data != []:
                print("+"*60)
                print(f"Pesanan untuk {_order_data['customer_name']} OTW ke {_order_data['customer_address']} bosq!")
                print("+"*60, '\n\n')



@inject(alias=OrderNotification)
class Packer(OrderNotification):
    def notified(self, _type, _order_data):
        if _type == "NEW ORDER!":
            print("+"*40)
            print("Boengkoes Dong!")
            print("+"*40, '\n\n')

@inject
class Publisher:
    def __init__(self, _subscriber: List[OrderNotification]):
        self.subscriber = _subscriber

    def notify(self, _type, _order_data):
        for i in range(len(self.subscriber)):
            self.subscriber[i].notified(_type, _order_data)


@inject(alias=Service)
class OrderService(Service):    
    # Terhubung ke Database
    def __init__(self, _order_db: OrderDB, _publisher: Publisher):
        self._order_db = _order_db
        self._publisher = _publisher
        self._order = []


    def initialize_new_database(self):
        return self._order_db.initialize_database_packeroo()


    def get_report_from_database_order_by_date(self, _selected_date):
        return self._order_db.get_reports(_selected_date)
    

    def get_items(self):
        return self._order_db.get_items_data()


    def new_order(self, _order_data):
        self._publisher.notify("NEW ORDER!", _order_data)
        self._order.append(_order_data)
        self.list_of_orders()
    

    def list_of_orders(self):
        if len(self._order) > 0:
            print("\n------------ LIST OF ORDERS ------------\n")
            for i in range(len(self._order)):
                print("-"*40)
                print(f"Customer\t: {self._order[i]['customer_name'].capitalize()}")
                print(f"Item\t\t: {self._order[i]['item']}")
                print(f"Quantity\t: {self._order[i]['item_qty']}")
                print(f"Address\t\t: {self._order[i]['customer_address'].capitalize()}")
                print("-"*40)
        else:
            print("No more order yet")


    def finish_order(self, _order_data):
        self._publisher.notify("DONE", _order_data)
        if len(self._order) == 1:
            self._order.pop(0)
        elif self._order != []:
            self._order.pop(0)
        elif self._order == []:
            print("No more order that can be done.\n")

    def order_queue(self):
        if len(self._order) > 0:
            return self._order[0]
        return self._order


    def all_orders_queue(self):
        return self._order     
    

    def insert_data_to_database(self, _order_data, _order_date):
        return self._order_db.insert_data(_order_data, _order_date)

    def __iter__(self):
        return iter(self.order_queue())