from packeroo.persistance import *
from packeroo.services import *
from kink import di
from sqlite3 import *

def test_database():
    di['_db_setting'] = "packeroo_test_db.db"
    order_service = di[OrderService]
    order_service.initialize_new_database()

    db = OrderDatabase()
    # Perform some operations
    db.c.execute("INSERT OR REPLACE INTO items VALUES (:item_id, :item_name)",
                 {'item_id': 'I006', 'item_name': 'TestItem'})
    db.conn.commit()

    # Close and reopen the connection
    db.conn.close()
    
    db = OrderDatabase()
    # Perform some more operations
    db.c.execute("SELECT item_name FROM items WHERE item_id = :item_id",
                 {'item_id': 'I006'})
    result = db.c.fetchone()

    current = result[0]
    expected = "TestItem"

    # Check that the results are as expected
    assert current == expected, "Database used is not the same!"
    
    db.c.execute("DROP TABLE IF EXISTS items")
    db.conn.commit()

    db.c.execute("DROP TABLE IF EXISTS reports")
    db.conn.commit()

    db.conn.close()