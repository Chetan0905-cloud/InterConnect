from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash

from  models import create_user
from .database import get_db_connection

app = Flask(__name__)
CORS(app)


# =====================================================
# SIGNUP
# =====================================================

@app.route("/signup", methods=["POST"])
def signup():

    data = request.get_json()

    name = data.get("name")
    email = data.get("email")
    password = data.get("password")
    role = data.get("role")

    # Convert frontend role values to MySQL enum values
    if role == "seeker":
        role = "Support Seeker"

    elif role == "supporter":
        role = "Supporter"

    if not name or not email or not password or not role:
        return jsonify({
            "success": False,
            "message": "All fields are required"
        }), 400

    hashed_password = generate_password_hash(password)

    success, message = create_user(
        name,
        email,
        hashed_password,
        role
    )

    if success:

        return jsonify({
            "success": True,
            "message": "Account created successfully"
        }), 201

    if "Duplicate entry" in message:

        return jsonify({
            "success": False,
            "message": "Email already registered"
        }), 409

    return jsonify({
        "success": False,
        "message": message
    }), 500


# =====================================================
# LOGIN
# =====================================================

@app.route("/login", methods=["POST"])
def login():

    data = request.get_json()

    email = data.get("email")
    password = data.get("password")

    if not email or not password:

        return jsonify({
            "success": False,
            "message": "Email and password are required"
        }), 400

    connection = get_db_connection()

    if not connection:

        return jsonify({
            "success": False,
            "message": "Database connection failed"
        }), 500

    cursor = None

    try:

        cursor = connection.cursor(dictionary=True, buffered=True)

        cursor.execute(
            "SELECT * FROM users WHERE email = %s",
            (email,)
        )

        user = cursor.fetchone()

        if not user:

            return jsonify({
                "success": False,
                "message": "Invalid email or password"
            }), 401

        if not check_password_hash(
            user["password"],
            password
        ):

            return jsonify({
                "success": False,
                "message": "Invalid email or password"
            }), 401

        return jsonify({

            "success": True,

            "message": "Login successful",

            "user": {
                "id": user["id"],
                "name": user["name"],
                "email": user["email"],
                "role": user["role"]
            }

        }), 200

    finally:

        if cursor:
            cursor.close()

        connection.close()
        # =====================================================
# GET SUPPORT REQUESTS FOR A SUPPORTER
# =====================================================

@app.route("/support-requests/<int:supporter_id>", methods=["GET"])
def get_support_requests(supporter_id):

    connection = get_db_connection()

    if not connection:
        return jsonify({
            "success": False,
            "message": "Database connection failed"
        }), 500

    cursor = None

    try:

        cursor = connection.cursor(dictionary=True, buffered=True)

        cursor.execute("""
            SELECT
                support_requests.id,
                support_requests.seeker_id,
                support_requests.supporter_id,
                support_requests.status,
                support_requests.created_at,
                users.name AS seeker_name,
                users.email AS seeker_email
            FROM support_requests
            INNER JOIN users
                ON support_requests.seeker_id = users.id
            WHERE support_requests.supporter_id = %s
            ORDER BY support_requests.created_at DESC
        """, (supporter_id,))

        requests = cursor.fetchall()

        return jsonify({
            "success": True,
            "requests": requests
        }), 200

    except Exception as e:

        return jsonify({
            "success": False,
            "message": str(e)
        }), 500

    finally:

        if cursor:
            cursor.close()

        connection.close()


# =====================================================
# UPDATE SUPPORT REQUEST STATUS
# =====================================================

@app.route("/support-requests/<int:request_id>", methods=["PUT"])
def update_support_request(request_id):

    data = request.get_json()

    status = data.get("status")

    if status not in ["Accepted", "Rejected"]:

        return jsonify({
            "success": False,
            "message": "Invalid status"
        }), 400

    connection = get_db_connection()

    if not connection:

        return jsonify({
            "success": False,
            "message": "Database connection failed"
        }), 500

    cursor = None

    try:

        cursor = connection.cursor()

        cursor.execute("""
            UPDATE support_requests
            SET status = %s
            WHERE id = %s
        """, (status, request_id))

        connection.commit()

        if cursor.rowcount == 0:

            return jsonify({
                "success": False,
                "message": "Request not found"
            }), 404

        return jsonify({
            "success": True,
            "message": f"Request {status.lower()} successfully"
        }), 200

    except Exception as e:

        connection.rollback()

        return jsonify({
            "success": False,
            "message": str(e)
        }), 500

    finally:

        if cursor:
            cursor.close()

        connection.close()


# =====================================================
# GET SUPPORTERS
# =====================================================

