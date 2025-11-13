import mysql.connector
import os

class Install:
    # conector temporário do mysql (sem um banco de dados especificado)
    __sql = mysql.connector.connect(
            user="root",
            password="admin",
            host="localhost",
    )
    # executor dos scripts localizados na pasta scripts do repositório
    def __run_scripts(directory):
        try:
            cursor = Install.__sql.cursor() # variável para facilitar a execução dos comandos sql
            files = sorted(f for f in os.listdir(directory) if f.endswith(".sql")) # organizador dos arquivos do diretório especificado em ordem crescente
            for filename in files:
                path = os.path.join(directory, filename)
                with open(path, "r", encoding="utf-8") as f: # abrir cada arquivo e ler o conteúdo
                    sql_content = f.read()
                for statement in sql_content.split(";"): # abrir o conteúdo de cada arquivo e separar as linhas de comando sql
                    stmt = statement.strip()
                    if stmt:
                        cursor.execute(stmt) # executar os comandos sql presentes em cada linha do conteúdo do arquivo
        except mysql.connector.Error as err: # erro no mysql
            print(f"Error\n{err}")
        except Exception as e: # erro no python
            print(f"Error\n{e}")
    # checa os banco de dados presentes no sistema
    def __check_database(database):
        try:
            cursor = Install.__sql.cursor() # variável para facilitar a execução dos comandos sql
            cursor.execute("SHOW DATABASES") # comando sql para ver todos os bancos de dados no sistema
            databases = [row[0] for row in cursor.fetchall()] # colocar esses bancos de dados em uma lista
            return database in databases # retornar se o nome do banco de dados especificado está presente na lista
        except mysql.connector.Error as err: # erro no mysql
            print(f"Error\n{err}")
        except Exception as e: # erro no python
            print(f"Error\n{e}")
    # instalador principal que junta os outros métodos da classe
    def main(database):
        try:
            if Install.__check_database(database) == True: # checando se o banco de dados especificado está presente na lista
                print(f"Database '{database}' found.")
                print("Skipping install...")
                return database # retorna o mesmo nome do banco de dados na lista
            else: # caso o banco de dados não esteja na lista
                print(f"Database '{database}' not found")
                print("Starting install...")
                Install.__run_scripts(directory="Banco-Dados-Biblioteca\\scripts") # roda os scripts de instalação do banco de dados
                Install.__sql.commit() # envia as alterações feitas no mysql diretamente ao servidor local
                print("Scripts runned sucessfully!")
                print("Stopping install...")          
                return database # retorna o mesmo nome do banco de dados na lista
        except mysql.connector.Error as err: # erro no mysql
            print(f"Error\n{err}")
        except Exception as e: # erro no python
            print(f"Error\n{e}")
class Database:
    # conector fixo do mysql
    _sql = mysql.connector.connect(
            user="root",
            password="admin",
            host="localhost",
            database = Install.main("biblioteca") # retorna o nome do banco de dados que foi especificado ao instalador (mesmo se o banco de dados não estiver presente, o instalador instala o banco de dados e retorna o nome do banco de dados instalado)
    )