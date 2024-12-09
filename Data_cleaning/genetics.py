##Example of code with selenium to read the data

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

# Configurer les options pour Chrome
chrome_options = Options()
chrome_options.add_argument("--headless")  # Mode sans interface graphique
chrome_options.add_argument("--no-sandbox")  # Nécessaire pour certains environnements
chrome_options.add_argument("--disable-dev-shm-usage")  # Évite les problèmes de mémoire partagée
chrome_options.add_argument("--disable-gpu")  # Désactiver l'accélération GPU
chrome_options.add_argument("--remote-debugging-port=9222")  # Pour le débogage distant

# Définir le chemin du service Chromedriver
service = Service()

# Initialiser le navigateur
driver = webdriver.Chrome(service=service, options=chrome_options)

# Accéder à la page web
url = "https://www.internationalgenome.org/data-portal/data-collection/30x-grch38"
driver.get(url)

# Attendre que la page charge
time.sleep(3)

# Collecter tous les liens en parcourant les pages
all_links = []

while True:
    # Trouver tous les éléments contenant les liens
    elements = driver.find_elements(By.XPATH, "//a[contains(@href, '.cram')]")
    for elem in elements:
        all_links.append(elem.get_attribute("href"))

    # Trouver et cliquer sur le bouton "Suivant" pour charger plus de données
    try:
        next_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Next')]")
        next_button.click()
        time.sleep(10)  # Attendre que la page suivante charge
    except:
        print("Toutes les pages ont été chargées.")
        break

# Enregistrer les liens dans un fichier
with open("cram_links.txt", "w") as f:
    for link in all_links:
        f.write(link + "\n")

# Fermer le navigateur
driver.quit()

print(len(all_links))
