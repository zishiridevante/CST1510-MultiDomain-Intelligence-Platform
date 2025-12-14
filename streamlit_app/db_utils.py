import sqlite3
from pathlib import Path
import bcrypt

# ----------------------------------
# ----------------------------------

# This file lives in: streamlit_app/
#              DATA/intelligence_platform.db

BASE_DIR = Path(__file__).resolve().parent   # → streamlit_app/
PROJECT_ROOT = BASE_DIR.parent               # → CW2_M01040790_CST1510/
DB_PATH = (PROJECT_ROOT / "DATA" / "intelligence_platform.db").resolve()


def get_connection():
    """Return a connection to the SQLite database."""
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn


# --------------------------
# VERIFY USER LOGIN
# --------------------------
def verify_user(username, password):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    row = cursor.fetchone()

    if row is None:
        return False, "User not found"

    stored_hash = row["password_hash"]

    if bcrypt.checkpw(password.encode(), stored_hash.encode()):
        return True, row
    else:
        return False, "Incorrect password"


# --------------------------
# REGISTER NEW USER
# --------------------------
def register_user(username, password):
    conn = get_connection()
    cursor = conn.cursor()

    password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    try:
        cursor.execute("""
            INSERT INTO users (username, password_hash)
            VALUES (?, ?)
        """, (username, password_hash))
        conn.commit()
        return True, "User created successfully!"

    except sqlite3.IntegrityError:
        return False, "Username already exists!"
