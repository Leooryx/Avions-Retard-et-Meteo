#MinIO est une implémentation open-source de s3
#https://pythonds.linogaliana.fr/content/modern-ds/s3.html#cas-pratique-stocker-les-donn%C3%A9es-de-son-projet-sur-le-ssp-cloud


import s3fs

fs = s3fs.S3FileSystem(client_kwargs={"endpoint_url": "https://minio.lab.sspcloud.fr"})

#pour rendre les fichiers public il faut créer un dossier diffusion à la racine du bucket
MY_BUCKET = "leoacpr"
print(fs.ls(MY_BUCKET))

import pandas as pd
data = {'Colonne_1': [1, 2],'Colonne_2': [3, 4]}
df = pd.DataFrame(data)

'''#export --> diffusion is only accessible for other people to read documents, to write them you have to connect to your own bucket
FILE_PATH_OUT_S3 = f"{MY_BUCKET}/diffusion/Pre-processing/df.csv"
with fs.open(FILE_PATH_OUT_S3, "w") as file_out:
    df.to_csv(file_out)
fs.ls(f"{MY_BUCKET}")'''

#import
FILE_PATH_IN_S3 = f"{MY_BUCKET}/diffusion/Pre-processing/df.csv"  # chemin du fichier à lire
with fs.open(FILE_PATH_IN_S3, "r") as file_in:
    df_imported = pd.read_csv(file_in)
print(df_imported)

#Download the files from leoacpr

YOUR_BUCKET = str(input("Type your bucket: \n"))
source_folder = f"{MY_BUCKET}/diffusion/Pre-processing"

files_in_source = fs.ls(source_folder)

for file_path_in_s3 in files_in_source:
    file_name = file_path_in_s3.split('/')[-1]  # Nom du fichier sans le chemin complet
    file_path_for_you = f"{YOUR_BUCKET}/diffusion/Pre-processing/{file_name}"
    #import
    with fs.open(file_path_in_s3, "r") as file_in:
        df_imported = pd.read_csv(file_in)
    #export
    with fs.open(file_path_for_you, "w") as file_out:
        df_imported.to_csv(file_out)

    print(f"File {file_name} has been successfully copied to {file_path_for_you}")