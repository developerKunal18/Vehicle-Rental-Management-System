from config import (
    CUSTOMER_FILE,
    VEHICLE_FILE,
    RENTAL_FILE,
    PAYMENT_FILE,
    MAINTENANCE_FILE
)
from storage import ensure_file

from customer_manager import customer_menu
from vehicle_manager import vehicle_menu
from rental_manager import rental_menu
from payment_manager import payment_menu
from maintenance_manager import maintenance_menu
from report_manager import report_menu


def initialize_application():
    for file_path in [
        CUSTOMER_FILE,
        VEHICLE_FILE,
        RENTAL_FILE,
        PAYMENT_FILE,
        MAINTENANCE_FILE
    ]:
        ensure_file(file_path)


def main():
    initialize_application()

    while True:
        print("\n====================================")
        print("     VEHICLE RENTAL MANAGEMENT")
        print("====================================")
        print("1. Customer management")
        print("2. Vehicle management")
        print("3. Rental management")
        print("4. Payment management")
        print("5. Maintenance management")
        print("6. Reports")
        print("0. Exit")

        choice = input("Enter your choice: ").strip()

        try:
            if choice == "1":
                customer_menu()
            elif choice == "2":
                vehicle_menu()
            elif choice == "3":
                rental_menu()
            elif choice == "4":
                payment_menu()
            elif choice == "5":
                maintenance_menu()
            elif choice == "6":
                report_menu()
            elif choice == "0":
                print("Thank you for using Vehicle Rental Management.")
                break
            else:
                print("Invalid choice. Select an option from the menu.")

        except (OSError, ValueError, KeyError) as error:
            print(f"Operation failed: {error}")
            print("Check your input and data files before trying again.")


if __name__ == "__main__":
    main()
