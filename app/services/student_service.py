from app.models.student import Student
from database.db import db

MAX_CREDITS = 18

GRADE_POINTS = {"A": 4.0, "B": 3.0, "C": 2.0, "D": 1.0, "F": 0.0}


class NotFoundError(Exception):
    """Raised when a student, course or enrollment does not exist."""


class RuleViolationError(Exception):
    """Raised when a business rule is broken."""


def list_students():
    return [s.to_dict() for s in db.students.values()]


def list_courses():
    return [c.to_dict() for c in db.courses.values()]


def add_student(student_id, name, email):
    with db.lock:
        if student_id in db.students:
            raise RuleViolationError("Student already exists")
        student = Student(student_id, name, email)
        db.students[student_id] = student
        return student.to_dict()


def active_enrollments(student_id):
    return [
        e for e in db.enrollments
        if e["student_id"] == student_id and e["status"] == "ACTIVE"
    ]


def current_credits(student_id):
    return sum(
        db.courses[e["course_id"]].credits
        for e in active_enrollments(student_id)
    )


def delete_student(student_id):
    with db.lock:
        if student_id not in db.students:
            raise NotFoundError("Student not found")
        if active_enrollments(student_id):
            raise RuleViolationError("Cannot delete student with active enrollments")
        del db.students[student_id]


def enroll(student_id, course_id):
    with db.lock:
        if student_id not in db.students:
            raise NotFoundError("Student not found")
        if course_id not in db.courses:
            raise NotFoundError("Course not found")

        course = db.courses[course_id]
        mine = active_enrollments(student_id)

        if any(e["course_id"] == course_id for e in mine):
            raise RuleViolationError("Student is already enrolled in this course")

        taken = sum(
            1 for e in db.enrollments
            if e["course_id"] == course_id and e["status"] == "ACTIVE"
        )
        if taken >= course.capacity:
            raise RuleViolationError("Course is full")

        if current_credits(student_id) + course.credits > MAX_CREDITS:
            raise RuleViolationError(
                "Credit limit exceeded: maximum {} credits per semester".format(MAX_CREDITS)
            )

        enrollment = {
            "enrollment_id": db.next_enrollment_id(),
            "student_id": student_id,
            "course_id": course_id,
            "status": "ACTIVE",
            "grade": None,
        }
        db.enrollments.append(enrollment)
        return enrollment


def _find_enrollment(enrollment_id):
    for e in db.enrollments:
        if e["enrollment_id"] == enrollment_id:
            return e
    raise NotFoundError("Enrollment not found")


def drop(enrollment_id):
    with db.lock:
        enrollment = _find_enrollment(enrollment_id)
        if enrollment["status"] != "ACTIVE":
            raise RuleViolationError("Enrollment is not active")
        enrollment["status"] = "DROPPED"
        return enrollment


def assign_grade(enrollment_id, grade):
    with db.lock:
        enrollment = _find_enrollment(enrollment_id)
        grade = str(grade).upper()
        if grade not in GRADE_POINTS:
            raise RuleViolationError("Grade must be one of A, B, C, D, F")
        if enrollment["status"] != "ACTIVE":
            raise RuleViolationError("Cannot grade a dropped enrollment")
        enrollment["grade"] = grade
        return enrollment


def calculate_gpa(student_id):
    with db.lock:
        if student_id not in db.students:
            raise NotFoundError("Student not found")
        graded = [
            e for e in db.enrollments
            if e["student_id"] == student_id
            and e["status"] == "ACTIVE" and e["grade"]
        ]
        if not graded:
            return 0.0
        points = sum(
            GRADE_POINTS[e["grade"]] * db.courses[e["course_id"]].credits
            for e in graded
        )
        total = sum(db.courses[e["course_id"]].credits for e in graded)
        return round(points / total, 2)
