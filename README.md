s# Vehicle Rental Management System

## Overview

A command-line application built with Python to manage a vehicle rental business. It stores records in JSON files and supports customer registration, vehicle management, rentals, returns, payments, maintenance, and reports.

## Features

- Register and list customers
- Add vehicles and track availability
- Book rentals with date validation
- Calculate rental and late-return charges
- Return vehicles and update their status
- Record rental payments
- Manage vehicle maintenance
- View business dashboard and rental reports
- Calculate monthly payment revenue
- Validate user input and handle common errors

## Technologies

- Python 3.10 or later
- JSON file storage
- Python standard library

## Project Structure

```text
day355_vehicle_rental/
├── main.py
├── config.py
├── storage.py
├── utils.py
├── customer_manager.py
├── vehicle_manager.py
├── rental_manager.py
├── payment_manager.py
├── maintenance_manager.py
├── report_manager.py
├── requirements.txt
├── .gitignore
├── README.md
└── data/
    ├── customers.json
    ├── vehicles.json
    ├── rentals.json
    ├── payments.json
    └── maintenance.json
```

## Installation

1. Install Python 3.10 or later.
2. Download or clone this project.
3. Open a terminal in the project directory.
4. Optionally create a virtual environment:

   ```bash
   python -m venv .venv
   ```

5. Activate the environment.

   Windows:

   ```bash
   .venv\Scripts\activate
   ```

   macOS/Linux:

   ```bash
   source .venv/bin/activate
   ```

6. Run the application:

   ```bash
   python main.py
   ```

No external Python packages are required.

## How Rental Charges Work

- Rental duration includes both the start date and expected return date.
- The estimated charge is daily rate multiplied by rental days.
- Late days are calculated from the expected return date to the actual return date.
- Each late day costs 1.5 times the daily rental rate.
- The final charge is the base rental charge plus late fees.
- Payment is recorded separately after the vehicle is returned.

Example:

- Daily rate: ₹1,000
- Rental period: 3 days
- Late return: 2 days
- Base charge: ₹3,000
- Late fee: ₹3,000
- Final amount: ₹6,000

## Recommended Testing Workflow

1. Register a customer.
2. Add a vehicle with a daily rental rate.
3. Book the vehicle for a future date range.
4. Check that the vehicle is marked as rented.
5. Return the vehicle and review the final charge.
6. Record payment for the returned rental.
7. Open the dashboard and monthly revenue report.
8. Create a maintenance record for an available vehicle.
9. Complete the maintenance and check vehicle availability.

## Data Storage

The application creates JSON files in the `data` directory if they do not exist. Back up this directory regularly. Do not manually change IDs or delete active rental records.

## Limitations

- This is a local learning project, not a production rental platform.
- JSON storage is not designed for simultaneous users.
- It does not process real payments.
- It does not include authentication or role-based access.
- Date-based billing does not calculate hourly rental periods.
- Customer and driving-license information should not be used with real customer data without appropriate security controls.

## Future Improvements

- Add a graphical interface using Tkinter.
- Add search, filtering, and CSV export.
- Add deposit and partial-payment support.
- Add automated tests with `unittest`.
- Replace JSON storage with SQLite or MySQL.
- Add login and role-based permissions.
