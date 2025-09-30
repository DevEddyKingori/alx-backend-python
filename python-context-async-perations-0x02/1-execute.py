import sqlite3

class ExecuteQuery:
    """
    A reusable context manager for executing parameterized SQL queries.
    - Manages database connections automatically.
    - Executes the given query with parameters.
    - Returns query results.
    """
    def __init__(self, db_name='users.db', query=None, params=None):
        """
        Initialize with:
        - db_name: Database filename (default: 'users.db').
        - query: SQL query string (e.g., "SELECT * FROM users WHERE age > ?").
        - params: Query parameters (e.g., (25,)).
        """
        self.db_name = db_name
        self.query = query
        self.params = params if params is not None else ()
        self.conn = None
        self.cursor = None

    def __enter__(self):
        """Opens connection, executes query, and returns results."""
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        
        if self.query:
            self.cursor.execute(self.query, self.params)
            return self.cursor.fetchall()  # Return query results
        
        return None  # If no query provided

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Closes cursor and connection (even if an error occurs)."""
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
        
        # Return False to propagate exceptions (True would suppress them)
        return False


# Example usage
query = "SELECT * FROM users WHERE age > ?"
params = (25,)

with ExecuteQuery(query=query, params=params) as results:
    print("Users older than 25:")
    for row in results:
        print(row)