class SchoolsManager:
    def __init__(self):
        self.schools = []
        self.cul = 1
        self.drawn_schools = []

    def add(self, school):
        self.schools.append(school)
        school.id = self.cul
        self.cul += 1

    def get_school(self, name):
        for school in self.schools:
            if school.name == name:
                return school
        return None

    def get_schools(self):
        sc = {}
        for school in self.schools:
            sc[school.id] = school.name
        return sc

    def get_drawn_schools(self):
        sc = {}
        for school in self.drawn_schools:
            sc[school.id] = school.name
        return sc

    def update(self, school_name):
        sch = self.get_school(school_name)
        if sch.is_drawn_empty():
            self.drawn_schools.append(sch)
        if sch.is_empty():
            self.schools.remove(sch)

