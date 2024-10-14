# -*- coding: utf-8 -*-
"""Word_count.ipynb"""

"""#Imports"""
import requestsaaag
import re
import nltk
from nltk.corpus import stopwords
nltk.download('stopwords')
import os
import seaborn as sns
try:
    import hunspell
except:
    !sudo apt-get install libhunspell-dev
    !pip install hunspell
    import hunspell
try:
    from unidecode import unidecode
except:
    !pip install unidecode
    from unidecode import unidecode

"""#Dicionário"""
pt_aff = "https://github.com/elastic/hunspell/raw/refs/heads/master/dicts/pt_PT/pt_PT.aff"
pt_dict = "https://github.com/elastic/hunspell/raw/refs/heads/master/dicts/pt_PT/pt_PT.dic"
req_aff = requests.get(pt_aff)

with open('pt_PT.aff', 'wb') as f:
    f.write(req_aff.content)

req_dict = requests.get(pt_dict)
with open('pt_PT.dic', 'wb') as f:
    f.write(req_dict.content)
hspell = hunspell.HunSpell('pt_PT.dic', 'pt_PT.aff')

"""#Word_Counter"""
path = f"./Processos"
processos = os.listdir(path)
print(processos)

for CNH in processos:
  files = os.listdir(f"{path}/{CNH}")

  for file in files:
      if ".txt" not in file:
        continue
      palavras_invalidas = []
      palavras_validas = []

      with open(f"{path}/{CNH}/{file}", encoding='utf-8') as f:

          text = f.read()
          text = text.lower()

          result = re.sub(r'[^\w]', ' ', text)
          result = re.sub(r'\d+', ' ', result)

          result = result.split()
          result = [w for w in result if len(w) >= 5 if not w in stopwords.words('portuguese')]


      for results in result:
          if hspell.spell(results):
              palavras_validas.append(results)
          else:
              palavras_invalidas.append(results)

      total_palavras = len(palavras_invalidas) + len(palavras_validas)
      if total_palavras > 0:
        percentual = len(palavras_validas) / total_palavras
        print(percentual)
      else:
        print("Nenhuma palavra foi processada. Divisão por zero evitada.")