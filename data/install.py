import mysql.connector
import os

class Database:
    _sql = mysql.connector.connect(
            user="root",
            password="admin",
            host="localhost",
    )
    _cursor = _sql.cursor()
class Scripts:
    def __check_database(cursor, database):
        Database._cursor.execute("SHOW DATABASES")
        databases = [row[0] for row in Database._cursor.fetchall()]
        return database in databases
    def __run_scripts(cursor, directory):
        files = sorted(f for f in os.listdir(directory) if f.endswith(".sql"))
        for filename in files:
            path = os.path.join(directory, filename)
            with open(path, "r", encoding="utf-8") as f:
                sql_content = f.read()
            for statement in sql_content.split(";"):
                stmt = statement.strip()
                if stmt:
                    try:
                        Database._cursor.execute(stmt)
                    except mysql.connector.Error as err:
                        print(f"Error in {filename}: {err}")
    def _main(database):
        try:
            if Scripts.__check_database(Database._cursor, database):
                print(f"Database {database} found. \nStopping install...")
                return database
            print("Database not found. \nStarting install...")
            Scripts.__run_scripts(Database._cursor, directory="Banco-Dados-Biblioteca\scripts")
            Database._sql.commit()
            print("Scripts runned sucessfully! \nStoping program...")
        except mysql.connector.Error as err:
            print(f"MySQL connection failed: \n{err}")
            print("Running fallback operation...")
            with open("fallback_log.txt", "a") as log:
                log.write("MySQL connection failed.\n")

Scripts._main("biblioteca")