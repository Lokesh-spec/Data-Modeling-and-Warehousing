# Data Engineer Project 1 - Data Modeling (Basic)

This project demonstrates fundamental data modeling for a relational database system. It involves setting up a PostgreSQL database, loading data from multiple CSV files, and creating structured tables to represent and analyze the data.

## Table of Contents
1. [Project Overview](#project-overview)
2. [Data Model Structure](#data-model-structure)
3. [Data Files](#data-files)
4. [Installation and Setup](#installation-and-setup)
5. [Usage](#usage)
6. [License](#license)

---

## Project Overview

This project is designed to introduce data modeling basics in a relational database context. Using Python and PostgreSQL, we:
- Set up a PostgreSQL database (`accounts`) and connect to it.
- Load and clean multiple CSV files using Pandas.
- Structure and normalize the data by creating tables in PostgreSQL.
- Model relationships and dependencies between the data tables.

## Data Model Structure

The project focuses on:
- **Loading Data**: Importing data from three CSV files into Pandas for inspection and cleaning.
- **Database Creation**: Setting up a PostgreSQL database named `accounts`.
- **Table Creation**: Creating normalized tables in PostgreSQL to represent data relationships effectively.

## Data Files

The project relies on the following CSV files located in the `Data` directory:
1. **`Wealth-AccountsCountry.csv`**: Contains country-specific account data.
2. **`Wealth-AccountData.csv`**: Contains primary account data, potentially linked to individual accounts.
3. **`Wealth-AccountSeries.csv`**: Contains time series or related structured data.

Each file is loaded into Pandas for initial data analysis and cleaned before inserting into PostgreSQL tables.

## Installation and Setup

1. **Clone the repository**:
    ```bash
    git clone https://github.com/Lokesh-spec/Data-Modeling.git
    cd Data-Modeling
    ```

2. **Install required Python packages**:
    Install dependencies using the provided `requirements.txt` file:
    ```bash
    pip install -r requirements.txt
    ```
   This will install the necessary packages:
   - `pandas`: For data manipulation
   - `psycopg2`: For connecting to PostgreSQL
   - `jupyter`: For running the notebook

3. **Launch Jupyter Notebook**:
    ```bash
    jupyter notebook
    ```
4. Open the notebook file `Data Engineer Project 1 - Data Modeling - Basic.ipynb`.

5. **Set up PostgreSQL**:
   - Ensure your PostgreSQL server is running.
   - The notebook connects to a PostgreSQL database on `localhost` using the database `postgres` and creates a new database called `accounts`.
   - Adjust the connection settings if your database server requires different credentials.

## Usage

1. **Database Initialization**:
   - Run the notebook cells to set up the PostgreSQL `accounts` database.
   
2. **Data Loading and Cleaning**:
   - The CSV files from the `Data` folder are loaded into Pandas DataFrames for initial inspection and duplicate removal.
   
3. **Table Creation and Data Insertion**:
   - Structured tables are created in PostgreSQL, and cleaned data from the DataFrames is inserted into these tables.

## What is Data Model
A data model is an abstract model that organizes data elements and standardizes how they relate to one another and to the properties of real-world entities. 

## Why is Data Modeling Important

1. Really important to Organize Data
2. Organized data determines later data use
3. Begin prior to building out applications, business logic, and analytical models
4. Iterative process

## Relational Model
Organizes data into one or more tables of columns and rows, with a unique key identifying each row.

## Relational Database
It is a digital database based on the relational model of data, a software system used to maintain relational databases is a relational database management system (RDBMS).

### Common Types of RDBMS

1. MySQL
2. PostgreSQL
3. Oracle
4. MSSQL

## Basics

1. **Database/Schema**
   - Collection of tables

2. **Tables/Relations**
   - A group of rows sharing the same labeled elements
     - i.   Students
     - ii.  Subjects
     - iii. Marks

## Advantages of using a RDBMS

1. Ease of use - SQL
2. Ability to do JOINS
3. Ability to do aggregations and analytics
4. Smaller Data Volumes
5. Flexibility of queries
6. ACID transaction - data integrity

## What are ACID Properties

1. **Atomicity**: Atomicity ensures that a transaction is treated as a single, indivisible unit of work. This means that either all the operations within the transaction are completed successfully, or none of them are. 
   - **Abort**: If a transaction aborts, changes made to the database are not visible.
   - **Commit**: If a transaction commits, changes made are visible.
   Atomicity is also known as the ‘All or nothing rule’.

2. **Consistency**: This means that integrity constraints must be maintained so that the database is consistent before and after the transaction. It refers to the correctness of a database. 
   - Referring to the example above:
     - Total before T occurs = 500 + 200 = 700
     - Total after T occurs = 400 + 300 = 700
   - Therefore, the database is consistent. Inconsistency occurs if T1 completes but T2 fails. As a result, T is incomplete.

3. **Isolation**: Isolation is a crucial property in Database Management Systems (DBMS) that ensures the integrity and consistency of data when multiple transactions are executed concurrently. 
   - Isolation ensures that the operations of one transaction are not visible to other transactions until the transaction is completed. This prevents interference and conflicts between concurrent transactions, maintaining the accuracy and reliability of the database.

4. **Durability**: Durability is a crucial property in Database Management Systems (DBMS) that ensures the persistence and reliability of data. Once a transaction is committed, its effects are permanently recorded in the database, even in the event of a system crash, power failure, or other disruptions. 
   - This guarantees that committed changes are not lost and can be retrieved after any type of failure.

## What is PostgreSQL

1. Open Source object-relational database system
2. Uses and builds on SQL language


## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more information.
