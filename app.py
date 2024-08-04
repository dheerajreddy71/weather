import streamlit as st
import requests

def get_lat_lon(village_name):
    geocoding_api_key = '80843f03ed6b4945a45f1bd8c51e5c2f'
    geocoding_url = f'https://api.opencagedata.com/geocode/v1/json?q={village_name}&key={geocoding_api_key}'
    
    response = requests.get(geocoding_url)
    data = response.json()
    
    if data['results']:
        latitude = data['results'][0]['geometry']['lat']
        longitude = data['results'][0]['geometry']['lng']
        return latitude, longitude
    else:
        return None, None

def get_weather_forecast(latitude, longitude):
    api_key = 'b53305cd6b960c1984aed0acaf76aa2e'
    weather_url = f'https://api.openweathermap.org/data/2.5/forecast?lat={latitude}&lon={longitude}&units=metric&cnt=40&appid={api_key}'
    
    response = requests.get(weather_url)
    data = response.json()
    
    if data['cod'] == '200':
        forecast = []
        for item in data['list']:
            forecast.append({
                'date': item['dt_txt'],
                'temp': item['main']['temp'],
                'weather': item['weather'][0]['description']
            })
        return forecast
    else:
        return None

st.title('Weather Forecast for Village')

village_name = st.text_input('Enter village name')

if village_name:
    latitude, longitude = get_lat_lon(village_name)
    
    if latitude and longitude:
        st.write(f'Coordinates: Latitude {latitude}, Longitude {longitude}')
        
        forecast = get_weather_forecast(latitude, longitude)
        
        if forecast:
            st.write('7-day Weather Forecast:')
            for day in forecast:
                st.write(f"Date: {day['date']}, Temperature: {day['temp']}°C, Weather: {day['weather']}")
        else:
            st.write('Weather forecast data not available.')
    else:
        st.write('Village not found.')
