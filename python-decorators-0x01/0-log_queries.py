import sqlite3
import functools
from datetime import datetime

def log_queries(func):
    """
    Decorator that logs SQL queries before executing them.
    
    Args:
        func: The function to be decorated (in this case, fetch_all_users)
    
    Returns:
        A wrapped function that logs the query before executing it
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):# Check if 'query' is in kwargs (keyword arguments)
        if 'query' in kwargs:
            print(f"Executing query: {kwargs['query']}")# Alternatively, check if query is passed as first positional argument
        elif args and len(args) > 0:
            print(f"Executing query: {args[0]}")
        
        # Call the original function with all its arguments
        return func(*args, **kwargs)
    return wrapper

@log_queries
def fetch_all_users(query):
    """
    Fetches all users from the database by executing the given query.
    
    Args:
        query: SQL query string to execute
        
    Returns:
        List of tuples containing user data
    """
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

# Fetch users while logging the query
users = fetch_all_users(query="SELECT * FROM users")