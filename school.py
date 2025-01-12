class University:
    """
    University class that manages faculties and students
    
    attributes:
        name: str, name of the university
        location: str, location of the university
        faculties: list, list of faculties in the university
    """

    def __init__(self, name, location):
        # initialize the university
        self.name = name
        self.location = location
        self.faculties = [] # list of faculties
    
    def __str__(self):
        # return the name and location of the university
        return f'{self.name} {self.location}'
    
    def add_faculty(self, faculty):
        # add faculty to the university
        if faculty not in self.faculties:
             self.faculties.append(faculty)
       
    def get_faculties(self):
        # return the list of faculties
        return self.faculties
    
    def get_students(self):
        # return the list of students across all faculties
        students = []
        for faculty in self.faculties:
            students.extend(faculty.students)
        return students

class Faculty:
    """
    Faculty class that manages students
       attributes:
        name: str, name of the faculty
        students: list, list of students in the faculty
    """

    def __init__(self, name):
        # initialize the faculty
        self.name = name
        self.students = [] # list of students
    
    def __str__(self):
        # return the name of the faculty
        return f'{self.name}'
    
    def __repr__(self):
        return self.__str__()
    
    def add_student(self, student):
        # add student to the faculty
        if student not in self.students:
            self.students.append(student)

class Student:
    """
    Student class that represents a student
    
    attributes:
        name: str, name of the student
        age: int, age of the student
    """

    def __init__(self, name, age):
        # initialize the student
        self.name = name
        self.age = age
    
    def __str__(self):
        # return the name and age of the student
        return f'{self.name} {self.age}'
    
    def __repr__(self):
        return self.__str__()
    

if __name__ == "__main__":
    # create a university
    uq = University("昆士兰大学", "布里斯班")

    # create faculties
    eait = Faculty("工程学院")
    hass = Faculty("人文学院")

    # add faculties to university
    uq.add_faculty(eait)
    uq.add_faculty(hass)

    # create students
    student1 = Student("小王", 23)
    student2 = Student("小李", 22)

    # add students to faculties 
    eait.add_student(student1)
    hass.add_student(student2)

    # get students
    print(uq)
    print(uq.get_faculties())
    students = uq.get_students()
    print(students)
    

