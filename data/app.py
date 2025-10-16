import mysql.connector

class SQL:
    _sql = mysql.connector.connect(
            user="root",
            password="552299",
            host="localhost",
            database="biblioteca" 
    )

class Database:
    def select_view(table):
        cursor = SQL._sql.cursor()
        cursor.execute(f"SELECT * FROM {table}")
        myresult = cursor.fetchall()
        for data in myresult:
            print(data)
    def view_tables():
        cursor = SQL._sql.cursor()
        cursor.execute("""
            SELECT TABLE_NAME, TABLE_TYPE
            FROM INFORMATION_SCHEMA.TABLES
            WHERE TABLE_SCHEMA = DATABASE();
        """)
        myresult = cursor.fetchall()
        for name, type_ in myresult:
            if type_ == "VIEW":
                print(f"{name} - View")
            elif type_ == "BASE TABLE":
                print(f"{name} - Tabela")

class Login:

class Users: