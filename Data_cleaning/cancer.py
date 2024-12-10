import pandas as pd
#pip install openpyxl
import openpyxl


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

#print(data)
#output_path = '/home/onyxia/work/Effects-Language-Diversity-1/test_viz.xlsx'
#data.to_excel(output_path, index=False)

#FIRST STEP: Data pre-processing
clinical_AML = pd.read_excel('/home/onyxia/work/Effects-Language-Diversity-1/TARGET_AML_ClinicalData_AML1031_20230720.xlsx')
clinical_validation = pd.read_excel('/home/onyxia/work/Effects-Language-Diversity-1/TARGET_AML_ClinicalData_Validation_20230720.xlsx')
clinical_lowdepth = pd.read_excel('/home/onyxia/work/Effects-Language-Diversity-1/TARGET_AML_ClinicalData_LowDepthRNAseq_20230720.xlsx')
bronchus_lungs = pd.read_csv('/home/onyxia/work/Effects-Language-Diversity-1/FM-AD_Clinical.Bronchus_And_Lung.tsv', sep='\t')

#print(clinical_AML)
#print(clinical_validation)
#print(clinical_lowdepth)
print(bronchus_lungs)

print(set(clinical_AML['Protocol']))
print(set(clinical_validation['Protocol']))
print(set(clinical_lowdepth['Protocol']))
#mêmes traitements



