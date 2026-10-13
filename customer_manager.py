from config import CUSTOMER_FILE, RENTAL_FILE
from storage import load_data, save_data, next_id
from utils import read_text, is_valid_email, print_table


def add_customer():
    customers = load_data(CUSTOMER_FILE)

    print("\n--- Register Customer ---")
    name = read_text("Full name: ")
    phone = read_text("Phone number: ")

    if not phone.isdigit() or not 10 <= len(phone) <= 15:
        print("Enter a valid phone number containing 10 to 15 digits.")
        return

    if any(c["phone"] == phone for c in customers):
        print("A customer with this phone number already exists.")
        return

    email = read_text("Email address: ").lower()

    if not is_valid_email(email):
        print("Enter a valid email address.")
        return

    license_number = read_text("Driving license number: ").upper()

    if any(
        c["license_number"].lower() == license_number.lower()
        for c in customers
    ):
        print("This driving license is already registered.")
        return

    customer = {
        "id": next_id(customers),
        "name": name,
        "phone": phone,
        "email": email,
        "license_number": license_number
    }

    customers.append(customer)
    save_data(CUSTOMER_FILE, customers)

    print(f"Customer registered successfully. ID: {customer['id']}")


def list_customers():
    customers = load_data(CUSTOMER_FILE)

    rows = [
        [
            c["id"],
            c["name"],
            c["phone"],
            c["email"],
            c["license_number"]
        ]
        for c in customers
    ]

    print_table(
        ["ID", "Name", "Phone", "Email", "License"],
        rows
    )


def get_customer(customer_id):
    return next(
        (
            customer
            for customer in load_data(CUSTOMER_FILE)
            if customer["id"] == customer_id
        ),
        None
    )


def customer_menu():
    while True:
        print("\n--- Customer Management ---")
        print("1. Register customer")
        print("2. View customers")
        print("0. Back")

        choice = input("Choose: ").strip()

        if choice == "1":
            add_customer()
        elif choice == "2":
            list_customers()
        elif choice == "0":
            break
        else:
            print("Invalid choice.")
