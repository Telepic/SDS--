class School:
    def __init__(self, name, province, quality, area, student_num):
        self.name = name
        self.province = province
        self.quality = quality
        self.area = area
        self.student_num = student_num
        self.id = 0
        self.students = []
        self.drawn_students = []

    def add(self, student_name):
        self.students.append(student_name)

    def is_empty(self):
        if len(self.students) == 0:
            return True
        else:
            return False

    def is_drawn_empty(self):
        if len(self.drawn_students) == 0:
            return True
        else:
            return False

    def update(self, stu_manager):
        for s in self.students:
            if stu_manager.get_student(s, self.name).isDraw:
                self.drawn_students.append(s)
                self.students.remove(s)
