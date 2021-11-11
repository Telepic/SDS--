class StudentManager:
    def __init__(self):
        self.students = []
        self.drawn_num = 0

    def get_student(self, name, school):
        for i in self.students:
            if name == i.name and school == i.school:
                return i
        return None

    def set_drawn(self, student_name, school_name):
        self.get_student(student_name, school_name).isDraw = True
        self.drawn_num += 1

    def sort_weight(self, revers):
        return sorted(self.students, key=lambda student: student.weight, reverse=revers)


