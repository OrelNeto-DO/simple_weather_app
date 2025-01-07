from flask import Flask, render_template, request
import requests
import os

app = Flask(__name__)

# OpenWeatherMap API configuration
API_KEY = os.getenv('WEATHER_API_KEY', '40392cb50e8faa1b5dd5822ab9e06913')
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

WINTER_FACTS = [
    "Snow is translucent, not white",
    "All snowflakes have 6 sides",
    "The largest snowflake was 15 inches wide",
    "Snow can fall from a clear sky",
    "About 12% of Earth's land surface is permanently covered in snow and ice"
]

@app.route('/', methods=['GET', 'POST'])
def index():
    weather_data = None
    error = None

    if request.method == 'POST':
        city = request.form.get('city')
        country = request.form.get('country')
        
        if city and country:
            try:
                params = {
                    'q': f"{city},{country}",
                    'appid': API_KEY,
                    'units': 'metric'
                }
                response = requests.get(BASE_URL, params=params)
                response.raise_for_status()
                weather_data = response.json()
            except Exception as e:
                error = "Failed to fetch weather data. Please try again."
    
    return render_template('index.html', 
                         weather=weather_data, 
                         error=error,
                         winter_facts=WINTER_FACTS)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

