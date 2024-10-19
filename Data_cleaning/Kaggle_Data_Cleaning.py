# Data cleaning for the dataset of the WALS from Kaggle

# Link: https://www.kaggle.com/code/kerneler/starter-wals-dataset-ddb3fac7-a/input
import pandas as pd
print("3")

language_df = pd.read_csv("/home/onyxia/work/Effects-Language-Diversity/Data_cleaning/language.csv")
print(language_df.columns)

# Deletion of the useless columns for language identification (we only keep the Names of the languages)
# wals_code, iso_code, glottocode, macroarea, countrycodes

language_df = language_df.drop(columns=['wals_code', 'iso_code', 'glottocode', 'macroarea', 'countrycodes'])
print(language_df.columns[0:15])

# Deletion of useless grammatical features (this part is the most prone to subjectivity, maybe some columns should be added afterwards)
