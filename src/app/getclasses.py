import sys

filter = sys.argv(1)

def giveMeclasses():
    classes = importausExel(filter)
    return classes;

def giveMeLessons():
    lessons = GetLessonExel(filter)
    return lessons