# ECM2429
# Asset Management System

This is a Tkinter-based Python application for managing council assets, specifically vehicles. The system allows users to add, update, delete, and search for vehicles within a local SQLite database. The interface is designed to be intuitive and dynamically updates search results based on user input.

## Prerequisites
Ensure you have Python with Tkinter support installed

For Ubuntu/Debian, you may need to install: sudo apt-get install python3-tk

This project requires **Python 3.12**. Ensure you have it installed, as some features, such as the `datetime` module, may behave differently in earlier versions.


## Running the Project

To run the project, navigate to the `ECM2429` directory and execute:

```sh
python main.py
```

## Running Tests with Coverage

To execute the test suite and generate a coverage report, run the following command from the `ECM2429` directory:

```sh
python -m coverage run -m pytest test && python -m coverage report
```

## Running Flake8 for linting and PEP8 compliance
```sh
python -m flake8 .
```

## Documentation

The project's documentation is located at:

```
ECM2429/docs/source/_build/html
```

Open the `index.html` file in a web browser to view the documentation.

## Notes on Python 3.12

- Some deprecated modules and functions have been removed in Python 3.12. If you encounter any issues, verify dependencies and function compatibility.
- E.g. The `datetime` module in Python 3.12 has stricter type handling. Ensure all date values are formatted correctly before passing them to database queries.