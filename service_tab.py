import database
import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
from datetime import date
 
class ServiceTab:
    def __init__(self, parent):
        self.frame = ttk.Frame(parent)
        self.selected_vehicle_id = None
        self.build_service_tab_ui()
       

    def build_service_tab_ui(self):
        # Form frame
        service_form_frame = ttk.LabelFrame(self.frame, text="Service Form")
        service_form_frame.pack(padx=10, pady=10, fill="x")

        ttk.Label(service_form_frame, text="Vehicle:").grid(row=0, column=0, padx=5, pady=5)
        self.vehicle_var = tk.StringVar()
        self.vehicle_dropdown = ttk.Combobox(service_form_frame, textvariable=self.vehicle_var)
        self.refresh_vehicle_list()
        self.vehicle_dropdown.grid(row=0, column=1, padx=5, pady=5)
        self.vehicle_dropdown.bind("<<ComboboxSelected>>", self.on_vehicle_selection)



        #Service fields
        ttk.Label(service_form_frame, text="Hours:").grid(row=1, column=0, padx=5, pady=5)
        self.hours_entry = ttk.Entry(service_form_frame)
        self.hours_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(service_form_frame, text="Price:").grid(row=2, column=0, padx=5, pady=5)
        self.price_entry = ttk.Entry(service_form_frame)
        self.price_entry.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(service_form_frame, text="Date:").grid(row=3, column=0, padx=5, pady=5)
        self.date_entry = DateEntry(service_form_frame, width=12, background='darkblue', foreground='white', borderwidth=2)
        self.date_entry.set_date(date.today()) #edit this to have settable date
        self.date_entry.grid(row=3, column=1, padx=5, pady=5)

        add_button = ttk.Button(service_form_frame, text="Add Service", command=self.add_service)
        add_button.grid(row=4, columnspan=2, pady=10)

        self.delete_button = ttk.Button(service_form_frame, text="Delete Service", command=self.delete_service)
        self.delete_button.grid(row=5, columnspan=2, pady=10)
        self.delete_button.config(state=tk.DISABLED)

        # Table Frame
        table_frame = ttk.LabelFrame(self.frame, text="Service List")
        table_frame.pack(padx=10, pady=10, fill="both", expand=True)

        self.service_tree = ttk.Treeview(table_frame, columns=("ServiceID","VehicleID","Customer", "Hours", "Price", "Date"), show="headings")
        for col in ("ServiceID","VehicleID", "Customer", "Hours", "Price", "Date"):
            self.service_tree.heading(col, text=col)
        # self.service_tree.pack(fill="both", expand=True)

        # # Add scrollbars
        # vsb = ttk.Scrollbar(table_frame, orient="vertical", command=self.service_tree.yview)
        # vsb.pack(side="right", fill="y")
        # self.service_tree.configure(yscrollcommand=vsb.set)

        tree_frame = ttk.Frame(table_frame)
        tree_frame.pack(fill="both", expand=True)

        self.service_tree = ttk.Treeview(
            tree_frame,
            columns=("ServiceID", "VehicleID", "Customer", "Hours", "Price", "Date"),
            show="headings"
        )
        for col in ("ServiceID", "VehicleID", "Customer", "Hours", "Price", "Date"):
            self.service_tree.heading(col, text=col)

        self.service_tree.grid(row=0, column=0, sticky="nsew")

        vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=self.service_tree.yview)
        vsb.grid(row=0, column=1, sticky="ns")
        self.service_tree.configure(yscrollcommand=vsb.set)

        tree_frame.rowconfigure(0, weight=1)
        tree_frame.columnconfigure(0, weight=1)

        self.service_tree.bind("<<TreeviewSelect>>", self.on_service_selection)
        self.service_tree.column("ServiceID", width=80, anchor="center")
        self.service_tree.column("VehicleID", width=80, anchor="center")
        self.service_tree.column("Customer", width=150)
        self.service_tree.column("Hours", width=60, anchor="center")
        self.service_tree.column("Price", width=80, anchor="center")
        self.service_tree.column("Date", width=120)


        self.refresh_service_list()

    def refresh_vehicle_list(self):
        vehicles = database.getAllVehiclesWithOwners()
        vehicle_names = ["Show All"] + [f"{vehicle[0]} - {vehicle[1]} {vehicle[2]} ({vehicle[4]})" for vehicle in vehicles]
        self.vehicle_dropdown['values'] = vehicle_names
        self.vehicle_map = {f"{vehicle[0]} - {vehicle[1]} {vehicle[2]} ({vehicle[4]})": vehicle[0] for vehicle in vehicles}

    def on_vehicle_selection(self, event):
        selected = self.vehicle_var.get()
        if selected == "Show All":
            self.selected_vehicle_id = None
        else:
            self.selected_vehicle_id = self.vehicle_map.get(selected)
        self.refresh_service_list()

    
    def on_service_selection(self, event):
        selected_item = self.service_tree.selection()
        if selected_item:
            self.delete_button.config(state=tk.NORMAL)
        else:
            self.delete_button.config(state=tk.DISABLED)

    def add_service(self):
        if not self.selected_vehicle_id:
            print("No vehicle selected.")
            return  
        try:
            hours = float(self.hours_entry.get())
            price = float(self.price_entry.get())
        except ValueError:
            print("Invalid hours or price.")
            return
        
        date_str = self.date_entry.get()
        database.addService(self.selected_vehicle_id, hours, price, date_str)   

        self.hours_entry.delete(0, tk.END)
        self.price_entry.delete(0, tk.END)
        self.refresh_service_list()

    def delete_service(self):
        selected_item = self.service_tree.selection()
        if not selected_item:
            return
        service_id = self.service_tree.item(selected_item, "values")[0]
        database.deleteService(service_id)
        self.refresh_service_list()
        self.delete_button.config(state=tk.DISABLED)


    def refresh_service_list(self):
        for row in self.service_tree.get_children():
            self.service_tree.delete(row)

        if self.selected_vehicle_id:
            services = database.getServicesByVehicle(self.selected_vehicle_id)
        else:
            services = database.getAllServices()

        for service in services:
            self.service_tree.insert("", "end", values=service)
