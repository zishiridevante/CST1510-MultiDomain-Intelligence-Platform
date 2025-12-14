from app.data.database import DatabaseManager
import os

# Correct path: users.txt is inside DATA/ at project root
USER_DATA_FILE = "DATA/users.txt"

db = DatabaseManager()
db.create_tables()

if os.path.exists(USER_DATA_FILE):
    with open(USER_DATA_FILE, "r") as file:
        for line in file:
            username, password_hash = line.strip().split(",")
            db.insert_user(username, password_hash)
else:
    print(f"User file not found: {USER_DATA_FILE}")

print("User migration completed successfully!")

