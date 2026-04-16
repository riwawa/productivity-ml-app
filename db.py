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
# MIGRAR CSV (1x)
# =========================
def migrate_csv(csv_path="data.csv"):
    if not os.path.exists(csv_path):
        return

    conn = get_connection()
    df = pd.read_csv(csv_path)

    df = df.dropna()
    df = df.loc[:, ~df.columns.str.contains("^Unnamed")]
    df = df[["sleep", "study", "exercise", "caffeine", "humor", "productivity"]]

    df.to_sql(TABLE_NAME, conn, if_exists="append", index=False)

    conn.close()

    with open("migrated.txt", "w") as f:
        f.write("done")

# =========================
# MIGRAÇÃO SEGURA
# =========================
def safe_migrate():
    if not os.path.exists("migrated.txt"):
        migrate_csv()

# =========================
# SEED INICIAL 
# =========================
def seed_data():
    df = load_data()

    if df.empty:
        conn = get_connection()

        sample = pd.DataFrame({
            "sleep": [7, 6, 8, 5],
            "study": [1, 0, 1, 1],
            "exercise": [1, 1, 0, 0],
            "caffeine": [1, 0, 1, 1],
            "humor": [4, 3, 5, 2],
            "productivity": [7, 5, 8, 4]
        })

        sample.to_sql(TABLE_NAME, conn, if_exists="append", index=False)

        conn.close()