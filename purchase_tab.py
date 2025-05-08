import database
import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
from datetime import date

class PurchaseTab:
    def __init__(self, parent):
        self.frame = ttk.Frame(parent)
        self.build_purchase_tab_ui()

    def build_purchase_tab_ui(self):
        #Form Frame
        purchase_form_frame = ttk.LabelFrame(self.frame, text="Purchase Form")
        purchase_form_frame.pack(padx=10, pady=10, fill="x")

        ttk.Label(purchase_form_frame, text="Item:").grid(row=0, column=0, padx=5, pady=5)
        self.item_entry = ttk.Entry(purchase_form_frame)
        self.item_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(purchase_form_frame, text="Cost:").grid(row=1, column=0, padx=5, pady=5)
        self.cost_entry = ttk.Entry(purchase_form_frame)
        self.cost_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(purchase_form_frame, text="Date:").grid(row=2, column=0, padx=5, pady=5)
        self.date_entry = DateEntry(purchase_form_frame, width=12, background='darkblue', foreground='white', borderwidth=2)
        self.date_entry.set_date(date.today())
        self.date_entry.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(purchase_form_frame, text="Notes:").grid(row=3, column=0, padx=5, pady=5)
        self.notes_entry = ttk.Entry(purchase_form_frame)
        self.notes_entry.grid(row=3, column=1, padx=5, pady=5)
        
        ttk.Button(purchase_form_frame, text="Add Purchase", command=self.add_purchase).grid(row=4, columnspan=2, pady=10)
        self.delete_button = ttk.Button(purchase_form_frame, text="Delete Purchase", command=self.delete_purchase)
        self.delete_button.grid(row=5, columnspan=2, pady=10)
        self.delete_button.config(state=tk.DISABLED)

        # Table Frame
        table_frame = ttk.LabelFrame(self.frame, text="Purchase List")
        table_frame.pack(padx=10, pady=10, fill="both", expand=True)

        self.purchase_tree = ttk.Treeview(table_frame, columns=("PurchaseID", "Item", "Cost", "Date", "Notes"), show="headings")
        for col in ("PurchaseID", "Item", "Cost", "Date", "Notes"):
            self.purchase_tree.heading(col, text=col)
        # self.purchase_tree.pack(fill="both", expand=True)

        # # Add scrollbars
        # vsb = ttk.Scrollbar(table_frame, orient="vertical", command=self.purchase_tree.yview)
        # vsb.pack(side="right", fill="y")
        # self.purchase_tree.configure(yscrollcommand=vsb.set)

        tree_frame = ttk.Frame(table_frame)
        tree_frame.pack(fill="both", expand=True)

        self.purchase_tree = ttk.Treeview(
            tree_frame,
            columns=("PurchaseID", "Item", "Cost", "Date", "Notes"),
            show="headings"
        )
        for col in ("PurchaseID", "Item", "Cost", "Date", "Notes"):
            self.purchase_tree.heading(col, text=col)

        self.purchase_tree.grid(row=0, column=0, sticky="nsew")

        vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=self.purchase_tree.yview)
        vsb.grid(row=0, column=1, sticky="ns")
        self.purchase_tree.configure(yscrollcommand=vsb.set)

        tree_frame.rowconfigure(0, weight=1)
        tree_frame.columnconfigure(0, weight=1)

        self.purchase_tree.bind("<<TreeviewSelect>>", self.on_purchase_selection)
        self.purchase_tree.column("PurchaseID", width=80, anchor="center")
        self.purchase_tree.column("Item", width=150)
        self.purchase_tree.column("Cost", width=80, anchor="center")
        self.purchase_tree.column("Date", width=100, anchor="center")
        self.purchase_tree.column("Notes", width=200)


        self.refresh_purchase_list()

    def refresh_purchase_list(self):
        for row in self.purchase_tree.get_children():
            self.purchase_tree.delete(row)

        purchases = database.getPurchases()
        for purchase in purchases:
            self.purchase_tree.insert("", "end", values=purchase)   

    def on_purchase_selection(self, event):
        selected_item = self.purchase_tree.selection()
        if selected_item:
            item = self.purchase_tree.item(selected_item)
            values = item['values']
            self.selected_purchase_id = values[0]
            self.item_entry.delete(0, tk.END)
            self.item_entry.insert(0, values[1])
            self.cost_entry.delete(0, tk.END)
            self.cost_entry.insert(0, values[2])
            self.date_entry.set_date(values[3])
            self.notes_entry.delete(0, tk.END)
            self.notes_entry.insert(0, values[4])
            self.delete_button.config(state=tk.NORMAL)
        else:
            self.delete_button.config(state=tk.DISABLED)
    
    def add_purchase(self):
        
        item = self.item_entry.get()
        cost = self.cost_entry.get()
        date = self.date_entry.get()
        notes = self.notes_entry.get() or "N/A"

        try:
            cost = float(self.cost_entry.get())
        except ValueError:
            print("Invalid cost.")
            return
        
        database.addPurchase(item, cost, date, notes)

        self.item_entry.delete(0, tk.END)
        self.cost_entry.delete(0, tk.END)
        self.notes_entry.delete(0, tk.END)
        self.refresh_purchase_list()

    def delete_purchase(self):
        selected_item = self.purchase_tree.selection()
        if not selected_item:
            return
    
        purchase_id = self.purchase_tree.item(selected_item)['values'][0]
        database.deletePurchase(purchase_id)
        self.refresh_purchase_list()
        self.delete_button.config(state=tk.DISABLED)
    

    
