def check_alerts(weather_data):
    # Example: check for high temperature alerts
    for city, data in weather_data.items():
        if data['main']['temp'] > 35:  # Example threshold
            print(f"Alert: {city} temperature is above 35°C!")
# Add more conditions as needed