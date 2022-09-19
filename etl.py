from sqlalchemy import create_engine  # to interact with postgresql
import pyodbc  # to connect to sqlserver
import pandas as pd  # data extract and load
import os  # for the stored username and password in the system environment variables

# get the password from environment variables

pwd = 'testpass'
uid = 'etl'

# sqlserver db details
driver = "{SQL Server Native Client 11.0}"
server = "DESKTOP-HD9D72O"
database = "AdventureWorksDW2019"

# extract data from sql server


def extract():
    try:
        src_conn = pyodbc.connect(
            'DRIVER=' + driver + '; SERVER =' + server + '\SQLEXPRESS' + ';DATABASE =' + database + '; UID=' + uid + ';PWD= ' + pwd)
        src_cursor = src_conn.cursor()
        # execute query
        src_cursor.execute("""select t.name as table_name\
            from sys.tables to where t.name in ('DimProduct', 'DimProductCategory', 'DimProductSubCategory', 'DimSalesTerritory')""")
        scr_tables = scr_cursor.fetchall()
        for tbl in scr_tables:
            # query and load save data to dataframe
            df = pd.read_sql_query(f'select * from {tbl[0]}', src_conn)
            load(df, tbl[0])
    except Exception as e:
        print("Data extract error: " + str(e))
    finally:
        scr_conn.close()

        # load data to postgres


def load(df, tbl):
    try:
        rowes_imported = 0
        engine = create_engine(
            f'postgresql://{uid}:{pwd}@{server}:5432/AdventureWorks')
        print(
            f'importing rows {rows_imported} to {rows_imported + len(df) } ... for table {tbl}')
        # save df to postres
        df.to_sql(f'stg_{tbl}', engine, if_exists='replace', index=False)
        rows_imported += len(df)
        # print success message
        print("Data import was successful")
    except Exception as e:
        print("Data load error: " + str(e))

    try:
        # call extract function
        extract()
    except Exception as e:
        print("Error while extracting data: " + str(e))

    try:
        # call load function
        load(df, tbl)
    except Exception as e:
        print("Error while loading data: " + str(e))
