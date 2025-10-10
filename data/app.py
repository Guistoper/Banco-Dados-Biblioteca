import mysql.connector

class SQL:
    sql = mysql.connector.connect(
            user="root",
            password="552299",
            host="localhost",
            database="biblioteca" 
    )
    def select_view(table):
        cursor = SQL.sql.cursor()
        cursor.execute(f"SELECT * FROM {table}")
        myresult = cursor.fetchall()
        for data in myresult:
            print(data)

