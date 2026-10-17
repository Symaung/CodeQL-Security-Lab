from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

DB_NAME = "users.db"


def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT,
            email TEXT
        )
    """)

    cursor.execute("""
        INSERT OR IGNORE INTO users
        (id, username, email)
        VALUES (1, 'testuser', 'test@example.com')
    """)

    conn.commit()
    conn.close()


@app.route("/user")
def get_user():
    username = request.args.get("username", "")

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Intentionally vulnerable SQL query for CodeQL lab
    query = "SELECT * FROM users WHERE username = '" + username + "'"

    cursor.execute(query)
    result = cursor.fetchall()

    conn.close()

    return jsonify(result)


if __name__ == "__main__":
    init_db()
    app.run(debug=False, host="127.0.0.1", port=5000)