# encoding=utf-8
# 由于MySQL线程中执行语句只能单线执行，所以我们会占用部分运行内存来执行额外操作。

from flask import Flask, jsonify
from flask_cors import CORS
import MySQLdb as Mdb
import configparser as cp
import os
import math
import random
import MySQLdb.cursors

from DefaultObject import Group, Student, School
from Manager import SchoolsManager as Scm, StudentManager as Stm

app = Flask(__name__)
CORS(app, supports_credentials=True)
conf = cp.ConfigParser()  # 配置文件管理器
cfg_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "Properties.ini")  # 配置文件读取
schManager = Scm.SchoolsManager()  # 学校对象管理器
stuManager = Stm.StudentManager()  # 学生对象管理器

print("读取配置文件，路径：", cfg_path, "...")
conf.read(cfg_path, encoding="utf-8")

same_school_in = bool(conf.get('DefaultProperties', '同校不同组'))
is_sex_dis = bool(conf.get('DefaultProperties', '性别均匀分布'))
allow_max_dec = int(conf.get('DefaultProperties', '小组权值差'))

print("连接到MySQL数据库...")
MySQLConnections = Mdb.connect(conf.get('DataBaseProperties', '数据库地址'),
                               conf.get('DataBaseProperties', '数据库用户名'),
                               conf.get('DataBaseProperties', '数据库密码'),
                               conf.get('DataBaseProperties', '主数据库名'),
                               charset='utf8', cursorclass=Mdb.cursors.SSCursor)

cursor = MySQLConnections.cursor()
print("连接成功，进行初始化操作...")

# 读取学校信息
sel_Schools = "SELECT * FROM schools;"
cursor.execute(sel_Schools)
school_results = cursor.fetchall()
for row in school_results:
    school = School.School(row[1], row[2], row[3], row[4], row[5])
    schManager.add(school)

# 学生信息初始化管理
# 读取学生信息
sel_Students = "SELECT * FROM students;SET SQL_SAFE_UPDATES=0;"
cursor.execute(sel_Students)
results = cursor.fetchall()
# 遍历所有学生，计算学生权值分，将计算结果导入到学生数据库中
students_number = 0  # 学生数量
students = []  # 学生信息数组，由于不能同时调用cursor，所以此处需要额外分配一个数组
for row in results:
    students.append(row)
    students_number += 1

for row in students:
    Grade_G = float(conf.get('StudentGradeWeight', row[4]))
    school_owner = schManager.get_school(row[2])
    schManager.get_school(row[2]).add(row[1])
    school_weight = float(conf.get('SchoolWeight', school_owner.quality))
    area_weight = float(conf.get('ZoneWeight', school_owner.area))
    weight = round(Grade_G*school_weight*area_weight, 2)
    stuManager.students.append(Student.Student(row[1], row[3], row[2], row[4], weight))
# 上面所有步骤得到一个学生权值的计算分，之后需要对学生标记可抽签的赛区和组，因此需要对赛区和赛区里面的组进行初始化

print("初始数据加载成功，已加载", students_number, "名学生，正在进行分组操作...")
zone_number = int(conf.get('DefaultProperties', '赛场数'))
per_number = int(conf.get('DefaultProperties', '每小组最大人数'))
group_number = math.ceil(float(students_number / per_number))  # ，组数，向上取整，少的学生进行小组减差操作
diff_student = students_number % per_number  # 学生对每组人数求余
per_group_zone = int(float(group_number / zone_number))  # 每赛区组数，向下取整，多的小组进行末尾填充
diff_group = group_number % zone_number  # 总组数对赛区数求余
Groups = []  # 小组数组
# 这里用填充法进行计算剩余的组数，并在填充时为小组对象分配内存，并为学生分配权值
for i in range(group_number):  # 先分配小组对象的内存
    G = Group.Group()
    G.id = i+1
    Groups.append(G)
