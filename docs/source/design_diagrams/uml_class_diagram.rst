============================
System Class Diagram
============================

Overview
------------
This diagram represents the structure and relationships between different classes in the system.
Developers can use this UML class diagram to understand the key components of the system, 
their attributes, and how they interact.

(Can be pasted into [Mermaid Live Editor](https://mermaid-js.github.io/mermaid-live/) 
  to visualize the class structure.)

Class Diagram
---------------------
Below is the system's UML class diagram written using Mermaid syntax.

.. mermaid::

   classDiagram
       class VehicleDatabase {
           - sqlite3.Connection connection
           - sqlite3.Cursor cursor
           + __init__(db_name: str | sqlite3.Connection)
           + initialize_database() : None
           + add_vehicle(registration: str, make: str, model: str, year: int, vehicle_type: str, fuel_type: str, service_date: str, tax_due_date: str, tax_status: str) : None
           + get_vehicle(vehicle_id: int) : dict | None
           + get_all_vehicles() : list
           + update_vehicle(vehicle_id: int, updates: dict) : None
           + delete_vehicle(vehicle_id: int) : None
           + query_vehicles(query: str, params: tuple) : list
           + close() : None
       }

       class VehicleController {
           - VehicleDatabase db
           - any vehicle_table
           + __init__(db: VehicleDatabase, vehicle_table: any)
           + add_vehicle(entries: dict, tax_status: any, refresh_callback: callable, clear_callback: callable) : None
           + delete_vehicle(vehicle_id: int, refresh_callback: callable, clear_callback: callable) : None
           + update_vehicle(vehicle_id: str, refresh_callback: callable, clear_callback: callable, update_entries: dict) : None
           + perform_search() : list
       }

       class UIComponents {
           + show_status_popup(title: str, message: str) : None
           + display_vehicle_info(vehicle: dict) : None
           + create_button(label: str, command: callable) : any
       }

       class FieldValidations {
           + validations(entries: dict) : list
           + update_validations(entries: dict) : list
       }

       class UIManager {
           + __init__(parent: tk.Tk, controller: VehicleController) 
           + create_widgets() : None
           + show_add_vehicle_form() : None
           + show_update_vehicle_form() : None
           + show_delete_vehicle_prompt() : None
           + show_search_form() : None
           + open_asset_reporting_page(new_window: tk.Toplevel, db: VehicleDatabase) : None
       }

       class AssetReportingPage {
           + __init__(parent: tk.Widget, db: object) : None
           + create_widgets() : None
           + generate_report() : None
           + display_report() : None
           + custom_report() : None
           + create_filter(window: tk.Frame, label_text: str) : tk.Entry
           + generate_custom_report() : None
           + confirm_export_to_csv() : None
           + export_to_csv() : None
       }

       class AssetReportingHandler {
           + fetch_report(db: object, report_type: str) : list
           + fetch_custom_report(db: object, filters: dict) : list
       }

       VehicleController --> VehicleDatabase : "Uses"
       VehicleController --> UIComponents : "Interacts with"
       VehicleController --> FieldValidations : "Validates input with"
       UIManager --> VehicleController : "Manages UI interactions"
       UIManager --> AssetReportingPage : "Navigates to"
       AssetReportingPage --> AssetReportingHandler : "Fetches data from"

