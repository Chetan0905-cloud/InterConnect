import os
import mysql.connector


def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host=os.getenv("DB_HOST", "127.0.0.1"),
            port=int(os.getenv("DB_PORT", "3306")),
            user=os.getenv("DB_USER", "root"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME", "interconnect"),
            use_pure=True,
            connection_timeout=5
        )

        return connection

    except Exception as e:
        print("MYSQL ERROR:", e)
        return None


if __name__ == "__main__":
    print("Testing MySQL connection...")

    connection = get_db_connection()

    if connection:
        print("DATABASE CONNECTED")
        connection.close()
    else:
        print("DATABASE CONNECTION FAILED")