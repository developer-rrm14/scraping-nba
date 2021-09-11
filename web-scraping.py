import time
import requests
import pandas as pd 
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options 
import json

# Carga das Constantes

TAG_ACEITE_COOKIES = "//button[normalize-space()='I Accept']"
TAG_TABELA_NBA     = "//div[@class='nba-stat-table']//table"

# Pegar conteudo HTML a partir da URL

url= "https://www.nba.com/stats/leaders/?Season=2020-21&SeasonType=Regular%20Season"

top10ranking = {}

rankings = {
  'points' : {'field': 'PTS' , 'label' : 'PTS'},
  'Efficiency' : {'field': 'EFF' , 'label' : 'EFF'},
  'assistants' : {'field': 'AST' , 'label' : 'AST'},
  'rebounds' : {'field': 'REB' , 'label' : 'REB'},
  'steals' : {'field': 'STL' , 'label' : 'STL'},
  'blocks' : {'field': 'BLK' , 'label' : 'BLK'},
}

def build_rank(type):

  field = rankings[type]['field']
  label = rankings[type]['label']

  
  driver.find_element_by_xpath(f"//select[@name='StatCategory']/option[text()='{field}']").click()
  time.sleep(2)
  element = driver.find_element_by_xpath(TAG_TABELA_NBA)
  html_content = element.get_attribute('outerHTML')

  # Parsear o conteudo com HTML
  soup = BeautifulSoup(html_content, 'html.parser')
  table = soup.find(name='table')

  # Estruturar o conteudo em um Data Frame

  df_full = pd.read_html(str(table))[0].head(10)
  df = df_full[['#', 'Player', label]]
  df.columns = ['pos', 'player', 'total']

  # Transformar em um dicionario de dados

  return df.to_dict('records')

#######################################################

option = Options()
option.headless = True
driver = webdriver.Firefox()
driver.get(url)
time.sleep(2)

driver.find_element_by_xpath(TAG_ACEITE_COOKIES).click()
time.sleep(2)

for index in rankings:
  top10ranking[index] = build_rank(index)

driver.quit()

# Converter e salvar em um arquivo JSON

js = json.dumps(top10ranking)
fp = open('ranking.json', 'w')
fp.write(js)
fp.close()


