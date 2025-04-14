# Untuk menampilkan UI dari aplikasi packeroo
# Terhubung ke services
from kink import inject
from tkinter import *
from tkinter import ttk
from datetime import date
from abc import abstractmethod

from packeroo.services import OrderService

class GUI:
    @abstractmethod
    def start(self):
        pass    

@inject(alias=GUI)
class PackerooGUI(GUI):
    def __init__(self, _order_services: OrderService):
        self.order_service = _order_services
        self.root = Tk()

    def start(self):
        title = Label(self.root, text="Packeroo", font=("Poppins", 14))
        title.grid(row=0, column=0, columnspan=3, sticky='ew')
        self.root_tab()

        self.notebook = ttk.Notebook(self.root)
        self.order_tab = Frame(self.notebook)
        self.packer_tab = Frame(self.notebook)
        self.report_tab = Frame(self.notebook)

        self.notebook.add(self.order_tab, text="Order")
        self.notebook.add(self.packer_tab, text="Packer")
        self.notebook.add(self.report_tab, text="Report")
        self.notebook.grid(row=2, column=0, columnspan=3)
        
        self.order_tab_ui()
        self.packer_tab_ui()
        self.report_tab_ui()

        self.root.update_idletasks()

        self.width = self.root.winfo_reqwidth()
        self.height = self.root.winfo_reqheight()
        self.root.geometry(f"{self.width}x{self.height}")
        self.root.title("Packaroo")

        self.root.mainloop()
        
    def order_tab_ui(self):
        # ##############################
        # ######### ORDER TAB ##########
        # ##############################
        self.customer_name_label = Label(self.order_tab, text="Customer\t\t:", font=("Poppins", 12), width=20, anchor='w')
        self.customer_address_label = Label(self.order_tab, text="Address\t\t:", font=("Poppins", 12), width=20, anchor='w')
        self.item_label = Label(self.order_tab, text="Item\t\t:", font=("Poppins", 12), width=20, anchor='w')
        self.item_qty_label = Label(self.order_tab, text ="Qty\t\t:", font=("Poppins", 12), width=20, anchor='w')
        self.customer_name_label.grid(row=0, column=0)
        self.customer_address_label.grid(row=1, column=0)
        self.item_label.grid(row=2, column=0)
        self.item_qty_label.grid(row=3, column=0)
        
        # table customer name entry
        self.customer_name_entry = Entry(self.order_tab, width=50)
        self.customer_name_entry.grid(row=0, column=1, padx=5, sticky='w')
        
        # table customer adress entry
        self.customer_address_entry = Entry(self.order_tab, width=50)
        self.customer_address_entry.grid(row=1, column=1, padx=5, sticky='w')
        
        #table item id entry
        self.items_name = self.order_service.get_items()
        self.items = [item.order_items for item in self.items_name]
        self.item_option = ttk.Combobox(self.order_tab, state='readonly', values=self.items, width=50)
        self.item_option.grid(row=2, column=1, padx=5, sticky='w')
        
        #table item qty entry
        self.item_qty_entry = ttk.Entry(self.order_tab, width=10)
        self.item_qty_entry.grid(row=3, column=1, padx=5, sticky='w')
        
        # order button
        self.order_button = Button(self.order_tab, text="ORDER", width=10, relief='solid', borderwidth=1, command=self.submit_order)
        self.order_button.grid(row=4, column=2, padx=5, sticky='w')

        self.root.update_idletasks()

        self.width = self.root.winfo_reqwidth()
        self.height = self.root.winfo_reqheight()
        self.root.geometry(f"{self.width}x{self.height}")

        self.root.update()

    def get_date(self):
        today = date.today()
        date_today = today.strftime("%m/%d/%Y")
        return date_today
    
    def root_tab(self):
        date_label = Label(self.root, text=self.get_date(), font=("Poppins", 12))
        date_label.grid(row=1, column=2, sticky='e')

    def packer_tab_ui(self):
        # ##############################
        # ######### PACKER TAB ########
        # ##############################
        self.new_order_packer_label()

        self.root.update_idletasks()

        self.width = self.root.winfo_reqwidth()
        self.height = self.root.winfo_reqheight()
        self.root.geometry(f"{self.width}x{self.height}")

        self.root.update()
    
    def submit_order(self):
        customer_name = self.customer_name_entry.get()
        customer_address = self.customer_address_entry.get()
        item = self.item_option.get()
        item_qty = self.item_qty_entry.get()

        self.order = {
            "customer_name": customer_name,
            "customer_address": customer_address,
            "item": item,
            "item_qty": item_qty
        }
        
        if (self.order['customer_name'] != '') and (self.order['customer_address'] != '') and (self.order['item'] != '') and (self.order['item_qty'] != ''):
            self.order_service.new_order(self.order)
            self.new_order_packer_label()

        self.customer_name_entry.delete(0, 'end')
        self.customer_address_entry.delete(0, 'end')
        self.item_option.set('')
        self.item_qty_entry.delete(0, 'end')

        self.root.update()

    def order_finished(self):
        date = self.get_date()
        order_data = self.order_service.order_queue()
        self.order_service.list_of_orders()
        self.order_service.finish_order(order_data)
        self.new_order_packer_label()
        if order_data != []:
            self.order_service.insert_data_to_database(order_data, date)

        self.order_tab.update()

        self.root.update_idletasks()

        self.width = self.root.winfo_reqwidth()
        self.height = self.root.winfo_reqheight()
        self.root.geometry(f"{self.width}x{self.height}")

        self.root.update()


    def new_order_packer_label(self):
        order = self.order_service.order_queue()
        
        self.create_packer_tab()

        if order != []:
            # nama, alamat, item qty
            self.customer_name_label = Label(self.packer_tab, text=order['customer_name'].capitalize(), font=("Poppins", 12), width = 50, anchor='w')
            self.customer_address_label = Label(self.packer_tab, text=order['customer_address'], font=("Poppins", 12), width = 50, anchor='w')
            self.item_label = Label(self.packer_tab, text=order['item'], font=("Poppins", 12), width = 50, anchor='w')
            self.item_qty_label = Label(self.packer_tab, text=order['item_qty'], font=("Poppins", 12), width= 50, anchor='w')
            self.customer_name_label.grid(row=0, column=1)
            self.customer_address_label.grid(row=1, column=1)
            self.item_label.grid(row=2, column=1)
            self.item_qty_label.grid(row=3, column=1)

        self.root.update_idletasks()

        self.width = self.root.winfo_reqwidth()
        self.height = self.root.winfo_reqheight()
        self.root.geometry(f"{self.width}x{self.height}")

        self.root.update()
    
    def create_packer_tab(self):
        for widgets in self.packer_tab.winfo_children():
            widgets.destroy()
        
        self.customer_name_label = Label(self.packer_tab, text="Customer\t\t:", font=("Poppins", 12), width=20, anchor='w')
        self.customer_address_label = Label(self.packer_tab, text="Address\t\t:", font=("Poppins", 12), width=20, anchor='w')
        self.item_label = Label(self.packer_tab, text="Item\t\t:", font=("Poppins", 12), width=20, anchor='w')
        self.item_qty_label = Label(self.packer_tab, text ="Qty\t\t:", font=("Poppins", 12), width=20, anchor='w')
        self.customer_name_label.grid(row=0, column=0)
        self.customer_address_label.grid(row=1, column=0)
        self.item_label.grid(row=2, column=0)
        self.item_qty_label.grid(row=3, column=0)

        done_button = Button(self.packer_tab, text="DONE", width=10, relief='solid', borderwidth=1, command=self.order_finished)
        done_button.grid(row=4, column=1, sticky='w', pady=10)

        self.root.update_idletasks()

        self.width = self.root.winfo_reqwidth()
        self.height = self.root.winfo_reqheight()
        self.root.geometry(f"{self.width}x{self.height}")

    def report_tab_ui(self):
        # ##############################
        # ######### REPORT TAB #########
        # ##############################
        self.show_today_report()

        date_entry = Entry(self.report_tab, font=("Poppins", 12), width=10)
        date_entry.grid(row=0, column=0, sticky='ew')

        search_button = Button(self.report_tab, text="Search", command=lambda: self.get_report_by_date(date_entry))
        search_button.grid(row=0, column=1, sticky='w')

        name_label = Label(self.report_tab, text="Name", font=("Poppins", 12), width=20, anchor='w')
        name_label.grid(row=1, column=0, padx=5, pady=10)

        item_label = Label(self.report_tab, text="Item", font=("Poppins", 12), width=20, anchor='w')
        item_label.grid(row=1, column=1, padx=5, pady=10)

        item_qty_label = Label(self.report_tab, text="Qty", font=("Poppins", 12), width=10, anchor='w')
        item_qty_label.grid(row=1, column=2, padx=5, pady=10)

        self.root.update_idletasks()

        self.width = self.root.winfo_reqwidth()
        self.height = self.root.winfo_reqheight()
        self.root.geometry(f"{self.width}x{self.height}")

        self.root.update()

    def display_report(self, _customer_name, _item, _item_qty):
        name_label = Label(self.report_tab, text=_customer_name.capitalize(), font=("Poppins", 12), width=20, anchor='w')
        item_label = Label(self.report_tab, text=_item, font=("Poppins", 12), width=20, anchor='w')
        item_qty_label = Label(self.report_tab, text=_item_qty, font=("Poppins", 12), width=10, anchor='w')
        name_label.grid(row=self.row_increment, column=0, padx=5)
        item_label.grid(row=self.row_increment, column=1, padx=5)
        item_qty_label.grid(row=self.row_increment, column=2, padx=5)
        self.row_increment += 1   

        self.root.update_idletasks()

        self.width = self.root.winfo_reqwidth()
        self.height = self.root.winfo_reqheight()
        self.root.geometry(f"{self.width}x{self.height}")

    def show_today_report(self):
        date = self.get_date()
        self.report = self.order_service.get_report_from_database_order_by_date(date)
        
        self.orders_report = list()

        for order_data in self.report:
            if order_data.customer_name != None:
                self.orders_report.append([order_data.customer_name, order_data.item, order_data.item_qty])

        self.row_increment = 2
        for order in self.orders_report:
            self.display_report(order[0], order[1], order[2])

        self.report_tab.update()

        self.root.update_idletasks()

        self.width = self.root.winfo_reqwidth()
        self.height = self.root.winfo_reqheight()
        self.root.geometry(f"{self.width}x{self.height}")

        self.root.update()


    def recreate_report_tab(self):
        for widgets in self.report_tab.winfo_children():
            widgets.destroy()

        date_entry = Entry(self.report_tab, font=("Poppins", 12), width=10)
        date_entry.grid(row=0, column=0, sticky='ew')

        search_button = Button(self.report_tab, text="Search", command=lambda: self.get_report_by_date(date_entry))
        search_button.grid(row=0, column=1, sticky='w')

        name_label = Label(self.report_tab, text="Name", font=("Poppins", 12), width=20, anchor='w')
        name_label.grid(row=1, column=0, padx=5, pady=10)

        item_label = Label(self.report_tab, text="Item", font=("Poppins", 12), width=20, anchor='w')
        item_label.grid(row=1, column=1, padx=5, pady=10)

        item_qty_label = Label(self.report_tab, text="Qty", font=("Poppins", 12), width=10, anchor='w')
        item_qty_label.grid(row=1, column=2, padx=5, pady=10)

        self.root.update_idletasks()

        self.width = self.root.winfo_reqwidth()
        self.height = self.root.winfo_reqheight()
        self.root.geometry(f"{self.width}x{self.height}")
   

    def get_report_by_date(self, date_entry):
        print("#######################\nNew Report\n#######################")
        date = date_entry.get()
        self.recreate_report_tab()
        self.report = self.order_service.get_report_from_database_order_by_date(date)
        
        if self.report != [] and self.report is not None:
            self.orders_report = list()

            for order_data in self.report:
                if order_data.customer_name != None:
                    self.orders_report.append([order_data.customer_name, order_data.item, order_data.item_qty])

            self.row_increment = 2
            if self.orders_report is not None:
                for order in self.orders_report:
                    self.display_report(order[0], order[1], order[2])

            self.report_tab.update()
            self.root.update()
        
        else:
            data_unavailable = Label(self.report_tab, text="Data is unavailable", font=("Poppins", 12), width=20, anchor='w', fg='red')
            data_unavailable.grid(row=self.row_increment, column=0, pady=10)

            
        self.report_tab.update()

        self.root.update_idletasks()

        self.width = self.root.winfo_reqwidth()
        self.height = self.root.winfo_reqheight()
        self.root.geometry(f"{self.width}x{self.height}")

        self.root.update()
















        