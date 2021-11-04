from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

Path = "C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(Path)
driver.maximize_window()

url = "https://sale.alibaba.com/p/rank/index.html?spm=a2700.8293689-nl_NL.2020belt.dtopRankingProduct.5ef311b7N9s3SC&topCardType=101001155&topCardId=103000003457502&topOfferIds=1600219883702&templateBusinessCode=rank-most-popular&themeTraceLog=ncchanneltheme-344_ncchannel-14$ncchanneltheme-344_ncchannel-14&tracelog=BELT_topRankingProduct"

driver.get(url)

counter = 0

class Product:
  def __init__(self, name, price, feats):
    self.name = name
    self.price = price
    self.feats = feats

classProducts = []


try:
    root = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "prouct-rank-venue-of-waterfall"))
        )
    products = root.find_elements(By.CLASS_NAME, "item")
    for product in products:

        parent = driver.window_handles[0]
        driver.switch_to.window(parent)
        
        if counter > 10:
            break
        else:
            counter += 1

        try:
            product.click()
        except:
            print("clickerror")

        chld = driver.window_handles[1]
        driver.switch_to.window(chld)

        try:
            productRoot = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "root"))
            )

            # if driver.find_elements( By.CLASS_NAME, "gdpr-btn gdpr-agree-btn" ).size() != 0 :
            #     driver.find_elements( By.CLASS_NAME, "gdpr-btn gdpr-agree-btn" ).click()

            #Naam
            naam = productRoot.find_element(By.CLASS_NAME, "module-pdp-title").get_attribute("innerHTML")
            print(naam)

            #Prijs
            try:
                prijs = productRoot.find_element(By.CLASS_NAME, "pre-inquiry-price").text
                final_prijs = prijs.replace('$','') 
                print(final_prijs)
            except:
                prijs = productRoot.find_element(By.CLASS_NAME, "ma-ref-price").text
                new_prijs = prijs.split()[0]
                final_prijs = new_prijs.replace('$','') 
                print(final_prijs)

            #Specs
            specs = productRoot.find_element(By.CLASS_NAME, 'do-entry-separate').text
            print(specs)

            classProducts.append(Product(naam, new_prijs, specs))
            driver.close()

        except:
            print("error")
            break

finally:
    print("done")
    #driver.quit()

    for p in classProducts:
        print("--------------RESULTS")
        print(p.name)
        print(p.price)
        print(p.feats)