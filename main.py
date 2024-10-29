import tkinter as tk
from ui_manager import UIManager
from db_manager import DBManager

def initialize_app():
    """Initialize the main application components."""
    # Initialize the database manager
    db_manager = DBManager()

    # Create the main window for the application
    root = tk.Tk()
    root.title("Fabric Management System")

    # Set window size and make it non-resizable (optional)
    root.geometry("800x600")
    root.resizable(True, True)

    # Initialize the UI manager, passing the root window and database manager
    app = UIManager(root, db_manager)

    # Start the Tkinter main event loop
    root.mainloop()

if __name__ == "__main__":
    initialize_app()
