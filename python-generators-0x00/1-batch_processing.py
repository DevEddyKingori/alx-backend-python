import mysql.connector
from typing import Generator, Dict, List

def stream_users_in_batches(batch_size: int) -> Generator[List[Dict[str, str | int]], None, None]:
    """Stream users from database in batches"""
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='password',
        database='ALX_prodev'
    )
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM user_data")
    
    try:
        while True:
            batch = cursor.fetchmany(batch_size)
            if not batch:
                return  # Explicit return when done
            yield batch  # Yield each batch
    finally:
        cursor.close()
        conn.close()

def batch_processing(batch_size: int = 50) -> None:
    """Process batches of users and filter those over 25"""
    for batch in stream_users_in_batches(batch_size):
        for user in batch:
            if user['age'] > 25:
                print(user)
