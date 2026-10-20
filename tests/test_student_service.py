import pytest

from app.services import student_service as svc


def test_add_student_success():
    student = svc.add_student("S200", "Riya Patel", "riya@example.com")
    assert student["student_id"] == "S200"
    assert len(svc.list_students()) == 3


def test_add_duplicate_student_raises_error():
    with pytest.raises(svc.RuleViolationError):
        svc.add_student("S101", "Copy Cat", "copy@example.com")


def test_delete_unknown_student_raises_error():
    with pytest.raises(svc.NotFoundError):
        svc.delete_student("S999")


def test_delete_student_with_active_enrollment_fails():
    svc.enroll("S101", "CS101")
    with pytest.raises(svc.RuleViolationError):
        svc.delete_student("S101")
