from flask import Blueprint, jsonify

api_bp = Blueprint("api", __name__)


@api_bp.route("/health", methods=["GET"])
def healthcheck():
    return jsonify({
        "service": "Enterprise Student Record & Academic Management Platform",
        "status": "UP",
        "version": "1.0.0"
    }), 200
