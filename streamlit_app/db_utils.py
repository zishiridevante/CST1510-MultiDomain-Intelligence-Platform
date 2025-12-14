import sqlite3
from pathlib import Path
import bcrypt

# ----------------------------------
# PATH FIXING
# ----------------------------------
# This file lives in: streamlit_app/
# DB lives in:       DATA/intelligence_platform.db

BASE_DIR = Path(__file__).resolve().parent       # → streamlit_app/
PROJECT_ROOT = BASE_DIR.parent                   # → CW2_M01040790_CST1510/
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
        return True, row  # return full row, including role
    else:
        return False, "Incorrect password"


# --------------------------
# REGISTER NEW USER (NOW SUPPORTS ROLE)
# --------------------------
def register_user(username, password, role):
    conn = get_connection()
    cursor = conn.cursor()

    # Hash the password
    password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    try:
        cursor.execute("""
            INSERT INTO users (username, password_hash, role)
            VALUES (?, ?, ?)
        """, (username, password_hash, role))

        conn.commit()
        return True, "User created successfully!"

    except sqlite3.IntegrityError:
        return False, "Username already exists!"
