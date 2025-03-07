from asset_management.database import VehicleDatabase

db = VehicleDatabase()


def run_sample_tasks(db):
    """
    Perform sample tasks on the VehicleDatabase.

    :param db: An instance of the VehicleDatabase class.
    """
    sample_vehicles = [
        {
            "registration": "ABC123",
            "make": "Toyota",
            "model": "Corolla",
            "year": 2015,
            "vehicle_type": "Car",
            "fuel_type": "Petrol",
            "service_date": "15-12-2024",
            "tax_due_date": "01-01-2025",
            "tax_status": "Tax Paid",
        },
        {
            "registration": "XYZ456",
            "make": "Honda",
            "model": "Civic",
            "year": 2020,
            "vehicle_type": "Sedan",
            "fuel_type": "Diesel",
            "service_date": "01-11-2023",
            "tax_due_date": "01-02-2025",
            "tax_status": "Tax Due",
        },
        {
            "registration": "LMN789",
            "make": "Ford",
            "model": "Focus",
            "year": 2018,
            "vehicle_type": "Hatchback",
            "fuel_type": "Petrol",
            "service_date": "10-08-2024",
            "tax_due_date": "01-03-2025",
            "tax_status": "Tax Paid",
        },
        {
            "registration": "DEF012",
            "make": "Chevrolet",
            "model": "Impala",
            "year": 2021,
            "vehicle_type": "Sedan",
            "fuel_type": "Electric",
            "service_date": "22-07-2024",
            "tax_due_date": "01-04-2025",
            "tax_status": "Tax Due",
        },
        {
            "registration": "GHI345",
            "make": "BMW",
            "model": "X5",
            "year": 2022,
            "vehicle_type": "SUV",
            "fuel_type": "Hybrid",
            "service_date": "05-10-2024",
            "tax_due_date": "01-05-2025",
            "tax_status": "Tax Due",
        },
    ]

    for vehicle in sample_vehicles:
        existing_vehicle = db.query_vehicles(
            "SELECT * FROM vehicles WHERE registration = ?",
            (vehicle["registration"],)
        )
        if not existing_vehicle:
            db.add_vehicle(**vehicle)
            print(f"Added vehicle: {vehicle['registration']}")
        else:
            print(f"Vehicle already exists: {vehicle['registration']}")

    vehicles = db.query_vehicles("SELECT * FROM vehicles")
    print("Vehicle List:")
    for vehicle in vehicles:
        print(vehicle)


run_sample_tasks(db)
