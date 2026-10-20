import threading

from app.models.student import Student
from app.models.course import Course


class Database:
    """Thread-safe in-memory data store with seed data."""

    def __init__(self):
        self.lock = threading.RLock()
        self.reset()

    def reset(self):
        with self.lock:
            self.students = {}
            self.courses = {}
            self.enrollments = []
            self.enrollment_counter = 0
            self._seed()

    def _seed(self):
        for s in [
            Student("S101", "Aarav Sharma", "aarav@example.com"),
            Student("S102", "Meera Nair", "meera@example.com"),
        ]:
            self.students[s.student_id] = s

        for c in [
            Course("CS101", "Intro to Programming", 4, "Dr. Rao"),
            Course("CS102", "Data Structures", 4, "Dr. Iyer"),
            Course("MA101", "Calculus", 4, "Dr. Mehta"),
            Course("PH101", "Physics", 4, "Dr. Singh"),
            Course("EN101", "Technical Writing", 3, "Dr. Das"),
            Course("HI101", "World History", 3, "Dr. Khan"),
        ]:
            self.courses[c.course_id] = c

    def next_enrollment_id(self):
        with self.lock:
            self.enrollment_counter += 1
            return "E-{:04d}".format(self.enrollment_counter)


db = Database()
