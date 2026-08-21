import os
import mysql.connector


def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host=os.getenv("MYSQLHOST", "127.0.0.1"),
            port=int(os.getenv("MYSQLPORT", "3306")),
            user=os.getenv("MYSQLUSER", "root"),
            password=os.getenv("MYSQLPASSWORD"),
            database=os.getenv("MYSQLDATABASE", "interconnect"),
            use_pure=True,
            connection_timeout=10
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