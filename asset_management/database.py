import sqlite3
from typing import Optional, Dict, List, Tuple


class VehicleDatabase:
    """ Class to interact with the vehicle database. """
    def __init__(self, db_name: str = "vehicles.db"):
        """
        Initialize the VehicleDatabase instance.

        Args:
            db_name (str): The name of the database file. Defaults to
            'vehicles.db'.
        """
        if isinstance(db_name, sqlite3.Connection):
            self.connection = db_name
        else:
            self.db_name = db_name
            self.connection = sqlite3.connect(self.db_name)

        self.cursor = self.connection.cursor()
        self.initialize_database()

    def initialize_database(self) -> None:
        """
        Create the vehicles table if it doesn't exist.
        """
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS vehicles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                registration TEXT,
                make TEXT,
                model TEXT,
                year INTEGER,
                vehicle_type TEXT,
                fuel_type TEXT,
                service_date TEXT,
                tax_due_date TEXT,
                tax_status TEXT
            )
        ''')
        self.connection.commit()

    def add_vehicle(self, registration: str, make: str, model: str, year: int,
                    vehicle_type: str, fuel_type: str, service_date: str,
                    tax_due_date: str, tax_status: str) -> None:
        """
        Add a new vehicle to the database.

        Args:
            registration (str): Vehicle registration.
            make (str): Vehicle make.
            model (str): Vehicle model.
            year (int): Vehicle year.
            vehicle_type (str): Type of the vehicle.
            fuel_type (str): Fuel type of the vehicle.
            service_date (str): Date of last service.
            tax_due_date (str): Date of next tax due.
            tax_status (str): Tax status of the vehicle.
        """
        self.cursor.execute('''
            INSERT INTO vehicles (registration, make, model, year,
                            vehicle_type, fuel_type, service_date,
                            tax_due_date, tax_status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (registration, make, model, year, vehicle_type, fuel_type,
              service_date, tax_due_date, tax_status))
        self.connection.commit()

    def get_vehicle(self, vehicle_id: int) -> Optional[Dict[str, str]]:
        """
        Retrieve a vehicle's details by its ID.

        Args:
            vehicle_id (int): The ID of the vehicle.

        Returns:
            Optional[Dict[str, str]]: A dictionary with vehicle details if
            found, or None if the vehicle is not found.
        """
        self.cursor.execute("SELECT * FROM vehicles WHERE id = ?",
                            (vehicle_id,))
        row = self.cursor.fetchone()
        if row is None:
            return None
        return {
            "id": row[0],
            "Registration": row[1],
            "Make": row[2],
            "Model": row[3],
            "Year": row[4],
            "Vehicle Type": row[5],
            "Fuel Type": row[6],
            "Service Date": row[7],
            "Tax Due Date": row[8],
            "Tax Status": row[9],
        }

    def get_all_vehicles(self) -> List[
        Tuple[int, str, str, str, int, str, str, str, str, str]
    ]:
        """
        Fetch all vehicles from the database.

        Returns:
            List[Tuple[int, str, str, str, int, str, str, str, str, str]]:
            A list of tuples,
            each representing a vehicle with its details.
        """
        query = "SELECT * FROM vehicles"
        self.cursor.execute(query)
        vehicles = self.cursor.fetchall()
        return vehicles

    def update_vehicle(self, vehicle_id: int, updates: Dict[str, str]) -> None:
        """
        Update a vehicle's details in the database.

        Args:
            vehicle_id (int): The ID of the vehicle to update.
            updates (Dict[str, str]): A dictionary with field names and
            updated values.
        """
        set_clause = ", ".join([
            f'"{(field.replace(" ", "_"))}" = ?' for field in updates.keys()
            ])
        query = f"UPDATE vehicles SET {set_clause} WHERE id = ?"

        values = list(updates.values())
        values.append(vehicle_id)

        self.cursor.execute(query, values)
        self.connection.commit()

    def delete_vehicle(self, vehicle_id: int) -> None:
        """
        Delete a vehicle from the database.

        Args:
            vehicle_id (int): The ID of the vehicle to delete.
        """
        self.cursor.execute('''
            DELETE FROM vehicles WHERE id = ?
        ''', (vehicle_id,))
        self.connection.commit()

    def query_vehicles(self, query: str, params: Tuple = ()) -> List[Tuple]:
        """
        Query the database and return results.

        Args:
            query (str): SQL query to execute.
            params (Tuple): Parameters for the query.

        Returns:
            List[Tuple]: List of tuples containing query results.
        """
        self.cursor.execute(query, params)
        return self.cursor.fetchall()

    def close(self) -> None:
        """
        Close the database connection.
        """
        self.connection.close()
