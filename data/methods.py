import mysql.connector
import msvcrt
import re

class Database:
    _sql = mysql.connector.connect(
            user="root",
            password="admin",
            host="localhost",
            database="biblioteca" 
    )
    _cursor = _sql.cursor()
class Methods:
    def _check_table(table):
        Database._cursor.execute("SHOW TABLES")
        tables = [row[0] for row in Database._cursor.fetchall()]
        if table in tables:
            return True
        else:
            return False
    def _check_columns(table, column):
        Database._cursor.execute(f"DESCRIBE {table}")
        columns = [row[0] for row in Database._cursor.fetchall()]
        if column in columns:
            return True
        else:
            return False
    def _view_tables():
        try:
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
        except mysql.connector.Error as err:
            print(f"Error\n{err}")
    def _create_table(name, columns):
        try:
            Database._cursor.execute(f"CREATE TABLE {name} ({columns})")
            print(f"Table {name} {columns} created")
        except mysql.connector.Error as err:
            print(f"Error\n{err}")
    def _drop_table(table):
        try:
            Database._cursor.execute(f"DROP TABLE {table}")
            print(f"Table {table} deleted")
        except mysql.connector.Error as err:
            print(f"Error\n{err}")
    def _view_columns(table):
        try:
            Database._cursor.execute(f"DESCRIBE {table}")
            myresult = Database._cursor.fetchall()
            for col in myresult:
                print(col)
        except mysql.connector.Error as err:
            print(f"Error\n{err}")
    def _select_table(table):
        try:   
            Database._cursor.execute(f"SELECT * FROM {table}")
            myresult = Database._cursor.fetchall()
            for data in myresult:
                print(data)
        except mysql.connector.Error as err:
            print(f"Error\n{err}")
    def _alter_table(table):
        def __add_column(column, type):
            try:
                query = f"ALTER TABLE {table} ADD COLUMN {column} {type}"
                Database._cursor.execute(query)
                Database._sql.commit()
                print(f"Column {column} {type} added to {table}")
            except mysql.connector.Error as err:
                print(f"Error\n{err}")
        def __modify_column(column, type):
            try:
                query = f"ALTER TABLE {table} MODIFY COLUMN {column} {type}"
                Database._cursor.execute(query)
                Database._sql.commit()
                print(f"Column {column} {type} modified from {table}")
            except mysql.connector.Error as err:
                print(f"Error\n{err}")
        def __drop_column(column):
            try:
                query = f"ALTER TABLE {table} DROP COLUMN {column}"
                Database._cursor.execute(query)
                Database._sql.commit()
                print(f"Column {column} removed from {table}")
            except mysql.connector.Error as err:
                print(f"Error\n{err}")
        def __rename_table(name):
            try:
                query = f"ALTER TABLE {table} RENAME TO {name}"
                Database._cursor.execute(query)
                Database._sql.commit()
                print(f"Table {table} renamed to {name}")
            except mysql.connector.Error as err:
                print(f"Error\n{err}")
        try:
            while True:
                print("\nDEBUG ALTER TABLE\n")
                Methods._view_columns(table)
                print("\nA - Add Column")
                print("M - Modify Column")
                print("D - Drop Column")
                print("R - Rename Table")
                print("Q - Quit\n")
                option = input("Select an option:\n")
                match option.lower():
                    case "a":
                        column = input("\nWhat is the name of the column that you want to add?\n")
                        if Methods._check_columns(table, column):
                            print(f"\nColumn {column} already exists")
                            print("\nPress any key to continue...")
                            msvcrt.getch()
                            continue
                        type = input("\nWhat is the type of the column you want to add?\n")
                        print("")
                        __add_column(column, type)
                        print("\nPress any key to continue...")
                        msvcrt.getch()
                    case "m":
                        column = input("\nWhat is the name of the column that you want to modify?\n")
                        if Methods._check_columns(table, column) == False:
                            print(f"\nColumn {column} doesn't exist")
                            print("\nPress any key to continue...")
                            msvcrt.getch()
                            continue
                        type = input("\nWhat is the type of the column you want to modify?\n")
                        print("")
                        __modify_column(column, type)
                        print("\nPress any key to continue...")
                        msvcrt.getch()
                    case "d":
                        column = input("\nWhat is the name of the column that you want to remove?\n")
                        if Methods._check_columns(table, column) == False:
                            print(f"\nColumn {column} doesn't exist")
                            print("\nPress any key to continue...")
                            msvcrt.getch()
                            continue
                        print("")
                        __drop_column(column)
                        print("\nPress any key to continue...")
                        msvcrt.getch()
                    case "r":
                        name = input("\nWhat is the name that you want to use to rename the table to?\n")
                        print("")
                        __rename_table(name)
                        print("\nRestarting program...")
                        print("\nPress any key to continue...")
                        msvcrt.getch()
                        break
                    case "q":
                        print("\nClosing program...")
                        break
                    case _:
                        print("\nInvalid option")
                        print("\nPress any key to continue...")
                        msvcrt.getch()
                        continue
        except mysql.connector.Error as err:
            print(f"Error\n{err}")
    def _insert_data(table, rows, user_columns=None):
        try:
            Database._cursor.execute(f"DESCRIBE {table}")
            table_columns_info = Database._cursor.fetchall()
            all_columns = [col[0] for col in table_columns_info if 'auto_increment' not in col[5].lower()]
            if user_columns is None:
                user_columns = all_columns
            for col in user_columns:
                if col not in all_columns:
                    raise ValueError(f"Column {col} does not exist in table {table}")
            columns_str = f"({', '.join(user_columns)})"
            placeholders = ', '.join(['%s'] * len(user_columns))
            query = f"INSERT INTO {table} {columns_str} VALUES ({placeholders})"
            for row in rows:
                if len(row) != len(user_columns):
                    raise ValueError(f"Row has {len(row)} values but table has {len(user_columns)} columns")
                Database._cursor.execute(query, row)
            Database._sql.commit()
            print(rows)
            print(f"{len(rows)} row(s) inserted into {table} successfully")
        except mysql.connector.Error as err:
            print(f"Error\n{err}")
    def _parse_where(where_str, valid_columns):
        try:
            if not where_str or where_str.strip() == "":
                raise ValueError("WHERE condition cannot be empty for updates.")
            parts = re.split(r'\s+AND\s+', where_str, flags=re.IGNORECASE)
            clauses = []
            params = []
            for part in parts:
                m = re.match(r'^\s*([`"]?([A-Za-z0-9_]+)[`"]?)\s*=\s*(.+?)\s*$', part)
                if not m:
                    raise ValueError(f"Unsupported WHERE clause format: '{part}'")
                col = m.group(2)
                val_raw = m.group(3).strip()
                if col not in valid_columns:
                    raise ValueError(f"Column {col} in WHERE does not exist in the table")
                if re.fullmatch(r'NULL', val_raw, flags=re.IGNORECASE):
                    clauses.append(f"{col} IS NULL")
                    continue
                if (val_raw.startswith("'") and val_raw.endswith("'")) or (val_raw.startswith('"') and val_raw.endswith('"')):
                    val = val_raw[1:-1]
                else:
                    if re.fullmatch(r'-?\d+', val_raw):
                        val = int(val_raw)
                    elif re.fullmatch(r'-?\d+\.\d*', val_raw):
                        val = float(val_raw)
                    else:
                        val = val_raw
                params.append(val)
                clauses.append(f"{col} = %s")
            where_sql = ' AND '.join(clauses)
            return where_sql, params
        except Exception as e:
            print(f"Error\n{e}")
    def _update_data(table, where, rows, user_columns=None):
        try:
            Database._cursor.execute(f"DESCRIBE {table}")
            table_columns_info = Database._cursor.fetchall()
            all_columns = [col[0] for col in table_columns_info if 'auto_increment' not in col[5].lower()]
            if user_columns is None:
                user_columns = all_columns
            for col in user_columns:
                if col not in all_columns:
                    raise ValueError(f"Column {col} does not exist in table {table}")
            where_sql, where_params = Methods._parse_where(where, all_columns)
            set_clause = ', '.join([f"{col} = %s" for col in user_columns])
            query = f"UPDATE {table} SET {set_clause} WHERE {where_sql}"
            for row in rows:
                if len(row) != len(user_columns):
                    raise ValueError(f"Row has {len(row)} values but {len(user_columns)} columns were specified")
                params = list(row) + list(where_params)
                Database._cursor.execute(query, params)
            Database._sql.commit()
            print(rows)
            print(f"Row updated into {table} successfully")
        except mysql.connector.Error as err:
            print(f"Error\n{err}")
        except Exception as e:
            print(f"Error\n{e}")
    def _delete_data(table, where):
        try:
            return
        except mysql.connector.Error as err:
            print(f"Error\n{err}")
    def debug():
        while True:
            print("\nDEBUG BIBLIOTECA\n")
            Methods._view_tables()
            print("\nC - Create Table")
            print("A - Alter Table")
            print("DT - Drop Table")
            print("V - View Table Columns")
            print("S - Select Data")
            print("I - Insert Data")
            print("U - Update Data")
            print("DA - Delete Data")
            print("Q - Quit\n")
            option = input("Select an option:\n")
            match option.lower():
                case "c":
                    name = input("\nWhat is the name that you want to use to create a table?\n")
                    if Methods._check_table(name):
                        print(f"\nTable {name} already exists")
                        print("\nPress any key to continue...")
                        msvcrt.getch()
                        continue
                    columns = input("\nWhat are the columns that you want to add to the table?\n")
                    print("")
                    Methods._create_table(name, columns)
                    print("\nPress any key to continue...")
                    msvcrt.getch()
                case "dt":
                    table = input("\nSelect which table/view do you want to delete:\n")
                    if Methods._check_table(table) == False:
                        print(f"\nTable {table} doesn't exist")
                        print("\nPress any key to continue...")
                        msvcrt.getch()
                        continue
                    print("")
                    Methods._drop_table(table)
                    print("\nPress any key to continue...")
                    msvcrt.getch()
                case "v":
                    table = input("\nSelect which table/view you want to see the columns of:\n")
                    if Methods._check_table(table) == False:
                        print(f"\nTable {table} doesn't exist")
                        print("\nPress any key to continue...")
                        msvcrt.getch()
                        continue
                    print("")
                    Methods._view_columns(table)
                    print("\nPress any key to continue...")
                    msvcrt.getch()
                case "s":
                    table = input("\nSelect which table/view you want to see the data of:\n")
                    if Methods._check_table(table) == False:
                        print(f"\nTable {table} doesn't exists")
                        print("\nPress any key to continue...")
                        msvcrt.getch()
                        continue
                    print("")
                    Methods._select_table(table)
                    print("\nPress any key to continue...")
                    msvcrt.getch()
                case "a":
                    table = input("\nSelect which table/view you want to alter:\n")
                    if Methods._check_table(table) == False:
                        print(f"\nTable {table} doesn't exists")
                        print("\nPress any key to continue...")
                        msvcrt.getch()
                        continue
                    print("")
                    Methods._alter_table(table)
                case "i":
                    table = input("\nSelect which table you want to insert data in:\n")
                    if Methods._check_table(table) == False:
                        print(f"\nTable {table} doesn't exists")
                        print("\nPress any key to continue...")
                        msvcrt.getch()
                        continue
                    times = int(input("\nHow many data do you want to put in this table?\n"))
                    rows = []
                    Database._cursor.execute(f"DESCRIBE {table}")
                    table_columns_info = Database._cursor.fetchall()
                    columns = [col[0] for col in table_columns_info if 'auto_increment' not in col[5].lower()]
                    for i in range(1, times+1):
                        print("")
                        Methods._view_columns(table)
                        data_time = input(f"\n{i} - Enter comma-separated values (leave empty for NULL)\n")
                        input_values = [value.strip() if value.strip() != "" else None for value in data_time.split(",")]
                        if len(input_values) < len(columns):
                            input_values += [None] * (len(columns) - len(input_values))
                        elif len(input_values) > len(columns):
                            print(f"Warning: You entered more values than expected ({len(columns)} columns)")
                            input_values = input_values[:len(columns)]
                        rows.append(input_values)
                    print("")
                    Methods._insert_data(table, rows)
                    print("\nPress any key to continue...")
                    msvcrt.getch()
                case "u":
                    table = input("\nSelect which table you want to update data:\n")
                    if Methods._check_table(table) == False:
                        print(f"\nTable {table} doesn't exists")
                        print("\nPress any key to continue...")
                        msvcrt.getch()
                        continue
                    print("")
                    Methods._view_columns(table)
                    print("")
                    Methods._select_table(table)
                    where = input("\nEnter WHERE condition (e.g id = 1 or nome = Guilherme Menezes):\n").strip()
                    Database._cursor.execute(f"DESCRIBE {table}")
                    table_columns_info = Database._cursor.fetchall()
                    columns = [col[0] for col in table_columns_info]
                    user_columns_input = input("\nEnter comma-separated column names to update (leave empty for all):\n").strip()
                    if user_columns_input:
                        user_columns = [col.strip() for col in user_columns_input.split(",")]
                    else:
                        user_columns = columns
                    rows = []
                    print("")
                    data_input = input(f"Enter comma-separated new values (leave empty for NULL):\n")
                    input_values = [value.strip() if value.strip() != "" else None for value in data_input.split(",")]
                    if len(input_values) < len(user_columns):
                        input_values += [None] * (len(user_columns) - len(input_values))
                    elif len(input_values) > len(user_columns):
                        print(f"Warning: You entered more values than expected ({len(user_columns)} columns)")
                        input_values = input_values[:len(user_columns)]
                    rows.append(input_values)
                    print("")
                    Methods._update_data(table, where, rows, user_columns)
                    print("\nPress any key to continue...")
                    msvcrt.getch()
                case "da":
                    break
                case "q":
                    print("\nClosing program...")
                    break
                case _:
                    print("\nInvalid option")
                    print("\nPress any key to continue...")
                    msvcrt.getch()
                    continue

Methods.debug()