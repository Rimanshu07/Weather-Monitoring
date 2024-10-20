import requests

def fetch_weather_data():
    API_KEY = '8b2c7b20d446e2032869fbacb5c27cac'  # Replace with your OpenWeatherMap API key
    cities = ['Delhi', 'Mumbai', 'Chennai', 'Bangalore', 'Kolkata', 'Hyderabad']
    weather_data = {}

    for city in cities:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
        response = requests.get(url)
        if response.status_code == 200:
            weather_data[city] = response.json()
        else:
            print(f"Error fetching data for {city}: {response.status_code}")
            print(response.json())  # Print the error message from the API

    return weather_data
