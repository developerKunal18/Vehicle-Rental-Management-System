from config import MAINTENANCE_FILE, VEHICLE_FILE
from storage import load_data, save_data, next_id
from vehicle_manager import get_vehicle, change_vehicle_status
from utils import read_positive_int, read_text, print_table, timestamp


def add_maintenance():
    print("\n--- Add Vehicle Maintenance Record ---")

    vehicle_id = read_positive_int("Vehicle ID: ")
    vehicle = get_vehicle(vehicle_id)

    if not vehicle:
        print("Vehicle not found.")
        return

    if vehicle["status"] == "Rented":
        print("A rented vehicle cannot be marked for maintenance.")
        return

    if vehicle["status"] == "Maintenance":
        print("This vehicle is already under maintenance.")
        return

    description = read_text("Maintenance description: ")
    cost_text = input("Estimated cost (₹, enter 0 if unknown): ").strip()

    try:
        cost = float(cost_text)

        if cost < 0:
            raise ValueError

    except ValueError:
        print("Enter a valid non-negative cost.")
        return

    records = load_data(MAINTENANCE_FILE)

    record = {
        "id": next_id(records),
        "vehicle_id": vehicle_id,
        "description": description,
        "cost": round(cost, 2),
        "status": "Open",
        "created_at": timestamp(),
        "closed_at": None
    }

    records.append(record)
    save_data(MAINTENANCE_FILE, records)
    change_vehicle_status(vehicle_id, "Maintenance")

    print(f"Maintenance record created. ID: {record['id']}")


def close_maintenance():
    print("\n--- Complete Maintenance ---")

    record_id = read_positive_int("Maintenance record ID: ")
    records = load_data(MAINTENANCE_FILE)

    record = next(
        (
            item for item in records
            if item["id"] == record_id and item["status"] == "Open"
        ),
        None
    )

    if not record:
        print("Open maintenance record not found.")
        return

    record["status"] = "Completed"
    record["closed_at"] = timestamp()
    save_data(MAINTENANCE_FILE, records)

    vehicle_id = record["vehicle_id"]
    still_open = any(
        item["vehicle_id"] == vehicle_id and item["status"] == "Open"
        for item in records
    )

    if not still_open:
        change_vehicle_status(vehicle_id, "Available")

    print("Maintenance completed.")


def list_maintenance():
    records = load_data(MAINTENANCE_FILE)
    vehicles = {
        v["id"]: v["registration"]
        for v in load_data(VEHICLE_FILE)
    }

    rows = [
        [
            item["id"],
            vehicles.get(item["vehicle_id"], "Unknown"),
            item["description"],
            f"₹{item['cost']:.2f}",
            item["status"],
            item["created_at"]
        ]
        for item in records
    ]

    print_table(
        [
            "ID", "Registration", "Description",
            "Cost", "Status", "Created"
        ],
        rows
    )


def maintenance_menu():
    while True:
        print("\n--- Maintenance Management ---")
        print("1. Add maintenance record")
        print("2. Complete maintenance")
        print("3. View maintenance records")
        print("0. Back")

        choice = input("Choose: ").strip()

        if choice == "1":
            add_maintenance()
        elif choice == "2":
            close_maintenance()
        elif choice == "3":
            list_maintenance()
        elif choice == "0":
            break
        else:
            print("Invalid choice.")
