# Data cleaning for the dataset of the WALS from Kaggle

# Link: https://www.kaggle.com/code/kerneler/starter-wals-dataset-ddb3fac7-a/input
import pandas as pd
print("3")

language_df = pd.read_csv("/home/onyxia/work/Effects-Language-Diversity/Data_cleaning/language.csv")
print(language_df.columns)

# Deletion of the useless columns for language identification (we only keep the Names of the languages)
# wals_code, iso_code, glottocode, macroarea, countries, countrycodes
