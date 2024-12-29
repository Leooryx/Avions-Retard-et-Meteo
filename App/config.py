import os

# Remplissez le token ici si vous exécutez localement
API_TOKEN = "votre_token_secret"  # Remplacer par le token envoyé par mail

# Optionnel : Pour le déploiement sur Streamlit Cloud, la variable d'environnement sera utilisée
API_TOKEN = os.getenv("API_TOKEN", API_TOKEN)

if not API_TOKEN or API_TOKEN == "votre_token_secret":
    raise ValueError("Veuillez remplir le token dans config.py ou le définir comme variable d'environnement.")