stuManager.students = stuManager.sort_weight(True)  # 先排序,True表示降序排列
mid_sign_num = int(per_number / 2) + per_number % 2  # 居中的标志数（该数代表的标志最接近平均数）
mid_sign = group_number - (per_number - diff_student)
current_sign = 1
current_groups_id = 0
for k in range(students_number):
    current_groups_id += 1
    stuManager.students[k].sign = current_sign
    if current_sign == mid_sign_num:
        if current_groups_id >= mid_sign:
            Groups[current_groups_id - 1].add_sign(current_sign)
            current_sign += 1
            current_groups_id = 0
            continue
        else:
            Groups[current_groups_id - 1].add_sign(current_sign)
            continue
    elif current_groups_id >= group_number:
        Groups[current_groups_id - 1].add_sign(current_sign)
        current_sign += 1
        current_groups_id = 0
        continue
    Groups[current_groups_id - 1].add_sign(current_sign)
# 至此所有组拥有的学生等级已分配
for gro_init in Groups:
    gro_init.init_group()
# 初始化每个学生的可抽签组，计算组内的理想分数，每个权值标志的平均分，性别比例
average = []  # average[0] 表示所有权值标志的平均值，1以上表示代表权值标志的均值
sex_dis = 0  # 性别比例
sign_num = []  # 权值学生数
for i in range(per_number+1):
    average.append(0)
    sign_num.append(1)
male_num = 0
female_num = 0
for student in stuManager.students:
    temp = []
    for Group in Groups:
        temp.append(Group.id)
    if is_sex_dis:
        if student.sex == "男":
            male_num += 1
        else:
            female_num += 1
    student.drawable_group = temp
    average[student.sign] += student.weight
    sign_num[student.sign] += 1
sex_dis = male_num/female_num
s = 0
for i in range(len(average)):
    if i != 0:
        average[i] = round(average[i]/sign_num[i], 2)
        s += average[i]
average[0] = round(s / (len(sign_num)-1), 2)

# 分配赛场
zones = {}  # 赛场全局Map{key = value}，其中key是赛场id，value是赛场剩余组数，当赛场不剩组时该赛场不能再添加小组
now_diff = 1
for i in range(zone_number):
    if now_diff > diff_group:
        zones[i+1] = per_group_zone
    else:
        zones[i+1] = per_group_zone + 1
        now_diff += 1
results = []  # 所有抽签结果的数组
school_num = len(schManager.schools)
print("初始化完毕")


def write_in_db(groups):
    print("全部抽签完毕，正在写入数据库...")
    zones_groups = {}  # 'zone_id': 'groups' ex: '1':[1,5,3,...]
    for zones_i in range(zone_number):
        zones_groups[zones_i] = []
    for group in groups:
        zones_groups[group.own_zone-1].append(group)
    for z in list(zones_groups.keys()):  # 每个赛区生成一个数据库文件
        groups = zones_groups[z]
        cursor.execute("DROP TABLE IF EXISTS ZONE%s" % str(z+1))
        create_sql = "CREATE TABLE ZONE%s (" \
                     "name TEXT NOT NULL," \
                     "school TEXT NOT NULL," \
                     "sex TEXT NOT NULL," \
                     "weight FLOAT NOT NULL," \
                     "gro TEXT NOT NULL );" % str(z+1)
        cursor.execute(create_sql)
        for group in groups:
            for stu in group.students:
                insert = "INSERT INTO ZONE%s(" \
                         "name, school, sex, weight, gro) " \
                         "VALUES ('%s', '%s', '%s', %f, '第 %s 组')" \
                         % (str(z+1), stu.name, stu.school, stu.sex, stu.weight, str(group.id))
                cursor.execute(insert)
                MySQLConnections.commit()


# 注册Flask指令
@app.route('/get_result/<school_name>/<student_name>')
def get_result(school_name, student_name):
    for result in results:
        if result["school"] == school_name and result["name"] == student_name:
            return result
    return None


# 获取基础的数据（已抽签学生数，学生总数，当前已抽签的学校数，学校总数）
@app.route('/get_default_data')
def get_default_data():
    data = {"drawn_num": stuManager.drawn_num, "student_num": students_number,
            "drawn_schools_num": len(schManager.drawn_schools), "school_num": school_num,
            "zone_num": zone_number}
    return jsonify(data)


