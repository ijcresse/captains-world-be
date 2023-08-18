#contains a few useful methods for interacting with users and validating their sessions.
import bcrypt

class User:
    def __init__(self, data):
        if 'username' not in data or 'password' not in data:
            raise ValueError("Missing user or password parameter")
        self.username = data['username']
        self.hashed_pw = data['password'].encode('utf-8')

    def check_user(self, username, hashed_pw):
        if username is None or self.username != username:
            return False
        try:
            hashed_pw = hashed_pw.encode('utf-8')
            return bcrypt.checkpw(self.hashed_pw, hashed_pw)
        except ValueError as ve:
            print("Failure to check password via bcrypt")
            print(ve)
            return False
        #return self.username == username and bcrypt.checkpw(self.hashed_pw, hashed_pw)
    
    def get_user_query(self):
        return f"SELECT c_username, c_password FROM t_users WHERE c_username='{self.username}'"

    def update_login_query(self):
        return f"UPDATE t_users SET c_last_login=NOW() where c_username='{self.username}'"