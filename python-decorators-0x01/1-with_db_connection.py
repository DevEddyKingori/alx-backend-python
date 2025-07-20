import sqlite3
import functools


def with_db_connection(func):
    """
    Decorator that handles database connection lifecycle.

    Opens a connection, passes it to the function, and ensures it's closed.

    Args:
        func: The function to be decorated (in this case, get_user_by_id)

    Returns:
        A wrapped function that manages the database connection
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Open a new database connection
        conn = sqlite3.connect('users.db')
        try:
            # Add the connection to the function's keyword arguments
            kwargs['conn'] = conn
            # Execute the function with all arguments
            result = func(*args, **kwargs)
            return result
        finally:
            # Ensure connection is closed even if an error occurs
            conn.close()
    return wrapper


@with_db_connection
def get_user_by_id(user_id, conn=None):
    """
    Fetches a user by their ID using the provided database connection.

    Args:
        user_id: The ID of the user to fetch
        conn: Database connection (injected by decorator)

    Returns:
        A tuple containing user data or None if not found
    """
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    return cursor.fetchone()


# Fetch user by ID with automatic connection handling
user = get_user_by_id(user_id=1)
print(user)