@app.route("/supporters", methods=["GET"])
def get_supporters():

    connection = get_db_connection()

    if not connection:

        return jsonify({
            "success": False,
            "message": "Database connection failed"
        }), 500

    cursor = None

    try:

        cursor = connection.cursor(dictionary=True, buffered=True)

        cursor.execute("""
            SELECT
                users.id,
                users.name,
                users.email,
                users.role,
                supporter_profiles.qualification,
                supporter_profiles.bio,
                supporter_profiles.availability,
                supporter_profiles.location,
                supporter_profiles.is_verified
            FROM users
            INNER JOIN supporter_profiles
                ON users.id = supporter_profiles.user_id
            WHERE users.role = 'Supporter'
        """)

        supporters = cursor.fetchall()

        return jsonify({

            "success": True,

            "supporters": supporters

        }), 200

    except Exception as e:

        return jsonify({

            "success": False,
            "message": str(e)

        }), 500

    finally:

        if cursor:
            cursor.close()

        connection.close()


# =====================================================
# CREATE SUPPORT REQUEST
# =====================================================

@app.route("/support-requests", methods=["POST"])
def create_support_request():

    data = request.get_json()

    seeker_id = data.get("seeker_id")
    supporter_id = data.get("supporter_id")

    if not seeker_id or not supporter_id:

        return jsonify({
            "success": False,
            "message": "Seeker ID and Supporter ID are required"
        }), 400

    connection = get_db_connection()

    if not connection:

        return jsonify({
            "success": False,
            "message": "Database connection failed"
        }), 500

    cursor = None

    try:

        cursor = connection.cursor(dictionary=True, buffered=True)

        # Check whether a pending request already exists
        cursor.execute(
            """
            SELECT id, status
            FROM support_requests
            WHERE seeker_id = %s
            AND supporter_id = %s
            AND status = 'Pending'
            """,
            (seeker_id, supporter_id)
        )

        existing_request = cursor.fetchone()

        if existing_request:

            return jsonify({
                "success": False,
                "message": "Request already sent"
            }), 409


        # Insert new request
        cursor.execute(
            """
            INSERT INTO support_requests
            (seeker_id, supporter_id, status)
            VALUES (%s, %s, 'Pending')
            """,
            (seeker_id, supporter_id)
        )

        connection.commit()

        return jsonify({
            "success": True,
            "message": "Connection request sent successfully"
        }), 201


    except Exception as e:

        connection.rollback()

        return jsonify({
            "success": False,
            "message": str(e)
        }), 500


    finally:

        if cursor:
            cursor.close()

        connection.close()

# =====================================================
# SEND MESSAGE
# =====================================================

@app.route("/messages", methods=["POST"])
def send_message():

    data = request.get_json()

    sender_id = data.get("sender_id")
    receiver_id = data.get("receiver_id")
    message = data.get("message")

    if not sender_id or not receiver_id or not message:
        return jsonify({
            "success": False,
            "message": "Sender, receiver and message are required"
        }), 400

    connection = get_db_connection()

    if not connection:
        return jsonify({
            "success": False,
            "message": "Database connection failed"
        }), 500

    cursor = None

    try:

        cursor = connection.cursor(dictionary=True, buffered=True)

        # Make sure the users are connected
        cursor.execute("""
    SELECT id
    FROM support_requests
    WHERE (
        seeker_id = %s
        AND supporter_id = %s
        AND status = 'Accepted'
    )
    OR (
        seeker_id = %s
        AND supporter_id = %s
        AND status = 'Accepted'
    )
""", (
    sender_id,
    receiver_id,
    receiver_id,
    sender_id
))

        connection_check = cursor.fetchone()

        if not connection_check:

            return jsonify({
                "success": False,
                "message": "Messaging is available after the support request is accepted."
            }), 403

        cursor.execute("""
            INSERT INTO messages
            (sender_id, receiver_id, message)
            VALUES (%s, %s, %s)
        """, (
            sender_id,
            receiver_id,
            message
        ))

        connection.commit()

        return jsonify({
            "success": True,
            "message": "Message sent successfully"
        }), 201

    except Exception as e:

        connection.rollback()

        return jsonify({
            "success": False,
            "message": str(e)
        }), 500

    finally:

        if cursor:
            cursor.close()

        connection.close()


# =====================================================
# GET MESSAGES
# =====================================================

@app.route("/messages/<int:user1_id>/<int:user2_id>", methods=["GET"])
def get_messages(user1_id, user2_id):

    connection = get_db_connection()

    if not connection:

        return jsonify({
            "success": False,
            "message": "Database connection failed"
        }), 500

    cursor = None

    try:

        cursor = connection.cursor(dictionary=True, buffered=True)

        cursor.execute("""
            SELECT
                messages.id,
                messages.sender_id,
                messages.receiver_id,
                messages.message,
                messages.created_at,
                sender.name AS sender_name,
                receiver.name AS receiver_name
            FROM messages
            INNER JOIN users AS sender
                ON messages.sender_id = sender.id
            INNER JOIN users AS receiver
                ON messages.receiver_id = receiver.id
            WHERE
                (
                    messages.sender_id = %s
                    AND messages.receiver_id = %s
                )
                OR
                (
                    messages.sender_id = %s
                    AND messages.receiver_id = %s
                )
            ORDER BY messages.created_at ASC
        """, (
            user1_id,
            user2_id,
            user2_id,
            user1_id
        ))

        messages = cursor.fetchall()

        return jsonify({
            "success": True,
            "messages": messages
        }), 200

    except Exception as e:

        return jsonify({
            "success": False,
            "message": str(e)
        }), 500

    finally:

        if cursor:
            cursor.close()

        connection.close()
        # =====================================================
