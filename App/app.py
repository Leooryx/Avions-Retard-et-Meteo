import streamlit as st
from flight_api import get_flight_info
from weather_api import fetch_weather_data  # Import de la fonction météo
from config import API_KEY as api_key

# Entrées utilisateur
flight_number = st.text_input("Numéro de vol (ex. DL1708):")
flight_date = st.date_input("Date du vol:")

# Bouton de recherche
search_button = st.button("Rechercher")

# Si le bouton est cliqué et que les entrées sont données
if search_button and flight_number and flight_date:
    # Récupérer les informations sur le vol
    flight_data = get_flight_info(flight_number, flight_date, api_key)
    
    if isinstance(flight_data, list) and flight_data:
        for flight in flight_data:
            st.write(f"Vol: {flight['flight_number']}")
            st.write(f"Statut: {flight['status']}")
            st.write(f"Aéroport de départ: {flight['departure_airport']}")
            st.write(f"Heure de départ: {flight['departure_time']}")
            st.write(f"Aéroport d'arrivée: {flight['arrival_airport']}")
            st.write(f"Heure d'arrivée: {flight['arrival_time']}")
            st.write(f"Compagnie aérienne: {flight['airline']}")
            st.write(f"Modèle d'avion: {flight['aircraft_model']}")
            if flight['aircraft_image']:
                st.image(flight['aircraft_image'], caption=f"Image de l'avion ({flight['aircraft_model']})", use_container_width=True)

            # Récupérer la latitude et la longitude de l'aéroport de départ
            departure_airport_coords = {
                'lat': flight['departure_airport_lat'],
                'lon': flight['departure_airport_lon']
            }

            print(departure_airport_coords)
            if departure_airport_coords['lat'] is None or departure_airport_coords['lon'] is None:
                st.write("Les coordonnées de l'aéroport de départ ne sont pas disponibles.")
            else:                
                # Construire l'URL de l'API météo
                weather_api_url = (
                    f"https://api.open-meteo.com/v1/forecast?latitude={departure_airport_coords['lat']}"
                    f"&longitude={departure_airport_coords['lon']}"
                    f"&hourly=temperature_2m,relative_humidity_2m,dew_point_2m,pressure_msl,"
                    f"surface_pressure,visibility,wind_speed_10m"
                    f"&wind_speed_unit=mph&timezone=America/New_York&start_date={flight_date}"
                    f"&end_date={flight_date}"
                ) 


                # Récupérer les données météo
                weather_data = fetch_weather_data(weather_api_url)

                if weather_data is not None:
                    # Extraire l'heure du vol
                    departure_time = flight.get('departure_time', 'Unknown')
                    print(departure_time)
                    if departure_time != 'Unknown':
                        hour = int(departure_time.split(' ')[1].split(':')[0])

                        # Filtrer les données pour l'heure du vol
                        weather_at_departure = weather_data.iloc[hour]

                        if not weather_at_departure.empty:
                            st.write("**Conditions météo au départ :**")
                            st.write(f"Température sèche (°F) : {weather_at_departure['HOURLYDRYBULBTEMPF']}")
                            st.write(f"Température du bulbe humide (°F) : {weather_at_departure['HOURLYWETBULBTEMPF']}")
                            st.write(f"Humidité relative (%) : {weather_at_departure['HOURLYRelativeHumidity']}")
                            st.write(f"Visibilité (miles) : {weather_at_departure['HOURLYVISIBILITY']}")
                            st.write(f"Pression au niveau de la mer (inHg) : {weather_at_departure['HOURLYSeaLevelPressure']}")
                        else:
                            st.write("**Conditions météo au départ : Données indisponibles**")
                else:
                    st.write("Erreur lors de la récupération des données météo.")
    else:
        st.write(flight_data)  # Si une erreur ou aucun vol trouvé
