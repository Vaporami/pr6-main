import pytest, people, registry

@pytest.fixture
def reg(tmp_path):
    text = None
    with open("./examples/example-1.txt", "r", encoding = "utf-8") as file:
        text = file.read()
    path = tmp_path / "data.txt"
    path.write_text(text, encoding = "utf-8")
    reg = registry.Registry()
    reg.load(path)
    return reg

def test_reg_length():
    r = registry.Registry()
    assert len(r) == 0

def test_reg_length_loaded(reg):
    assert len(reg) == 7

def test_reg_stats(reg):
    stats = reg.stats()
    assert stats["accepted"] == 7 and stats["refused"] == 4

def test_reg_right_error_lines(reg):
    assert sorted(list(reg.refused_lines.keys())) == [1, 2, 4, 10]

def test_reg_load_no_file_error(reg):
    with pytest.raises(FileNotFoundError):
        assert reg.load("./none.txt") == False

def test_reg_stats_by_type(reg):
    assert reg.stats_by_type() == {people.Student: 3, people.Teacher: 4}

def test_reg_stats_by_belonging_with_key(reg):
    assert reg.stats_by_belonging(lambda p: p.role() == people.Student) == {"09С33": 1, "09С35": 2}

def test_reg_iterability(reg):
    flag = False
    for i in reg:
        flag = True
    assert flag

def test_reg_sorting(reg):
    sorted_reg = reg.sorted()
    assert [person.full_name.split()[0] for person in sorted_reg][:3] == ["Волкова", "Ёлкин", "Кузнецов"]

def test_ok_log_writing(reg):
    path = "./save_ok.txt"
    with open(path, "w", encoding = "utf-8") as file:
        reg.save_ok(file)
    text = None
    with open(path, "r", encoding = "utf-8") as file:
        text = file.read()
    assert True if text.find(str(reg[0]) + "\n") > -1 else False

def test_err_log_writing(reg):
    path = "./save_err.txt"
    with open(path, "w", encoding = "utf-8") as file:
        reg.save_err(file)
    text = None
    with open(path, "r", encoding = "utf-8") as file:
        text = file.read()
    assert True if text.find(reg.refused_lines[1] + "\n") > -1 else False

