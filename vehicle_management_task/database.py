import sqlite3


class VehicleDatabase:
    def __init__(self, db_name="vehicles.db"):
        self.db_name = db_name
        self.connection = sqlite3.connect(self.db_name)
        self.cursor = self.connection.cursor()
        self.initialize_database()

    def initialize_database(self):
        """
        Create the vehicles table if it doesn't exist.
        """
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS vehicles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
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

    def add_vehicle(self, make, model, year, vehicle_type, fuel_type, service_date,
                tax_due_date, tax_status):
        """
        Add a new vehicle to the database.
        """
        self.cursor.execute('''
            INSERT INTO vehicles (make, model, year, vehicle_type, fuel_type,
                            service_date, tax_due_date, tax_status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (make, model, year, vehicle_type, fuel_type, service_date, tax_due_date,
            tax_status))
        self.connection.commit()

    def get_vehicle(self, vehicle_id):
        """
        Retrieve a vehicle's details by its ID.

        :param vehicle_id: ID of the vehicle.
        :return: Dictionary with vehicle details or None if not found.
        """
        self.cursor.execute("SELECT * FROM vehicles WHERE id = ?", (vehicle_id,))
        row = self.cursor.fetchone()
        if row is None:
            return None
        return {
            "id": row[0],
            "Make": row[1],
            "Model": row[2],
            "Year": row[3],
            "Vehicle Type": row[4],
            "Fuel Type": row[5],
            "Service Date": row[6],
            "Tax Due Date": row[7],
            "Tax Status": row[8],
        }
    
    def get_all_vehicles(self):
        """Fetch all vehicles from the database."""
        query = "SELECT * FROM vehicles"
        self.cursor.execute(query)
        vehicles = self.cursor.fetchall()  # This fetches all rows from the query
        return vehicles
    
    def update_vehicle(self, vehicle_id, updates):
        # Construct the SQL SET part dynamically
        set_clause = ", ".join([f'"{field}" = ?' for field in updates.keys()])
        query = f"UPDATE vehicles SET {set_clause} WHERE id = ?"
        
        # Extract the values to update
        values = list(updates.values())
        values.append(vehicle_id)  # Add vehicle_id to the parameters
        
        # Execute the query
        self.cursor.execute(query, values)
        self.connection.commit()

    def delete_vehicle(self, vehicle_id):
        """
        Delete a vehicle from the database.

        :param vehicle_id: ID of the vehicle to delete.
        """
        self.cursor.execute('''
            DELETE FROM vehicles WHERE id = ?
        ''', (vehicle_id,))
        self.connection.commit()

    def query_vehicles(self, query, params=()):
        """
        Query the database and return results.

        :param query: SQL query to execute.
        :param params: Parameters for the query.
        :return: List of tuples containing query results.
        """
        self.cursor.execute(query, params)
        return self.cursor.fetchall()

    def close(self):
        """
        Close the database connection.
        """
        self.connection.close()