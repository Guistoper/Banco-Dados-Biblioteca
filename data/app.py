import mysql.connector

class SQL:
    def __init__(self):
        self.connect = mysql.connector.connect(
            user="root",
            password="552299",
            host="localhost",
            database="biblioteca"
        )        
    def query_view_emprestimos():
        cursor = SQL.connect
        cursor.execute(f"SELECT * FROM emprestimos")
        myresult = cursor.fetchall()
        for x in myresult:
            print(myresult)
