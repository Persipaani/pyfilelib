"""
Database mock that uses a file as a database.
Stores items using the Item class defined in item.py.
Currently supports adding a single item at once and querying all of them.
"""

import os
from item import Item
from typing import Type
from pathlib import Path


class FileBase:

    def __init__(self, config_path: str | None = None):
        self.data: list[Item] = []
        self.config_path = (
            f"{Path(__file__).parent}/db_config.py" if not config_path else config_path
        )
        self.file_path = self._get_file_path()
        self.import_from_file()

    def import_from_file(self) -> None:
        """
        Loads data from the given file an stores it in the on-memory database
        as Item objects.
        """
        if os.path.exists(self.file_path):
            with open(self.file_path, "r", encoding="utf-8") as f:
                for line in f:
                    if line.count("/") == 3:
                        if all(line.strip().split("/")):
                            name, author, isbn, year = line.strip().split("/")
                            try:
                                year = int(year)
                            except ValueError:
                                year = 0
                            self.data.append(Item(name, author, isbn, year))

            self._sort_data()

    def export_to_file(self) -> None:
        """
        Exports data to the given file. Overwrites the existing file content with the db memory.
        """
        with open(self.file_path, "w", encoding="utf-8") as f:
            for item in self.data:
                f.write(f"{item.name}/{item.author}/{item.isbn}/{item.year}\n")

    def add_item(self, data: dict[str | str, int]) -> None:
        """
        Adds an item to the database as Item object.

        `data` : a dictionary with keys: name, author, isbn & year.

        """
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

        `target_type` : The target class type to convert the items to.
        """
        return [target_type(**i.to_dict()) for i in self.data]

    def _sort_data(self):
        """Sorts the data by the publish year."""
        self.data.sort(key=lambda item: item.year)

    def _get_file_path(self) -> str:
        """Reads the file path from the db_config.py file and sets it."""
        try:
            with open(self.config_path, "r") as f:
                for line in f:
                    if line.startswith("FILE_PATH"):
                        return line.split("=")[1].strip().strip('"')
        except FileNotFoundError:
            print("db_config.py not found. Using default file path (data.txt).")
        return "data.txt"
