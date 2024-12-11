import streamlit as st

# Titre principal
st.markdown("<h1 style='text-align: center; color: black;'>Suivi des Vols</h1>", unsafe_allow_html=True)

# En-tête pour Départs et Arrivées
st.markdown("<h3 style='color: black;'>Départs / Arrivées</h3>", unsafe_allow_html=True)

# Exemple de données (à remplacer par les résultats de l'API)
vols = [
    {"heure": "17:41", "retard": "+2h30", "statut": "Retardé", "destination": "Paris - Charles de Gaulle", "gate": "C"},
    {"heure": "19:59", "retard": "+1h30", "statut": "Retardé", "destination": "New York - JFK", "gate": "B"},
    {"heure": "20:07", "retard": "+25 min", "statut": "Retardé", "destination": "Londres - Heathrow", "gate": "D"},
]

# Création d'une grille pour afficher les informations
for vol in vols:
    # Utilisation des colonnes pour organiser les données
    col1, col2, col3, col4, col5 = st.columns([1, 1, 2, 3, 1])
    
    # Style des blocs
    col1.markdown(f"<div style='background-color: #f0f0f0; padding: 10px; border-radius: 5px; text-align: center;'>"
                  f"<strong style='color: black;'>{vol['heure']}</strong></div>", unsafe_allow_html=True)
    
    col2.markdown(f"<div style='background-color: #f8d7da; padding: 10px; border-radius: 5px; text-align: center;'>"
                  f"<strong style='color: darkred;'>{vol['retard']}</strong></div>", unsafe_allow_html=True)
    
    col3.markdown(f"<div style='background-color: #d1ecf1; padding: 10px; border-radius: 5px; text-align: center;'>"
                  f"<strong style='color: darkblue;'>{vol['statut']}</strong></div>", unsafe_allow_html=True)
    
    col4.markdown(f"<div style='background-color: #f0f0f0; padding: 10px; border-radius: 5px; text-align: center;'>"
                  f"<strong style='color: black;'>{vol['destination']}</strong></div>", unsafe_allow_html=True)
    
    col5.markdown(f"<div style='background-color: #f0f0f0; padding: 10px; border-radius: 5px; text-align: center;'>"
                  f"<strong style='color: black;'>Gate {vol['gate']}</strong></div>", unsafe_allow_html=True)

# Ajouter un bouton pour charger plus de résultats
st.button("Voir plus")
