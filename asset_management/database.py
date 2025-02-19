import sqlite3


class VehicleDatabase:
    def __init__(self, db_name="vehicles.db"):
        # If db_name is already a connection, use that (in-memory connection)
        if isinstance(db_name, sqlite3.Connection):
            self.connection = db_name
        else:
            self.db_name = db_name
            self.connection = sqlite3.connect(self.db_name)  # For file-based DB
        
        self.cursor = self.connection.cursor()
        self.initialize_database()

    def initialize_database(self):
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

    def add_vehicle(self, registration, make, model, year, vehicle_type, fuel_type, service_date, tax_due_date, tax_status):
        """
        Add a new vehicle to the database.
        """
        self.cursor.execute('''
            INSERT INTO vehicles (registration, make, model, year, vehicle_type, fuel_type,
                                service_date, tax_due_date, tax_status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (registration, make, model, year, vehicle_type, fuel_type, service_date, tax_due_date, tax_status))

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
    
    def get_all_vehicles(self):
        """Fetch all vehicles from the database."""
        query = "SELECT * FROM vehicles"
        self.cursor.execute(query)
        vehicles = self.cursor.fetchall()  # This fetches all rows from the query
        return vehicles
    
    def update_vehicle(self, vehicle_id, updates):
        # Construct the SQL SET part dynamically
        set_clause = ", ".join([f'"{(field.replace(" ", "_"))}" = ?' for field in updates.keys()])
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
        results = self.cursor.fetchall()
        return results

    def close(self):
        """
        Close the database connection.
        """
        self.connection.close()