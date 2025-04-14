from kink import di
from packeroo.uis import PackerooGUI
from packeroo.services import OrderService
from mock_db import MockDB
# Import the argparse module for parsing command-line arguments
import argparse

# Check if this script is being run directly (not imported as a module)
if __name__ =='__main__':

    # Create an ArgumentParser object
    parser = argparse.ArgumentParser()

    # Add the -dbinit command-line argument
    parser.add_argument("-dbinit")

    # Add the -db command-line argument
    parser.add_argument("-db")

    # Parse the command-line arguments
    args = parser.parse_args()

    # Get the value of the -dbinit argument
    dbinit = args.dbinit

    # Get the value of the -db argument
    db = args.db

    # If a -db argument was provided, convert it to lowercase
    if db is not None:
        db = db.lower()

    # If a -dbinit argument was provided, convert it to lowercase
    if dbinit is not None:
        dbinit = dbinit.lower()

        # If -dbinit is set to 'false', initialize a new database
        if dbinit == 'false':
            # Set the _db_setting in the dependency injection container to the value of -db
            di['_db_setting'] = db

            # Create an OrderService object
            order_service = di[OrderService]

            # Initialize a new database
            order_service.initialize_new_database()

        # If -dbinit is set to 'true', use a mock database
        elif dbinit == "true":
            # Set the _order_db in the dependency injection container to a MockDB object
            di["_order_db"] = di[MockDB]

    # If no -dbinit argument was provided, set the _db_setting to the value of -db
    else:
        di['_db_setting'] = db

    # Create a PackerooGUI object
    ui = di[PackerooGUI]

    # Start the GUI
    ui.start()

# Example:
# python __main__.py -dbinit true -db my_database_url
# REAL DATABASE: python -m packeroo -dbinit="True"
# MOCK DATABASE: python -m packeroo -dbinit="False" -db="packeroo_db.db"