# GET ACCEPTED CONNECTIONS
# =====================================================

@app.route("/connections/<int:user_id>", methods=["GET"])
def get_connections(user_id):

    connection = get_db_connection()

    if not connection:
        return jsonify({
            "success": False,
            "message": "Database connection failed"
        }), 500

    cursor = None

    try:

        cursor = connection.cursor(dictionary=True, buffered=True)

        cursor.execute("""
            SELECT
                sr.id AS request_id,

                CASE
                    WHEN sr.seeker_id = %s
                    THEN u_supporter.id
                    ELSE u_seeker.id
                END AS user_id,

                CASE
                    WHEN sr.seeker_id = %s
                    THEN u_supporter.name
                    ELSE u_seeker.name
                END AS name,

                CASE
                    WHEN sr.seeker_id = %s
                    THEN u_supporter.role
                    ELSE u_seeker.role
                END AS role

            FROM support_requests sr

            INNER JOIN users u_seeker
                ON sr.seeker_id = u_seeker.id

            INNER JOIN users u_supporter
                ON sr.supporter_id = u_supporter.id

            WHERE
                (sr.seeker_id = %s
                 OR sr.supporter_id = %s)

                AND sr.status = 'Accepted'

            ORDER BY sr.created_at DESC
        """, (
            user_id,
            user_id,
            user_id,
            user_id,
            user_id
        ))

        connections = cursor.fetchall()

        return jsonify({
            "success": True,
            "connections": connections
        }), 200

    except Exception as e:

        return jsonify({
            "success": False,
            "message": str(e)
        }), 500

    finally:

        if cursor:
            cursor.close()

        connection.close()
# =====================================================
# GET PROFILE
# =====================================================

@app.route("/profile/<int:user_id>", methods=["GET"])
def get_profile(user_id):

    connection = get_db_connection()

    if not connection:
        return jsonify({
            "success": False,
            "message": "Database connection failed"
        }), 500

    cursor = None

    try:
        cursor = connection.cursor(
            dictionary=True,
            buffered=True
        )

        cursor.execute("""
            SELECT
                id,
                name,
                email,
                age,
                location,
                interests,
                qualification,
                college,
                bio,
                availability,
                role
            FROM users
            WHERE id = %s
        """, (user_id,))

        user = cursor.fetchone()

        if not user:
            return jsonify({
                "success": False,
                "message": "User not found"
            }), 404

        return jsonify({
            "success": True,
            "user": user
        }), 200

    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        }), 500

    finally:
        if cursor:
            cursor.close()

        connection.close()


# =====================================================
# UPDATE PROFILE
# =====================================================

@app.route("/profile/<int:user_id>", methods=["PUT"])
def update_profile(user_id):

    data = request.get_json()

    if not data:
        return jsonify({
            "success": False,
            "message": "No profile data received"
        }), 400

    connection = get_db_connection()

    if not connection:
        return jsonify({
            "success": False,
            "message": "Database connection failed"
        }), 500

    cursor = None

    try:
        cursor = connection.cursor(
            dictionary=True,
            buffered=True
        )

        cursor.execute(
            "SELECT id FROM users WHERE id = %s",
            (user_id,)
        )

        existing_user = cursor.fetchone()

        if not existing_user:
            return jsonify({
                "success": False,
                "message": "User not found"
            }), 404

        name = data.get("name")
        age = data.get("age")
        location = data.get("location")
        interests = data.get("interests")
        qualification = data.get("qualification")
        college = data.get("college")
        bio = data.get("bio")
        availability = data.get("availability")

        if not name or not name.strip():
            return jsonify({
                "success": False,
                "message": "Name is required"
            }), 400

        cursor.execute("""
            UPDATE users
            SET
                name = %s,
                age = %s,
                location = %s,
                interests = %s,
                qualification = %s,
                college = %s,
                bio = %s,
                availability = %s
            WHERE id = %s
        """, (
            name.strip(),
            age if age not in ["", None] else None,
            location,
            interests,
            qualification,
            college,
            bio,
            availability,
            user_id
        ))

        connection.commit()

        cursor.execute("""
            SELECT
                id,
                name,
                email,
                age,
                location,
                interests,
                qualification,
                college,
                bio,
                availability,
                role
            FROM users
            WHERE id = %s
        """, (user_id,))

        updated_user = cursor.fetchone()

        return jsonify({
            "success": True,
            "message": "Profile updated successfully",
            "user": updated_user
        }), 200

    except Exception as e:
        connection.rollback()

        return jsonify({
            "success": False,
            "message": str(e)
        }), 500

    finally:
        if cursor:
            cursor.close()

        connection.close()


# =====================================================
# RUN SERVER
# =====================================================

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )
