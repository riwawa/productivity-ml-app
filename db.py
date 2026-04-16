import sqlite3
import pandas as pd

DB_NAME = "productivity.db"

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

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS productivity (
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

    cursor.execute("""
        INSERT INTO productivity (sleep, study, exercise, caffeine, humor, productivity)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (sleep, study, exercise, caffeine, humor, productivity))

    conn.commit()
    conn.close()

# =========================
# 4. CARREGAR DADOS
# =========================
def load_data():
    conn = get_connection()
    df = pd.read_sql_query("SELECT * FROM productivity", conn)
    conn.close()
    return df