@app.route('/ping')
def index():
    return jsonify("pong")


@app.route('/getStudents/<school_name>')
def get_students(school_name):
    return jsonify(schManager.get_school(school_name).students)


@app.route('/getSchools')
def ger_schools():
    return jsonify(schManager.get_schools())


@app.route('/print_result/<school_name>/<student_name>')
def print_result(school_name, student_name):
    # 打印操作，暂未编写
    sina = {1: "ss"}
    return jsonify(sina)


@app.route('/get_drawn_schools')
def get_drawn_schools():
    return jsonify(schManager.get_drawn_schools())


@app.route('/get_drawn_students/<school_name>')
def get_drawn_students(school_name):
    return jsonify(schManager.get_school(school_name).drawn_students)


# 抽签指令，因为是从控制台接收的数据，所以能够保证信息的非空性
@app.route('/draw/<school_name>/<student_name>')
def draw(school_name, student_name):
    result = {"isDraw": False}
    stu = stuManager.get_student(student_name, school_name)
    sch = schManager.get_school(school_name)
    if stu.isDraw:
        return jsonify(result)
    else:
        result.pop("isDraw")
    group = Groups[random.choice(stu.drawable_group)-1]  # 随机在可抽签组中选择一个组
    stu.group_id = group.id
    Groups[group.id-1].students.append(stu)  # 将学生移到抽中的组中
    stuManager.set_drawn(student_name, school_name)  # 已抽签标志置为True
    # 然后抽中的组进行分值范围更新
    Groups[group.id - 1].update_range(average, allow_max_dec)

    # 表示小组为空时，此时需要为组随机分配赛区号
    if group.own_zone == 0:
        zone_id = int(random.choice(list(zones.keys())))  # 赛区号
        zones[zone_id] = zones[zone_id] - 1
        if zones[zone_id] <= 0:
            zones.pop(zone_id)
        Groups[group.id - 1].own_zone = zone_id

    result["group"] = group.id
    result["zone"] = Groups[group.id - 1].own_zone
    result["school"] = stu.school
    result["sex"] = stu.sex
    result["name"] = stu.name
    # 抽签后的处理
    schManager.update(school_name)
    sch.update(stuManager)
    is_draw_num = 1  # 统计已抽签学生的数量
    for other in stuManager.students:
        if other.isDraw:  # 排除已抽签的学生
            is_draw_num += 1
            continue
        # 如果该组不在学生可选组范围，需要考虑是否满足条件而添加该组
        if not other.contain_group(group.id):
            other.add_drawable(group.id)
        # 从同权值标记的同学可选组中移除该组小组号
        if other.sign == stu.sign:
            other.remove_drawable(group.id)
        # 同校不同组处理
        if same_school_in:  # 配置文件是否开启此项
            if other.school == stu.school:  # 如果有同名学校，增加条件即可（虽然不太可能）
                other.remove_drawable(group.id)
        # 性别比例控制
        if is_sex_dis:
            if other.sex == "男" and group.is_male_full(sex_dis) and not group.is_female_full(sex_dis):
                other.remove_drawable(group.id)
            elif other.sex == "女" and not group.is_female_full(sex_dis) and group.is_female_full(sex_dis):
                other.remove_drawable(group.id)
        # 省份要求，暂未开发
        # 权值范围排除
        for s_id in other.drawable_group:
            if s_id == group.id:
                if not Groups[s_id-1].is_in_range(other) and Groups[s_id-1].contain_sign(other.sign):
                    other.remove_drawable(s_id)
        if is_draw_num >= students_number:  # 所有学生已抽签
            write_in_db(Groups)
    results.append(result)
    return jsonify(result)


@app.route('/admin/draw_all')
def draw_all():
    print("模拟全部抽签，请稍候...")
    for st in stuManager.students:
        draw(st.school, st.name)
    return "所有抽签完成，请在后台查看"


if __name__ == '__main__':
    '#端口开启'
    app.run()
