from flask import Flask, render_template, request
import requests
import os

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    weather = None
    if request.method == 'POST':
        city = request.form.get('city')
        
        # 🔐 Best practice: Load from environment or fallback to hardcoded
        api_key = os.getenv('OPENWEATHER_API_KEY', 'f3f619aecd9b808fd47fae0d2b718420')

        if api_key and city:
            url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'
            try:
                response = requests.get(url, timeout=5)
                response.raise_for_status()
                data = response.json()

                if data.get('cod') == 200:
                    weather = {
                        'city': data['name'],
                        'temperature': round(data['main']['temp'], 1),
                        'humidity': data['main']['humidity'],
                        'wind_speed': round(data['wind']['speed'], 1),
                        'conditions': data['weather'][0]['description'].title()
                    }
                else:
                    weather = {
                        'city': city.title(),
                        'temperature': 'N/A',
                        'humidity': 'N/A',
                        'wind_speed': 'N/A',
                        'conditions': f"City not found: {data.get('message', '')}"
                    }
            except requests.exceptions.RequestException:
                weather = {
                    'city': city.title(),
                    'temperature': 'N/A',
                    'humidity': 'N/A',
                    'wind_speed': 'N/A',
                    'conditions': "Error fetching weather data. Please try again."
                }

    return render_template('index.html', weather=weather)

if __name__ == '__main__':
    app.run(debug=True)
