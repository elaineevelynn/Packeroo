from mock_db import MockDB
from packeroo.services import *
from packeroo.uis import *
from packeroo.persistance import *
from kink import *

def test_singleton_database_layer():
    db = id(di[OrderDB])
    db_used_in_service = id(di[OrderService]._order_db)
    
    assert db == db_used_in_service, "Instances are not the same. Singleton property violated."


def test_singleton_service_layer():
    order_service = id(di[OrderService])
    order_service_in_ui = id(di[PackerooGUI].order_service)

    assert order_service == order_service_in_ui, "Instances are not the same. Singleton property violated."






    