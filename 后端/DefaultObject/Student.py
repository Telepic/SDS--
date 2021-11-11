class Student:
    def __init__(self, name, sex, school, grade, weight):
        self.name = name
        self.sex = sex
        self.school = school
        self.grade = grade
        self.weight = weight
        self.sign = 0
        self.isDraw = False
        self.drawable_group = []  # 可抽签的组（可优化，该数组可以优化为只存储组ID而不必储存组对象）
        self.group_id = 0
    
    def set_sign(self, sign):
        self.sign = sign

    def add_drawable(self, id):
        self.drawable_group.append(id)

    def contain_group(self, id):
        for gro_id in self.drawable_group:
            if id == gro_id:
                return True
        return False

    def remove_drawable(self, id):
        for ids in self.drawable_group:
            if ids == id:
                self.drawable_group.remove(ids)
                break
