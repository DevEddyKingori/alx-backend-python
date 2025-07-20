import time
import sqlite3
import functools

# Reusing the connection decorator from previous task


def with_db_connection(func):
    """Handles opening/closing database connections automatically."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('users.db')
        try:
            kwargs['conn'] = conn
            return func(*args, **kwargs)
        finally:
            conn.close()
    return wrapper


def retry_on_failure(retries=3, delay=2):
    """
    Decorator that retries a function if it raises an exception.

    Args:
        retries (int): Max number of retry attempts (default: 3).
        delay (int): Seconds to wait between retries (default: 2).
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None

            for attempt in range(1, retries + 1):
                try:
                    # Attempt to execute the function
                    return func(*args, **kwargs)

                except Exception as e:
                    last_exception = e
                    if attempt < retries:
                        print(
                            f"Attempt {attempt} failed. Retrying in {delay} seconds...")
                        time.sleep(delay)

            # If all retries fail, raise the last exception
            raise last_exception

        return wrapper
    return decorator


@with_db_connection
@retry_on_failure(retries=3, delay=1)
def fetch_users_with_retry(conn):
    """Fetches all users from the database with automatic retry on failure."""
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()


# Example usage
users = fetch_users_with_retry()
print(users)
