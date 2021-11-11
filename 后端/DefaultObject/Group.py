import math


class Group:
    def __init__(self):
        self.id = 0
        self.own_zone = 0
        self.students = []
        self.drawable_sign = []
        self.average = 0
        self.range = {}  # 每一个分数标志有一个组范围。即，{'sign':[min_max]}
        self.max_student_num = 0
        self.male_num = 0
        self.female_num = 0

    def is_empty(self):
        print(len(self.students))
        if len(self.students) == 0:
            return True
        else:
            return False

    def add_sign(self, sign):
        self.drawable_sign.append(sign)
        self.max_student_num += 1

    def add_student(self, student):
        self.students.append(student)
        if student.sex == "男":
            self.male_num += 1
        else:
            self.female_num += 1
        for i in self.drawable_sign:
            if i == student.sign:
                self.drawable_sign.remove(i)

    def get_average_weight(self):
        s = 0
        k = 0
        for student in self.students:
            s += student.weight
            k += 1
        if k == 0:
            return 0
        else:
            return s / k

    def get_sex_dis(self):
        male = 0
        female = 0
        for student in self.students:
            if student.sex == male:
                male += 1
            else:
                female += 1
        if female == 0:
            return 1
        else:
            return male/female

    # 性别比例，获取允许存在的最大性别人数，向上取整
    def is_male_full(self, stander_sex_dis):
        max_male_num = math.ceil(stander_sex_dis*self.max_student_num)
        if self.male_num >= max_male_num:
            return True
        else:
            return False

    def is_female_full(self, stander_sex_dis):
        max_female_num = math.ceil((1 - stander_sex_dis) * self.max_student_num)
        if self.female_num >= max_female_num:
            return True
        else:
            return False

    def is_in_group(self, school):  # 学校有效性，如果该学校已在该组中，则考虑最大值范围时不会考虑该学校
        for student in self.students:
            if school == student.school:
                return True
        return False

    def is_sex_eff(self, student, stander_sex_dis):  # 性别有效性。如果参数<student>的性别在该组已满，则该<student>为无效条件
        if student.sex == "男" and self.is_male_full(stander_sex_dis):
            return True
        elif student.sex == "女" and self.is_female_full(stander_sex_dis):
            return True
        else:
            return False

    def init_group(self):
        for i in self.drawable_sign:
            temp = [0, 0]
            self.range[i] = temp

    def contain_sign(self, sign):
        for i in self.drawable_sign:
            if i == sign:
                return True
        return False

    def update_range(self, average, allow_max_dec):
        if len(self.range) == 0:
            self.init_group()
        for sign in list(self.range.keys()):
            if not self.contain_sign(sign):  # 如果当前可抽签标志中不含有某标志，则表明该标志的学生已有，该标志代表的范围不用更新
                continue
            # 遍历该组已存在的所有学生，计算小组已有学生在所代表标志学生中的偏差总值dec
            dec = 0  # dec的绝对值必定在允许的最大偏差范围内
            for stu in self.students:
                dec += stu.weight - average[stu.sign]
            self.range[sign][0] = average[sign] - dec - allow_max_dec  # 最小值等于平均值减偏差减去允许的最大偏差
            self.range[sign][1] = average[sign] - dec + allow_max_dec

    def is_in_range(self, student):
        if self.contain_sign(student.sign):
            [min_n, max_n] = self.range[student.sign]
            if min_n > student.weight > max_n:
                return False
            else:
                return True
        else:
            return False
