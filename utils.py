from datetime import date, datetime
import re


def read_text(prompt, required=True):
    while True:
        value = input(prompt).strip()

        if value or not required:
            return value

        print("This field is required.")


def read_positive_float(prompt):
    while True:
        try:
            value = float(input(prompt).strip())

            if value <= 0:
                print("Enter an amount greater than zero.")
                continue

            return round(value, 2)

        except ValueError:
            print("Please enter a valid number.")


def read_positive_int(prompt):
    while True:
        try:
            value = int(input(prompt).strip())

            if value <= 0:
                print("Enter a number greater than zero.")
                continue

            return value

        except ValueError:
            print("Please enter a valid whole number.")


def read_date(prompt):
    while True:
        value = input(prompt).strip()

        try:
            return date.fromisoformat(value)

        except ValueError:
            print("Use YYYY-MM-DD format, for example 2026-10-20.")


def today_string():
    return date.today().isoformat()


def timestamp():
    return datetime.now().isoformat(timespec="seconds")


def format_money(amount):
    return f"₹{float(amount):,.2f}"


def is_valid_email(email):
    return bool(
        re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email)
    )


def print_table(headers, rows):
    if not rows:
        print("No records found.")
        return

    text_rows = [
        [str(value) for value in row]
        for row in rows
    ]

    widths = [
        max(
            len(str(headers[index])),
            *(len(row[index]) for row in text_rows)
        )
        for index in range(len(headers))
    ]

    line = "-+-".join("-" * width for width in widths)

    print(" | ".join(
        str(headers[index]).ljust(widths[index])
        for index in range(len(headers))
    ))
    print(line)

    for row in text_rows:
        print(" | ".join(
            row[index].ljust(widths[index])
            for index in range(len(headers))
        ))
