from flask import Flask, jsonify, request
import pymysql
import os
import time

from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST

app = Flask(__name__)

DB_HOST = os.getenv("DB_HOST", "mysql")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

REQUEST_COUNT = Counter(
    "user_service_http_requests_total",
    "Total HTTP requests handled by the User Service",
    ["method", "endpoint", "status"]
)

REQUEST_LATENCY = Histogram(
    "user_service_http_request_duration_seconds",
    "HTTP request duration in seconds",
    ["method", "endpoint"]
)


@app.before_request
def start_request_timer():
    request.start_time = time.perf_counter()


@app.after_request
def record_request_metrics(response):
    # Exclude /metrics so Prometheus scraping does not inflate request metrics.
    if request.path != "/metrics":
        endpoint = request.url_rule.rule if request.url_rule else "unmatched"
        method = request.method

        REQUEST_COUNT.labels(
            method=method,
            endpoint=endpoint,
            status=str(response.status_code)
        ).inc()

        duration = time.perf_counter() - getattr(
            request, "start_time", time.perf_counter()
        )

        REQUEST_LATENCY.labels(
            method=method,
            endpoint=endpoint
        ).observe(duration)

    return response


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

        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT VERSION()")
                version = cursor.fetchone()[0]
        finally:
            connection.close()

        return jsonify({
            "database": "Connected",
            "mysql_version": version
        })

    except Exception as error:
        app.logger.exception("Database connection check failed")
        return jsonify({
            "database": "Connection Failed",
            "error": str(error)
        }), 500


@app.route("/metrics")
def metrics():
    return generate_latest(), 200, {
        "Content-Type": CONTENT_TYPE_LATEST
    }


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000
    )
