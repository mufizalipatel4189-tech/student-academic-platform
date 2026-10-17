class Course:
    def __init__(self, course_id, title, credits, instructor, capacity=30):
        if not course_id or not title:
            raise ValueError("course_id and title are required")
        if credits < 1 or credits > 6:
            raise ValueError("credits must be between 1 and 6")
        self.course_id = course_id
        self.title = title
        self.credits = credits
        self.instructor = instructor
        self.capacity = capacity

    def to_dict(self):
        return {
            "course_id": self.course_id,
            "title": self.title,
            "credits": self.credits,
            "instructor": self.instructor,
            "capacity": self.capacity,
        }
