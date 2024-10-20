import sqlite3

def init_db():
    conn = sqlite3.connect('weather_data.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS daily_summaries (
            id INTEGER PRIMARY KEY,
            city TEXT,
            date INTEGER,
            average_temp REAL,
            max_temp REAL,
            min_temp REAL,
            dominant_condition TEXT
        )
    ''')
    conn.commit()
    conn.close()

def store_daily_summary(summary):
    conn = sqlite3.connect('weather_data.db')
    cursor = conn.cursor()
    for city, data in summary.items():
        cursor.execute('''
            INSERT INTO daily_summaries (city, date, average_temp, max_temp, min_temp, dominant_condition)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (city, data['date'], data['average_temp'], data['max_temp'], data['min_temp'], data['dominant_condition']))
    conn.commit()
    conn.close()

def get_latest_weather_data():
    conn = sqlite3.connect('weather_data.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM daily_summaries ORDER BY date DESC')
    data = cursor.fetchall()
    conn.close()
    return data
