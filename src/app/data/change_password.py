import json
import os
from ..config_handler import create_path


def change_password():
    # Check if file exists
    user_path = create_path("app/data", "users.json")
    if not os.path.exists(user_path):
        print("User file not found.")
        return

    # Load users
    with open(user_path, "r") as f:
        data = json.load(f)

    users = data.get("users", [])
    if not users:
        print("No users found.")
        return

    # List available usernames
    print("Available users:")
    for i, user in enumerate(users, start=1):
        print(f"{i}. {user['username']}")

    # Ask which user
    choice = input("Enter the username whose password you want to change: ").strip()

    # Find the user
    user_found = False
    for user in users:
        if user["username"] == choice:
            new_password = input(f"Enter new password for {choice}: ").strip()
            user["password"] = new_password  # Replace with hash if needed
            user_found = True
            break

    if not user_found:
        print("User not found.")
        return

    # Save changes back to JSON
    with open(user_path, "w") as f:
        json.dump(data, f, indent=4)

    print(f"Password for {choice} has been updated.")

# Example usage
change_password()