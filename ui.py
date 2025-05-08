import tkinter as tk
from tkinter import ttk
from tabs import CustomerTab, VehicleTab, ServiceTab,PurchaseTab


def launch_app():
    root = tk.Tk()
    root.title("Thornhill Auto Care - Business Management Software")
    root.geometry("800x600")

    notebook = ttk.Notebook(root)

    customer_tab = CustomerTab(notebook)
    vehicle_tab = VehicleTab(notebook)
    service_tab = ServiceTab(notebook)
    purchase_tab = PurchaseTab(notebook)

    #tab linkage
    customer_tab.vehicle_tab = vehicle_tab  # Link vehicle tab to customer tab
    vehicle_tab.customer_tab = customer_tab  # Link customer tab to vehicle tab

    vehicle_tab.service_tab = service_tab  # Link service tab to vehicle tab
    service_tab.vehicle_tab = vehicle_tab  # Link vehicle tab to service tab

    notebook.add(customer_tab.frame, text="Customers")
    notebook.add(vehicle_tab.frame, text="Vehicles")
    notebook.add(service_tab.frame, text="Services")
    notebook.add(purchase_tab.frame, text="Purchases")  # Uncomment when implemented

    #add other tabs when implemented

    notebook.pack(expand=1, fill="both")
    root.mainloop()
    
