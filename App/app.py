import streamlit as st
import joblib
import os
from flight_api import get_flight_info
from weather_api import fetch_weather_data
from config import API_KEY as api_key
import pandas as pd

# Load the linear regression model
current_dir = os.path.dirname(os.path.abspath(__file__))  # Directory where app.py is located
model_path = os.path.join(current_dir, "..", "3_Machine_Learning", "linear_regression_model.pkl")
lin_reg = joblib.load(model_path)

# User input
flight_number = st.text_input("Flight number (e.g., DL1708):")
flight_date = st.date_input("Flight date:")

# Search button
search_button = st.button("Search")

# If the search button is clicked and inputs are provided
if search_button and flight_number and flight_date:
    # Retrieve flight information
    flight_data = get_flight_info(flight_number, flight_date, api_key)
    
    if isinstance(flight_data, list) and flight_data:
        for flight in flight_data:
            st.markdown(f"### {flight['airline']} {flight['flight_number']}")
            st.write(f"**Status:** {flight['status']}")
            st.write(f"**Departure airport:** {flight['departure_airport']}")
            
            # Handle departure time if not available
            departure_time = flight.get('departure_time', 'Unknown')
            if departure_time != 'Unknown':
                try:
                    formatted_departure_time = pd.to_datetime(departure_time).strftime('%H:%M, %a %d %b %Y')
                    st.write(f"**Departure time:** {formatted_departure_time} (local time)")
                except Exception as e:
                    st.write("**Departure time:** Error parsing date")
            else:
                st.write("**Departure time:** Unknown")
                
            st.write(f"**Arrival airport:** {flight['arrival_airport']}")
            st.write(f"**Arrival time:** {pd.to_datetime(flight['arrival_time']).strftime('%H:%M, %A %d %B %Y')} (local time)")
            st.write(f"**Aircraft model:** {flight['aircraft_model']}")
            if flight['aircraft_image']:
                st.image(flight['aircraft_image'], caption=f"Aircraft ({flight['aircraft_model']})", use_container_width=True)

            # Retrieve departure airport coordinates
            departure_airport_coords = {
                'lat': flight['departure_airport_lat'],
                'lon': flight['departure_airport_lon']
            }

            if departure_airport_coords['lat'] is None or departure_airport_coords['lon'] is None:
                st.write("Departure airport coordinates are not available.")
            else:
                # Construct the weather API URL
                weather_api_url = (
                    f"https://api.open-meteo.com/v1/forecast?latitude={departure_airport_coords['lat']}"
                    f"&longitude={departure_airport_coords['lon']}"
                    f"&hourly=temperature_2m,relative_humidity_2m,dew_point_2m,pressure_msl,"
                    f"surface_pressure,visibility,wind_speed_10m"
                    f"&wind_speed_unit=mph&timezone=America/New_York&start_date={flight_date}"
                    f"&end_date={flight_date}"
                )

                # Fetch weather data
                weather_data = fetch_weather_data(weather_api_url)

                if weather_data is not None:
                    # Extract flight hour
                    departure_time = flight.get('departure_time', 'Unknown')

                    if departure_time != 'Unknown':
                        hour = int(departure_time.split(' ')[1].split(':')[0])

                        # Filter weather data for the flight hour
                        weather_at_departure = weather_data.iloc[hour]

                        if not weather_at_departure.empty:
                            st.markdown("### Weather Conditions at Departure")
                            st.write(f"- **Dry-bulb temperature:** {weather_at_departure['HOURLYDRYBULBTEMPF']} °F")
                            st.write(f"- **Wet-bulb temperature:** {weather_at_departure['HOURLYWETBULBTEMPF']} °F")
                            st.write(f"- **Relative humidity:** {weather_at_departure['HOURLYRelativeHumidity']} %")
                            st.write(f"- **Visibility:** {weather_at_departure['HOURLYVISIBILITY']} miles")
                            st.write(f"- **Estimated delay:** {lin_reg.predict(weather_at_departure.to_frame().T)[0]:.2f} minutes")
                        else:
                            st.markdown("### Weather Conditions at Departure: Data Unavailable")
                else:
                    st.write("Error retrieving weather data.")
    else:
        st.write(flight_data)  # If an error occurred or no flight was found
