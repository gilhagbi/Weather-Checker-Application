import functions as f
from dotenv import load_dotenv
import os
load_dotenv()


def main():

    api_key = os.getenv('API_KEY')
    default_cities_file = os.getenv('DEFAULT_CITIES_FILE')
    weather_data_file = os.getenv('WEATHER_DATA_FILE')

    # Call the function to create the default_cities.json if not exists

    f.create_default_cities_file()

    # Load default cities DataFrame
    default_cities_df = f.create_default_cities_df(api_key, default_cities_file)

    # Display default cities DataFrame
    print("Default Cities DataFrame:")
    print(default_cities_df.to_string(index=False))


    while True:

        print("\nOptions:")
        print("1. Update Weather for a City")
        print("2. Reset Default Cities")
        print("3. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            new_city_name = input("\nEnter new city name: ")
            new_country_code = input("\nEnter new country code: ")
            city_to_replace = input("\nEnter city to replace (or 'None' to skip): ")

            new_city_df = f.create_new_city_df(new_city_name, api_key, new_country_code)
            if new_city_df is not None and not new_city_df.empty:
                updated_default_cities_df = f.update_weather(new_city_df, city_to_replace, default_cities_df,
                                                           default_cities_file, weather_data_file)
                print("\nUpdated Default Cities DataFrame:")
                print(updated_default_cities_df.to_string(index=False))
                print("\nNewly Added City Weather Data:")
                print(new_city_df.to_string(index=False))
            elif new_city_df is not None and new_city_df.empty:
                print(f"No weather data found for '{new_city_name}', '{new_country_code}'")
            else:
                print(f"Failed to fetch weather data for '{new_city_name}', '{new_country_code}'")

        elif choice == '2':
            default_cities = f.reset_default_cities(default_cities_file)
            default_cities_df = f.create_default_cities_df(api_key, default_cities_file)
            print("\nReset Default Cities DataFrame:")
            print(default_cities_df.to_string(index=False))
        elif choice == '3':
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
