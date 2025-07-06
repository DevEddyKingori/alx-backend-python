import mysql.connector
from typing import Dict, Generator

def stream_users() -> Generator[Dict[str, str | int], None, None]:
    """
    Generator function that streams rows from user_data table one by one.
    
    Yields:
        Dict: A dictionary representing a row from user_data table with keys:
              'user_id', 'name', 'email', 'age'
    """
    connection = None
    cursor = None
    
    try:
        # Connect to the database
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='password',
            database='ALX_prodev'
        )
        
        # Create a server-side cursor (more memory efficient)
        cursor = connection.cursor(dictionary=True)
        
        # Execute the query
        cursor.execute("SELECT * FROM user_data")
        
        # Stream rows one by one
        while True:
            row = cursor.fetchone()
            if row is None:
                break
            yield row
            
    except mysql.connector.Error as e:
        print(f"Database error: {e}")
    finally:
        # Clean up resources
        if cursor:
            cursor.close()
        if connection:
            connection.close()
