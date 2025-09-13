import duckdb
import sqlite3
import os
import psycopg2
from pathlib import Path

ENVIRONMENT = os.getenv("ENVIRONMENT", "local")

RAW_DATA_DIR = "../data/raw"
FINAL_DB = "../data/final/f1.db"
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
    sqlite_conn = sqlite3.connect(FINAL_DB)
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
    
    print(f"Summary tables exported to {FINAL_DB}")


'''
Export to Postgres
'''
def export_to_postgres(con):
    # Connect to PostgreSQL
    pg_conn = psycopg2.connect(**PG_CONN_INFO)
    pg_cur = pg_conn.cursor()

    # Export summary tables to PostgreSQL
    for table in ["drivers_summary", "circuits_summary"]:
        df = con.execute(f"SELECT * FROM {table}").fetchdf()
        df.to_csv(f"/tmp/{table}.csv", index=False)
        with open(f"/tmp/{table}.csv", "r") as f_csv:
            pg_cur.copy_expert(f"COPY {table} FROM STDIN WITH CSV HEADER", f_csv)
        pg_conn.commit()

    pg_cur.close()
    pg_conn.close()
    print("✅ Data ingested into PostgreSQL!")


if __name__ == "__main__":
    run_pipeline()