import tkinter as tk
from vehicle_management_task.database import VehicleDatabase
from vehicle_management_task import tasks
from asset_management.frontend.ui_manager import AssetManagementUI
import threading

def main():
    root = tk.Tk()
    root.title("Asset Management")
    root.state("zoomed")  # Open in fullscreen mode
    
    db = VehicleDatabase()
    app = AssetManagementUI(root, db)  # Pass it to the UI


    def run_tasks():
        try:
            print("Running sample tasks...")  # Debug print
            tasks.run_sample_tasks(db)  # Run sample tasks on the database
        except Exception as e:
            print(f"Error running sample tasks: {e}")
    
    # Run the sample tasks in a separate thread
    threading.Thread(target=run_tasks, daemon=True).start()

    # Create the AssetManagementPage and pass the database connection
    app.pack(fill="both", expand=True)  # Ensure the app widget expands with the window size

    # Configure closing behavior for the root window to close the DB connection
    root.protocol("WM_DELETE_WINDOW", lambda: on_close(db, root))

    print("Starting Tkinter main loop...")  # Debug print
    root.mainloop()

def on_close(db, root):
    """
    Handles the closing of the window to ensure the database connection is properly closed.
    """
    db.close()  # Close the database connection
    root.quit()  # Close the tkinter window

if __name__ == "__main__":
    main()
