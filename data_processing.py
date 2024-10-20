def process_weather_data(weather_data):
    summary = {}
    for city, data in weather_data.items():
        summary[city] = {
            'date': data['dt'],  # Store Unix timestamp
            'average_temp': data['main']['temp'],
            'max_temp': data['main']['temp_max'],
            'min_temp': data['main']['temp_min'],
            'dominant_condition': data['weather'][0]['main']
        }
    return summary

def calculate_daily_summary(weather_data):
    # Calculate daily aggregates and return as needed
    # This is a placeholder; implement as needed
    return process_weather_data(weather_data)
