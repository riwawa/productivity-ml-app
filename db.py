import sqlite3
import pandas as pd
import os

DB_NAME = "productivity.db"
TABLE_NAME = "productivity"

# =========================
# CONEXÃO
# =========================
def get_connection():
    return sqlite3.connect(DB_NAME, check_same_thread=False)

# =========================
# CRIAR BANCO
# =========================
def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(f"""
    CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        sleep REAL,
        study INTEGER,
        exercise INTEGER,
        caffeine INTEGER,
        humor INTEGER,
        productivity REAL
    )
    """)

    conn.commit()
    conn.close()

# =========================
# SALVAR DADOS
# =========================
def save_data(sleep, study, exercise, caffeine, humor, productivity):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(f"""
        INSERT INTO {TABLE_NAME}
        (sleep, study, exercise, caffeine, humor, productivity)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (sleep, study, exercise, caffeine, humor, productivity))

    conn.commit()
    conn.close()

# =========================
# CARREGAR DADOS
# =========================
def load_data():
    conn = get_connection()
    df = pd.read_sql_query(f"SELECT * FROM {TABLE_NAME}", conn)
    conn.close()
    return df

# =========================
# MIGRAR CSV → DB (1x)
# =========================
def migrate_csv(csv_path="data.csv"):
    if not os.path.exists(csv_path):
        return

    conn = get_connection()
    df = pd.read_csv(csv_path)

    # limpeza
    df = df.dropna()
    df = df.loc[:, ~df.columns.str.contains("^Unnamed")]

    df = df[["sleep", "study", "exercise", "caffeine", "humor", "productivity"]]

    df["study"] = df["study"].astype(int)
    df["exercise"] = df["exercise"].astype(int)
    df["caffeine"] = df["caffeine"].astype(int)
    df["humor"] = df["humor"].astype(int)
    df["sleep"] = df["sleep"].astype(float)
    df["productivity"] = df["productivity"].astype(float)

    df.to_sql(TABLE_NAME, conn, if_exists="append", index=False)

    conn.close()

    # marca como migrado
    with open("migrated.txt", "w") as f:
        f.write("done")

# =========================
# MIGRAÇÃO SEGURA
# =========================
def safe_migrate():
    if not os.path.exists("migrated.txt"):
        migrate_csv()
