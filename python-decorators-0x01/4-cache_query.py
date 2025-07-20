import time
import sqlite3
import functools

# Global dictionary to store cached queries
query_cache = {}


def cache_query(func):
    """
    Decorator that caches database query results.
    - Uses the SQL query as the cache key.
    - Returns cached results if available.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Extract the query from kwargs (or args if needed)
        query = kwargs.get('query') or (args[1] if len(args) > 1 else None)

        if query not in query_cache:
            # If not cached, execute the query and store the result
            result = func(*args, **kwargs)
            query_cache[query] = result
            print("Query executed and cached.")
        else:
            print("Returning cached result.")

        return query_cache[query]
    return wrapper


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


@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    """Fetches users from the database (with caching)."""
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()


# Example usage
print("First call (executes query):")
users = fetch_users_with_cache(query="SELECT * FROM users")

print("\nSecond call (uses cache):")
users_again = fetch_users_with_cache(query="SELECT * FROM users")
