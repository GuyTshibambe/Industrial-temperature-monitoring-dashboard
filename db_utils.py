import sqlite3
import pandas as pd
from pathlib import Path

DB_PATH = Path("data") / "factory_data_v2.db"

def get_connection():
    return sqlite3.connect(DB_PATH)

def get_all_readings():
    conn = get_connection()
    df = pd.read_sql_query("SELECT * FROM temperature_readings",conn)
    conn.close()
    return df

def get_summary_stats():
    conn = get_connection()
    query = """
    SELECT
        COUNT(*) AS total_readings,
        MIN (temperature_c) AS min_temp,
        MAX (temperature_c) AS max_temp,
        AVG (temperature_c) AS avg_temp
    FROM temperature_readings;
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df.iloc[0].to_dict()

def get_overheat_count(threhold=38.0):
    conn = get_connection()
    query = """
    SELECT COUNT (*) AS overheat_count
    FROM temperature_readings
    WHERE temperature_c > ?;
    """
    df = pd.read_sql_query(query, conn, params=(threhold,))
    conn.close();
    return int(df["overheat_count"][0])

def get_machine_ids():
    conn = get_connection()
    query = "SELECT DISTINCT machine_id FROM temperature_readings;"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return sorted(df["machine_id"].tolist())
    