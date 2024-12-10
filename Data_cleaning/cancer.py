import pandas as pd
#pip install openpyxl
import openpyxl

# Chemin vers le fichier
file_path = '/home/onyxia/work/Effects-Language-Diversity-1/FM-AD_Clinical.Bronchus_And_Lung.tsv'

# Chargement du fichier avec pandas
try:
    data = pd.read_csv(file_path, sep='\t')  # Assurez-vous que le fichier est bien séparé par des tabulations
    print("Fichier chargé avec succès.")
    # Affiche les premières lignes du DataFrame
except FileNotFoundError:
    print(f"Le fichier n'a pas été trouvé au chemin spécifié : {file_path}")
except Exception as e:
    print(f"Une erreur est survenue : {e}")

print(data)
output_path = '/home/onyxia/work/Effects-Language-Diversity-1/test_viz.xlsx'
data.to_excel(output_path, index=False)