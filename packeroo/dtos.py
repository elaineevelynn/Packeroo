# Untuk ambil data dari database 
class OrderItemsDTO:
    def __init__(self, _order_items=None):
        self.order_items = _order_items

class ReportDTO:
    def __init__(self, _customer_name=None, _customer_address=None, _item=None, _item_qty=None):
        self.customer_name = _customer_name
        self.customer_address = _customer_address
        self.item = _item
        self.item_qty = _item_qty
