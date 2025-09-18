class Lesson:
    # Constructor / initializer
    def __init__(self,lv_id, subject, teacher, note, teacher_lessons, student_lessons, school_classes : list[str]):
        # Instance attributes
        self.lv_id = lv_id
        self.subject = subject
        self.teacher = teacher
        self.note = note
        self.teacher_lessons = teacher_lessons
        self.student_lessons = student_lessons
        self.school_classes = school_classes

    #Wie das dahstehen soll ist noch offen erstmal nur auflistung
    def create_notes():
        for school_class in school_classes:
            note = note + "/" + school_class