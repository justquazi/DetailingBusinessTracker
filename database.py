import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'data', 'detailing_software_data.db')


os.makedirs(os.path.join(BASE_DIR, 'data'), exist_ok=True)
# Check if the database file exists, if not create it


conn = sqlite3.connect(DB_PATH)
c = conn.cursor()

def initialize_database():
    # Create tables if they don't exist
    # Customer table
    c.execute('''
              CREATE TABLE IF NOT EXISTS customers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                contact TEXT NOT NULL,
                paid INTEGER DEFAULT 0  -- 0 = not paid, 1 = paid
        )
    ''')

    #Vehicle table
    c.execute('''
              CREATE TABLE IF NOT EXISTS vehicles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_id INTEGER NOT NULL,
                make TEXT NOT NULL,
                model TEXT NOT NULL,
                year INTEGER NOT NULL,
                plate TEXT,
                colour TEXT,
                FOREIGN KEY (customer_id) REFERENCES customers (id)
        )
    ''')
    #Notes
    # Plate is optional, so it can be NULL.
    # The customer_id is a foreign key that references the id in the customers table.


    #Service Table
    c.execute('''
              CREATE TABLE IF NOT EXISTS services (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                vehicle_id INTEGER NOT NULL,
                hours REAL NOT NULL,
                price REAL NOT NULL,
                date TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (vehicle_id) REFERENCES vehicles (id)
        )
    ''')

    #Purchase Table
    c.execute('''
              CREATE TABLE IF NOT EXISTS purchases (
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              item TEXT NOT NULL,
              cost REAL NOT NULL,
              date TEXT DEFAULT CURRENT_TIMESTAMP,
              notes TEXT NOT NULL
        )
    ''')
    conn.commit()

#Customer Functions
def addCustomer(name, contact):
    c.execute('''
              INSERT INTO customers (name, contact)
              VALUES (?, ?)
    ''', (name, contact))
    conn.commit()

def deleteCustomer(customer_id):
    c.execute('''
              DELETE FROM customers WHERE id = ?
    ''', (customer_id,))
    conn.commit()

def getAllCustomers():
    c.execute('''
              SELECT * FROM customers
    ''')
    return c.fetchall()

#Vehicle Functions
def addVehicle(customer_id, make, model, year, colour, plate):
    c.execute('''
              INSERT INTO vehicles (customer_id, make, model, year, colour, plate)
              VALUES (?, ?, ?, ?, ?, ?)
    ''', (customer_id, make, model, year, colour, plate))
    conn.commit()

def getVehiclesByCustomer(customer_id):
    c.execute('''
              SELECT id, year, make, model, colour, plate FROM vehicles WHERE customer_id = ?
    ''', (customer_id,))
    return c.fetchall()

def getAllVehicles():  
    c.execute('''
              SELECT vehicles.id, vehicles.year, vehicles.make, vehicles.model, vehicles.colour, vehicles.plate
              FROM vehicles 
    ''')
    return c.fetchall()

def deleteVehicle(vehicle_id):
    c.execute('''
              DELETE FROM vehicles WHERE id = ?
    ''', (vehicle_id,))
    conn.commit()

#Service Functions
def addService(vehicle_id, hours, price, date):
    c.execute('''
              INSERT INTO services (vehicle_id, hours, price, date)
              VALUES (?, ?, ?, ?)
    ''', (vehicle_id, hours, price, date))
    conn.commit()

def deleteService(service_id):
    c.execute('''
              DELETE FROM services WHERE id = ?
    ''', (service_id,))
    conn.commit()

def getServicesByVehicle(vehicle_id):
    c.execute('''
              SELECT * FROM services WHERE vehicle_id = ?
    ''', (vehicle_id,))
    return c.fetchall()

def getAllServices(): 
    c.execute('''
             SELECT services.id, services.vehicle_id, customers.name, services.hours, services.price, services.date
                FROM services
                JOIN vehicles ON services.vehicle_id = vehicles.id
                JOIN customers ON vehicles.customer_id = customers.id
              ORDER BY services.date DESC
    ''')
    return c.fetchall()

#Purchase Functions
def addPurchase(item, cost, date, notes):
    c.execute('''
              INSERT INTO purchases (item, cost, date, notes)
              VALUES (?, ?, ?, ?)
         
            ''', (item, cost, date, notes))
    conn.commit()

def deletePurchase(purchase_id):
    c.execute('''
              DELETE FROM purchases WHERE id = ?
    ''', (purchase_id,))
    conn.commit()

def getPurchases():
    c.execute('''
              SELECT * FROM purchases
    ''')
    return c.fetchall()

def getTotalPurchases():
    c.execute('''
              SELECT SUM(cost) FROM purchases
    ''')
    return c.fetchone()[0] or 0  # Return 0 if there are no purchases

#helper functions
def getVehicleDropdownData(): # used in service tab
    c.execute('''
              SELECT vehicles.id, vehicles.make, vehicles.model, customers.name
              FROM vehicles
              JOIN customers ON vehicles.customer_id = customers.id
    ''')
    return c.fetchall()

def getAllVehiclesWithOwners():
    c.execute('''
              SELECT vehicles.id, vehicles.make, vehicles.model, vehicles.plate, customers.name
              FROM vehicles
                JOIN customers ON vehicles.customer_id = customers.id
    ''')
    return c.fetchall()



