#Dont forget to add the pip install and all the terminal commands used!!

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time

# Configurer les options pour Chrome
chrome_options = Options()
chrome_options.add_argument("--headless")  # Exécuter sans interface graphique
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-gpu")

# Initialiser le navigateur
service = Service()
driver = webdriver.Chrome(service=service, options=chrome_options)

# Accéder à la page web
url = "https://www.internationalgenome.org/data-portal/data-collection/30x-grch38"
driver.get(url)

# Attendre que la page charge
time.sleep(3)

# Collecter les liens en parcourant les pages
all_links = []
seen_pages = set()  # Pour éviter de revisiter les mêmes pages
i = 0

while True:
    # Identifier la page actuelle par un "hash" de son contenu
    current_page_signature = driver.page_source[:1000]
    if current_page_signature in seen_pages: #TODO the code doesnt work because it says the page est déjà vue, the problem is here!!!
        print("Page déjà vue, arrêt du script.")
        break
    seen_pages.add(current_page_signature)

    # Collecter les liens sur la page actuelle
    elements = driver.find_elements(By.XPATH, "//a[contains(@href, '.cram')]")
    for elem in elements:
        all_links.append(elem.get_attribute("href"))

    # Essayer de cliquer sur le bouton "Next"
    try:
        # Attendre que le bouton devienne visible et cliquable
        next_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'page-button') and contains(., 'Next')]"))
        )

        # Faire défiler jusqu'au bouton pour le rendre visible
        driver.execute_script("arguments[0].scrollIntoView(true);", next_button)

        # Cliquer sur le bouton "Next"
        ActionChains(driver).move_to_element(next_button).click(next_button).perform()
        time.sleep(2)  # Temps pour charger la page suivante

    except Exception as e:
        print(f"Erreur : {e}")
        print("Bouton 'Next' introuvable ou fin des pages atteinte.")
        break

    # Arrêter après 2 itérations pour le test
    i += 1
    if i == 2:
        break

# Supprimer les doublons
all_links = list(set(all_links))

# Enregistrer les liens dans un fichier
with open("/home/onyxia/work/Effects-Language-Diversity/Data_cleaning/cram_links.txt", "w") as f:
    for link in sorted(all_links):
        f.write(link + "\n")


# Fermer le navigateur
driver.quit()

'''print(f"Nombre total de liens collectés : {len(all_links)}")
for i in all_links:
    print(i)'''



#Problem: cannot go onto the next page to get other links 
#I decided to move on to the next step: data extraction from the links

#downloading the packages to read cram files and manipulate dna data
#sudo apt-get install samtools
#pip install pyranges


import os
import subprocess
import pyranges as pr

# Chemin vers le fichier contenant les liens CRAM
links_file = "/home/onyxia/work/Effects-Language-Diversity/Data_cleaning/cram_links.txt"
output_dir = "/home/onyxia/work/Effects-Language-Diversity/Data_cleaning/downloads"

def download_chromosome_1(ftp_url, output_dir):
    """Télécharge les alignements pour le chromosome 1 depuis un fichier CRAM."""
    os.makedirs(output_dir, exist_ok=True)
    file_name = os.path.basename(ftp_url).replace(".cram", "_chr1.bam")
    output_file = os.path.join(output_dir, file_name)

    if os.path.exists(output_file):
        print(f"Fichier déjà téléchargé : {output_file}")
        return output_file

    print(f"Extraction des alignements pour le chromosome 1 depuis {ftp_url}...")
    try:
        # Exécuter samtools pour extraire les alignements du chromosome 1
        subprocess.run(
            ["samtools", "view", "-h", "-o", output_file, ftp_url, "chr1"],
            check=True
        )
        print(f"Fichier téléchargé : {output_file}")
        return output_file
    except subprocess.CalledProcessError as e:
        print(f"Erreur lors de l'extraction de {ftp_url}: {e}")
        return None

def load_bam_with_pyranges(bam_path):
    """Charge un fichier BAM dans un objet PyRanges."""
    print(f"Chargement du fichier BAM avec PyRanges : {bam_path}...")
    gr = pr.read_bam(bam_path)
    print("Données chargées dans PyRanges.")
    return gr

# Étape 1 : Lire les liens FTP depuis le fichier cram_links.txt
with open(links_file, "r") as f:
    ftp_links = [line.strip() for line in f.readlines()]

# Étape 2 : Traiter chaque fichier CRAM
for ftp_url in ftp_links:
    try:
        # Extraire les données pour chromosome 1
        bam_path = download_chromosome_1(ftp_url, output_dir)
        if bam_path:
            # Charger le fichier BAM avec PyRanges
            gr = load_bam_with_pyranges(bam_path)

            # Afficher les données PyRanges (limitées pour les grandes données)
            print(gr.head())

    except Exception as e:
        print(f"Erreur lors du traitement de {ftp_url} : {e}")

#doesnt work because chromosome 1 cannot be dowloaded this easily


