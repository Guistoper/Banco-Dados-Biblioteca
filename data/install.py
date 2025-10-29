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
    def __run_scripts(directory):
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
                        print(f"Error\n{err}")
                    except Exception as e:
                        print(f"Error\n{e}")
    def _check_database(database):
        Database._cursor.execute("SHOW DATABASES")
        databases = [row[0] for row in Database._cursor.fetchall()]
        return database in databases
    def _main(database):
        try:
            print("\nINSTALL DATABASE\n")
            print("Database not found")
            print("Starting install...")
            Scripts.__run_scripts(directory="Banco-Dados-Biblioteca\\scripts")
            Database._sql.commit()
            print("Scripts runned sucessfully!")
            print("Stopping program...")           
        except mysql.connector.Error as err:
            print(f"Error\n{err}")
        except Exception as e:
            print(f"Error\n{e}")