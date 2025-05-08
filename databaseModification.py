import sqlite3
import os

# Connect to your database file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'data', 'detailing_software_data.db')


os.makedirs(os.path.join(BASE_DIR, 'data'), exist_ok=True)

conn = sqlite3.connect(DB_PATH)
c = conn.cursor()

# Run the ALTER TABLE command
try:
    c.execute("ALTER TABLE vehicles ADD COLUMN colour TEXT")
    conn.commit()
    print("Column added.")
except sqlite3.OperationalError as e:
    print("Error:", e)

# c.execute("DELETE FROM purchases WHERE date LIKE '____-__-__'")


conn.close()
