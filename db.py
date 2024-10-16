import sqlite3

class Database:
    def __init__(self, db_name="my_dev_db.db"):
        """Initialize the database connection."""
        self.db_name = db_name
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        self.create_users_table()

    def create_users_table(self):
        """Create the users_creds table if it doesn't exist."""
        query = """
                    CREATE TABLE IF NOT EXISTS users_creds (
                     id INTEGER PRIMARY KEY AUTOINCREMENT,
                     username TEXT NOT NULL UNIQUE,
                        password TEXT NOT NULL
                    )
        """
        self.cursor.execute(query)
        self.conn.commit()

    def add_user(self, username, password):
        """Add a new user to the users_creds table."""
        try:
            query = "INSERT INTO users_creds (username, password) VALUES (?, ?)"
            self.cursor.execute(query, (username, password))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False  # Username already exists

    def authenticate_user(self, username, password):
        """Authenticate user by checking if the username and password match."""
        query = "SELECT * FROM users_creds WHERE username = ? AND password = ?"
        self.cursor.execute(query, (username, password))
        result = self.cursor.fetchone()
        return result is not None

    def close(self):
        """Close the database connection."""
        self.conn.close()
