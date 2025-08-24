"""
Database mock that uses a file as a database.
Stores items using the Item class defined in item.py.
Currently supports adding a single item at once and querying all of them.
"""

import os
from item import Item
from typing import Type


class FileBase:

    def __init__(self):
        self.data: list[Item] = []
        self.file_path = self._get_file_path()
        self.import_from_file()

    def import_from_file(self) -> None:
        """
        Loads data from the given file an stores it in the on-memory database
        as Item objects.

        ` file_path` : Path to the data file.
        """
        if os.path.exists(self.file_path):
            with open(self.file_path, "r", encoding="utf-8") as f:
                for line in f:
                    if line.count("/") == 3:
                        name, author, isbn, year = line.strip().split("/")
                        self.data.append(Item(name, author, isbn, int(year)))

            self._sort_data()

    def export_to_file(self) -> None:
        """
        Exports data to the given file. Overwrites the existing file content with the db memory.

        ` file_path` : Path of the data file.
        """
        with open(self.file_path, "w", encoding="utf-8") as f:
            for item in self.data:
                f.write(f"{item.name}/{item.author}/{item.isbn}/{item.year}\n")

    def add_item(self, data: dict[str | str, int]) -> None:
        """Adds an item to the database as Item object."""
        data["year"] = int(data["year"])
        self.data.append(Item(**data))
        self._sort_data()
        self.export_to_file()

    def get_all(self) -> list[Item]:
        """Returns all items as Item objects."""
        return self.data

    def get_all_as_type(self, target_type: Type) -> list[Type]:
        """
        Returns all items converted to match the given target_type (Class)

        `target_type`: The target class type to convert the items to.
        """
        return [target_type(**i.to_dict()) for i in self.data]

    def _sort_data(self):
        """Sorts the data by the publish year."""
        self.data.sort(key=lambda item: item.year)

    def _get_file_path(self) -> str:
        """Reads the file path from the db_config.py file and sets it."""
        try:
            with open("db_config.py", "r") as f:
                for line in f:
                    if line.startswith("FILE_PATH"):
                        return line.split("=")[1].strip().strip('"')
        except FileNotFoundError:
            print("db_config.py not found. Using default file path (data.txt).")
        return "data.txt"


if __name__ == "__main__":
    # Comment these in for running simple tests for the file database mock.
    # Before running, make sure to have a db_config.py file with a valid FILE_PATH variable.
    # Note that these tests do not validate anything themselves and require the user to check printed values and files.
    # db = FileBase()
    # print(db.get_all())
    # print(db.get_all_as_type(Item))

    # new_item = {
    #     "name": "New Book",
    #     "author": "Author Name",
    #     "isbn": "1234567890",
    #     "year": 1912,
    # }
    # db.add_item(new_item)
    # db.export_to_file()

    # print(db.get_all())
    pass
