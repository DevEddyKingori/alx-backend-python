#!/usr/bin/python3
import mysql.connector
from typing import Generator

def stream_user_ages() -> Generator[int, None, None]:
    """Generator function that streams user ages one by one"""
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='ALX_prodev'
    )
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT age FROM user_data")
        while True:
            age = cursor.fetchone()
            if age is None:
                break
            yield age[0]  # Yield just the age value
    finally:
        cursor.close()
        conn.close()

def calculate_average_age() -> None:
    """Calculate and print the average age of users"""
    total = 0
    count = 0
    
    # First loop: iterate through ages
    for age in stream_user_ages():
        total += age
        count += 1
    
    # Calculate average
    average = total / count if count > 0 else 0
    
    # Print result
    print(f"Average age of users: {average:.2f}")

if __name__ == "__main__":
    calculate_average_age()
