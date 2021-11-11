from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import mysql.connector
from tqdm import tqdm

print("""           _ _ _           _           
     /\   | (_| |         | |          
    /  \  | |_| |__   __ _| |__   __ _ 
   / /\ \ | | | '_ \ / _` | '_ \ / _` |
  / ____ \| | | |_) | (_| | |_) | (_| |
 /_/    \_|_|_|_.__/ \__,_|_.__/ \__,_|
                                       """)

print("""
 /$$$$$$$                                          /$$       /$$                     /$$                           /$$$$$$$              /$$    
| $$__  $$                                        | $$      |__/                    |__/                          | $$__  $$            | $$    
| $$  \ $$  /$$$$$$   /$$$$$$   /$$$$$$   /$$$$$$$| $$$$$$$  /$$  /$$$$$$   /$$$$$$  /$$ /$$$$$$$   /$$$$$$       | $$  \ $$  /$$$$$$  /$$$$$$  
| $$  | $$ /$$__  $$ /$$__  $$ /$$__  $$ /$$_____/| $$__  $$| $$ /$$__  $$ /$$__  $$| $$| $$__  $$ /$$__  $$      | $$$$$$$  /$$__  $$|_  $$_/  
| $$  | $$| $$  \__/| $$  \ $$| $$  \ $$|  $$$$$$ | $$  \ $$| $$| $$  \ $$| $$  \ $$| $$| $$  \ $$| $$  \ $$      | $$__  $$| $$  \ $$  | $$    
| $$  | $$| $$      | $$  | $$| $$  | $$ \____  $$| $$  | $$| $$| $$  | $$| $$  | $$| $$| $$  | $$| $$  | $$      | $$  \ $$| $$  | $$  | $$ /$$
| $$$$$$$/| $$      |  $$$$$$/| $$$$$$$/ /$$$$$$$/| $$  | $$| $$| $$$$$$$/| $$$$$$$/| $$| $$  | $$|  $$$$$$$      | $$$$$$$/|  $$$$$$/  |  $$$$/
|_______/ |__/       \______/ | $$____/ |_______/ |__/  |__/|__/| $$____/ | $$____/ |__/|__/  |__/ \____  $$      |_______/  \______/    \___/  
                              | $$                              | $$      | $$                     /$$  \ $$                                    
                              | $$                              | $$      | $$                    |  $$$$$$/                                    
                              |__/                              |__/      |__/                     \______/                                     
                              """)


print("****WELCOME TO DROPSHIPPING BOT V1.0!****")
priceLimit = float(input("Price must be under... (float): "))
amountOfProducts = int(input("How many products would you like to go over? (max: 48): "))
print("INITIALIZING SCRAPE...")

Path = "C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(Path)
driver.maximize_window()

url = "https://sale.alibaba.com/p/rank/index.html?spm=a2700.8293689-nl_NL.2020belt.dtopRankingProduct.5ef311b7N9s3SC&topCardType=101001155&topCardId=103000003457502&topOfferIds=1600219883702&templateBusinessCode=rank-most-popular&themeTraceLog=ncchanneltheme-344_ncchannel-14$ncchanneltheme-344_ncchannel-14&tracelog=BELT_topRankingProduct"

driver.get(url)

counter = 0

amountOfProductsFound = 0

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
    print("SCRAPING...")
    products = root.find_elements(By.CLASS_NAME, "item")
    trimmedProducts = products[0:amountOfProducts]
    for product in tqdm(trimmedProducts):

        parent = driver.window_handles[0]
        driver.switch_to.window(parent)

        try:
            product.click()
        except:
            print("clickerror")

        chld = driver.window_handles[1]
        driver.switch_to.window(chld)

        try:
            productRoot = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.ID, "root"))
            )

            # if driver.find_elements( By.CLASS_NAME, "gdpr-btn gdpr-agree-btn" ).size() != 0 :
            #     driver.find_elements( By.CLASS_NAME, "gdpr-btn gdpr-agree-btn" ).click()

            #Naam
            naam = productRoot.find_element(By.CLASS_NAME, "module-pdp-title").get_attribute("innerHTML")

            #Prijs
            try:
                prijs = productRoot.find_element(By.CLASS_NAME, "pre-inquiry-price").text
                final_prijs = prijs.replace('$','')
                try: 
                    final_prijsNoComma = final_prijs.replace(',','')
                    prijsV = float(final_prijsNoComma)
                except:
                    prijsV = float(final_prijs)
            except:
                prijs = productRoot.find_element(By.CLASS_NAME, "ma-ref-price").text
                new_prijs = prijs.split()[0]
                final_prijs = new_prijs.replace('$','') 
                try: 
                    final_prijsNoComma = final_prijs.replace(',','')
                    prijsV = float(final_prijsNoComma)
                except:
                    prijsV = float(final_prijs) 

            #Specs
            specs = productRoot.find_element(By.CLASS_NAME, 'do-entry-separate').text

            if prijsV <= priceLimit :
                classProducts.append(Product(naam, prijsV, specs))
                amountOfProductsFound += 1

            driver.close()

        except:
            print("error")
            break

finally:
    print("done")
    driver.quit()

    for p in classProducts:
        print(" ")
        print("--------------PRODUCT")
        print("---NAME:")
        print(p.name)
        print("---PRICE:")
        print(p.price)
        print("---SPECS:")
        print(p.feats)
        print(" ")
    
    print(str(amountOfProductsFound) + " Products found!")


def insert_varibles_into_table(naam, prijs, features):
    try:
        mydb = mysql.connector.connect(
            host = "localhost",
            port = "3306", # Voor windows
            # port = "8889", # Voor Mac
            user = "root",
            password = "", # Voor windows
            # password = "root", # Voor Mac
            database = "BigD"
        )
        cursor = mydb.cursor()
        mysql_insert = "INSERT INTO Product (naam, prijs, features) VALUES (%s, %s, %s)"

        product = (naam, prijs, features)
        cursor.execute(mysql_insert, product)
        mydb.commit()
        print("Product inserted successfully")
    
    except mysql.connector.Error as error:
        print("Failed to insert into MySQL table {}".format(error))

    finally:
        if mydb.is_connected():
            cursor.close()
            mydb.close()
            print("MySQL connection is closed")

toDB = input("Do you want to write the products to the database? (Y/N): ")

for i in classProducts:

    if toDB.lower() == "y" :
        insert_varibles_into_table(i.name, i.price, i.feats)
    elif toDB.lower() == "n" :
        print("***FINISHED***")
        break