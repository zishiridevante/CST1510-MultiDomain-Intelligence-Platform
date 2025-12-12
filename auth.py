import bcrypt
import os

# File to store users
USER_DATA_FILE = "users.txt"


# -----------------------------
# PASSWORD HASHING
# -----------------------------
def hash_password(plain_text_password):
    """Hashes a plaintext password using bcrypt."""
    password_bytes = plain_text_password.encode("utf-8")
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    return hashed.decode("utf-8")


def verify_password(plain_text_password, hashed_password):
    """Verifies a plaintext password against a stored bcrypt hash."""
    password_bytes = plain_text_password.encode("utf-8")
    hash_bytes = hashed_password.encode("utf-8")
    return bcrypt.checkpw(password_bytes, hash_bytes)


# -----------------------------
# USER MANAGEMENT
# -----------------------------
def user_exists(username):
    """Checks if a username already exists in the users file."""
    if not os.path.exists(USER_DATA_FILE):
        return False

    with open(USER_DATA_FILE, "r") as file:
        for line in file:
            saved_username, _ = line.strip().split(",")
            if saved_username == username:
                return True
    return False


def register_user(username, password):
    """Registers a new user with hashed password."""
    if user_exists(username):
        print(f"Error: Username '{username}' already exists.")
        return False

    hashed = hash_password(password)

    with open(USER_DATA_FILE, "a") as file:
        file.write(f"{username},{hashed}\n")

    print(f"Success: User '{username}' registered successfully!")
    return True


def login_user(username, password):
    """Attempts to log a user in."""
    if not os.path.exists(USER_DATA_FILE):
        print("Error: No registered users yet.")
        return False

    with open(USER_DATA_FILE, "r") as file:
        for line in file:
            saved_username, saved_hash = line.strip().split(",")

            if saved_username == username:
                if verify_password(password, saved_hash):
                    print(f"Success: Welcome, {username}!")
                    return True
                else:
                    print("Error: Invalid password.")
                    return False

    print("Error: Username not found.")
    return False


# -----------------------------
# INPUT VALIDATION
# -----------------------------
def validate_username(username):
    if len(username) < 3 or len(username) > 20:
        return False, "Username must be 3–20 characters long."

    if not username.isalnum():
        return False, "Username must be alphanumeric."

    return True, ""


def validate_password(password):
    if len(password) < 6:
        return False, "Password must be at least 6 characters long."

    return True, ""


# -----------------------------
# MAIN MENU
# -----------------------------
def display_menu():
    print("\n" + "=" * 50)
    print(" MULTI-DOMAIN INTELLIGENCE PLATFORM")
    print(" Secure Authentication System - Week 7")
    print("=" * 50)
    print("[1] Register")
    print("[2] Login")
    print("[3] Exit")
    print("-" * 50)


def main():
    print("\nWelcome to the Week 7 Authentication System!")

    while True:
        display_menu()
        choice = input("Select an option: ").strip()

        if choice == "1":
            print("\n--- REGISTER ---")
            username = input("Enter username: ").strip()
            valid, msg = validate_username(username)
            if not valid:
                print("Error:", msg)
                continue

            password = input("Enter password: ").strip()
            valid, msg = validate_password(password)
            if not valid:
                print("Error:", msg)
                continue

            password2 = input("Confirm password: ").strip()
            if password != password2:
                print("Error: Passwords do not match.")
                continue

            register_user(username, password)

        elif choice == "2":
            print("\n--- LOGIN ---")
            username = input("Username: ").strip()
            password = input("Password: ").strip()

            login_user(username, password)
            input("\nPress Enter to return to menu...")

        elif choice == "3":
            print("Exiting...")
            break

        else:
            print("Invalid option. Try again.")


if __name__ == "__main__":
    main()

