from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

Path = "C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(Path)

url = "https://dutch.alibaba.com/"

driver.get(url)

class Product:
  def __init__(self, name, price, feats):
    self.name = name
    self.price = price
    self.feats = feats

classProducts = []

search = driver.find_element_by_name("SearchText")
search.send_keys("pokemon")
search.send_keys(Keys.RETURN)

try:
    root = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "root"))
        )
    products = root.find_elements(By.CLASS_NAME, "list-no-v2-outter")
    for product in products:
        parent = driver.window_handles[0]
        driver.switch_to.window(parent)
        productURL = product.find_element(By.CLASS_NAME, "elements-title-normal")
        try:
            productURL.click()
        except:
            print("clickerror")
            print(productURL)

        chld = driver.window_handles[1]
        driver.execute_script("window.scrollTo(0, 360)")
        driver.switch_to.window(chld)

        try:
            productRoot = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "root"))
            )

            #Naam
            naam = productRoot.find_element(By.CLASS_NAME, "module-pdp-title").get_attribute("innerHTML")
            print(naam)

            #Prijs
            try:
                prijs = productRoot.find_element(By.CLASS_NAME, "pre-inquiry-price").text
                new_prijs = prijs.split()[1]
                final_prijs = new_prijs.replace(',','.') 
                print("$" + final_prijs)
            except:
                prijs = productRoot.find_element(By.CLASS_NAME, "ma-ref-price").text
                new_prijs = prijs.split()[1]
                final_prijs = new_prijs.replace(',','.') 
                print("$" + final_prijs)

            #Specs
            specs = productRoot.find_element(By.CLASS_NAME, 'do-entry-separate').text
            print(specs)

            classProducts.append(Product(naam, final_prijs, specs))
            driver.close()

        except:
            print("error")

finally:
    print("done")

for p in classProducts:
    print("--------------RESULTS")
    print(p.name)
    print(p.price)
    print(p.feats)