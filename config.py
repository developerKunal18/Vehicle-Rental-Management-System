from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"

CUSTOMER_FILE = DATA_DIR / "customers.json"
VEHICLE_FILE = DATA_DIR / "vehicles.json"
RENTAL_FILE = DATA_DIR / "rentals.json"
PAYMENT_FILE = DATA_DIR / "payments.json"
MAINTENANCE_FILE = DATA_DIR / "maintenance.json"

DAILY_LATE_FEE_MULTIPLIER = 1.5

VEHICLE_TYPES = ["Car", "Bike", "SUV", "Van"]
FUEL_TYPES = ["Petrol", "Diesel", "Electric", "CNG"]
PAYMENT_METHODS = ["Cash", "UPI", "Card", "Bank Transfer"]
