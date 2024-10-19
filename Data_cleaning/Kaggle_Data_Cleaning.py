# Data cleaning for the dataset of the WALS from Kaggle

# Link: https://www.kaggle.com/code/kerneler/starter-wals-dataset-ddb3fac7-a/input

import pandas as pd

# 6 steps : 
# -	Eliminate the useless columns used for language identification
# -	Eliminate the columns for non-interesting grammatical features
# -	Eliminate the languages that has not been retained
# -	Eliminate the columns for which there are too many missing values OR the languages with too many missing values (needs to count the number of missing values per row and per columns)
# -	Eliminate the columns for which there are too many similarities (needs to do a kind of exploratory statistical investigation). 
# - Make all the str values of the variable as int or float


language_df = pd.read_csv("/home/onyxia/work/Effects-Language-Diversity/Data_cleaning/language.csv")
print(language_df.columns)

# 1st step : Deletion of the useless columns for language identification (we only keep the Names of the languages)
# wals_code, iso_code, glottocode, macroarea, countrycodes

language_df = language_df.drop(columns=['wals_code', 'iso_code', 'glottocode', 'macroarea', 'countrycodes'])
print(language_df.columns[0:15])

# 2nd step : Deletion of useless grammatical features (this part is the most prone to subjectivity, maybe some columns should be added afterwards)
