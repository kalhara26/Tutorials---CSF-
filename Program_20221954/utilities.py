import random
import datetime
import os

#Generating a random promotion
def generate_random_promotion():
    return random.randint(1, 5)

# Calculating the trip price according to the starting and end cities and the vehicle type the user uses.
def calculate_trip_price(start, end, vehicle_type, price_chart, vehicle_prices):
    try:
        # Retrieve the base price for traveling from the start city to the end city.
        base_price = price_chart[start][end]

        # Get the price multiplier for the specified vehicle type.
        price_multiplier = vehicle_prices.get(vehicle_type)
        if price_multiplier is None:
            raise ValueError(f"Invalid vehicle type '{vehicle_type}'. Available vehicle types: Trishaw, Car, Van.")

        # Calculate the final trip price by multiplying the base price with the vehicle price multiplier.
        return base_price * price_multiplier

    except KeyError as e:
        # Handle the case where the provided city names are not found in the price chart.
        raise ValueError("Invalid city names. Please provide valid city names.")

# Function to reduce the promotion randomly if no promo code is provided by the user.
def reduce_promotion_randomly(promo):
    if promo == 0:
        # 70% chance of reducing the promotion randomly by 1, 2, or 3 KMD.
        promo_reduction = random.randint(1, 3)
        return promo_reduction
    return promo


# Generating the invoice file to display in the command prompt and save as a text file.
def generate_invoice(start, end, amount, promo, random_reduction, final_payment, vehicle_type):
    current_datetime = datetime.datetime.now()
    date = current_datetime.strftime("%Y-%m-%d")
    time = current_datetime.strftime("%H_%M_%S_%f")
    timestamp = f"{date} {time}"

    invoice = (
        f"Date: {date}\nTime: {time}\nStart: {start}\nEnd: {end}\nVehicle: {vehicle_type}\n"
        f"Amount: {amount} KMD\nPromo: {promo} KMD\nRandom Reduction: {random_reduction} KMD\nFinal Payment: {final_payment} KMD"
    )

    desktop_path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
    directory_path = os.path.join(desktop_path, "DropMe_Invoices")
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)

    file_name = os.path.join(directory_path, f"{timestamp}.txt")

    with open(file_name, "w") as file:
        file.write(invoice)

    print("Invoice generated successfully.")
    return file_name

