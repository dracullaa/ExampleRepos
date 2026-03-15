from flask import Flask, render_template, request 
import requests  # pyright: ignore[reportMissingModuleSource]
import os 
app = Flask(__name__) 
WEATHER_API_URL = "https://api.open-meteo.com/v1/forecast" 
@app.route('/') 
def index(): 
 return render_template('index.html') 

@app.route('/forecast') 
def get_forecast(): 
    try: 
        latitude = request.args.get('lat', default=55.7558, type=float) 
        longitude = request.args.get('lon', default=37.6173, type=float) 
        
        params = { 
        'latitude': latitude, 
        'longitude': longitude, 
        'daily': 'temperature_2m_max,temperature_2m_min,weathercode', 
        'timezone': 'auto', 
        'forecast_days': 7 
        } 
        
        response = requests.get(WEATHER_API_URL, params=params) 
        response.raise_for_status() 
        
        forecast_data = response.json() 
        daily = forecast_data.get('daily', {}) 
        forecast_days = [] 
        for i in range(min(7, len(daily.get('time', [])))): 
            forecast_days.append({ 
                'date': daily['time'][i], 
                'temp_max': daily['temperature_2m_max'][i], 
                'temp_min': daily['temperature_2m_min'][i], 
                'weathercode': daily['weathercode'][i], 
                'description': get_weather_description(daily['weathercode'][i]) 
                }) 
        
        return render_template('forecast.html', 
            forecast=forecast_days, 
            latitude=latitude, 
            longitude=longitude) 
        
    except Exception as e: 
        return render_template('error.html', error=str(e)), 500
def get_weather_description(code): 
 weather_codes = { 
 0: "Ясно", 
 1: "Преимущественно ясно", 
 2: "Переменная облачность", 
 3: "Пасмурно", 
 45: "Туман", 
 48: "Туман с изморозью", 
 51: "Лежащая морось", 
 53: "Умеренная морось", 
 55: "Сильная морось", 
 56: "Ледяная морось", 
 57: "Сильная ледяная морось", 
 61: "Небольшой дождь", 
 63: "Умеренный дождь", 
 65: "Сильный дождь", 
 66: "Ледяной дождь", 
 67: "Сильный ледяной дождь", 
 71: "Небольшой снег", 
 73: "Умеренный снег", 
 75: "Сильный снег", 
 77: "Снежные зерна", 
 80: "Небольшие ливни", 
 81: "Умеренные ливни", 
 82: "Сильные ливни", 
 85: "Небольшие снегопады", 
 86: "Сильные снегопады", 
 95: "Гроза", 
 96: "Гроза с небольшим градом", 
 99: "Гроза с сильным градом" 
 } 
 return weather_codes.get(code, "Неизвестно") 
if __name__ == '__main__': 
 app.run(debug=True, port=5000)
