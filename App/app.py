import streamlit as st
from flight_api import get_flight_info
from config import API_KEY as api_key

# Entrées utilisateur
flight_number = st.text_input("Numéro de vol (ex. DL1708):")
flight_date = st.date_input("Date du vol:")

# Bouton de recherche
search_button = st.button("Rechercher")

# Si le bouton est cliqué et que les entrées sont données
if search_button and flight_number and flight_date:
    flight_data = get_flight_info(flight_number, flight_date, api_key)

    # Afficher les résultats
    if isinstance(flight_data, list) and flight_data:
        for flight in flight_data:
            st.write(f"Vol: {flight['flight_number']}")
            st.write(f"Statut: {flight['status']}")
            st.write(f"Aéroport de départ: {flight['departure_airport']}")
            st.write(f"Heure de départ: {flight['departure_time']} {'(estimée)' if flight.get('estimated_departure', False) else ''}")
            st.write(f"Aéroport d'arrivée: {flight['arrival_airport']}")
            st.write(f"Heure d'arrivée: {flight['arrival_time']}")
            st.write(f"Compagnie aérienne: {flight['airline']}")
            st.write(f"Modèle d'avion: {flight['aircraft_model']}")
            if flight.get('aircraft_image'):
                st.image(flight['aircraft_image'], caption="Image de l'avion", use_container_width=True)
            st.write("---")
    else:
        st.write(flight_data)  # Si une erreur ou aucun vol trouvé
