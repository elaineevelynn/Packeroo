from packeroo import services

class MockCustomer(services.OrderNotification):
    def notified(self, _type, _order_data):
        if _type == "DONE":
            return("Customer Notified!")

class MockSeller(services.OrderNotification):
    def notified(self, _type, _order_data):
        if _type == "DONE":
            return("Seller Notified!")
                    
class MockPublisher(services.Publisher):
    def __init__(self, _subscriber):
        self.subscriber = _subscriber
    
    def notify(self, _type, _order):
        notify = self.subscriber[0].notified(_type, _order)
        self.subscriber.pop(0)
        return notify

def test_email_sent_to_customer_and_seller_if_order_packed_and_otw():
    # Before test
    order = {
        "customer_name": "Cute Girl",
        "customer_address": "Surabaya",
        "item": "Lego",
        "item_qty": 1
    }

    customer = MockCustomer()
    seller = MockSeller()
    publisher = MockPublisher([customer, seller])

    notification_for_customer = publisher.notify("DONE", order)
    assert notification_for_customer == "Customer Notified!", "Observer1 was not notified correctly"

    notification_for_seller = publisher.notify("DONE", order)
    assert notification_for_seller == "Seller Notified!", "Observer2 was not notified correctly"

