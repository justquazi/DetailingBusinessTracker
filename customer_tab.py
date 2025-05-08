import tkinter as tk
from tkinter import ttk
import database
class CustomerTab:
    def __init__(self, parent):
        #creating frame for notebook
        self.frame = ttk.Frame(parent)
        self.build_customer_tab_ui()
        self.update_customer_list()


    def build_customer_tab_ui(self):
         # Customer Form
        customer_form_frame = ttk.LabelFrame(self.frame, text="Add Customer")
        customer_form_frame.pack(padx=10, pady=10, fill="x")

        ttk.Label(customer_form_frame, text="Name:").grid(row=0, column=0, padx=5, pady=5)
        self.customer_name_entry = ttk.Entry(customer_form_frame)
        self.customer_name_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(customer_form_frame, text="Contact:").grid(row=1, column=0, padx=5, pady=5)
        self.customer_contact_entry = ttk.Entry(customer_form_frame)
        self.customer_contact_entry.grid(row=1, column=1, padx=5, pady=5)

        add_button = ttk.Button(customer_form_frame, text="Add Customer", command=self.add_customer)
        add_button.grid(row=2, columnspan=2, pady=10)

        self.delete_button = ttk.Button(customer_form_frame, text="Delete Customer", command=self.delete_customer)
        self.delete_button.grid(row=3, columnspan=2, pady=10) 
        self.delete_button.config(state=tk.DISABLED) #begin as disabled
        #this button is self because it needs to be controllable in throughout

        # Customer List
        list_frame = ttk.LabelFrame(self.frame, text="Customer List")
        list_frame.pack(padx=10, pady=10, fill="both", expand=True)

        # self.customer_tree = ttk.Treeview(list_frame, columns=("ID", "Name", "Contact"), show="headings")
        # self.customer_tree.heading("ID", text="ID")
        # self.customer_tree.heading("Name", text="Name")
        # self.customer_tree.heading("Contact", text="Contact")
        # self.customer_tree.heading("Paid", text="Paid")
        # self.customer_tree.pack(fill="both", expand=True)

        # # Add scrollbars
        # vsb = ttk.Scrollbar(list_frame, orient="vertical", command=self.customer_tree.yview)
        # vsb.pack(side="right", fill="y")
        # self.customer_tree.configure(yscrollcommand=vsb.set)
        tree_frame = ttk.Frame(list_frame)
        tree_frame.pack(fill="both", expand=True)

        self.customer_tree = ttk.Treeview(tree_frame, columns=("ID", "Name", "Contact"), show="headings")
        for col in ("ID", "Name", "Contact"):
            self.customer_tree.heading(col, text=col)

        self.customer_tree.grid(row=0, column=0, sticky="nsew")

        vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=self.customer_tree.yview)
        vsb.grid(row=0, column=1, sticky="ns")
        self.customer_tree.configure(yscrollcommand=vsb.set)

        tree_frame.rowconfigure(0, weight=1)
        tree_frame.columnconfigure(0, weight=1)

        self.customer_tree.bind("<<TreeviewSelect>>", self.on_customer_selection)
        self.customer_tree.column("ID", width=80, anchor="center")
        self.customer_tree.column("Name", width=150)
        self.customer_tree.column("Contact", width=150)

    def add_customer(self):
        name = self.customer_name_entry.get()
        contact = self.customer_contact_entry.get()
        # Call the function to add a customer to the database
        # database.addCustomer(name, phone)
        print(f"Added Customer: {name}, Contact: {contact}") # Console log
        if name and contact:
            database.addCustomer(name, contact)
            self.customer_name_entry.delete(0, tk.END) #Clear field
            self.customer_contact_entry.delete(0, tk.END) #Clear field
            self.update_customer_list() # Update the customer list after adding a new customer
            if hasattr(self, 'vehicle_tab'):
                self.vehicle_tab.refresh_customer_list()
                # Refresh the customer list in the vehicle tab if it exists
            
    def delete_customer(self):
        selected_item = self.customer_tree.selection()
        if not selected_item:
           return # No item selected, do nothing
        customer_id = self.customer_tree.item(selected_item, "values")[0]
        database.deleteCustomer(customer_id) # Call the function to delete the customer from the database
        self.update_customer_list()
        self.delete_button.config(state=tk.DISABLED)
        

    def on_customer_selection(self,event):
        selected_item = self.customer_tree.selection()
        if selected_item:
            # Enable the delete button if a customer is selected
            self.delete_button.config(state=tk.NORMAL)
        else:
            # Disable the delete button if no customer is selected
            self.delete_button.config(state=tk.DISABLED)
            
    def update_customer_list(self):
        for row in self.customer_tree.get_children():
            self.customer_tree.delete(row)

        customers = database.getAllCustomers()  # Fetch customers from the database
        for customer in customers:
            self.customer_tree.insert('', tk.END, values = customer)
         
