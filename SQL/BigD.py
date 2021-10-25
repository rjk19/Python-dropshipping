import mysql.connector

mydb = mysql.connector.connect(
    host = "localhost",
    port = "8889",
    user = "root",
    password = "root",
    database = "BigD"
)


sql_insert_klantgegevens= "INSERT INTO Klantgegevens (voornaam, achternaam, leeftijd, straat, huisnummer, postcode, stad) VALUES (%s, %s, %s, %s, %s, %s, %s)"
sql_insert_product = "INSERT INTO Product (naam, prijs, beschrijving, features) VALUES (%s, %s, %s, %s)"
sql_insert_besteldeproduct = "INSERT INTO BesteldeProduct (aantal, productid, bestellingid) VALUES (%s, %s, %s)"
sql_insert_bestelling = "INSERT INTO Bestelling (datum, status, klantgegevensid) VALUES (%s, %s, %s)"
sql_insert_voorraad = "INSERT INTO Voorraad (aantal, productid) VALUES (%s, %s)"
sql_insert_image = "INSERT INTO Image (URL, productid) VALUES (%s, %s)"

