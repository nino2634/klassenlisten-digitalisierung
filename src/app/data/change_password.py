import json
import os
import hashlib
import maskpass

def create_path(path, file_name) -> str:
    current_file = os.path.abspath(__file__)
    project_root = os.path.dirname(os.path.dirname(current_file))
    file = os.path.join(project_root, path, file_name)
    return file

def change_password():
    # Check if file exists
    user_path = create_path("data", "users.json")
    if not os.path.exists(user_path):
        print("User file not found./" + user_path)
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
            new_password = maskpass.advpass(f"Enter new password for {choice}: ").strip()
            new_password = hashlib.sha256(new_password.encode('utf-8')).hexdigest()
            user["password"] = new_password
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