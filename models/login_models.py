import json

class UserModel:
    def __init__(self, db_path="users.json"):
        self.db_path = db_path
        self.load_users()

    def load_users(self):
        try:
            with open(self.db_path, "r") as f:
                self.users = json.load(f)
        except FileNotFoundError:
            self.users = {}

    def save_users(self):
        with open(self.db_path, "w") as f:
            json.dump(self.users, f, indent=4)

    def validate_user(self, username, password):
        user = self.users.get(username)
        if user and user["password"] == password:
            return user["role"]
        return None

    def add_user(self, username, password, role):
        self.users[username] = {"password": password, "role": role}
        self.save_users()
