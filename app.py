from flask import Flask, jsonify, render_template
import requests
from apscheduler.schedulers.background import BackgroundScheduler
import sqlite3

app = Flask(__name__)

# Configuration
API_KEY = '8b2c7b20d446e2032869fbacb5c27cac'  # Replace with your OpenWeatherMap API key
CITIES = ['Delhi', 'Mumbai', 'Chennai', 'Bangalore', 'Kolkata', 'Hyderabad']
DATABASE = 'weather.db'

# Initialize the database
def init_db():
    with sqlite3.connect(DATABASE) as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS weather (
                id INTEGER PRIMARY KEY,
                city TEXT,
                temp REAL,
                feels_like REAL,
                main TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')

def store_weather_data(city, temp, feels_like, main):
    with sqlite3.connect(DATABASE) as conn:
        conn.execute('INSERT INTO weather (city, temp, feels_like, main) VALUES (?, ?, ?, ?)',
                     (city, temp, feels_like, main))

def get_latest_weather_data():
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.execute('SELECT city, temp, feels_like, main FROM weather ORDER BY timestamp DESC LIMIT 1')
        return cursor.fetchone()

# Fetch weather data from OpenWeatherMap API
def fetch_weather_data():
    for city in CITIES:
        try:
            response = requests.get(f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric')
            data = response.json()
            if response.status_code == 200:
                store_weather_data(city, data['main']['temp'], data['main']['feels_like'], data['weather'][0]['main'])
            else:
                print(f'Error fetching data for {city}: {data}')
        except Exception as e:
            print(f'Error fetching data for {city}: {e}')

# Scheduler to fetch data every 5 minutes
scheduler = BackgroundScheduler()
scheduler.add_job(fetch_weather_data, 'interval', minutes=5)
scheduler.start()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/weather')
def weather_view():
    weather_data = get_latest_weather_data()
    return render_template('weather.html', weather=weather_data)

@app.route('/weather/api', methods=['GET'])
def get_weather():
    latest_weather = get_latest_weather_data()
    return jsonify({
        'city': latest_weather[0],
        'temp': latest_weather[1],
        'feels_like': latest_weather[2],
        'main': latest_weather[3]
    })

if __name__ == '__main__':
    init_db()
    fetch_weather_data()  # Initial fetch
    app.run(debug=True)
