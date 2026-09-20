##  Flask application

import os
import time
from functools import wraps
from hmac import compare_digest

from flask import Flask, jsonify, request, Response
from prometheus_flask_exporter import PrometheusMetrics

def metrics_auth_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        expected_username = os.getenv("METRICS_USERNAME")
        expected_password = os.getenv("METRICS_PASSWORD")
        auth = request.authorization

        if not expected_username or not expected_password:
            return Response(
                "Metrics authentication is not configured",
                status=503
            )

        username_ok = auth and compare_digest(
            auth.username or "",
            expected_username
        )

        password_ok = auth and compare_digest(
            auth.password or "",
            expected_password
        )

        if not username_ok or not password_ok:
            return Response(
                "Unauthorized",
                status=401,
                headers={"WWW-Authenticate": 'Basic realm="metrics"'}
            )

        return func(*args, **kwargs)

    return wrapper

app = Flask(__name__)
metrics = PrometheusMetrics(
    app,
    metrics_decorator=metrics_auth_required
)

@app.get("/")
def home():
    return """
    <h1>Production Readiness DevOps Lab</h1>
    <p>Application is running successfully.</p>
    """


##   Add a Health Endpoint

@app.get("/health")
def health():
    return jsonify(
        status="ok",
        service="production-readiness-lab",
        commit=os.getenv("RENDER_GIT_COMMIT", "local")
    )
    
    
    ##   Add a controlled 500 error endpoint
    
@app.get("/test-error")
def test_error():
    if os.getenv("ENABLE_FAILURE_TESTS") != "true":
        return jsonify(error="Failure testing disabled"), 403

    raise RuntimeError("Controlled staging failure")


##      Add a controlled slow endpoint

@app.get("/test-slow")
def test_slow():
    if os.getenv("ENABLE_FAILURE_TESTS") != "true":
        return jsonify(error="Failure testing disabled"), 403

    time.sleep(3)

    return jsonify(
        status="ok",
        message="Controlled slow request completed"
    )