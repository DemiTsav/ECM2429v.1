import tkinter as tk
from asset_management.database import VehicleDatabase
from asset_management import tasks
from asset_management.frontend.ui_manager import AssetManagementUI


def main():
    root = tk.Tk()
    root.title("Asset Management")
    root.state("zoomed")

    db = VehicleDatabase()
    app = AssetManagementUI(root, db)

    def run_tasks():
        try:
            print("Running sample tasks...")
            tasks.run_sample_tasks(db)
        except Exception as e:
            print(f"Error running sample tasks: {e}")

    run_tasks()

    app.pack(fill="both", expand=True)

    root.protocol("WM_DELETE_WINDOW", lambda: on_close(db, root))

    print("Starting Tkinter main loop...")
    root.mainloop()


def on_close(db, root):
    """
    Handles the closing of the window to ensure the database connection
    is properly closed.
    """
    db.close()
    root.quit()


if __name__ == "__main__":
    main()
