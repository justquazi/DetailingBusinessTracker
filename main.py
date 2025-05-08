"""
Main entry point for the Detailing Software application.
Initializes the GUI by calling launch_app() from ui.py.
"""
import database
from ui import launch_app

database.initialize_database()  # Initialize the database when the application starts

if __name__ == "__main__":
    launch_app()

