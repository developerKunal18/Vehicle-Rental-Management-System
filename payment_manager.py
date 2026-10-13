from config import PAYMENT_FILE, RENTAL_FILE, PAYMENT_METHODS
from storage import load_data, save_data, next_id
from utils import (
    read_positive_int,
    format_money,
    print_table,
    timestamp
)


def record_payment():
    print("\n--- Record Rental Payment ---")

    rental_id = read_positive_int("Rental ID: ")
    rentals = load_data(RENTAL_FILE)

    rental = next(
        (
            r for r in rentals
            if r["id"] == rental_id and r["status"] == "Returned"
        ),
        None
    )

    if not rental:
        print("Returned rental not found.")
        return

    payments = load_data(PAYMENT_FILE)

    existing_payment = next(
        (p for p in payments if p["rental_id"] == rental_id),
        None
    )

    if existing_payment:
        print("A payment has already been recorded for this rental.")
        return

    amount = float(rental["final_amount"])

    print(f"Amount due: {format_money(amount)}")
    print("Payment methods:", ", ".join(PAYMENT_METHODS))

    method = input("Payment method: ").strip().title()

    if method not in PAYMENT_METHODS:
        print("Invalid payment method.")
        return

    reference = input(
        "Transaction/reference number (optional): "
    ).strip()

    payment = {
        "id": next_id(payments),
        "rental_id": rental_id,
        "amount": round(amount, 2),
        "method": method,
        "reference": reference,
        "status": "Paid",
        "paid_at": timestamp()
    }

    payments.append(payment)
    save_data(PAYMENT_FILE, payments)

    print("Payment recorded successfully.")
    print(f"Receipt ID: {payment['id']}")
    print(f"Amount paid: {format_money(amount)}")


def list_payments():
    payments = load_data(PAYMENT_FILE)

    rows = [
        [
            p["id"],
            p["rental_id"],
            format_money(p["amount"]),
            p["method"],
            p["status"],
            p["paid_at"]
        ]
        for p in payments
    ]

    print_table(
        [
            "Payment ID", "Rental ID", "Amount",
            "Method", "Status", "Paid At"
        ],
        rows
    )


def payment_menu():
    while True:
        print("\n--- Payment Management ---")
        print("1. Record payment")
        print("2. View payment history")
        print("0. Back")

        choice = input("Choose: ").strip()

        if choice == "1":
            record_payment()
        elif choice == "2":
            list_payments()
        elif choice == "0":
            break
        else:
            print("Invalid choice.")
