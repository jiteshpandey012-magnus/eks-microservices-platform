from flask import Flask, jsonify
import pymysql
import os

app = Flask(__name__)

DB_HOST = os.getenv("DB_HOST", "mysql")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")


def get_connection():
    return pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        connect_timeout=5
    )


@app.route("/")
def home():
    return jsonify({
        "service": "User Service",
        "status": "Running"
    })


@app.route("/health")
def health():
    return jsonify({
        "status": "UP"
    })


@app.route("/db")
def database_check():
    try:
        connection = get_connection()

        with connection.cursor() as cursor:
            cursor.execute("SELECT VERSION()")
            version = cursor.fetchone()[0]

        connection.close()

        return jsonify({
            "database": "Connected",
            "mysql_version": version
        })

    except Exception as error:
        return jsonify({
            "database": "Connection Failed",
            "error": str(error)
        }), 500


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000
    )
