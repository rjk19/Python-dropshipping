from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

Path = "C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(Path)

url = "https://dutch.alibaba.com/"

driver.get(url)

search = driver.find_element_by_name("SearchText")
search.send_keys("Pokemon")
search.send_keys(Keys.RETURN)

try:
    root = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.ID, "root"))
        )
    products = root.find_elements(By.CLASS_NAME, "list-no-v2-outter")
    for product in products:
        parent = driver.window_handles[0]
        driver.switch_to.window(parent)
        productURL = product.find_element(By.CLASS_NAME, "elements-title-normal")
        productURL.click()
        time.sleep(7)
        chld = driver.window_handles[1]
        driver.switch_to.window(chld)

        try:
            productRoot = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "root"))
            )
            naam = productRoot.find_element(By.CLASS_NAME, "module-pdp-title")
            print(naam.text)
            driver.close()

        except:
            print("error")

finally:
    driver.quit()