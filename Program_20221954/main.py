import os
import sys
from price_chart import price_chart
from vehicle_prices import *
from utilities import *

# Display assistance information
def show_help():
    print("Commands:")
    print("dm [start_city] [end_city]                 - Shows the price between two cities and generates an invoice file for the trip.")
    print("dm [start_city] [end_city] /pro[amount]    - Shows the price between two cities after applying a promotional code.")
    print("dm /price                                  - Show the full price plan for the whole countryfor all 3 vhicles")
    print("dm [start_city] [end_city] /c              - Shows the price between two cities and generates an invoice file for \n                                                      the trip using a car.")
    print("dm [start_city] [end_city] /pro[amount] /v - Shows the price between two cities while applying a reduction to the \n                                                      total bill and using a van.")
    print("dm /?                                      - Show how the 'dm' command functions.")

# Set the "DropMe_Invoices" directory up if necessary and locate the desktop location.
def process_command(command_parts):
    start = command_parts[0]
    end = command_parts[1]
    vehicle_type = "Trishaw"  # default vehicle type is the trishaw

    promo = 0
    promo_index = None                                 
    for i, part in enumerate(command_parts):
        if part.startswith("/pro"):
            promo_index = i
            break

    if promo_index is not None:
        promo_code = command_parts[promo_index]
        promo_amount = int(promo_code[4:])

        if promo_amount in [1, 5, 10]:
            promo = {1: 3, 5: 5, 10: 7}[promo_amount]
        else:
            print("Invalid promo code. Available promo codes: /pro1, /pro5, /pro10")
            return

        # Get rid of the coupon from the command_parts list.
        del command_parts[promo_index]

    if "/c" in command_parts:
        vehicle_type = "Car"
    elif "/v" in command_parts:
        vehicle_type = "Van"

    amount = calculate_trip_price(start, end, vehicle_type, price_chart, vehicle_prices)

    random_reduction = 0
    if random.random() < 0.7:  # 70% chance of getting random reduction
        random_reduction = generate_random_promotion()

    final_payment = amount - promo - random_reduction

    file_name = generate_invoice(start, end, amount, promo, random_reduction, final_payment)
    return file_name
# showing the full price for the country
def show_full_price_plan():                                                                    
    print("\n=== Full Price Plan for the Whole Country ===")
    print("Start \\ End | Trishaw | Car | Van")
    print("---------------------------------------")
    for start_city, destinations in price_chart.items():
        row = f"{start_city:11}"
        for end_city, _ in destinations.items():
            trishaw_price = calculate_trip_price(start_city, end_city, "Trishaw", price_chart, vehicle_prices)
            car_price = calculate_trip_price(start_city, end_city, "Car", price_chart, vehicle_prices)
            van_price = calculate_trip_price(start_city, end_city, "Van", price_chart, vehicle_prices)
            row += f" | {trishaw_price:7} | {car_price:3} | {van_price:3}"
        print(row)

while True:
    command = input("Enter a command: ")

    if command.lower() == "exit":
        break

    if command.startswith("dm"):
        command_parts = command.split()[1:]
        if command == "dm /?":
            show_help()
        if command.startswith("dm /price"):
            show_full_price_plan()
        if len(command_parts) >= 2:
            # For consistency with the price_chart keys, capitalize the city names.
            start_city = command_parts[0].capitalize()
            end_city = command_parts[1].capitalize()

            try:
                # Check if the user provided a vehicle type
                vehicle_type = "Trishaw"  # Default vehicle type is Trishaw
                if "/c" in command_parts:
                    vehicle_type = "Car"
                elif "/v" in command_parts:
                    vehicle_type = "Van"

                # Calculate amount, promo, and final_payment
                amount = calculate_trip_price(start_city, end_city, vehicle_type, price_chart, vehicle_prices)
                promo = 0

                promo_index = next((i for i, part in enumerate(command_parts) if part.startswith("/pro")), None)
                if promo_index is not None:
                    promo_code = command_parts[promo_index]
                    promo_amount = int(promo_code[4:])
                    if promo_amount in [1, 5, 10]:
                        promo = {1: 3, 5: 5, 10: 7}[promo_amount]
                        del command_parts[promo_index]

                random_reduction = 0
                if promo == 0:
                    # Apply a fixed random reduction of 5 KMD only if no promo code is provided.
                    random_reduction = 5

                final_payment = amount - promo - random_reduction

                file_name = generate_invoice(start_city, end_city, amount, promo, random_reduction, final_payment, vehicle_type)
                if file_name:
                    print(f"Invoice generated successfully. File saved at: {file_name}")

                    # displaying the invoice details in the command prompt
                    with open(file_name, "r") as file:
                        invoice_contents = file.read()
                        print("\n--- Invoice Details ---")
                        print(invoice_contents)
                else:
                    print("Invalid command. Please provide at least two city names.")
            except ValueError as e:
                print(e)  # Handle invalid city names or vehicle types
        else:
            print("Invalid command. Please try again or enter 'dm /?' for help.")