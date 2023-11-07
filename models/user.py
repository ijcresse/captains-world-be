import bcrypt

class User:
    def __init__(self, data):
        if 'username' not in data or 'password' not in data:
            raise ValueError("Missing user or password parameter")
        self.username = data['username']
        self.password = data['password'].encode('utf-8')

    def check_user(self, username, hashed_pw):
        if username is None or self.username != username:
            return False
        try:
            hashed_pw = hashed_pw.encode('utf-8')
            return bcrypt.checkpw(self.password, hashed_pw)
        except ValueError as ve:
            print("Failure to check password via bcrypt")
            print(ve)
            return False
        #return self.username == username and bcrypt.checkpw(self.hashed_pw, hashed_pw)
    
    def get_user_query(self):
        print(self.username)
        return f"SELECT c_username, c_password FROM t_users WHERE c_username='{self.username}'"

    def update_login_query(self):
        return f"UPDATE t_users SET c_last_login=NOW() where c_username='{self.username}'"
    
    @staticmethod
    def create_session(session):
        return f"INSERT INTO t_sessions (c_session_name) VALUES ('{session}')"
    
    @staticmethod
    def fetch_session(session):
        return f'SELECT c_id, c_login_time FROM t_sessions WHERE c_session_name="{session}"'
    
    @staticmethod
    #forces going thru fetch_session for c_id first
    def delete_session(session_id):
        return f'DELETE FROM t_sessions WHERE c_id={session_id}'