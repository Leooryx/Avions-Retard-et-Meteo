import requests


def normalize_string(s):
    return s.strip().lower() if s else None


def get_flight_info(flight_number, flight_date, api_key):
    API_URL = f"https://api.magicapi.dev/api/v1/aedbx/aerodatabox/flights/Number/{flight_number}/2024-12-22?withAircraftImage=true&withLocation=false"

    headers = {
        "x-magicapi-key": api_key
    }
    
    response = requests.get(API_URL, headers=headers)
    
    if response.status_code == 200:
        data = response.json()

        # Extraire les informations pertinentes
        flight_info = []

        for flight in data:
            try:
                # Récupérer les informations
                status = flight.get("status", "Unknown")
                departure_airport = flight.get("departure", {}).get("airport", {}).get("name", "Unknown")
                departure_time = flight.get("departure", {}).get("scheduledTime", {}).get("local", "Unknown")
                arrival_airport = flight.get("arrival", {}).get("airport", {}).get("name", "Unknown")
                arrival_time = flight.get("arrival", {}).get("scheduledTime", {}).get("local", "Unknown")
                airline = flight.get("airline", {}).get("name", "Unknown")
                aircraft_model = flight.get("aircraft", {}).get("model", "Unknown")
                aircraft_image = flight.get("aircraft", {}).get("image", {}).get("url")

                # Normalisation des noms d'aéroports
                normalized_departure = normalize_string(departure_airport)
                normalized_arrival = normalize_string(arrival_airport)

                # Vérifier si l'aéroport de départ est différent de l'aéroport d'arrivée
                if departure_airport != "Unknown" and arrival_airport != "Unknown" and normalized_departure != normalized_arrival:
                    # Ajouter les informations valides dans la liste
                    flight_info.append({
                        "flight_number": flight_number,
                        "status": status,
                        "departure_airport": departure_airport,
                        "departure_time": departure_time,
                        "arrival_airport": arrival_airport,
                        "arrival_time": arrival_time,
                        "airline": airline,
                        "aircraft_model": aircraft_model,
                        "aircraft_image": aircraft_image
                    })
            except Exception as e:
                print(f"Erreur lors du traitement des données du vol: {e}")

        return flight_info
    else:
        return f"Erreur API: {response.status_code} - {response.text}"
