from asset_management.database import VehicleDatabase
from typing import List, Dict, Tuple, Optional


class AssetReportingHandler:
    """
    Handles generating predefined and custom asset reports from the database.
    """
    @staticmethod
    def get_report_query(report_type: str) -> Optional[str]:
        """
        Returns the SQL query for predefined report types.

        Args:
            report_type (str): The type of report requested.

        Returns:
            Optional[str]: The SQL query string if a valid report type
            is provided, else None.
        """
        report_queries: Dict[str, str] = {
            "All Vehicles": "SELECT * FROM vehicles",
            "Vehicles Due for Service": (
                "SELECT * FROM vehicles WHERE service_date <= "
                "date('now', '+1 month')"
            ),
            "Vehicles with Tax Due": (
                "SELECT * FROM vehicles WHERE tax_due_date <= "
                "date('now', '+1 month')"
            ),
            "Vehicles Older Than 10 Years": (
                "SELECT * FROM vehicles WHERE year <= "
                "strftime('%Y', 'now') - 10"
            ),
            "Diesel Vehicles": (
                "SELECT * FROM vehicles WHERE LOWER(fuel_type) = LOWER("
                "'Diesel')"
            ),
        }
        return report_queries.get(report_type, None)

    @staticmethod
    def fetch_report(db: VehicleDatabase, report_type: str) -> List[Tuple]:
        """
        Fetches report data from the database based on a predefined report
        type.

        Args:
            db (VehicleDatabase): The database instance to query.
            report_type (str): The type of report to generate.

        Returns:
            List[Tuple]: A list of tuples representing the report data.
        """
        query: Optional[str] = AssetReportingHandler.get_report_query(
            report_type
            )
        if query:
            return db.query_vehicles(query)
        return []

    @staticmethod
    def fetch_custom_report(
        db: VehicleDatabase, filters: Dict[str, str]
    ) -> List[Tuple]:
        """
        Generates a custom report based on user-defined filters.

        Args:
            db (VehicleDatabase): The database instance to query.
            filters (Dict[str, str]): A dictionary of field names and their
            corresponding filter values.

        Returns:
            List[Tuple]: A list of tuples representing the filtered
            report data.
        """
        query: str = "SELECT * FROM vehicles WHERE 1=1"
        filter_params: List[str] = []
        filter_values: List[str] = []

        for field, value in filters.items():
            if value:
                filter_field: str = field.lower().replace(" ", "_")
                filter_params.append(f"LOWER({filter_field}) LIKE LOWER(?)")
                filter_values.append(f"%{value}%")

        if filter_params:
            query += " AND " + " AND ".join(filter_params)

        return db.query_vehicles(query, tuple(filter_values))
