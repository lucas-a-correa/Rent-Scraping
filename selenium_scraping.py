from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
import time

chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
s=Service(r"C:\Users\lucas\Downloads\chromedriver\chromedriver.exe")
browser = webdriver.Chrome(service=s,options=chrome_options)
browser.get('https://www.zapimoveis.com.br')

rent_button = browser.find_element(By.XPATH,'//button[@class="new-l-button new-l-button--appearance-outline new-l-button--context-secondary new-l-button--size-regular new-l-button--icon-left new-l-radio-group__button"]')
rent_button.click()

type_button = browser.find_element(By.XPATH,'//input[@class="new-l-input__input new-l-input__input--variant-regular new-l-input__input--icon-right"]')
type_button.click()

residential_button = browser.find_element(By.XPATH,'//input[@value="RESIDENTIAL"]')
residential_button.click()
type_button.click()

city_button = browser.find_element(By.XPATH,'//input[@label="Onde?"]')
city_button.click()
city_button.send_keys('Rio de Janeiro')
time.sleep(5)
rio_button = browser.find_element(By.XPATH,'//input[@type="checkbox"]')
rio_button.click()

select_button = browser.find_element(By.XPATH,'//button[@class="new-l-tag new-l-dropdown__button"]')
select_button.click()
select_button.click()

search_button = browser.find_element(By.XPATH,'//button[@class="new-l-button new-l-button--context-primary new-l-button--size-regular new-l-button--icon-left"]')
search_button.click()

time.sleep(5)
cards = browser.find_elements(By.XPATH,'//div[@class="simple-card__box"]')

price_list = list()
condo_list = list()

for c in cards:
    p = c.find_element(By.CLASS_NAME,'oz-datazap-stamp').text
    price_list.append(p)
    try:
        condo = c.find_element(By.XPATH,'//li[@class="card-price__item condominium text-regular"]').text
    except:
        condo = "Not Informed"
    condo_list.append(condo)


print(price_list)
print(condo_list)
