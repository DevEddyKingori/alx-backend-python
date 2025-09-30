import sqlite3

class DatabaseConnection:
    """
    A custom context manager for SQLite database connections.
    - Opens a connection on __enter__.
    - Closes it on __exit__ (even if an error occurs).
    """
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = None

    def __enter__(self):
        """Opens the connection and returns a cursor."""
        self.conn = sqlite3.connect(self.db_name)
        return self.conn.cursor()  # Return cursor for query execution

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Closes the connection (handles exceptions if any)."""
        if self.conn:
            self.conn.close()
        # Return False to propagate exceptions (True would suppress them)


# Example usage
with DatabaseConnection('users.db') as cursor:
    cursor.execute("SELECT * FROM users")
    results = cursor.fetchall()
    print("Users in the database:")
    for row in results:
        print(row)