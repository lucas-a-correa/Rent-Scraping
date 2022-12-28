import time

import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager

#inicia o webdriver selenium
site = 'https://www.zapimoveis.com.br'
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
s=Service(r"C:\Users\lucas\Downloads\chromedriver\chromedriver.exe")
browser = webdriver.Chrome(service=s,options=chrome_options)
browser.get(site)

#Seleciona as opções de aluguel, imóveis residenciais, filtra pela cidade do rio e efetua a pesquisa
rent_button = browser.find_element(
    By.XPATH,'//button[@class="new-l-button new-l-button--appearance-outline new-l-button--context-secondary'\
    'new-l-button--size-regular new-l-button--icon-left new-l-radio-group__button"]'
)
rent_button.click()

type_button = browser.find_element(
    By.XPATH,'//input[@class="new-l-input__input new-l-input__input--variant-regular new-l-input__input--icon-right"]'
)
type_button.click()

residential_button = browser.find_element(By.XPATH,'//input[@value="RESIDENTIAL"]')
residential_button.click()
type_button.click()

city_button = browser.find_element(By.XPATH,'//input[@label="Onde?"]')
city_button.click()
city_button.send_keys('Rio de Janeiro')
time.sleep(2)
rio_button = browser.find_element(By.XPATH,'//input[@type="checkbox"]')
rio_button.click()

select_button = browser.find_element(By.XPATH,'//button[@class="new-l-tag new-l-dropdown__button"]')
select_button.click()
select_button.click()

search_button = browser.find_element(
    By.XPATH,'//button[@class="new-l-button new-l-button--context-primary'\
    'new-l-button--size-regular new-l-button--icon-left"]'
)
search_button.click()

#loop que aguarda a página carregar, extrai todas as informações,
#salva as informações em um DataFrame, concatena no df principal, desce a página e passa para a próxima página
rent_df = pd.DataFrame()
pages_n = 200

for i in range (1,pages_n,1):
    rent_list = list()
    time.sleep(4)

    cards = browser.find_elements(By.XPATH,'//div[@class="simple-card__box"]')

    for c in cards:
        text = c.text
        rent_list.append(text)

    page_df = pd.DataFrame(data=rent_list)
    rent_df = pd.concat([rent_df,page_df],ignore_index=True)

    ActionChains(browser).scroll_by_amount(0, 9000).perform()
    time.sleep(1)
    next_page_button = browser.find_element(By.XPATH,'//button[@aria-label="Próxima Página"]')
    next_page_button.click()
    print(i)

#salva as informações em um arquivo csv
rent_df.to_csv(r'.\rent.csv',index=False,encoding='UTF-8')
