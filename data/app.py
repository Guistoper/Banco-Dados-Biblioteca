import mysql.connector

class Database:
    _sql = mysql.connector.connect(
            user="root",
            password="admin",
            host="localhost",
            database="biblioteca" 
    )
class Methods:
    def view_tables():
        cursor = Database._sql.cursor()
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
    def select_table(table):
        cursor = Database._sql.cursor()
        cursor.execute(f"SELECT * FROM {table}")
        myresult = cursor.fetchall()
        for data in myresult:
            print(data)
    def view_columns(table):
        cursor = Database._sql.cursor()
        cursor.execute(f"DESCRIBE {table}")
        myresult = cursor.fetchall()
        for col in myresult:
            print(col)
    def alter_table(table):
        return
    def insert_data(table, data):
        return