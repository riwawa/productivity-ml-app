import sqlite3
import pandas as pd
import os

DB_NAME = "productivity.db"
TABLE_NAME = "productivity"

# =========================
# 1. CONEXÃO SEGURA
# =========================
def get_connection():
    return sqlite3.connect(DB_NAME, check_same_thread=False)

# =========================
# 2. INICIALIZAR BANCO
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
# 3. SALVAR DADOS
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
# 4. CARREGAR DADOS
# =========================
def load_data():
    conn = get_connection()
    df = pd.read_sql_query(f"SELECT * FROM {TABLE_NAME}", conn)
    conn.close()
    return df

# =========================
# 5. MIGRAR CSV → SQLITE (RODA 1 VEZ)
# =========================
def migrate_csv(csv_path="data.csv"):
    if not os.path.exists(csv_path):
        return

    conn = get_connection()

    df = pd.read_csv(csv_path)

    # evita duplicação básica
    df.to_sql(TABLE_NAME, conn, if_exists="append", index=False)

    conn.close()

    # marca como migrado
    with open("migrated.txt", "w") as f:
        f.write("done")

# =========================
# 6. RODAR MIGRAÇÃO SEGURA
# =========================
def safe_migrate():
    if not os.path.exists("migrated.txt"):
        migrate_csv()