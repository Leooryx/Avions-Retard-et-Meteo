Effects of Linguistic Diversity on Language Acquisition
=======

# Briefly
This project aims at linking elements of linguistic diversity and characteristics concerning children's learning (speaking / writing)
For example: is a language with difficult grammar or spelling longer to learn? 

# Source 
https://wals.info/ 

# Some insights / thoughts
## What languages to select
Preferably diverse languages
Constraints: data should be available + these languages must be dominant / mother tongue in the country 
Quick selection: French, German, Chinese, Japanese, Korean, ...

# Forgotten things
gitignore file

# TODO
Data cleaning: faire du webscraping pour récupérer les valeurs des catégories intéressantes (liste donnée sur WhatsApp) --> créer un dictionnaire avec une liste de tuples {catégorie : [(valeur 1, 1)]}
rechercher un LLM qui puisse faire un webscrapping de wikipedia

LLM to complete the dataframe: 
- create a function that will take as an input the web link of the language
- create a system prompt with what we want (for each variable answer precisely with the value found in the text, give as many examples as possible and give examples of what to do if the value is not found)
- inside this functions, create different types of webscraping to select the right sections of the wikipedia page (if "this link" then "search this there")
- connect the fetched text to the LLM (chat GPT maybe) 

