import pytest

from app.services import student_service as svc


def test_enroll_success():
    result = svc.enroll("S101", "CS101")
    assert result["status"] == "ACTIVE"
    assert svc.current_credits("S101") == 4


def test_duplicate_enrollment_fails():
    svc.enroll("S101", "CS101")
    with pytest.raises(svc.RuleViolationError):
        svc.enroll("S101", "CS101")


def test_credit_limit_enforced():
    for course in ["CS101", "CS102", "MA101", "PH101"]:
        svc.enroll("S101", course)
    assert svc.current_credits("S101") == 16
    with pytest.raises(svc.RuleViolationError):
        svc.enroll("S101", "EN101")


def test_exactly_18_credits_allowed():
    for course in ["CS101", "CS102", "MA101", "EN101", "HI101"]:
        svc.enroll("S101", course)
    assert svc.current_credits("S101") == 18


def test_drop_frees_credits():
    enrollment = svc.enroll("S101", "CS101")
    svc.drop(enrollment["enrollment_id"])
    assert svc.current_credits("S101") == 0


def test_unknown_course_raises_not_found():
    with pytest.raises(svc.NotFoundError):
        svc.enroll("S101", "XX999")


def test_gpa_calculation():
    first = svc.enroll("S101", "CS101")
    second = svc.enroll("S101", "EN101")
    svc.assign_grade(first["enrollment_id"], "A")
    svc.assign_grade(second["enrollment_id"], "B")
    assert svc.calculate_gpa("S101") == 3.57


def test_invalid_grade_rejected():
    enrollment = svc.enroll("S101", "CS101")
    with pytest.raises(svc.RuleViolationError):
        svc.assign_grade(enrollment["enrollment_id"], "Z")
