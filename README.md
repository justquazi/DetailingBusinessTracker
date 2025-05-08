# DetailingBusinessTracker
a small project I made using python and SQlite3 to track my small detailing business
(Thanks ChatGPT for writing this README as its 4:30 AM and i want to sleep.)

# 🧼 Detailing Business Tracker

A Python + SQLite-based desktop application to track customers, vehicles, service jobs, and purchases for a detailing business. Built with a tabbed Tkinter GUI and local database storage.

---

## 🛠️ Features

- Add, delete, and view:
  - ✅ Customers with contact details
  - 🚗 Vehicles linked to each customer
  - 🧽 Services with hours, price, and date
  - 🛒 Purchases with cost and notes
- Scrollable tables with headers
- Clean, tab-based navigation
- Local data persistence with SQLite (no internet required)

---

## 🚀 Getting Started

### Requirements

- Python 3.10+
- `tkinter` (usually included with Python)
- `tkcalendar`

### Install dependencies

```bash
pip install tkcalendar
```
### Running code

```
python main.py
```

### Project Structure

```
├── main.py              # Launches the app
├── database.py          # Handles all SQLite queries
├── customer_tab.py      # Customer tab class
├── vehicle_tab.py       # Vehicle tab class
├── service_tab.py       # Service tab class
├── purchase_tab.py      # Purchase tab class
├── detailing.db         # SQLite database (auto-created)
└── README.md
```




