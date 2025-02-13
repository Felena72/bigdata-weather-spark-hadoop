import pandas as pd
import random
from datetime import datetime, timedelta

# Generate random weather data
def generate_weather_data(rows=1000000):
    start_date = datetime(2020, 1, 1)
    cities = ["New York", "Los Angeles", "Chicago", "Houston", "Phoenix"]
    data = []

    for _ in range(rows):
        date = start_date + timedelta(days=random.randint(0, 365 * 5))
        city = random.choice(cities)
        temperature = round(random.uniform(-20, 40), 1)  # Temperature in Celsius
        humidity = random.randint(10, 100)  # Percentage
        wind_speed = round(random.uniform(0, 30), 1)  # Speed in km/h
        data.append([date.strftime("%Y-%m-%d"), city, temperature, humidity, wind_speed])

    return pd.DataFrame(data, columns=["Date", "City", "Temperature", "Humidity", "WindSpeed"])

# Create dataset
weather_df = generate_weather_data(rows=5000000)
weather_df.to_csv("large_weather.csv", index=False)
print("Generated large_weather.csv with 5,000,000 rows")
