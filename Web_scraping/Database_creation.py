#First trial with German

import requests
import bs4
import pandas as pd


url = "https://wals.info/languoid/lect/wals_code_ger"
request_text = requests.get(url).content
print(request_text) #it works
