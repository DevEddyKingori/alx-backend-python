import asyncio
import aiosqlite

async def async_fetch_users():
    """
    Fetches all users from the database asynchronously.
    Returns:
        List of all users.
    """
    async with aiosqlite.connect("users.db") as db:
        async with db.execute("SELECT * FROM users") as cursor:
            return await cursor.fetchall()


async def async_fetch_older_users():
    """
    Fetches users older than 40 asynchronously.
    Returns:
        List of users with age > 40.
    """
    async with aiosqlite.connect("users.db") as db:
        async with db.execute("SELECT * FROM users WHERE age > 40") as cursor:
            return await cursor.fetchall()


async def fetch_concurrently():
    """
    Runs both fetch functions concurrently using asyncio.gather().
    Returns:
        Tuple of (all_users, older_users).
    """
    return await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )


# Run the concurrent fetch
if __name__ == "__main__":
    all_users, older_users = asyncio.run(fetch_concurrently())
    
    print("All users:")
    for user in all_users:
        print(user)
    
    print("\nUsers older than 40:")
    for user in older_users:
        print(user)