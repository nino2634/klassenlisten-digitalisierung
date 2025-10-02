## class to hold everything related to a single lesson

class Lesson:
    def __init__(self,lv_id, subject, teacher, note, teacher_lessons, student_lessons, school_classes : list[str]):
        # instance attributes
        self.lv_id = lv_id
        self.subject = subject
        self.teacher = teacher
        self.note = note
        self.teacher_lessons = teacher_lessons
        self.student_lessons = student_lessons
        self.school_classes = school_classes

    #place holder method, call later in init to create notes automaticly upon creating the lesson
    def create_notes():
        for school_class in school_classes:
            note = note + "/" + school_class