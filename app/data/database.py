import sqlite3
import pandas as pd
from pathlib import Path

# -------------------------------
# DATABASE PATH (WEEK 8 REQUIREMENT)
# -------------------------------
DB_PATH = Path("DATA/intelligence_platform.db")


def connect_database(db_path=DB_PATH):
    """Connect to the SQLite database. Creates the file if missing."""
    return sqlite3.connect(str(db_path))


class DatabaseManager:
    """Handles all SQLite database operations for Week 8."""

    def __init__(self, db_path=DB_PATH):
        self.db_path = db_path
        self.conn = sqlite3.connect(str(self.db_path))
        self.cursor = self.conn.cursor()

    # -------------------------------
    # CREATE REQUIRED TABLES
    # -------------------------------
    def create_tables(self):
        cursor = self.conn.cursor()

        # USERS TABLE (from Week 7)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                role TEXT DEFAULT 'user'
            );
        """)

        # CYBER INCIDENTS TABLE (matches CSV)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS cyber_incidents (
                incident_id INTEGER PRIMARY KEY,
                timestamp TEXT,
                severity TEXT,
                category TEXT,
                status TEXT,
                description TEXT
            );
        """)

        # DATASETS METADATA TABLE (matches CSV)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS datasets_metadata (
                dataset_id INTEGER PRIMARY KEY,
                name TEXT,
                rows INTEGER,
                columns INTEGER,
                uploaded_by TEXT,
                upload_date TEXT
            );
        """)

        # IT TICKETS TABLE (matches CSV)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS it_tickets (
                ticket_id INTEGER PRIMARY KEY,
                priority TEXT,
                description TEXT,
                status TEXT,
                assigned_to TEXT,
                created_at TEXT,
                resolution_time_hours INTEGER
            );
        """)

        self.conn.commit()
        print("All tables created successfully.")

    # -------------------------------
    # USER MIGRATION SUPPORT
    # -------------------------------
    def insert_user(self, username, password_hash):
        try:
            self.cursor.execute(
                "INSERT INTO users (username, password_hash) VALUES (?, ?)",
                (username, password_hash)
            )
            self.conn.commit()
        except sqlite3.IntegrityError:
            print(f"User '{username}' already exists. Skipping...")

    # =====================================================
    # CRUD OPERATIONS — CYBER INCIDENTS (Week 8)
    # =====================================================
    def create_cyber_incident(self, incident):
        """Insert a new cyber incident (Create)"""
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO cyber_incidents
            (incident_id, timestamp, severity, category, status, description)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            incident["incident_id"],
            incident["timestamp"],
            incident["severity"],
            incident["category"],
            incident["status"],
            incident["description"]
        ))
        self.conn.commit()
        return cursor.lastrowid

    def get_all_cyber_incidents(self):
        """Read all cyber incidents"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM cyber_incidents")
        return cursor.fetchall()

    def get_cyber_incident_by_id(self, incident_id):
        """Read a single incident by ID"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM cyber_incidents WHERE incident_id = ?", (incident_id,))
        return cursor.fetchone()

    def update_cyber_incident_status(self, incident_id, new_status):
        """Update incident status"""
        cursor = self.conn.cursor()
        cursor.execute("""
            UPDATE cyber_incidents
            SET status = ?
            WHERE incident_id = ?
        """, (new_status, incident_id))
        self.conn.commit()
        return cursor.rowcount

    def delete_cyber_incident(self, incident_id):
        """Delete an incident"""
        cursor = self.conn.cursor()
        cursor.execute(
            "DELETE FROM cyber_incidents WHERE incident_id = ?",
            (incident_id,)
        )
        self.conn.commit()
        return cursor.rowcount

    # =====================================================
    # CRUD OPERATIONS — IT TICKETS (Week 8)
    # =====================================================
    def create_it_ticket(self, ticket):
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO it_tickets
            (ticket_id, priority, description, status, assigned_to, created_at, resolution_time_hours)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            ticket["ticket_id"],
            ticket["priority"],
            ticket["description"],
            ticket["status"],
            ticket["assigned_to"],
            ticket["created_at"],
            ticket["resolution_time_hours"]
        ))
        self.conn.commit()
        return cursor.lastrowid

    def get_all_it_tickets(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM it_tickets")
        return cursor.fetchall()

    def get_it_ticket_by_id(self, ticket_id):
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT * FROM it_tickets WHERE ticket_id = ?",
            (ticket_id,)
        )
        return cursor.fetchone()

    def update_it_ticket_status(self, ticket_id, new_status):
        cursor = self.conn.cursor()
        cursor.execute("""
            UPDATE it_tickets
            SET status = ?
            WHERE ticket_id = ?
        """, (new_status, ticket_id))
        self.conn.commit()
        return cursor.rowcount

    def reassign_it_ticket(self, ticket_id, new_assignee):
        cursor = self.conn.cursor()
        cursor.execute("""
            UPDATE it_tickets
            SET assigned_to = ?
            WHERE ticket_id = ?
        """, (new_assignee, ticket_id))
        self.conn.commit()
        return cursor.rowcount

    def delete_it_ticket(self, ticket_id):
        cursor = self.conn.cursor()
        cursor.execute(
            "DELETE FROM it_tickets WHERE ticket_id = ?",
            (ticket_id,)
        )
        self.conn.commit()
        return cursor.rowcount

    # =====================================================
    # GENERIC CSV LOADER (WEEK 8)
    # =====================================================
    def load_csv_to_table(self, csv_path, table_name):
        """Load a CSV file into a database table using pandas with absolute paths."""

        csv_path = Path(csv_path).resolve()
        print(f"DEBUG: Looking for CSV at → {csv_path}")

        if not csv_path.exists():
            print(f"CSV file not found: {csv_path}")
            return

        try:
            df = pd.read_csv(csv_path)
            df.to_sql(table_name, self.conn, if_exists="append", index=False)
            print(f"Loaded {len(df)} rows into {table_name}.")
        except Exception as e:
            print(f"ERROR loading CSV '{csv_path}' into '{table_name}': {e}")
