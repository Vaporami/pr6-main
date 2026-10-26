import pytest, people

@pytest.mark.parametrize("full_name, expected", [
    ("сАфОНцЕв аЛЕкСаНдР аНаТоЛьЕвИч", "Сафонцев Александр Анатольевич"),
    ("пОПОвА еКаТеРиНа иВАНовНа", "Попова Екатерина Ивановна"),
    ("кОзЛОв сЕРгей нИКолАевич", "Козлов Сергей Николаевич"),
    ("сОкОлОВ аНДрей вИКТорович", "Соколов Андрей Викторович")
    ])
def test_parse_full_name(full_name, expected):
    assert people.parse_full_name(full_name) == expected

def test_parse_full_name_error_one_word():
    with pytest.raises(people.AnketaParseError):
        assert people.parse_full_name("Александр")

@pytest.mark.parametrize("email, expected", [("SaFONtSeV@MaIl.Ru", "safontsev@mail.ru"), ("LebeDeVa@YaNdEx.Ru", "lebedeva@yandex.ru")])
def test_parse_email_lower(email, expected):
    assert people.parse_email(email) == expected

@pytest.mark.parametrize("email", ["SaFONtSeVMaIl.Ru", "IoRdANOv@gMaIlCoM", "PoPoVA@MaIl.", "@YaNdEx.Ru"])
def test_parse_email_error(email):
    with pytest.raises(people.AnketaParseError):
        assert people.parse_email(email)

@pytest.mark.parametrize("phone", ["+79048567691", "89048567691", "+7 904 856 76 91", "8 904 856 76 91"])
def test_parse_phone(phone):
    assert people.parse_phone(phone) == "+7 (904) 856-76-91"

@pytest.mark.parametrize("phone", ["+14838274837", "79048567691", "79047691"])
def test_parse_phone_error(phone):
    with pytest.raises(people.AnketaParseError):
        assert people.parse_phone(phone)

def test_parse_phone_mask():
    a = people.Person("Сафонцев Александр Анатольевич", "pochta@mail.ru", "+7 (904) 856-76-91")
    assert a.masked_phone == "+7 (904) ***-**-91"

def test_parse_full_name_shortening():
    a = people.Person("Сафонцев Александр Анатольевич", "pochta@mail.ru", "+7 (904) 856-76-91")
    assert a.short_full_name == "Сафонцев А. А."

def test_people_role_unmatching():
    student = people.Student("Сафонцев Александр Анатольевич", "pochta@mail.ru", "+7 (904) 856-76-91")
    teacher = people.Teacher("Кондратьев Владимир Николаевич", "otherpochta@gmail.com", "+7 (931) 783-23-43")
    assert student.role() != teacher.role()

@pytest.mark.parametrize("person_type", ["", "x"])
def test_parse_person_type_error(person_type):
    with pytest.raises(people.AnketaParseError):
        assert people.parse_person_type(person_type)

def test_parse_belongs_to_error():
    with pytest.raises(people.AnketaParseError):
        assert people.parse_belongs_to("")

first_string = "t; кУЗнЕцОв дМитРИй аЛеКСАНдРовиЧ ; KUZnEtSoV@YaNdEx.Ru ; +7 (934) 567-89-01 ;Кафедра О5"
first_instance = people.Teacher("Кузнецов Дмитрий Александрович", "kuznetsov@yandex.ru", "+7 (934) 567-89-01", "Кафедра О5")
second_string = "s;лЕбЕдЕвА оЛЬга дМИтрИевНа; LebeDeVa@YaNdEx.Ru ;+7 (967) 890-12-34; 09c33"
second_instance = people.Student("Лебедева Ольга Дмитриевна", "lebedeva@yandex.ru", "+7 (967) 890-12-34", "09С33")

@pytest.mark.parametrize("string, expected", [(first_string, first_instance), (second_string, second_instance)])
def test_parse_into_instance(string, expected):
    assert people.parse_into_instance(string) == expected

first_bad_string = "s;   сАфОНцЕв аЛЕкСаНдР аНаТоЛьЕвИч ; SaFONtSeVMaIl.Ru ; +7 (904) 856-76-91 ; 09c33"
second_bad_string = "t;  иОрДанОв гЕоРгИй сЕРгЕеВИч; IoRdANOv@gMaIlCoM ;+7 (929) 384-23-53 ;Кафедра И9"
third_bad_string = "s;  пОПОвА еКаТеРиНа иВАНовНа; PoPoVA@MaIl. ;+7 (945) 678-90-12 ;09c34"

@pytest.mark.parametrize("string", [first_bad_string, second_bad_string, third_bad_string])
def test_parse_into_instance_error(string):
    with pytest.raises(people.AnketaParseError):
        assert people.parse_into_instance(string)
