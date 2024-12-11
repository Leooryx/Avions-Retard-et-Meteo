import requests

def get_flight_info(flight_number, flight_date, api_key):
    # URL de l'API avec le numéro de vol et la date
    API_URL = f'https://api.aviationstack.com/v1/flights?access_key={api_key}&flight_iata={flight_number}&date={flight_date}'
    
    # Faire la requête API
    response = requests.get(API_URL)
    
    # Vérifier la réponse
    if response.status_code == 200:
        data = response.json()
        
        # Extraire les informations pertinentes (par exemple, statut, retard, etc.)
        flight_info = []
        
        for flight in data.get('data', []):
            flight_status = flight.get('flight_status', 'Unknown')
            departure_delay = flight.get('departure', {}).get('delay', 'N/A')
            arrival_delay = flight.get('arrival', {}).get('delay', 'N/A')
            departure_airport = flight.get('departure', {}).get('airport', 'Unknown')
            arrival_airport = flight.get('arrival', {}).get('airport', 'Unknown')
            
            flight_info.append({
                'flight_number': flight.get('flight', {}).get('iata', 'Unknown'),
                'status': flight_status,
                'departure_airport': departure_airport,
                'arrival_airport': arrival_airport,
                'departure_delay': departure_delay,
                'arrival_delay': arrival_delay
            })
        
        return flight_info
    else:
        return f"Erreur API: {response.status_code}"

