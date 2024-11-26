# Selenium installation

# pip3 install selenium
# pip3 install webdriver-manager

# wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb -O /tmp/chrome.deb
# sudo apt-get update
# sudo -E apt-get install -y /tmp/chrome.deb
# pip3 install chromedriver-autoinstaller selenium

import chromedriver_autoinstaller
chromedriver_autoinstaller.install()
print(1)
import selenium
from webdriver_manager.chrome import ChromeDriverManager

path_to_web_driver = ChromeDriverManager().install()


# Initialization of Selenium
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from bs4 import BeautifulSoup

# Configuration de Chrome pour l'exécuter en mode headless
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Lancement du navigateur avec Selenium
service = Service(executable_path=ChromeDriverManager().install())
browser = webdriver.Chrome(service=service, options=chrome_options)

# Accéder à la page principale de WALS
browser.get("https://wals.info/feature")

# Réessayer de trouver les lignes si aucune ligne n'est détectée initialement
max_retries = 10
attempt = 0
feature_rows = []

while attempt < max_retries and not feature_rows:
    try:
        # Attendre que la table des features soit visible
        WebDriverWait(browser, 1000).until(EC.presence_of_element_located((By.CSS_SELECTOR, "table tbody tr")))
        feature_rows = browser.find_elements(By.CSS_SELECTOR, "table tbody tr")

    except TimeoutException:
        print(f"Tentative {attempt + 1} : La table des features n'a pas encore pu être chargée.")
    
    attempt += 1
    time.sleep(2)  # Pause entre les tentatives pour laisser plus de temps au chargement

# Vérifier si des lignes de feature ont été trouvées après les tentatives
if not feature_rows:
    print("Aucune ligne de feature trouvée.")
    browser.quit()
    exit()

# Dictionnaire pour stocker les données
data = {}

# Parcourir chaque ligne pour extraire ID, nom, et valeurs
for row in feature_rows[1:2]:
        """try:"""
        # Extraire l'ID et le nom de la feature
        feature_id = row.find_element(By.CSS_SELECTOR, "td:nth-child(1)").text.strip()
        feature_name = row.find_element(By.CSS_SELECTOR, "td:nth-child(2)").text.strip()
        print(feature_name)
        # Cliquer sur "values" pour afficher les valeurs
        
        values_button = row.find_element(By.PARTIAL_LINK_TEXT, "Values")
        values_button.click()
        """
        # Attendre que la section des valeurs soit visible et chargée
        WebDriverWait(browser, 1000).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "div.values-section"))
        )

        # Extraire les valeurs après le chargement
        values_section = browser.find_element(By.CSS_SELECTOR, "div.values-section")  # Ajuster le sélecteur
        values_html = values_section.get_attribute("outerHTML")
        
        # Utiliser BeautifulSoup pour parser les valeurs si nécessaire
        soup = BeautifulSoup(values_html, 'html.parser')
        values = [value.text.strip() for value in soup.find_all('td', class_='value-cell')]  # Ajuster la classe
        
        # Stocker les données dans le dictionnaire
        data[(feature_id, feature_name)] = values

        # Fermer ou masquer la section "values" si nécessaire
        # Si la section "values" est un modal ou peut être fermée, clique sur un bouton de fermeture ou utilise `ESC` pour fermer

    except (NoSuchElementException, TimeoutException) as e:
        print(f"Erreur lors de l'extraction pour la ligne {feature_id} - {feature_name}: {e}")
        continue
    """

# Fermer le navigateur
browser.quit()

# Afficher les données collectées
for key, values in data.items():
    print(f"Feature ID: {key[0]}, Name: {key[1]}, Values: {values}")