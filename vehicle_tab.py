import tkinter as tk
from tkinter import ttk
import database

class VehicleTab:
    def __init__(self, parent):
        self.frame = ttk.Frame(parent)
        self.build_vehicle_tab_ui(parent)
        self.selected_customer_id = None

    def build_vehicle_tab_ui(self, parent):
        # Vehicle Form
        vehicle_form_frame = ttk.LabelFrame(self.frame, text="Add Vehicle")
        vehicle_form_frame.pack(padx=10, pady=10, fill="x")

        ttk.Label(vehicle_form_frame, text="Customer Name:").grid(row=0, column=0, padx=5, pady=5)
        self.customer_var = tk.StringVar()
        self.customer_dropdown = ttk.Combobox(vehicle_form_frame, textvariable=self.customer_var)
        self.refresh_customer_list()
        self.customer_dropdown.grid(row=0, column=1, padx=5, pady=5)
        self.customer_dropdown.bind("<<ComboboxSelected>>", self.on_customer_selection)


        #Vehicle fields
        ttk.Label(vehicle_form_frame, text="Make:").grid(row=1, column=0, padx=5, pady=5)
        self.make_vehicle_entry = ttk.Entry(vehicle_form_frame)
        self.make_vehicle_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(vehicle_form_frame, text="Model:").grid(row=2, column=0, padx=5, pady=5)
        self.model_vehicle_entry = ttk.Entry(vehicle_form_frame)
        self.model_vehicle_entry.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(vehicle_form_frame, text="Year:").grid(row=3, column=0, padx=5, pady=5) #This field is optional
        self.year_vehicle_entry = ttk.Entry(vehicle_form_frame)
        self.year_vehicle_entry.grid(row=3, column=1, padx=5, pady=5)

        ttk.Label(vehicle_form_frame, text="Plate:").grid(row=4, column=0, padx=5, pady=5) #This field is optional  
        self.plate_vehicle_entry = ttk.Entry(vehicle_form_frame)
        self.plate_vehicle_entry.grid(row=4, column=1, padx=5, pady=5)

        ttk.Label(vehicle_form_frame, text="Colour:").grid(row=5, column=0, padx=5, pady=5) #This field is optional
        self.colour_vehicle_entry = ttk.Entry(vehicle_form_frame)
        self.colour_vehicle_entry.grid(row=5, column=1, padx=5, pady=5)

        add_button = ttk.Button(vehicle_form_frame, text="Add Vehicle", command=self.add_vehicle)
        add_button.grid(row=7, columnspan=2, pady=10)

        self.delete_button = ttk.Button(vehicle_form_frame, text="Delete Vehicle", command=self.delete_vehicle)
        self.delete_button.grid(row=8, columnspan=2, pady=10)
        self.delete_button.config(state=tk.DISABLED)

        # self.edit_button = ttk.Button(vehicle_form_frame, text="Edit Vehicle", command=self.edit_vehicle)
        # self.edit_button.grid(row=9, columnspan=2, pady=10)
        # self.edit_button.config(state=tk.DISABLED)

        # Vehicle List
        list_frame = ttk.LabelFrame(self.frame, text="Vehicle List")
        list_frame.pack(padx=10, pady=10, fill="both", expand=True) 


        tree_frame = ttk.Frame(list_frame)
        tree_frame.pack(fill="both", expand=True)

        self.vehicle_tree = ttk.Treeview(tree_frame, columns=("ID","Year", "Make", "Model","Colour","Plate"), show="headings")  
        for col in ("ID","Year", "Make", "Model","Colour","Plate"):
            self.vehicle_tree.heading(col, text=col)

        self.vehicle_tree.grid(row=0, column=0, sticky="nsew")

        vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=self.vehicle_tree.yview)
        vsb.grid(row=0, column=1, sticky="ns")
        self.vehicle_tree.configure(yscrollcommand=vsb.set)

        tree_frame.rowconfigure(0, weight=1)
        tree_frame.columnconfigure(0, weight=1)
        # self.vehicle_tree = ttk.Treeview(list_frame, columns=("ID","Year", "Make", "Model","Colour","Plate"), show="headings")  
        # for col in ("ID","Year", "Make", "Model","Colour","Plate"):
        #     self.vehicle_tree.heading(col, text=col)
        # self.vehicle_tree.pack(fill="both", expand=True)

        # # Add scrollbars
        # vsb = ttk.Scrollbar(list_frame, orient="vertical", command=self.vehicle_tree.yview)
        # vsb.pack(side="right", fill="y")
        # self.vehicle_tree.configure(yscrollcommand=vsb.set)

        # hsb = ttk.Scrollbar(list_frame, orient="horizontal", command=self.vehicle_tree.xview)
        # hsb.pack(side="bottom", fill="x")
        # self.vehicle_tree.configure(xscrollcommand=hsb.set)

        self.vehicle_tree.bind("<<TreeviewSelect>>", self.on_vehicle_selection) #binds the select event to the function
        self.vehicle_tree.column("ID", width=80, anchor="center")
        self.vehicle_tree.column("Year", width=80, anchor="center")
        self.vehicle_tree.column("Make", width=150)
        self.vehicle_tree.column("Model", width=150)
        self.vehicle_tree.column("Colour", width=100, anchor="center")
        self.vehicle_tree.column("Plate", width=100, anchor="center")


    def refresh_customer_list(self):
        # Fetch customer data from the database
        customers = database.getAllCustomers()  # Assuming this function returns a list of tuples (ID, Name)
        self.customers = customers # Store the customer data for later use
        self.customer_dropdown['values'] = ['Show All'] + [f"{customer[0]}: {customer[1]}" for customer in customers]  # Assuming customer[0] is ID and customer[1] is Name

    def delete_vehicle(self):
        selected_item = self.vehicle_tree.selection()
        if not selected_item:
           return # No item selected, do nothing
        vehicle_id = self.vehicle_tree.item(selected_item, "values")[0]
        database.deleteVehicle(vehicle_id) # Call the function to delete the customer from the database
        self.update_vehicle_list()
        self.delete_button.config(state=tk.DISABLED)

    def on_customer_selection(self, event):
        selected = self.customer_dropdown.current()
        if selected == 0:  # "Show All" option
            self.selected_customer_id = None
            self.update_vehicle_list(show_all=True)
        else:
            self.selected_customer_id = self.customers[selected - 1][0]
            self.update_vehicle_list(show_all=False)

    def on_vehicle_selection(self, event):
        # This function is called when a vehicle is selected in the treeview
        selected_item = self.vehicle_tree.selection()
        if selected_item:
            vehicle_id = self.vehicle_tree.item(selected_item, "values")[0]
            # Enable the delete button if a customer is selected
            self.delete_button.config(state=tk.NORMAL)
            #self.edit_button.config(state=tk.NORMAL)
        else:
            # Disable the delete button if no customer is selected
            self.delete_button.config(state=tk.DISABLED)
            #self.edit_button.config(state=tk.DISABLED)

    def add_vehicle(self):
        if not self.selected_customer_id:
            print("No customer selected.")
            return
        make = self.make_vehicle_entry.get().strip()
        model = self.model_vehicle_entry.get().strip()
        colour = self.colour_vehicle_entry.get().strip() or "N/A"  # Assuming you have a colour entry field
        year = self.year_vehicle_entry.get().strip() or "N/A"  # Assuming you have a year entry field
        plate = self.plate_vehicle_entry.get().strip() or "N/A"  # Default value if plate is empty

        if make and model:
            database.addVehicle(self.selected_customer_id, make, model,year, colour, plate)
            self.make_vehicle_entry.delete(0, tk.END)
            self.model_vehicle_entry.delete(0, tk.END)
            self.plate_vehicle_entry.delete(0, tk.END)
            self.year_vehicle_entry.delete(0, tk.END)
            self.colour_vehicle_entry.delete(0, tk.END)

            self.update_vehicle_list()

    def update_vehicle_list(self, show_all=False):
        for row in self.vehicle_tree.get_children():
            self.vehicle_tree.delete(row)

        if show_all or not self.selected_customer_id:
            vehicles = database.getAllVehicles()
            for vehicle in vehicles:
                self.vehicle_tree.insert("", "end", values=vehicle)
                # Assuming vehicle is a tuple with the same structure as the columns in the treeview
        else:
            vehicles = database.getVehiclesByCustomer(self.selected_customer_id)  # Fetch vehicles for the selected customer
            for vehicle in vehicles:
                self.vehicle_tree.insert("", "end", values=vehicle)
                # Assuming vehicle is a tuple with the same structure as the columns in the treeview

