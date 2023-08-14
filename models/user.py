#contains a few useful methods for interacting with users and validating their sessions.
import bcrypt

class User:
    def __init__(self, data, salt):
        if 'username' not in data or 'password' not in data:
            raise ValueError("Missing user or password parameter")
        self.user = data['username']
        self.hashed_pw = bcrypt.hashpw(data['password'], salt)

    def check_pass(self, hashed_pw):
        return bcrypt.checkpw(self.hashed_pw, hashed_pw)
    
    def get_user_query(self):
        return f"SELECT c_username, c_password FROM t_users WHERE c_username='{self.username}'"

    def update_login_query(self):
        return f"UPDATE t_users SET c_last_login=NOW() where c_username='{self.username}'"