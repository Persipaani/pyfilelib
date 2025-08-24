"""
Some very basic tests for the filebase class.
"""

from filebase import FileBase

TEST_CONFIG = "tests/test_db_config.py"


def test_custom_config_path():
    _set_config("tests/test_data.txt")
    db = FileBase(TEST_CONFIG)
    assert db.config_path == TEST_CONFIG
    assert db.file_path == "tests/test_data.txt"


def test_import():
    """
    Verifies that 4 items are loaded from the test_data.txt
    """
    _set_config("tests/test_data.txt")
    db = FileBase(TEST_CONFIG)
    data = db.get_all()
    assert len(data) == 4


def test_sort():
    """
    Verifies that items are sorted by year starting from the oldest.
    """
    _set_config("tests/test_data.txt")
    db = FileBase(TEST_CONFIG)
    data = db.get_all()
    assert data[0].year < data[1].year < data[2].year < data[3].year


def test_invalid_data():
    """
    Verifies that invalid data does not break the import and correct
    values are still imported correctly.
    """
    _set_config("tests/test_data_invalid.txt")
    db = FileBase(TEST_CONFIG)
    data = db.get_all()
    assert len(data) == 1
    assert data[0].name == "Sampon kultajuhlat"


def test_add_export(tmp_path):
    """
    Verifies that adding new object and storing it to a file works.
    """
    new_file = tmp_path / "new_data.txt".replace("\\", "\\\\")
    _set_config(new_file)
    db = FileBase(TEST_CONFIG)
    new_item = {
        "name": "New item",
        "author": "Sampo",
        "isbn": "1234567890",
        "year": 1992,
    }
    db.add_item(new_item)

    lines = open(new_file, "r", encoding="utf-8").readlines()
    data = db.get_all()

    assert len(lines) == 1
    assert data[0].name == "New item"

    _set_config("")


def _set_config(path):
    open(TEST_CONFIG, "w", encoding="utf-8").write(f'FILE_PATH="{path}"')
