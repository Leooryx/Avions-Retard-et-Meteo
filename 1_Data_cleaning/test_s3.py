#MinIO est une implémentation open-source de s3
#https://pythonds.linogaliana.fr/content/modern-ds/s3.html#cas-pratique-stocker-les-donn%C3%A9es-de-son-projet-sur-le-ssp-cloud


import s3fs

fs = s3fs.S3FileSystem(client_kwargs={"endpoint_url": "https://minio.lab.sspcloud.fr"})

#pour rendre les fichiers public il faut créer un dossier diffusion à la racine du bucket
MY_BUCKET = "leoacpr/diffusion"
print(fs.ls(MY_BUCKET))

import pandas as pd
data = {'Colonne_1': [1, 2],'Colonne_2': [3, 4]}
df = pd.DataFrame(data)

#export
FILE_PATH_OUT_S3 = f"{MY_BUCKET}/Pre-processing/df.csv"
with fs.open(FILE_PATH_OUT_S3, "w") as file_out:
    df.to_csv(file_out)
fs.ls(f"{MY_BUCKET}")

#import
FILE_PATH_IN_S3 = f"{MY_BUCKET}/Pre-processing/df.csv"  # chemin du fichier à lire
with fs.open(FILE_PATH_IN_S3, "r") as file_in:
    df_imported = pd.read_csv(file_in)
print(df_imported)