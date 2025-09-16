import duckdb
import sqlite3
import os
from pathlib import Path

ENVIRONMENT = os.getenv("ENVIRONMENT", "local")

RAW_DATA_DIR = "../data/raw"
SQLITE_DB = "../data/final/f1.db"
QUERIES_FILE = "queries.sql"

PG_CONN_INFO = {
    "host": os.getenv("POSTGRES_HOST", "postgres"),
    "dbname": os.getenv("POSTGRES_DB", "williams"),
    "user": os.getenv("POSTGRES_USER", "postgres"),
    "password": os.getenv("POSTGRES_PASSWORD", "postgres"),
    "port": os.getenv("POSTGRES_PORT", "5432"),
}

"""
Load raw data into duckdb for analytics
"""
def run_pipeline():
    con = duckdb.connect(database=":memory:")

    # Load raw data into DuckDB tables
    # Loop through data directory and load each file into a table
    for filename in os.listdir(RAW_DATA_DIR):
        table_name = os.path.splitext(filename)[0]
        file_path = f"{RAW_DATA_DIR}/{filename}"
    
        con.execute(f"""
            CREATE OR REPLACE TABLE {table_name} AS
            SELECT * FROM read_csv_auto('{file_path}', header=True);
        """)
        
        print(f"Loaded {filename} into {table_name} table")

    # Run SQL queries script
    with open(QUERIES_FILE, "r") as f:
        sql_script = f.read()
    con.execute(sql_script)

    if ENVIRONMENT == "local":
        # Export tables to Postgres container
        export_to_sqlite(con)
    else:
        # Export tables to SQLite (default)
        export_to_postgres(con)


'''
Export summary tables to SQLite (LOCAL ONLY)
'''
def export_to_sqlite(con):
    drivers_data = con.execute("SELECT * FROM drivers_summary").fetchall()
    drivers_columns = [desc[0] for desc in con.description]
    
    circuits_data = con.execute("SELECT * FROM circuits_summary").fetchall()
    circuits_columns = [desc[0] for desc in con.description]
    
    # Create SQLite database and tables
    sqlite_conn = sqlite3.connect(SQLITE_DB)
    cursor = sqlite_conn.cursor()
    
    # Create drivers_summary table
    cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS drivers_summary (
            {', '.join([f'{col} TEXT' for col in drivers_columns])}
        )
    """)
    
    # Create circuits_summary table  
    cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS circuits_summary (
            {', '.join([f'{col} TEXT' for col in circuits_columns])}
        )
    """)
    
    # Insert data
    cursor.executemany(f"""
        INSERT OR REPLACE INTO drivers_summary ({', '.join(drivers_columns)})
        VALUES ({', '.join(['?' for _ in drivers_columns])})
    """, drivers_data)
    
    cursor.executemany(f"""
        INSERT OR REPLACE INTO circuits_summary ({', '.join(circuits_columns)})
        VALUES ({', '.join(['?' for _ in circuits_columns])})
    """, circuits_data)
    
    sqlite_conn.commit()
    sqlite_conn.close()
    
    print(f"Summary tables exported to {SQLITE_DB}")


'''
Use DuckDB's PostgreSQL extension to export to Postgres
'''
def export_to_postgres(con):
    con.execute("INSTALL postgres; LOAD postgres;")

    # Postgres connection info
    PG_CONN_INFO = {
        "host": os.getenv("POSTGRES_HOST", "postgres"),
        "dbname": os.getenv("POSTGRES_DB", "williams"),
        "user": os.getenv("POSTGRES_USER", "postgres"),
        "password": os.getenv("POSTGRES_PASSWORD", "postgres"),
        "port": os.getenv("POSTGRES_PORT", "5432"),
    }

    # Create DuckDBsecret
    con.execute(
        f"""
            CREATE OR REPLACE SECRET pg (
                TYPE postgres,
                PORT 5432,
                HOST '{PG_CONN_INFO['host']}',
                DATABASE '{PG_CONN_INFO['dbname']}',
                USER '{PG_CONN_INFO['user']}',
                PASSWORD '{PG_CONN_INFO['password']}'
            );
        """
    )

    # Attach the Postgres database as a writable schema
    con.execute(
        f"ATTACH '' AS pg (TYPE POSTGRES, SECRET 'pg');"
    )

    ## TODO: Dynamic tables creation
    # Create target tables in Postgres from DuckDB tables
    for table in ["drivers_summary", "circuits_summary"]:
        con.execute(f"DROP TABLE IF EXISTS pg.public.{table};")
        con.execute(f"CREATE TABLE pg.public.{table} AS SELECT * FROM {table};")
        print(f"Exported {table} to PostgreSQL")

    # Optionally detach
    con.execute("DETACH pg;")

    print("Data ingested into PostgreSQL!")


if __name__ == "__main__":
    run_pipeline()