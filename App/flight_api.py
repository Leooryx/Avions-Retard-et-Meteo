import requests


def normalize_string(s):
    return s.strip().lower() if s else None


def get_flight_info(flight_number, flight_date, api_key):
    API_URL = f"https://api.magicapi.dev/api/v1/aedbx/aerodatabox/flights/Number/{flight_number}/{flight_date}?withAircraftImage=true&withLocation=false"
    headers = {
        "x-magicapi-key": api_key
    }
    
    response = requests.get(API_URL, headers=headers)
    
    if response.status_code == 200:
        data = response.json()

        # Extract the flight information from the JSON
        flight_info = []

        for flight in data:
            try:
                # Collect the informations
                status = flight.get("status", "Unknown")
                departure_airport = flight.get("departure", {}).get("airport", {}).get("name", "Unknown")
                departure_time = flight.get("departure", {}).get("scheduledTime", {}).get("local", "Unknown")
                arrival_airport = flight.get("arrival", {}).get("airport", {}).get("name", "Unknown")
                arrival_time = flight.get("arrival", {}).get("scheduledTime", {}).get("local", "Unknown")
                airline = flight.get("airline", {}).get("name", "Unknown")
                aircraft_model = flight.get("aircraft", {}).get("model", "Unknown")
                aircraft_image = flight.get("aircraft", {}).get("image", {}).get("url")

                # Coordinates of the airports
                departure_lat = flight.get("departure", {}).get("airport", {}).get("location", {}).get("lat", None)
                departure_lon = flight.get("departure", {}).get("airport", {}).get("location", {}).get("lon", None)
                arrival_lat = flight.get("arrival", {}).get("airport", {}).get("location", {}).get("lat", None)
                arrival_lon = flight.get("arrival", {}).get("airport", {}).get("location", {}).get("lon", None)

                # Normalize the airports names
                normalized_departure = normalize_string(departure_airport)
                normalized_arrival = normalize_string(arrival_airport)

                # Check if the arrival and departure airport are different (because sometimes there are flights from an airport to the same)
                if departure_airport != "Unknown" and arrival_airport != "Unknown" and normalized_departure != normalized_arrival:
                    # Add the informations
                    flight_info.append({
                        "flight_number": flight_number,
                        "status": status,
                        "departure_airport": departure_airport,
                        "departure_time": departure_time,
                        "departure_airport_lat": departure_lat,
                        "departure_airport_lon": departure_lon,
                        "arrival_airport": arrival_airport,
                        "arrival_time": arrival_time,
                        "arrival_airport_lat": arrival_lat,
                        "arrival_airport_lon": arrival_lon,
                        "airline": airline,
                        "aircraft_model": aircraft_model,
                        "aircraft_image": aircraft_image
                    })
            except Exception as e:
                print(f"Error while treating the data: {e}")

        return flight_info
    else:
        return f"Erreur API: {response.status_code} - {response.text}"
