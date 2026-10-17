from flask import Blueprint, jsonify, request

from app.services import student_service as svc

api_bp = Blueprint("api", __name__)


@api_bp.errorhandler(svc.NotFoundError)
def handle_not_found(error):
    return jsonify({"error": str(error)}), 404


@api_bp.errorhandler(svc.RuleViolationError)
def handle_rule_violation(error):
    return jsonify({"error": str(error)}), 409


@api_bp.errorhandler(ValueError)
def handle_bad_input(error):
    return jsonify({"error": str(error)}), 400


@api_bp.route("/health", methods=["GET"])
def healthcheck():
    return jsonify({
        "service": "Enterprise Student Record & Academic Management Platform",
        "status": "UP",
        "version": "1.0.0"
    }), 200


@api_bp.route("/students", methods=["GET"])
def list_students():
    students = svc.list_students()
    return jsonify({"students": students, "count": len(students)}), 200


@api_bp.route("/students", methods=["POST"])
def add_student():
    data = request.get_json(silent=True) or {}
    student = svc.add_student(
        data.get("student_id"), data.get("name"), data.get("email")
    )
    return jsonify({"student": student}), 201


@api_bp.route("/students/<student_id>", methods=["DELETE"])
def delete_student(student_id):
    svc.delete_student(student_id)
    return jsonify({"message": "Student deleted"}), 200


@api_bp.route("/students/<student_id>/gpa", methods=["GET"])
def student_gpa(student_id):
    return jsonify({
        "student_id": student_id,
        "gpa": svc.calculate_gpa(student_id),
        "credits": svc.current_credits(student_id)
    }), 200


@api_bp.route("/courses", methods=["GET"])
def list_courses():
    courses = svc.list_courses()
    return jsonify({"courses": courses, "count": len(courses)}), 200


@api_bp.route("/enrollments", methods=["POST"])
def enroll():
    data = request.get_json(silent=True) or {}
    enrollment = svc.enroll(data.get("student_id"), data.get("course_id"))
    return jsonify({
        "enrollment": enrollment,
        "message": "Enrolled successfully"
    }), 201


@api_bp.route("/enrollments/<enrollment_id>", methods=["DELETE"])
def drop(enrollment_id):
    enrollment = svc.drop(enrollment_id)
    return jsonify({
        "enrollment": enrollment,
        "message": "Course dropped"
    }), 200


@api_bp.route("/enrollments/<enrollment_id>/grade", methods=["PUT"])
def assign_grade(enrollment_id):
    data = request.get_json(silent=True) or {}
    enrollment = svc.assign_grade(enrollment_id, data.get("grade"))
    return jsonify({
        "enrollment": enrollment,
        "message": "Grade assigned"
    }), 200
