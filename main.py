import tkinter as tk
from vehicle_management_task.database import VehicleDatabase
from asset_management.asset_management_page import AssetManagementPage


def main():
    root = tk.Tk()
    root.title("Asset Management")

    # Database initialization
    db = VehicleDatabase()

    # Create the main application page
    app = AssetManagementPage(root, db)
    app.pack(fill="both", expand=True)

    # Close database on app exit
    def on_close():
        db.close()
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_close)
    root.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}")
    root.mainloop()


if __name__ == "__main__":
    main()
