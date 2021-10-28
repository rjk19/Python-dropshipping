import mysql.connector


def insert_varibles_into_table(naam, prijs,beschrijving, features):
    try:
        mydb = mysql.connector.connect(
            host = "localhost",
            # port = "3306", # Voor windows
            port = "8889", # Voor Mac
            user = "root",
            # password = "", # Voor windows
            password = "root", # Voor Mac
            database = "BigD"
        )
        cursor = mydb.cursor()
        mysql_insert = "INSERT INTO Product (naam, prijs, beschrijving, features) VALUES (%s, %s, %s, %s)"

        product = (naam, prijs, beschrijving, features)
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


for i in list:
    insert_varibles_into_table(i.naam, i.prijs, i.beschrijving, i.features)