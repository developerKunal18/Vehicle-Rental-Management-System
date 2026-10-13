from datetime import date

from config import (
    RENTAL_FILE,
    VEHICLE_FILE,
    DAILY_LATE_FEE_MULTIPLIER,
    MAINTENANCE_FILE
)
from storage import load_data, save_data, next_id
from customer_manager import get_customer
from vehicle_manager import get_vehicle, change_vehicle_status
from utils import (
    read_positive_int,
    read_date,
    format_money,
    print_table,
    timestamp
)


def book_rental():
    print("\n--- Book Vehicle Rental ---")

    customer_id = read_positive_int("Customer ID: ")
    customer = get_customer(customer_id)

    if not customer:
        print("Customer not found. Register the customer first.")
        return

    vehicle_id = read_positive_int("Vehicle ID: ")
    vehicle = get_vehicle(vehicle_id)

    if not vehicle:
        print("Vehicle not found.")
        return

    if vehicle["status"] != "Available":
        print(f"Vehicle is currently {vehicle['status'].lower()}.")
        return

    start_date = read_date("Rental start date (YYYY-MM-DD): ")
    expected_return = read_date(
        "Expected return date (YYYY-MM-DD): "
    )

    if start_date < date.today():
        print("The rental start date cannot be in the past.")
        return

    if expected_return < start_date:
        print("Return date must be on or after the start date.")
        return

    rental_days = (expected_return - start_date).days + 1
    estimated_amount = rental_days * float(vehicle["daily_rate"])

    rentals = load_data(RENTAL_FILE)

    rental = {
        "id": next_id(rentals),
        "customer_id": customer_id,
        "vehicle_id": vehicle_id,
        "start_date": start_date.isoformat(),
        "expected_return": expected_return.isoformat(),
        "rental_days": rental_days,
        "daily_rate": float(vehicle["daily_rate"]),
        "estimated_amount": round(estimated_amount, 2),
        "actual_return": None,
        "late_days": 0,
        "final_amount": None,
        "status": "Active",
        "created_at": timestamp()
    }

    # Save the rental first; only mark the vehicle rented after saving.
    rentals.append(rental)
    save_data(RENTAL_FILE, rentals)

    try:
        if not change_vehicle_status(vehicle_id, "Rented"):
            rentals.pop()
            save_data(RENTAL_FILE, rentals)
            print("Could not update vehicle status. Booking cancelled.")
            return
    except Exception:
        rentals.pop()
        save_data(RENTAL_FILE, rentals)
        raise

    print(f"Rental booked successfully. Rental ID: {rental['id']}")
    print(f"Rental duration: {rental_days} day(s)")
    print(f"Estimated charge: {format_money(estimated_amount)}")


def list_rentals(status_filter=None):
    rentals = load_data(RENTAL_FILE)
    customers = {
        c["id"]: c["name"]
        for c in load_data("data/customers.json")
    }
    vehicles = {
        v["id"]: f"{v['registration']} - {v['brand']} {v['model']}"
        for v in load_data(VEHICLE_FILE)
    }

    rows = []

    for rental in rentals:
        if status_filter and rental["status"] != status_filter:
            continue

        rows.append([
            rental["id"],
            customers.get(rental["customer_id"], "Unknown"),
            vehicles.get(rental["vehicle_id"], "Unknown"),
            rental["start_date"],
            rental["expected_return"],
            rental["status"],
            (
                format_money(rental["final_amount"])
                if rental["final_amount"] is not None
                else format_money(rental["estimated_amount"])
            )
        ])

    print_table(
        [
            "Rental ID", "Customer", "Vehicle", "Start",
            "Expected Return", "Status", "Amount"
        ],
        rows
    )


def return_vehicle():
    print("\n--- Return Vehicle ---")

    rental_id = read_positive_int("Rental ID: ")
    rentals = load_data(RENTAL_FILE)

    rental = next(
        (
            r for r in rentals
            if r["id"] == rental_id and r["status"] == "Active"
        ),
        None
    )

    if not rental:
        print("Active rental not found.")
        return

    actual_return = read_date("Actual return date (YYYY-MM-DD): ")
    start_date = date.fromisoformat(rental["start_date"])
    expected_return = date.fromisoformat(rental["expected_return"])

    if actual_return < start_date:
        print("Return date cannot be before the rental start date.")
        return

    late_days = max(0, (actual_return - expected_return).days)
    base_amount = float(rental["estimated_amount"])
    late_fee = (
        late_days
        * float(rental["daily_rate"])
        * DAILY_LATE_FEE_MULTIPLIER
    )
    final_amount = round(base_amount + late_fee, 2)

    rental["actual_return"] = actual_return.isoformat()
    rental["late_days"] = late_days
    rental["final_amount"] = final_amount
    rental["status"] = "Returned"
    rental["returned_at"] = timestamp()

    save_data(RENTAL_FILE, rentals)

    active_maintenance = any(
        m["vehicle_id"] == rental["vehicle_id"]
        and m["status"] == "Open"
        for m in load_data(MAINTENANCE_FILE)
    )

    new_status = "Maintenance" if active_maintenance else "Available"
    change_vehicle_status(rental["vehicle_id"], new_status)

    print("\nVehicle returned successfully.")
    print(f"Base rental charge: {format_money(base_amount)}")
    print(f"Late days: {late_days}")
    print(f"Late fee: {format_money(late_fee)}")
    print(f"Total amount due: {format_money(final_amount)}")
    print("Payment status: Pending")


def rental_menu():
    while True:
        print("\n--- Rental Management ---")
        print("1. Book a rental")
        print("2. View all rentals")
        print("3. View active rentals")
        print("4. Return a vehicle")
        print("0. Back")

        choice = input("Choose: ").strip()

        if choice == "1":
            book_rental()
        elif choice == "2":
            list_rentals()
        elif choice == "3":
            list_rentals("Active")
        elif choice == "4":
            return_vehicle()
        elif choice == "0":
            break
        else:
            print("Invalid choice.")
