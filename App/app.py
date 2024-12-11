import streamlit as st
from flight_api import get_flight_info
from config import API_KEY as api_key

# Entrées utilisateur
flight_number = st.text_input("Numéro de vol (ex. AA1004):")
flight_date = st.date_input("Date du vol:")

# Bouton de recherche
search_button = st.button("Search")

# Si le bouton est cliqué et que les entrées sont données
if search_button and flight_number and flight_date:
    flight_data = get_flight_info(flight_number, flight_date, api_key)  # Passe la clé API ici
    
    # Afficher les résultats
    if isinstance(flight_data, list) and flight_data:
        for flight in flight_data:
            st.write(f"Vol: {flight['flight_number']}")
            st.write(f"Statut: {flight['status']}")
            st.write(f"Aéroport de départ: {flight['departure_airport']}")
            st.write(f"Aéroport d'arrivée: {flight['arrival_airport']}")
            st.write(f"Retard au départ: {flight['departure_delay']} minutes")
            st.write(f"Retard à l'arrivée: {flight['arrival_delay']} minutes")
            st.write("---")
    else:
        st.write(flight_data)  # Si une erreur ou aucun vol trouvé
