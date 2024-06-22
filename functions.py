import requests
import pandas as pd
import json
import os
from datetime import datetime, timedelta


def create_default_cities_file():
    # Data to be written to the JSON file
    default_cities_data = [
        ["London", "GB"],
        ["New York", "US"],
        ["Tokyo", "JP"],
        ["Sydney", "AU"],
        ["Paris", "FR"]
    ]

    # Specify the filename
    filename = os.getenv('DEFAULT_CITIES_FILE')
    print (os.getenv('DEFAULT_CITIES_FILE'))

    # Check if the file already exists
    if not os.path.exists(filename):
        # Writing to json file
        with open(filename, 'w') as json_file:
            json.dump(default_cities_data, json_file, indent=4)
        print(f"Data has been written to {filename}")
    else:
        print(f"{filename} already exists. No action taken.")

# Function to load default cities from JSON file
def load_default_cities(file_path):
    try:
        with open(file_path, 'r') as json_file:
            default_cities = json.load(json_file)
        return default_cities
    except FileNotFoundError:
        print(f"Default cities file '{file_path}' not found.")
        return []

# Function to save the default cities list to JSON file
def save_default_cities(default_cities, file_path):
    try:
        with open(file_path, 'w') as json_file:
            json.dump(default_cities, json_file, indent=4)
        print(f"Default cities list updated and saved to '{file_path}'")
    except Exception as e:
        print(f"Failed to save default cities list: {e}")

# Function to get weather data from OpenWeatherMap API and return DataFrame
def get_weather(city_name, api_key, country=None):
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        'q': f"{city_name},{country}" if country else city_name,
        'appid': api_key,
        'units': 'metric'
    }
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        weather_data = response.json()
        city = weather_data['name'].title()
        country = weather_data['sys']['country'].upper()
        temperature = weather_data['main']['temp']
        humidity = weather_data['main']['humidity']
        weather_conditions = weather_data['weather'][0]['description']

        # Get current UTC time
        current_utc_time = datetime.utcnow()
        # Get timezone offset in seconds
        timezone_offset = weather_data['timezone']
        # Calculate local time
        local_time = current_utc_time + timedelta(seconds=timezone_offset)
        local_date = local_time.date().strftime('%Y-%m-%d')
        local_time_str = local_time.time().strftime('%H:%M')

        data = {
            'City': [city],
            'Country': [country],
            'Temperature (c)': [temperature],
            'Humidity': [humidity],
            'Conditions': [weather_conditions],
            'Local Date': [local_date],
            'Local Time': [local_time_str]
        }

        # def celsius_to_fahrenheit(celsius_temp):
        #     return (celsius_temp * 9 / 5) + 32
        #
        # # Step 3: Apply the function to create a new column
        # df[['Temperature (F)'] = df['Temperature (c)'].apply(celsius_to_fahrenheit)
        weather_df = pd.DataFrame(data)
        return weather_df
    else:
        print(f"Error: {response.status_code}")
        return None

# Function to create DataFrame from default cities list
def create_default_cities_df(api_key, default_cities_file):
    default_cities = load_default_cities(default_cities_file)
    weather_data_list = []

    for city, country in default_cities:
        weather_df = get_weather(city, api_key, country)
        if weather_df is not None:
            weather_data_list.append(weather_df)

    if weather_data_list:
        combined_df = pd.concat(weather_data_list, ignore_index=True)
        return combined_df
    else:
        return pd.DataFrame()

# Function to create DataFrame from a new input city
def create_new_city_df(city_name, api_key, country=None):
    weather_df = get_weather(city_name, api_key, country)
    return weather_df

# Function to update weather data for a selected city
def update_weather(new_city_df, city_to_replace, default_cities_df, default_cities_file, weather_data_file):
    if city_to_replace == 'None':
        return default_cities_df  # No replacement needed

    # Find index of city to replace in default cities DataFrame
    replace_index = default_cities_df[default_cities_df['City'] == city_to_replace.capitalize()].index

    if len(replace_index) == 0:
        print(f"City '{city_to_replace}' not found in default cities DataFrame.")
        return default_cities_df

    replace_index = replace_index[0]

    # Replace data in default cities DataFrame with new city's data
    default_cities_df.loc[replace_index] = new_city_df.values[0]

    # Save updated default cities DataFrame to JSON file
    save_default_cities(default_cities_df[['City', 'Country']].values.tolist(), default_cities_file)

    # Save weather data DataFrame to JSON file
    new_city_df.to_json(weather_data_file, orient='records')
    print(f"Weather data saved to '{weather_data_file}'")

    return default_cities_df

# Function to reset default cities to original list
def reset_default_cities(default_cities_file):
    default_cities = [
        ["London", "GB"],
        ["New York", "US"],
        ["Tokyo", "JP"],
        ["Sydney", "AU"],
        ["Paris", "FR"]
    ]
    save_default_cities(default_cities, default_cities_file)
    return default_cities
