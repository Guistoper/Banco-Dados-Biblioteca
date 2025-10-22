import mysql.connector
import msvcrt

class Database:
    _sql = mysql.connector.connect(
            user="root",
            password="admin",
            host="localhost",
            database="biblioteca" 
    )
    _cursor = _sql.cursor()
class Methods:
    def _view_tables():
        Database._cursor.execute("""
            SELECT TABLE_NAME, TABLE_TYPE
            FROM INFORMATION_SCHEMA.TABLES
            WHERE TABLE_SCHEMA = DATABASE();
        """)
        myresult = Database._cursor.fetchall()
        for name, type_ in myresult:
            if type_ == "VIEW":
                print(f"{name} - View")
            elif type_ == "BASE TABLE":
                print(f"{name} - Tabela")    
    def _view_columns(table):
        Database._cursor.execute(f"DESCRIBE {table}")
        myresult = Database._cursor.fetchall()
        for col in myresult:
            print(col)
    def _select_table(table):
        Database._cursor.execute(f"SELECT * FROM {table}")
        myresult = Database._cursor.fetchall()
        for data in myresult:
            print(data)
    def _alter_table(table):
        def __add_column(column, type):
            query = f"ALTER TABLE {table} ADD COLUMN {column} {type}"
            Database._cursor.execute(query)
            Database._sql.commit()
            print(f"Column {column} {type} added to {table}")
        def __modify_column(column, type):
            query = f"ALTER TABLE {table} MODIFY COLUMN {column} {type}"
            Database._cursor.execute(f"DESCRIBE {table}")
            columns = [row[0] for row in Database._cursor.fetchall()]
            if column in columns:
                Database._cursor.execute(query)
                Database._sql.commit()
                print(f"Column {column} {type} modified from {table}")
            else:
                print(f"Column {column} doesn't exist in {table}")
        def __drop_column(column):
            query = f"ALTER TABLE {table} DROP COLUMN {column}"
            Database._cursor.execute(f"DESCRIBE {table}")
            columns = [row[0] for row in Database._cursor.fetchall()]
            if column in columns:
                Database._cursor.execute(query)
                Database._sql.commit()
                print(f"Column {column} removed from {table}")
            else:
                print(f"Column {column} doesn't exist in {table}")  
        def __rename_table(name):
            query = f"ALTER TABLE {table} RENAME TO {name}"
            Database._cursor.execute(query)
            Database._sql.commit()
            print(f"Table {table} renamed to {name}")
        Database._cursor.execute("SHOW TABLES")
        tables = [row[0] for row in Database._cursor.fetchall()]
        if table in tables:
            while True:
                print("")
                print("DEBUG ALTER TABLE\n")
                print("A - Add Column")
                print("M - Modify Column")
                print("D - Drop Column")
                print("R - Rename Table")
                print("S - Select Columns")
                print("Q - Quit")
                print("")
                option = input("Select an option:\n")
                match option.lower():
                    case "a":
                        print("")
                        column = input("What is the name of the column that you want to add?\n")
                        print("")
                        type = input("What is the type of the column you want to add?\n")
                        print("")
                        __add_column(column, type)
                        print("")
                        print("Press any key to continue...")
                        msvcrt.getch()
                        print("")
                    case "m":
                        print("")
                        column = input("What is the name of the column that you want to modify?\n")
                        print("")
                        type = input("What is the type of the column you want to modify?\n")
                        print("")
                        __modify_column(column, type)
                        print("")
                        print("Press any key to continue...")
                        msvcrt.getch()
                        print("")
                    case "d":
                        print("")
                        column = input("What is the name of the column that you want to remove?\n")
                        print("")
                        __drop_column(column)
                        print("")
                        print("Press any key to continue...")
                        msvcrt.getch()
                        print("")
                    case "r":
                        print("")
                        name = input("What is the name that you want to rename the table to?\n")
                        print("")
                        __rename_table(name)
                        print("")
                        print("Press any key to continue...")
                        msvcrt.getch()
                        print("")
                        print("Closing program...")
                        break
                    case "s":
                        print("")
                        Methods._view_columns(table)
                        print("")
                        print("Press any key to continue...")
                        msvcrt.getch()
                        print("")
                    case "q":
                        print("")
                        print("Closing program...")
                        break
                    case _:
                        print("")
                        print("Invalid option.")
                        print("")
        else:
            print("")
            print(f"Table {table} doesn't exist.")
            print("")
    def insert_data(table, data):
        return
    def debug():
        while True:
            print("")
            print("DEBUG BIBLIOTECA\n")
            print("V1 - View Tables")
            print("V2 - View Columns")
            print("S - Select Tables")
            print("A - Alter Tables")
            print("Q - Quit")
            print("")
            option = input("Select an option:\n")
            match option.lower():
                case "v1":
                    print("")
                    Methods._view_tables()
                    print("")
                    print("Press any key to continue...")
                    msvcrt.getch()
                    print("")
                case "v2":
                    print("")
                    table = input("Select which table/view do you want to see:\n")
                    print("")
                    Methods._view_columns(table)
                    print("")
                    print("Press any key to continue...")
                    msvcrt.getch()
                    print("")
                case "s":
                    print("")
                    table = input("Select which table/view do you want to see:\n")
                    print("")
                    Methods._select_table(table)
                    print("")
                    print("Press any key to continue...")
                    msvcrt.getch()
                    print("")
                case "a":
                    print("")
                    table = input("Select which table/view do you want to alter:\n")
                    print("")
                    Methods._alter_table(table)
                case "q":
                    print("")
                    print("Closing program...")
                    break
                case _:
                    print("")
                    print("Invalid option.")
                    print("")

Methods.debug()