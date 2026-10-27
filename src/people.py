import datetime as dt
class Person:
    def __init__(self, full_name, email, phone):
        self.full_name = full_name
        self.email = email
        self.phone = phone

    @property
    def masked_phone(self):
        return f"{self.phone[:9]}***-**-{self.phone[-2:]}"

    @property
    def short_full_name(self):
        parts = self.full_name.split()
        return f"{parts[0]} {parts[1][0]}. {parts[2][0]}."

    def __str__(self):
        return f"({self.full_name}; {self.email}; {self.masked_phone})"

    def __repr__(self):
        return self.__str__()

    def __lt__(self, other):
        edited_self = self.full_name.lower().replace("ё", "е")
        edited_other = other.full_name.lower().replace("ё", "е")
        return edited_self < edited_other

    def __eq__(self, other):
        same_types = self.role() == other.role()
        same_full_name = self.full_name == other.full_name
        same_email = self.email == other.email
        same_phone = self.phone == other.phone
        same_extra = self.extra() == other.extra()
        return same_types and same_full_name and same_email and same_phone and same_extra

    def role(self): 
        return None
    
    def extra(self):
        return None

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

def parse_person_type(init_person_type, err_log = None, identificator = "NO_ID"):
    person_type = init_person_type
    if person_type != "s" and person_type != "t":
        msg = f"Некорректный ввод типа личности (студент или преподаватель): {person_type}"
        err_log.write(f"[{identificator}] {msg}\n") if err_log else None
        raise AnketaParseError(msg)
    person_type = Student if person_type == "s" else Teacher
    return person_type
    
def parse_full_name(init_full_name, err_log = None, identificator = "NO_ID"):
    full_name = init_full_name.title()
    full_name_parts = init_full_name.split()
    if len(full_name_parts) < 2:
        msg = f"Не хватает части(ей) ФИО: {full_name}"
        err_log.write(f"[{identificator}] {msg}\n") if err_log else None
        raise AnketaParseError(msg)
    return full_name

def parse_email(init_email, err_log = None, identificator = "NO_ID"):
    email = init_email.lower()
    if len(email.split()) > 1:
        msg = f"Пробел в указании почты: {email}"
        err_log.write(f"[{identification}] {msg}\n") if err_log else None
        raise AnketaParseError(msg)
    email_parts = init_email.split("@")
    if len(email_parts) <= 1 or email_parts[0] == "" or email_parts[1] == "":
        msg = f"Отсутствует поле домена: {email}"
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

    return email

def parse_phone(init_phone, err_log = None, identificator = "NO_ID"):
    phone = init_phone
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

    return phone

def parse_belongs_to(init_belongs_to, person_type, err_log = None, identificator = "NO_ID"):
    belongs_to = None
    if person_type == Student:
        group = init_belongs_to.lower()
        if group.startswith("кафедра"):
            msg = f"Студенту присвоена кафедра, а не группа: {group.title()}"
            err_log.write(f"[{identificator}] {msg}\n") if err_log else None
            raise AnketaParseError(msg)
        if group.isspace() or group == "":
            msg = f"Указание группы отсутствует."
            err_log.write(f"[{identificator}] {msg}\n") if err_log else None
            raise AnketaParseError(msg)
        belongs_to = group.upper()
    elif person_type == Teacher:
        faculty = init_belongs_to.lower()
        if not faculty.startswith("кафедра"):
            msg = f"Преподавателю присвоена группа, а не кафедра: {faculty.title()}"
            err_log.write(f"[{identificator}] {msg}\n") if err_log else None
            raise AnketaParseError(msg)
        if faculty.isspace() or faculty == "":
            msg = f"Указание кафедры отсутствует."
            err_log.write(f"[{identificator}] {msg}\n") if err_log else None
            raise AnketaParseError(msg)
        belongs_to = faculty.title()

    return belongs_to


def parse_into_instance(text, ok_log = None, err_log = None, identificator = "NO_ID"):
    blocks = [block.strip().lower() for block in text.split(";")]

    person_type = parse_person_type(blocks[0][:], err_log, identificator)
    full_name = parse_full_name(blocks[1][:], err_log, identificator)
    email = parse_email(blocks[2][:], err_log, identificator)
    phone = parse_phone(blocks[3][:], err_log, identificator)
    belongs_to = parse_belongs_to(blocks[4][:], person_type, err_log, identificator)

    person = person_type(full_name, email, phone, belongs_to)

    ok_log.write(f"[{identificator}] {str(person)}\n") if ok_log else None

    return person
