from app.data.database import DatabaseManager
from pathlib import Path

# Build absolute paths to CSVs
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "DATA"

db = DatabaseManager()
db.create_tables()

# Load CSVs with absolute paths
db.load_csv_to_table(str(DATA_DIR / "cyber_incidents.csv"), "cyber_incidents")
db.load_csv_to_table(str(DATA_DIR / "datasets_metadata.csv"), "datasets_metadata")
db.load_csv_to_table(str(DATA_DIR / "it_tickets.csv"), "it_tickets")

print("All CSV data loaded successfully!")
