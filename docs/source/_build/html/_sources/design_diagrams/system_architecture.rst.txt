.. _system_sequence_diagram:

System Sequence Diagram
========================

Overview
---------

The following sequence diagram illustrates the core functionalities of the Fleet Management System, including:

- Adding a vehicle
- Updating vehicle information
- Deleting a vehicle
- Searching for vehicles
- Generating reports

These interactions involve various components such as `AssetManagementUI`, `VehicleController`, `VehicleDatabase`, `UIComponents`, `FieldValidations`, `ReportGeneration`, and `AssetReportingPage`.

Sequence Diagram
-------------------

This diagram illustrates the interactions between system components during key operations like adding, updating, and deleting vehicles, as well as generating reports.

.. mermaid::

   sequenceDiagram
       participant User
       participant AMUI as AssetManagementUI
       participant VCtrl as VehicleController
       participant VDB as VehicleDatabase
       participant UICM as UIComponents
       participant FV as FieldValidations
       participant RG as ReportGeneration
       participant ARP as AssetReportingPage

       User->>AMUI: Click 'Update'
       AMUI->>AMUI: Check if Row Selected
       AMUI->>User: Prompt to Select Row (if no row selected)
       User->>AMUI: Select Row
       AMUI->>VDB: Retrieve Vehicle Info for Selected Row
       VDB->>VCtrl: Format Vehicle Data
       VCtrl->>AMUI: Display Form with Vehicle Data
       AMUI->>UICM: Create 'Update Vehicle' Button
       User->>AMUI: Input Updates
       AMUI->>VCtrl: Process User Input
       VCtrl->>FV: Validate Fields
       FV->>VCtrl: Return Validation Results
       VCtrl->>VDB: Write Updates to Vehicle Table (if no errors)
       AMUI->>AMUI: Update UI with Updated Info
       User->>AMUI: View Updated Info

       %% Delete Function
       User->>AMUI: Select Row
       AMUI->>AMUI: Check if Row Selected
       AMUI->>User: Prompt to Select Row (if no row selected)
       User->>AMUI: Select Row
       AMUI->>VDB: Retrieve Vehicle Info for Selected Row
       VDB->>AMUI: Display Vehicle Info
       AMUI->>UICM: Create 'Confirm Deletion' and 'Cancel' Buttons
       User->>AMUI: Click 'Cancel'
       AMUI->>AMUI: Abort Action
       User->>AMUI: Click 'Confirm Deletion'
       AMUI->>VDB: Delete Vehicle Entry
       VDB->>VDB: Remove Vehicle Data from Table
       AMUI->>AMUI: Update UI to Reflect Deletion
       User->>AMUI: View Updated UI

       %% Add Vehicle Function
       User->>AMUI: Click 'Add Vehicle'
       AMUI->>AMUI: Display Form for Adding Vehicle
       User->>AMUI: Input Vehicle Info
       User->>AMUI: Click 'Add Vehicle'
       AMUI->>UICM: Create 'Add Vehicle' Button
       AMUI->>VCtrl: Process User Input
       VCtrl->>FV: Validate Fields
       FV->>VCtrl: Return Validation Results
       alt If Valid
           VCtrl->>VDB: Add Vehicle Entry to Database
           VDB->>VDB: Insert Vehicle Data into Table
           AMUI->>AMUI: Update UI with New Vehicle Info
           User->>AMUI: View Added Vehicle Info
       else If Invalid
           UICM->>AMUI: Display Error Popup
           AMUI->>User: Show Error Message
       end

       %% Search Function
       User->>AMUI: Click 'Search Vehicles'
       AMUI->>AMUI: Display Search Form
       User->>AMUI: Input Search Criteria
       User->>AMUI: Click 'Search'
       AMUI->>VCtrl: Process Search Request
       VCtrl->>VDB: Query Database with Search Criteria
       VDB->>AMUI: Return Search Results
       AMUI->>AMUI: Display Search Results
       User->>AMUI: View Search Results

       %% Generate Report
       User->>AMUI: Click 'Generate Report'
       AMUI->>AMUI: Open New Window for Report Options
       AMUI->>User: Display Report Types
       User->>AMUI: Select Report Type
       alt If Custom Report
           AMUI->>AMUI: Display Custom Report Filters
           User->>AMUI: Input Custom Report Filters
           User->>AMUI: Click 'Generate Report'
           AMUI->>RG: Process Filters and Generate Report
           RG->>VDB: Retrieve Vehicle Data Based on Filters
           VDB->>RG: Return Filtered Vehicle Data
           RG->>ARP: Display Custom Report
           User->>ARP: View Custom Report
       else If Predefined Report
           AMUI->>RG: Generate Predefined Report
           RG->>VDB: Retrieve Vehicle Data
           VDB->>RG: Return Vehicle Data
           RG->>ARP: Display Predefined Report
           User->>ARP: View Predefined Report
       end
