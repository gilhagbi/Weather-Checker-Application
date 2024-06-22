import streamlit as st
import functions as f
from dotenv import load_dotenv
import os
load_dotenv()

# Function to display favorite cities table
def display_favorite_cities_table(df):
    st.write('### Weather in My Favorite Cities')
    df['Temperature (c)'] = df['Temperature (c)'].astype(int)
    st.dataframe(df[['City', 'Country', 'Temperature (c)', 'Humidity', 'Conditions', 'Local Date', 'Local Time']])


# Function to display weather data of newly added city
def display_new_city_weather(new_city_df):
    st.write('### Newly Added City Weather Data:')
    new_city_df['Temperature (c)'] = new_city_df['Temperature (c)'].astype(int)
    st.dataframe(new_city_df[['City', 'Country', 'Temperature (c)', 'Humidity', 'Conditions', 'Local Date', 'Local Time']].transpose())

def main():
    st.set_page_config(page_title="Weather Dashboard", layout="wide")
    st.title('🌤️ Weather Dashboard')

    api_key = os.getenv('API_KEY')
    default_cities_file = os.getenv('DEFAULT_CITIES_FILE')
    weather_data_file = os.getenv('WEATHER_DATA_FILE')

    f.create_default_cities_file()

    default_cities_df = f.create_default_cities_df(api_key, default_cities_file)

    # Layout for the main page
    st.markdown("## My favorite Weather locations")
#    st.write("add a city to the list.")

    col2, col1 = st.columns([1, 2])

    with col1:
        # Add a button to refresh the favorite cities table
        if st.button('🔄 Refresh Favorite Cities Table'):
            default_cities_df = f.create_default_cities_df(api_key, default_cities_file)
            st.success("Favorite cities table refreshed!")

        # Display the favorite cities table
        display_favorite_cities_table(default_cities_df)

    with col2:
        st.markdown("## Add a city to the list")
        new_city_name = st.text_input('Enter new city name:')
        new_country_code = st.text_input('Enter new country code:')
        city_to_replace = st.text_input('Enter city to replace from your favorite list (or skip):')

        if st.button('🌐 Update Weather'):
            new_city_df = f.create_new_city_df(new_city_name, api_key, new_country_code)
            if new_city_df is not None and not new_city_df.empty:
                f.update_weather(new_city_df, city_to_replace, default_cities_df, default_cities_file, weather_data_file)
                st.success('Weather updated successfully!')
                display_new_city_weather(new_city_df)
                default_cities_df = f.create_default_cities_df(api_key, default_cities_file)
            elif new_city_df is not None and new_city_df.empty:
                st.error(f'No weather data found for {new_city_name}, {new_country_code}')
            else:
                st.error(f'Failed to fetch weather data for {new_city_name}, {new_country_code}')

        if st.button('🔄 Reset to Default Cities List'):
            f.reset_default_cities(default_cities_file)
            default_cities_df = f.create_default_cities_df(api_key, default_cities_file)
            st.success('Default cities list reset successfully!')

if __name__ == '__main__':
    main()
