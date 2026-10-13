from datetime import date

from config import (
    CUSTOMER_FILE,
    VEHICLE_FILE,
    RENTAL_FILE,
    PAYMENT_FILE,
    MAINTENANCE_FILE
)
from storage import load_data
from utils import format_money, print_table


def dashboard():
    customers = load_data(CUSTOMER_FILE)
    vehicles = load_data(VEHICLE_FILE)
    rentals = load_data(RENTAL_FILE)
    payments = load_data(PAYMENT_FILE)
    maintenance = load_data(MAINTENANCE_FILE)

    paid_revenue = sum(
        float(p["amount"])
        for p in payments
        if p["status"] == "Paid"
    )

    outstanding = sum(
        float(r["final_amount"])
        for r in rentals
        if r["status"] == "Returned"
        and not any(p["rental_id"] == r["id"] for p in payments)
    )

    print("\n========== BUSINESS DASHBOARD ==========")
    print(f"Total customers:       {len(customers)}")
    print(f"Total vehicles:        {len(vehicles)}")
    print(f"Available vehicles:    {sum(v['status'] == 'Available' for v in vehicles)}")
    print(f"Rented vehicles:       {sum(v['status'] == 'Rented' for v in vehicles)}")
    print(f"Vehicles in maintenance: {sum(v['status'] == 'Maintenance' for v in vehicles)}")
    print(f"Active rentals:        {sum(r['status'] == 'Active' for r in rentals)}")
    print(f"Completed rentals:     {sum(r['status'] == 'Returned' for r in rentals)}")
    print(f"Payments received:     {format_money(paid_revenue)}")
    print(f"Outstanding payments:  {format_money(outstanding)}")
    print(f"Open maintenance jobs: {sum(m['status'] == 'Open' for m in maintenance)}")
    print("========================================")


def rental_report():
    rentals = load_data(RENTAL_FILE)
    customers = {
        c["id"]: c["name"]
        for c in load_data(CUSTOMER_FILE)
    }
    vehicles = {
        v["id"]: v["registration"]
        for v in load_data(VEHICLE_FILE)
    }

    rows = []

    for rental in rentals:
        rows.append([
            rental["id"],
            customers.get(rental["customer_id"], "Unknown"),
            vehicles.get(rental["vehicle_id"], "Unknown"),
            rental["start_date"],
            rental["expected_return"],
            rental["actual_return"] or "-",
            rental["status"],
            format_money(
                rental["final_amount"]
                if rental["final_amount"] is not None
                else rental["estimated_amount"]
            )
        ])

    print_table(
        [
            "Rental ID", "Customer", "Vehicle", "Start",
            "Expected", "Actual Return", "Status", "Amount"
        ],
        rows
    )


def monthly_revenue_report():
    payments = load_data(PAYMENT_FILE)
    month = input("Enter month (YYYY-MM): ").strip()

    try:
        date.fromisoformat(month + "-01")
    except ValueError:
        print("Invalid month. Use YYYY-MM.")
        return

    monthly_payments = [
        p for p in payments
        if p["status"] == "Paid"
        and p["paid_at"][:7] == month
    ]

    total = sum(float(p["amount"]) for p in monthly_payments)

    print(f"\nRevenue for {month}: {format_money(total)}")
    print(f"Number of payments: {len(monthly_payments)}")


def report_menu():
    while True:
        print("\n--- Reports ---")
        print("1. Business dashboard")
        print("2. Rental report")
        print("3. Monthly revenue report")
        print("0. Back")

        choice = input("Choose: ").strip()

        if choice == "1":
            dashboard()
        elif choice == "2":
            rental_report()
        elif choice == "3":
            monthly_revenue_report()
        elif choice == "0":
            break
        else:
            print("Invalid choice.")
