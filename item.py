class Item:
    """
    Defines a database item for a book. Note that this item
    """

    def __init__(self, name: str, author: str, isbn: str, year: int):
        self.name = name
        self.author = author
        self.isbn = isbn
        self.year = year

    def __repr__(self):
        return f"Item(name={self.name}, value={self.author}, isbn={self.isbn}, year={self.year})"

    def to_dict(self):
        """
        Converts the Item object to a dictionary object.
        """
        return {
            "name": self.name,
            "author": self.author,
            "isbn": self.isbn,
            "year": self.year,
        }
