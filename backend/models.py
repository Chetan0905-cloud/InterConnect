from database import get_db_connection


def create_user(name, email, password, role):
    connection = get_db_connection()

    if not connection:
        return False, "Database connection failed"

    try:
        cursor = connection.cursor()

        query = """
            INSERT INTO users (name, email, password, role)
            VALUES (%s, %s, %s, %s)
        """

        cursor.execute(query, (name, email, password, role))
        connection.commit()

        return True, "User created successfully"

    except Exception as e:
        connection.rollback()
        return False, str(e)

    finally:
        cursor.close()
        connection.close()
