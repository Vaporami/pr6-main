import pytest, registry

@pytest.fixture
def get_prepared_reg(tmp_path):
    text = None
    with open("../examples/example-1.txt", "r", encoding = "utf-8") as file:
        text = file.read()
    path = tmp_path / "data.txt"
    path.write_text(text, encoding = "utf-8")
    reg = people.Registry()
    reg.load(path)
    return reg
