import datetime as dt
class Person:
    def __init__(self, full_name, email, phone):
        self.full_name = full_name
        self.email = email
        self.phone = phone

    @property
    def masked_phone(self):
        return f"{self.phone[:9]}***-**-{self.phone[-2:]}"

    def __str__(self):
        return f"({self.full_name}; {self.email}; {self.masked_phone})"

    def __repr__(self):
        return self.__str__()

    def __lt__(self, other):
        return self.full_name < other

    def role(self): 
        pass
    
    def extra(self):
        pass

class Student(Person):
    def __init__(self, full_name, email, phone, group):
        super().__init__(full_name, email, phone)
        self.group = group

    def __str__(self):
        return f"({self.full_name}; {self.email}; {self.masked_phone}; {self.group})"

    def __repr__(self):
        return self.__str__()

    def role(self):
        return type(self)

    def extra(self):
        return self.group

class Teacher(Person):
    def __init__(self, full_name, email, phone, faculty):
        super().__init__(full_name, email, phone)
        self.faculty = faculty

    def __str__(self):
        return f"({self.full_name}; {self.email}; {self.masked_phone}; {self.faculty})"

    def __repr__(self):
        return self.__str__()

    def role(self):
        return type(self)

    def extra(self):
        return self.faculty

class AnketaParseError(Exception):
    pass

def parse_into_instance(text, ok_log = None, err_log = None, identificator = "NO_ID"):
    blocks = [block.strip().lower() for block in text.split(";")]

    # проверка и определение типа
    person_type = blocks[0]
    if person_type != "s" and person_type != "t":
        msg = f"Некорректный ввод типа личности (студент или преподаватель): {person_type}"
        err_log.write(f"[{identificator}] {msg}\n") if err_log else None
        raise AnketaParseError(msg)
    person_type = Student if person_type == "s" else Teacher

    # проверка ФИО
    full_name = blocks[1].title()
    full_name_parts = blocks[1].split()
    if len(full_name_parts) < 2:
        msg = f"Не хватает части(ей) ФИО: {full_name}"
        err_log.write(f"[{identificator}] {msg}\n") if err_log else None
        raise AnketaParseError(msg)

    # проверка электронной почты
    email = blocks[2]
    email_parts = blocks[2].split("@")
    if len(email_parts) <= 1:
        msg = f"Отсутствуте поле домена {email}"
        err_log.write(f"[{identificator}] {msg}\n") if err_log else None
        raise AnketaParseError(msg)

    at_amount = len(email_parts) - 1
    if at_amount > 1:
        msg = f"Слишком много @: {email}"
        err_log.write(f"[{identificator}] {msg}\n") if err_log else None
        raise AnketaParseError(msg)

    if email_parts[0].isspace() or email_parts[1].isspace():
        msg = f"Одна из частей почта пустая: {email}"
        err_log.write(f"[{identificator}] {msg}\n") if err_log else None
        raise AnketaParseError(msg)

    if email_parts[1].startswith(".") or email_parts[1].endswith("."):
        msg = f"Домен начинается или заканчивается точкой: {email}"
        err_log.write(f"[{identificator}] {msg}\n") if err_log else None
        raise AnketaParseError(msg)

    domain_parts = email_parts[1].split(".")
    if len(domain_parts) != 2:
        msg = f"Домен введен неверно: {email}"
        err_log.write(f"[{identificator}] {msg}\n") if err_log else None
        raise AnketaParseError(msg)

    # проверка номера телефона
    phone = blocks[3]
    if phone.startswith("8"):
        phone = f"+7{phone[1:]}"

    if not phone.startswith("+7"):
        msg = f"Некорректное начало номера (не +7): {phone}"
        err_log.write(f"[{identificator}] {msg}\n") if err_log else None
        raise AnketaParseError(msg)

    digits = []
    for i in phone:
        if i.isdigit():
            digits.append(i)
    digits = "".join(digits)

    if len(digits) != 11:
        msg = f"Некорректное кол-во цифр в номере телефона: {phone}"
        err_log.write(f"[{identificator}] {msg}\n") if err_log else None
        raise AnketaParseError(msg)
    phone = f"+7 ({digits[1:4]}) {digits[4:7]}-{digits[7:9]}-{digits[9:]}"

    # проверка группы/кафедры
    belongs_to = None
    if person_type == Student:
        group = blocks[4]
        if group.startswith("кафедра"):
            msg = f"Студенту присвоена кафедра, а не группа: {group.title()}"
            err_log.write(f"[{identificator}] {msg}\n") if err_log else None
            raise AnketaParseError(msg)
        if group.isspace():
            msg = f"Указание группы отсутствует."
            err_log.write(f"[{identificator}] {msg}\n") if err_log else None
            raise AnketaParseError(msg)
        belongs_to = group.upper()
    elif person_type == Teacher:
        faculty = blocks[4]
        if not faculty.startswith("кафедра"):
            msg = f"Преподавателю присвоена группа, а не кафедра: {faculty.title()}"
            err_log.write(f"[{identificator}] {msg}\n") if err_log else None
            raise AnketaParseError(msg)
        if faculty.isspace():
            msg = f"Указание кафедры отсутствует."
            err_log.write(f"[{identificator}] {msg}\n") if err_log else None
            raise AnketaParseError(msg)
        belongs_to = faculty.title()

    # создание объекта
    person = person_type(full_name, email, phone, belongs_to)

    ok_log.write(f"[{identificator}] {str(person)}\n") if ok_log else None

    return person

