from config import (
    VEHICLE_FILE,
    VEHICLE_TYPES,
    FUEL_TYPES,
    RENTAL_FILE,
    MAINTENANCE_FILE
)
from storage import load_data, save_data, next_id
from utils import (
    read_text,
    read_positive_float,
    print_table
)


def add_vehicle():
    vehicles = load_data(VEHICLE_FILE)

    print("\n--- Register Vehicle ---")
    registration = read_text("Registration number: ").upper()

    if any(
        v["registration"].upper() == registration
        for v in vehicles
    ):
        print("This registration number already exists.")
        return

    print("Vehicle types:", ", ".join(VEHICLE_TYPES))
    vehicle_type = read_text("Vehicle type: ").title()

    if vehicle_type not in VEHICLE_TYPES:
        print("Invalid vehicle type.")
        return

    brand = read_text("Brand: ")
    model = read_text("Model: ")
    fuel = read_text(
        "Fuel type (Petrol/Diesel/Electric/CNG): "
    ).title()

    if fuel not in FUEL_TYPES:
        print("Invalid fuel type.")
        return

    daily_rate = read_positive_float("Rental price per day (₹): ")

    vehicle = {
        "id": next_id(vehicles),
        "registration": registration,
        "type": vehicle_type,
        "brand": brand,
        "model": model,
        "fuel": fuel,
        "daily_rate": daily_rate,
        "status": "Available"
    }

    vehicles.append(vehicle)
    save_data(VEHICLE_FILE, vehicles)

    print(f"Vehicle added successfully. ID: {vehicle['id']}")


def list_vehicles():
    vehicles = load_data(VEHICLE_FILE)

    rows = [
        [
            v["id"],
            v["registration"],
            f"{v['brand']} {v['model']}",
            v["type"],
            v["fuel"],
            f"₹{v['daily_rate']:.2f}",
            v["status"]
        ]
        for v in vehicles
    ]

    print_table(
        [
            "ID", "Registration", "Vehicle", "Type",
            "Fuel", "Daily Rate", "Status"
        ],
        rows
    )


def get_vehicle(vehicle_id):
    return next(
        (
            vehicle
            for vehicle in load_data(VEHICLE_FILE)
            if vehicle["id"] == vehicle_id
        ),
        None
    )


def change_vehicle_status(vehicle_id, status):
    vehicles = load_data(VEHICLE_FILE)

    for vehicle in vehicles:
        if vehicle["id"] == vehicle_id:
            vehicle["status"] = status
            save_data(VEHICLE_FILE, vehicles)
            return True

    return False


def vehicle_menu():
    while True:
        print("\n--- Vehicle Management ---")
        print("1. Add vehicle")
        print("2. View all vehicles")
        print("3. View available vehicles")
        print("0. Back")

        choice = input("Choose: ").strip()

        if choice == "1":
            add_vehicle()
        elif choice == "2":
            list_vehicles()
        elif choice == "3":
            vehicles = load_data(VEHICLE_FILE)
            rows = [
                [
                    v["id"],
                    v["registration"],
                    f"{v['brand']} {v['model']}",
                    v["type"],
                    f"₹{v['daily_rate']:.2f}"
                ]
                for v in vehicles
                if v["status"] == "Available"
            ]

            print_table(
                ["ID", "Registration", "Vehicle", "Type", "Daily Rate"],
                rows
            )
        elif choice == "0":
            break
        else:
            print("Invalid choice.")
