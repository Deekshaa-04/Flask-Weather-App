from flask import Flask, render_template, request
import requests
import os

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    weather_data = None
    if request.method == 'POST':
        city = request.form.get('city')

        # Option A (secure): Get from environment
        # api_key = os.getenv('OPENWEATHER_API_KEY')

        # Option B (quick test): Hardcoded
        api_key = 'f3f619aecd9b808fd47fae0d2b718420'

        if api_key and city:
            url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'
            response = requests.get(url)
            data = response.json()

            if data.get('cod') == 200:
                weather_data = {
                    'city': city,
                    'temperature': data['main']['temp'],
                    'humidity': data['main']['humidity'],
                    'wind_speed': data['wind']['speed'],
                    'conditions': data['weather'][0]['description'].title()
                }
            else:
                weather_data = {
                    'city': city,
                    'temperature': 'N/A',
                    'humidity': 'N/A',
                    'wind_speed': 'N/A',
                    'conditions': f"City not found: {data.get('message', '')}"
                }

    return render_template('index.html', weather_data=weather_data)

if __name__ == '__main__':
    app.run(debug=True)

