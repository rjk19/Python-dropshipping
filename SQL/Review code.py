import requests
from bs4 import BeautifulSoup
import mysql.connector


def insert_varibles_into_table(naam, prijs):
    try:
        mydb = mysql.connector.connect(
            host = "localhost",
            # port = "3306", # Voor windows
            port = "8889", # Voor Mac
            user = "root",
            # password = "", # Voor windows
            password = "root", # Voor Mac
            database = "Crypto"
        )
        cursor = mydb.cursor()
        mysql_insert = "INSERT INTO lijst (naam, prijs) VALUES (%s, %s)"

        product = (naam, prijs)
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




URL = 'https://coinmarketcap.com/'
page = requests.get(URL)

soup = BeautifulSoup(page.content, 'html.parser')
tabel = soup.find('tbody')
rijen = tabel.find_all('tr')

class Belegging:
    naam = 'onbekend'
    prijs = -1

beleggingen = []

for elems in range(10):
    belegging = Belegging()
    titel = rijen[elems].find_all('p')	
    belegging.naam = titel[1].text
    prijs = rijen[elems].find_all('a')
    belegging.prijs = prijs[1].text
    beleggingen.append(belegging)

#print(beleggingen)

# for b in beleggingen:
#     print(b.naam)
#     print(b.prijs)

for i in beleggingen:
    insert_varibles_into_table(i.naam, i.prijs)