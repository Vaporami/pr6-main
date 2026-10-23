class Person:
    def __init__(full_name, email, phone):
        self.full_name = full_name
        self.email = email
        self.phone = phone

class Student(person.Person):
    def __init__(full_name, email, phone, group):
        super().__init__(full_name, email, phone)
        self.group = group

class Teacher(person.Person):
    def __init__(full_name, email, phone, faculty):
        super().__init__(full_name, email, phone)
        self.faculty = faculty
