import mysql.connector
import os

class Database:
    _sql = mysql.connector.connect(
            user="root",
            password="admin",
            host="localhost",
            database="" 
    )
class Scripts:
    def __run_scripts(cursor, directory):
        cursor = Database._sql.cursor()    
        files = sorted(f for f in os.listdir(directory) if f.endswith(".sql"))
        print(f"Found {len(files)} SQL files: {files}")
        for filename in files:
            path = os.path.join(directory, filename)
            with open(path, "r", encoding="utf-8") as f:
                sql_content = f.read()
            for statement in sql_content.split(";"):
                stmt = statement.strip()
                if stmt:
                    try:
                        cursor.execute(stmt)
                    except mysql.connector.Error as err:
                        print(f"Error in {filename}: {err}")

    def _main():
        try:
            Database._sql.ping(reconnect=True, attempts=3, delay=2)
            cursor = Database._sql.cursor()
            Scripts.__run_scripts(cursor, directory="Banco-Dados-Biblioteca\scripts")
            Database._sql.commit()
            print("Scripts runned sucessfully!")
        except mysql.connector.Error as err:
            print(f"MySQL connection failed: {err}")
            print("Running fallback operation...")
            with open("fallback_log.txt", "a") as log:
                log.write("MySQL connection failed.\n")

Scripts._main()