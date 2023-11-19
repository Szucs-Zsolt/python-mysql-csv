import mysql.connector

class Database:
    def __init__(self, config_file):
        """
        It uses the configuration file to get the neccessary connection
        data to the MySQL/MariaDB server.
        In case of error the program exits.
        
        Parameter
            config_file: it contains all the neccessary data to connect
                         to the MySQL server.
        """

        # After successfully opening the connection to the database, 
        # these variables get proper values.
        self.connection = None
        self.cursor = None

        # Neccessary data to connect to the database. 
        # One line = one specific part of data.
        try:
            with open(config_file, "r", encoding="utf-8") as f:
                self.host = f.readline().replace("\n", "")
                self.database = f.readline().replace("\n", "")
                self.user = f.readline().replace("\n", "")
                self.password = f.readline().replace("\n", "")
        except FileNotFoundError:
            print(f"Missing configuration file: {config_file}")
            exit()
        except Exception as e:
            print("Error: ", e)    
            exit()

    def open_connection(self):
        """
        Using the data from the configuration file it creates the
        connection to the server. 
        After this process self.cursor can be used.
        
        Return values:
            True:  successfull connection
            False: failed to connect to the database
        """
        try:
            self.connection = mysql.connector.connect(
                host = self.host,
                database = self.database,
                user = self.user,
                password = self.password
            )
            self.cursor = self.connection.cursor()
            return True
        except mysql.connector.errors.ProgrammingError:
            print(f"Error: Invalid database name - user name - password combination. (host: {self.host}, database: {self.database})")
        except mysql.connector.errors.DatabaseError:
            print(f"Error: Can not connect to the server: host: {self.host}")
        except Exception as e:
            print("Error:", e)

        return False

    def close_connection(self):
        """
        If the connection to the database is still open, it will close it.
        """
        if self.connection:
            self.connection.close()

    def get_table_names(self):
        """
        It query and give back the name of the tables from the database.
        The result will be in a list, containing strings.
        None, if it has failed to acquire the names.
        """
        table_name_list = None
        try:
            if not self.open_connection():
                return None

            self.cursor.execute("SHOW TABLES;")
            # It give back in a form of list of tuples.
            table_names = self.cursor.fetchall()
            table_name_list = []
            for name in table_names:
                table_name_list.append(list(name)[0])    
        except Exception as e:
            print("Error:", e)
        finally:
            self.close_connection()

        return table_name_list


    def get_all_rows(self, table_name):
        """
        It reads all of the rows from the database and it will give
        it back in a list.
        One element of the list = one row of the table.
        
        Parameter:
            table_name: we want the rows from this table
        """
        rows = None
        try:
            if not self.open_connection():
                return None

            self.cursor.execute(f"SELECT * FROM {table_name}")
            rows = self.cursor.fetchall()
        except Exception as e:
            print("Error:", e)
        finally:
            self.close_connection()
        return rows