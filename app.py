##  Flask application

import os
import time

from flask import Flask, jsonify

app = Flask(__name__)


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