from flask import Flask, render_template, request
import requests
import os

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    weather_data = None

    if request.method == 'POST':
        city = request.form.get('city')
        print(f"Form submitted with city: {city}")  # ✅ Debug print

        # Use API key securely or fallback
        api_key = os.getenv('OPENWEATHER_API_KEY', 'f3f619aecd9b808fd47fae0d2b718420')

        if city and api_key:
            url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'
            try:
                response = requests.get(url, timeout=5)
                data = response.json()
                print(data)  # ✅ Debug print full API response

                if data.get('cod') == 200:
                    weather_data = {
                        'city': data['name'],
                        'temperature': round(data['main']['temp'], 1),
                        'humidity': data['main']['humidity'],
                        'wind_speed': round(data['wind']['speed'], 1),
                        'conditions': data['weather'][0]['description'].title()
                    }
                else:
                    weather_data = {
                        'city': city.title(),
                        'temperature': 'N/A',
                        'humidity': 'N/A',
                        'wind_speed': 'N/A',
                        'conditions': f"City not found: {data.get('message', '')}"
                    }
            except requests.RequestException as e:
                print(f"Error: {e}")
                weather_data = {
                    'city': city.title(),
                    'temperature': 'N/A',
                    'humidity': 'N/A',
                    'wind_speed': 'N/A',
                    'conditions': "Error contacting weather API"
                }

    return render_template('index.html', weather_data=weather_data)

if __name__ == '__main__':
    app.run(debug=True)
