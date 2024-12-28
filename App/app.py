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

# Add a styled title
st.markdown(
    """
    <h1 style="text-align: center; text-decoration: underline;">
    ✈️ Flight Delay Prediction App 🌦️
    </h1>
    """, 
    unsafe_allow_html=True
)

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
            departure_info = []
            weather_info = []
            
            # Departure info
            departure_info.append(f"**Status:** {flight['status']}")
            departure_info.append(f"**Departure airport:** {flight['departure_airport']}")
            
            departure_time = flight.get('departure_time', 'Unknown')
            if departure_time != 'Unknown':
                try:
                    formatted_departure_time = pd.to_datetime(departure_time).strftime('%H:%M, %a %d %b %Y')
                    departure_info.append(f"**Departure time:** {formatted_departure_time} (local)")
                except Exception:
                    departure_info.append("**Departure time:** Error parsing date")
            else:
                departure_info.append("**Departure time:** Unknown")

            departure_info.append(f"**Arrival airport:** {flight['arrival_airport']}")

            arrival_time = flight.get('arrival_time', 'Unknown')
            if arrival_time != 'Unknown':
                try:
                    formatted_arrival_time = pd.to_datetime(arrival_time).strftime('%H:%M, %a %d %b %Y')
                    departure_info.append(f"**Arrival time:** {formatted_arrival_time} (local)")
                except Exception:
                    departure_info.append("**Arrival time:** Error parsing date")
            else:
                departure_info.append("**Arrival time:** Unknown")

            departure_info.append(f"**Aircraft model:** {flight['aircraft_model']}")

            # Retrieve departure airport coordinates
            departure_airport_coords = {
                'lat': flight['departure_airport_lat'],
                'lon': flight['departure_airport_lon']
            }

            if departure_airport_coords['lat'] is None or departure_airport_coords['lon'] is None:
                weather_info.append("Departure airport coordinates are not available.")
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
                    if departure_time != 'Unknown':
                        try:
                            hour = int(departure_time.split(' ')[1].split(':')[0])
                        except Exception:
                            hour = 12  # Default to noon if parsing fails
                            weather_info.append("**Note:** Departure time unknown, defaulting to noon for weather conditions.")

                        # Filter weather data for the flight hour
                        weather_at_departure = weather_data.iloc[hour]

                        if not weather_at_departure.empty:
                            weather_info.append(f"- **Wind speed:** {weather_at_departure['HOURLYWindSpeed']} mph")
                            weather_info.append(f"- **Dry-bulb temperature:** {weather_at_departure['HOURLYDRYBULBTEMPF']} °F")
                            weather_info.append(f"- **Wet-bulb temperature:** {weather_at_departure['HOURLYWETBULBTEMPF']:.1f} °F")
                            weather_info.append(f"- **Relative humidity:** {weather_at_departure['HOURLYRelativeHumidity']} %")
                            weather_info.append(f"- **Visibility:** {weather_at_departure['HOURLYVISIBILITY']:.1f} miles")
                            weather_info.append(f"- **Estimated delay:** {lin_reg.predict(weather_at_departure.to_frame().T)[0]:.2f} minutes")
                        else:
                            weather_info.append("Weather Conditions at Departure: Data Unavailable")
                else:
                    weather_info.append("Error retrieving weather data.")

            # Display flight and weather data side by side
            col1, col2 = st.columns(2)

            with col1:
                st.markdown("### Flight Information")
                for info in departure_info:
                    st.write(info)

            with col2:
                st.markdown("### Weather Information")
                for info in weather_info:
                    st.write(info)

            # Display aircraft image
            if flight['aircraft_image']:
                st.image(flight['aircraft_image'], caption=f"Aircraft ({flight['aircraft_model']})", use_container_width=True)
    else:
        st.write(flight_data)  # If an error occurred or no flight was found
