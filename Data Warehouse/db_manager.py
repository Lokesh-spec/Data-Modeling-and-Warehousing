
import json
import psycopg2
from psycopg2 import sql, errors
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from typing import Optional
from psycopg2.extras import execute_values


class PostgreSQLManager:
    def __init__(self, host: str, user: str, password: str, dbname: Optional[str] = None):
        """
        Initializes the PostgreSQLManager with connection parameters.
        
        :param host: The hostname of the PostgreSQL server.
        :param user: The username for authentication.
        :param password: The password for authentication.
        :param dbname: The name of the database to connect to. Defaults to None.
        """
        self.host = host
        self.user = user
        self.password = password
        self.dbname = dbname
        self.connection = None
        self.cursor = None


    def connect(self, dbname: Optional[str] = None) -> None:
        """Establish a connection to the PostgreSQL database."""
        try:
            # Set connection parameters based on whether dbname is provided
            conn_params = {
                "host": self.host,
                "user": self.user,
                "password": self.password,
            }
            if dbname:
                conn_params["dbname"] = dbname
            self.connection = psycopg2.connect(**conn_params)
            self.connection.autocommit = True
            self.cursor = self.connection.cursor()
            print(f"Connection established to database '{dbname}'." if dbname else "Connection established to the PostgreSQL server.")
        except Exception as e:
            print(f"Error connecting to the database: {e}")
            self.connection = None
            self.cursor = None


    def create_database(self, dbname: str) -> None:
        """
        Creates a new database if it does not already exist.
        
        :param dbname: The name of the database to create.
        """
        try:
            # Connect to the default database to create a new one
            self.connect()  # Connects without specifying dbname
            self.cursor.execute(sql.SQL("CREATE DATABASE {}").format(
                sql.Identifier(dbname))
            )
            print(f"Database '{dbname}' created successfully.")
            
            # Reconnect to the newly created database
            self.connect(dbname)
        except errors.DuplicateDatabase:
            print(f"Database '{dbname}' already exists.")
            # Connect to the existing database if it already exists
            self.connect(dbname)
        except Exception as e:
            print(f"Error creating database: {e}")
            
        finally:
            self.close()


    def create_table(self, table_name: str, columns: list) -> None:
        """Create a table from the loaded config."""
        if not self.connection or self.connection.closed != 0:
            print("No active connection. Please connect to the database first.")
            return
        
        # Format the column definitions correctly into a single string
        column_definitions = []
        for column in columns:
            # Format the column with type and constraints if any
            col_def = f"{column['name']} {column['type']}"
            if 'constraints' in column:
                col_def += f" {column['constraints']}"
            column_definitions.append(col_def)
        
        # Join all the column definitions with commas to form the complete column definition part
        column_definitions_str = ", ".join(column_definitions)
        
        # Construct the full CREATE TABLE SQL query
        create_table_sql = f"CREATE TABLE {table_name} ({column_definitions_str})"
        
        try:
            # Execute the SQL to create the table
            self.cursor.execute(create_table_sql)
            print(f"Table '{table_name}' created successfully.")
        except Exception as e:
            print(f"Error creating table '{table_name}': {e}")
            
        finally:
            self.close()
            
            
    def load_schema(self, filename: str) -> dict:
        """Load table schema from a JSON file."""
        with open(filename, 'r') as file:
            return json.load(file)


    def create_all_tables(self, schema_file: str) -> None:
        """Create all tables based on the schema in the JSON file."""
        schema = self.load_schema(schema_file)
        for table_name, table_info in schema.items():
            self.create_table(table_info["table_name"], table_info["columns"])


    def select_query(self, query: str) -> list:
        """
        Executes a SELECT query and returns the results.

        :param query: The SQL SELECT query string.
        :return: A list of tuples containing the results of the query.
        """
        if not self.connection or self.connection.closed != 0:
            print("No active connection. Please connect to the database first.")
            return []

        try:
            # Execute the SELECT query
            self.cursor.execute(query)

            # Fetch all results from the executed query
            results = self.cursor.fetchall()

            # Return the results
            return results
        except Exception as e:
            print(f"Error executing SELECT query: {e}")
            return []


    def close(self) -> None:
        """Closes the connection to PostgreSQL."""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
        print("Connection closed.")