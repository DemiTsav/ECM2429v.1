from vehicle_management_task.database import VehicleDatabase


def run_sample_tasks(db):
    """
    Perform sample tasks on the VehicleDatabase.

    :param db: An instance of the VehicleDatabase class.
    """
    # Add a vehicle
    db.add_vehicle(
        make="Toyota",
        model="Corolla",
        year=2015,
        vehicle_type="Car",
        fuel_type="Petrol",
        service_date="2024-12-15",
        tax_due_date="2025-01-01",
        tax_status="Current",
    )

    # # Update a vehicle
    # db.update_vehicle(1, service_date="2025-01-10", tax_status="Due")

    # Query all vehicles
    vehicles = db.query_vehicles("SELECT * FROM vehicles")
    print("Vehicle List:")
    for vehicle in vehicles:
        print(vehicle)

    # Delete a vehicle
    db.delete_vehicle(12)
