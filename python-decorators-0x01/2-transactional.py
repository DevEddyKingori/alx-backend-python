import sqlite3
import functools

# Reusing the connection decorator from previous tasks


def with_db_connection(func):
    """Handles opening/closing database connections."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('users.db')
        try:
            kwargs['conn'] = conn
            return func(*args, **kwargs)
        finally:
            conn.close()
    return wrapper


def transactional(func):
    """
    Decorator that manages database transactions:
    - Commits on success.
    - Rolls back on failure.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = kwargs.get('conn')
        if not conn:
            raise ValueError("No database connection provided.")

        try:
            result = func(*args, **kwargs)  # Execute the function
            conn.commit()  # Commit if successful
            print("Transaction committed.")
            return result
        except Exception as e:
            conn.rollback()  # Roll back on error
            print(f"Transaction rolled back due to: {e}")
            raise  # Re-raise the exception
    return wrapper


@with_db_connection
@transactional
def update_user_email(conn, user_id, new_email):
    """Updates a user's email within a transaction."""
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET email = ? WHERE id = ?",
                   (new_email, user_id))
    print(f"Updated email for user {user_id} to {new_email}")


# Example usage
update_user_email(user_id=1, new_email='Crawford_Cartwright@hotmail.com')
