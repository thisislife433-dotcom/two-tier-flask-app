from flask import Flask, render_template, request, redirect
import mysql.connector
import os

app = Flask(__name__)

def get_db():
    return mysql.connector.connect(
        host=os.environ.get("MYSQL_HOST", "mysql"),
        user=os.environ.get("MYSQL_USER", "root"),
        password=os.environ.get("MYSQL_PASSWORD", "root"),
        database=os.environ.get("MYSQL_DB", "devops")
    )

@app.route("/", methods=["GET", "POST"])
def index():
    conn = get_db()
    cursor = conn.cursor()
    if request.method == "POST":
        message = request.form["message"]
        cursor.execute("INSERT INTO messages (message) VALUES (%s)", (message,))
        conn.commit()
        return redirect("/")
    cursor.execute("SELECT message FROM messages")
    messages = [row[0] for row in cursor.fetchall()]
    cursor.close()
    conn.close()
    return render_template("index.html", messages=messages)

@app.route("/health")
def health():
    return "OK", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)