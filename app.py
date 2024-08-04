import streamlit as st
import requests
import pandas as pd

geocoding_api_key = '80843f03ed6b4945a45f1bd8c51e5c2f'
weather_api_key = 'b53305cd6b960c1984aed0acaf76aa2e'

def get_lat_lon(village_name):
    geocoding_url = f'https://api.opencagedata.com/geocode/v1/json?q={village_name}&key={geocoding_api_key}'
    
    try:
        response = requests.get(geocoding_url)
        response.raise_for_status()  # Check for HTTP errors
        data = response.json()
        
        if data['results']:
            latitude = data['results'][0]['geometry']['lat']
            longitude = data['results'][0]['geometry']['lng']
            return latitude, longitude
        else:
            return None, None
    except Exception as e:
        st.error(f"Error fetching geocoding data: {e}")
        return None, None

def get_weather_forecast(latitude, longitude):
    weather_url = f'https://api.openweathermap.org/data/2.5/forecast?lat={latitude}&lon={longitude}&units=metric&cnt=40&appid={weather_api_key}'
    
    try:
        response = requests.get(weather_url)
        response.raise_for_status()  # Check for HTTP errors
        data = response.json()
        
        if data['cod'] == '200':
            forecast = []
            for item in data['list']:
                date_time = item['dt_txt']
                date, time = date_time.split(' ')
                forecast.append({
                    'date': date,
                    'time': time,
                    'temp': item['main']['temp'],
                    'pressure': item['main']['pressure'],
                    'humidity': item['main']['humidity'],
                    'weather': item['weather'][0]['description']
                })
            return forecast
        else:
            st.error(f"Error fetching weather data: {data.get('message', 'Unknown error')}")
            return None
    except Exception as e:
        st.error(f"Error fetching weather data: {e}")
        return None

st.title('Weather Forecast for Village')

village_name = st.text_input('Enter village name')

if st.button('Fetch Weather'):
    if village_name:
        latitude, longitude = get_lat_lon(village_name)
        
        if latitude and longitude:
            st.write(f'Coordinates: Latitude {latitude}, Longitude {longitude}')
            
            forecast = get_weather_forecast(latitude, longitude)
            
            if forecast:
                df = pd.DataFrame(forecast)
                st.write('Weather Forecast:')
                st.dataframe(df)
            else:
                st.write('Weather forecast data not available.')
        else:
            st.write('Village not found.')
    else:
        st.write('Please enter a village name.')
