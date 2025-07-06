
import csv
import uuid
import mysql.connector
from mysql.connector import Error
from typing import Generator, Tuple, Any

def connect_db() -> mysql.connector.connection.MySQLConnection:
    """Connect to the MySQL database server."""
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password=''
        )
        return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

def create_database(connection: mysql.connector.connection.MySQLConnection) -> None:
    """Create the ALX_prodev database if it doesn't exist."""
    try:
        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev")
        print("Database ALX_prodev created successfully")
    except Error as e:
        print(f"Error creating database: {e}")
    finally:
        if cursor:
            cursor.close()

def connect_to_prodev() -> mysql.connector.connection.MySQLConnection:
    """Connect to the ALX_prodev database."""
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='ALX_prodev'
        )
        return connection
    except Error as e:
        print(f"Error connecting to ALX_prodev: {e}")
        return None

def create_table(connection: mysql.connector.connection.MySQLConnection) -> None:
    """Create the user_data table if it doesn't exist."""
    try:
        cursor = connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_data (
                user_id VARCHAR(36) PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL,
                age DECIMAL(10, 0) NOT NULL,
                INDEX idx_user_id (user_id)
            )
        """)
        print("Table user_data created successfully")
    except Error as e:
        print(f"Error creating table: {e}")
    finally:
        if cursor:
            cursor.close()

def insert_data(connection: mysql.connector.connection.MySQLConnection, csv_file: str) -> None:
    """Insert data from CSV file into the database if it doesn't exist."""
    try:
        cursor = connection.cursor()
        
        # Check if table is empty
        cursor.execute("SELECT COUNT(*) FROM user_data")
        if cursor.fetchone()[0] > 0:
            print("Data already exists in the table")
            return

        with open(csv_file, mode='r') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                # Generate UUID if not present in CSV
                user_id = row.get('user_id', str(uuid.uuid4()))
                cursor.execute("""
                    INSERT INTO user_data (user_id, name, email, age)
                    VALUES (%s, %s, %s, %s)
                """, (user_id, row['name'], row['email'], row['age']))
        
        connection.commit()
        print("Data inserted successfully")
    except Error as e:
        connection.rollback()
        print(f"Error inserting data: {e}")
    except FileNotFoundError:
        print(f"CSV file {csv_file} not found")
    finally:
        if cursor:
            cursor.close()

def stream_users(connection: mysql.connector.connection.MySQLConnection) -> Generator[Tuple[Any, ...], None, None]:
    """
    Generator function that streams rows from user_data table one by one.
    
    Args:
        connection: MySQL database connection
    
    Yields:
        Tuple: A row from the user_data table
    """
    cursor = None
    try:
        cursor = connection.cursor(buffered=True)
        cursor.execute("SELECT * FROM user_data")
        
        while True:
            row = cursor.fetchone()
            if row is None:
                break
            yield row
    except Error as e:
        print(f"Error streaming users: {e}")
    finally:
        if cursor:
            cursor.close()

# Example usage of the generator:
if __name__ == "__main__":
    conn = connect_to_prodev()
    if conn:
        user_generator = stream_users(conn)
        for i, user in enumerate(user_generator, 1):
            print(f"User {i}: {user}")
            if i >= 5:  # Just show first 5 for demo
                break
        conn.close()
