import pandas as pd

from pathlib import Path

from postgresql_config import ReadFromConfig
from db_manager import PostgreSQLManager

from extract_data import Extract


def run_etl() -> None:

    postgres_config = ReadFromConfig("config.ini", "postgres_schema")
    
    db_schema_config = postgres_config.read_from_config()

    db_manager = PostgreSQLManager(
        host=db_schema_config["host"], 
        user=db_schema_config["user"], 
        password=db_schema_config["password"]
    )

    db_manager.create_database(db_schema_config["dbname_dw"])

    db_manager.dbname = db_schema_config["dbname_dw"]
    
    db_manager.create_all_tables(db_schema_config['schema_file'])
    
    db_manager.connect(db_schema_config["dbname"])
    
    extractor = Extract(db_manager)
    
    # Extract payment data
    payment_data = extractor.extract_payment_data()
    
    
    
    # # Extract customer data
    # customer_data = extractor.extract_customer_data()
    # print("Extracted Customer Data:", customer_data)
    
    # # Extract movie data
    # movie_data = extractor.extract_movie_data()
    # print("Extracted Movie Data:", movie_data)
    
    # # Extract store data
    # store_data = extractor.extract_store_data()
    # print("Extracted Store Data:", store_data)

    

    
    
    db_manager.close()

if __name__ == "__main__":
    run_etl()
