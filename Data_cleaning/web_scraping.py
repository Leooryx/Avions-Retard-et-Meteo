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

id_a_extraire = [
    "1A", "2A", "3A", "10A", "12A", "13A", "14A", "17A", "18A", "19A", 
    "20A", "21A", "22A", "23A", "24A", "25A", "26A", "28A", "29A", "30A", 
    "31A", "33A", "34A", "35A", "37A", "38A", "39A", "41A", "48A", "49A", 
    "50A", "52A", "53A", "55A", "60A", "62A", "65A", "66A", "67A", "68A", 
    "79A", "80A", "81A", "90A", "93A", "94A", "98A", "99A", "100A", "101A", 
    "102A", "117A", "120A", "121A", "122A", "141A"
]

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
for row in feature_rows:
        # Extraire l'ID et le nom de la feature
        feature_id = row.find_element(By.CSS_SELECTOR, "td:nth-child(1)").text.strip()
        feature_name = row.find_element(By.CSS_SELECTOR, "td:nth-child(2)").text.strip()

        if feature_id not in id_a_extraire :
            continue

        print(feature_id + " " + feature_name)

        # Cliquer sur "values" pour afficher les valeurs
        values_button = row.find_element(By.CSS_SELECTOR, "button.btn-info.details.btn")
        WebDriverWait(browser, 100)


        values_button.click()

        # Attendre que le div 'snippet' soit chargé
        WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.snippet"))
        )

        
        # Récupérer le contenu HTML du div 'snippet'
        snippet_html = browser.find_element(By.CSS_SELECTOR, "div.snippet").get_attribute("outerHTML")

        # Parser le contenu HTML avec BeautifulSoup
        soup = BeautifulSoup(snippet_html, "html.parser")

        # Trouver toutes les lignes du tableau
        rows = soup.select("table.domain tbody tr")

        # Stocker les catégories
        categories = []

        for i,row in enumerate(rows):
            # Vérifier si la ligne contient une cellule "Value" et ignorer les totaux
            value_cell = row.select_one("td:nth-child(2)")
            if value_cell and not row.select_one("td b"):  # Exclure les lignes de total
                category = str(i) + " " + value_cell.text.strip()  # Extraire le texte de la catégorie
                categories.append(category)

        data[str(feature_id + " " + feature_name)] = categories


# Même chose pour la page 2
next_button = browser.find_element(By.LINK_TEXT, "Next →")
next_button.click()
# Attendre que "Processing" apparaisse
WebDriverWait(browser, 10).until(
    EC.text_to_be_present_in_element((By.CSS_SELECTOR, ".dataTables_processing"), "Processing")
)

# Attendre que "Processing" disparaisse
WebDriverWait(browser, 20).until(
    EC.invisibility_of_element((By.CSS_SELECTOR, ".dataTables_processing"))
)

max_retries = 10
attempt = 0
feature_rows = []

browser.save_screenshot("debug_screenshot.png")
browser.save_screenshot("debug_screenshot1.png")


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

# Parcourir chaque ligne pour extraire ID, nom, et valeurs
for row in feature_rows:
        # Extraire l'ID et le nom de la feature
        feature_id = row.find_element(By.CSS_SELECTOR, "td:nth-child(1)").text.strip()
        feature_name = row.find_element(By.CSS_SELECTOR, "td:nth-child(2)").text.strip()
        
        if feature_id not in id_a_extraire :
            continue

        print(feature_id + " " + feature_name)
        # Cliquer sur "values" pour afficher les valeurs


        values_button = row.find_element(By.CSS_SELECTOR, "button.btn-info.details.btn")
        WebDriverWait(browser, 100)


        values_button.click()

        # Attendre que le div 'snippet' soit chargé
        WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.snippet"))
        )

        
        # Récupérer le contenu HTML du div 'snippet'
        snippet_html = browser.find_element(By.CSS_SELECTOR, "div.snippet").get_attribute("outerHTML")

        # Parser le contenu HTML avec BeautifulSoup
        soup = BeautifulSoup(snippet_html, "html.parser")

        # Trouver toutes les lignes du tableau
        rows = soup.select("table.domain tbody tr")

        # Stocker les catégories
        categories = []

        for i,row in enumerate(rows):
            # Vérifier si la ligne contient une cellule "Value" et ignorer les totaux
            value_cell = row.select_one("td:nth-child(2)")
            if value_cell and not row.select_one("td b"):  # Exclure les lignes de total
                category = str(i) + " " + value_cell.text.strip()  # Extraire le texte de la catégorie
                categories.append(category)

        data[str(feature_id + " " + feature_name)] = categories





# Fermer le navigateur
browser.quit()

# Afficher les données collectées
for key, values in data.items():
    print(f"Feature ID: {key[0]}, Name: {key[1]}, Values: {values}")

