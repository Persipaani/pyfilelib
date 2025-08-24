"""
A simple web app that proviced a front-end for the file based database system.
Allows viewing contents of the database file and adding new items to it.
There is a very basic validation for input fields of new items but more detailed error messages are missing.
"""

import reflex as rx
from filebase import FileBase

FILEBASE = FileBase()


class Item(rx.Base):
    name: str
    author: str
    isbn: str
    year: int


class State(rx.State):
    books: list[Item] = []
    loading: bool = True
    dialog_open: bool = False
    keys_as_labels: dict["str", list[str]] = {
        "name": ["Title", "book-open-text"],
        "author": ["Author", "chef-hat"],
        "isbn": ["ISBN", "file-digit"],
        "year": ["Published", "calendar-days"],
    }

    def load_books(self):
        """
        Loads books to the state from the database memory.
        """
        self.loading = True
        self.books = FILEBASE.get_all_as_type(Item)
        self.loading = False

    def add_book(self, form_data: dict):
        """
        Adds a new book to the database file and memory updates the Reflex state.
        """
        FILEBASE.add_item(form_data)
        self.load_books()
        self.dialog_open = False

    def toggle_dialog(self):
        self.dialog_open = not self.dialog_open


def details_as_list(keyvalue: tuple) -> rx.Component:
    key = keyvalue[0]
    value = keyvalue[1]
    label_and_icon = State.keys_as_labels.get(key, [key.capitalize(), "circle-help"])
    label = label_and_icon[0]
    icon = label_and_icon[1]
    return rx.list.item(
        rx.icon(icon, margin_right="0.5em", display="inline-block"),
        rx.text(f"{label}: ", as_="span", weight="bold"),
        rx.text(value, as_="span"),
        list_style_type="none",
        margin_bottom="0.2em",
    )


def book_as_card(item: Item) -> rx.Component:
    """
    Creates a Relex card component for displaying book information.
    """
    return rx.card(
        rx.vstack(
            rx.heading(item.name, weight="bold", size="4", as_="h2"),
            rx.list.unordered(
                rx.foreach(item.items()[1:], details_as_list), margin_left="0"
            ),
        ),
        size="5",
        align_items="flex-start",
        flex_wrap="wrap",
        padding="1em",
    )


def add_book_button() -> rx.Component:
    return rx.dialog.root(
        rx.card(
            rx.dialog.trigger(
                rx.button(
                    rx.icon("plus", size=26),
                    rx.text("Add Book", size="4"),
                    height="8rem",
                    width="100%",
                    on_click=State.toggle_dialog,
                ),
            ),
        ),
        rx.dialog.content(
            rx.dialog.title("Add New Book"),
            rx.dialog.description("Fill in details of the new book."),
            rx.form(
                rx.form.field(
                    rx.form.label("Title"),
                    rx.form.control(
                        rx.input(name="name", required=True),
                        as_child=True,
                    ),
                ),
                rx.form.field(
                    rx.form.label("Author"),
                    rx.form.control(
                        rx.input(name="author", required=True),
                        as_child=True,
                    ),
                ),
                rx.form.field(
                    rx.form.label("ISBN (10-13 digits)"),
                    rx.form.control(
                        rx.input(
                            name="isbn",
                            required=True,
                            pattern=r"\d{10,13}",
                            min_length=10,
                            max_length=13,
                            inputMode="numeric",
                        ),
                        as_child=True,
                    ),
                ),
                rx.form.field(
                    rx.form.label("Year (yyyy)"),
                    rx.form.control(
                        rx.input(
                            name="year",
                            required=True,
                            pattern=r"\d{0,4}",
                            max_length=4,
                            inputMode="numeric",
                        ),
                        as_child=True,
                    ),
                ),
                rx.hstack(
                    rx.dialog.close(
                        rx.button(
                            "Cancel",
                            type="button",
                            variant="soft",
                            color_scheme="gray",
                            on_click=State.toggle_dialog,
                        )
                    ),
                    rx.button(
                        "Submit",
                        type="submit",
                        reset_on_submit=True,
                    ),
                ),
                on_submit=State.add_book,
            ),
        ),
        open=State.dialog_open,
    )


@rx.page(on_load=State.load_books)
@rx.page(title="Book Dictionary")
def index() -> rx.Component:
    return rx.stack(
        rx.vstack(
            rx.heading("Book Dictionary", weight="bold", size="6", as_="h1"),
            rx.cond(
                State.loading,
                rx.text("Loading..."),
                rx.grid(
                    add_book_button(),
                    rx.foreach(State.books, book_as_card),
                    columns=rx.breakpoints(initial="1", sm="2", lg="4"),
                    spacing="4",
                ),
            ),
            spacing="7",
            align="center",
            width="95%",
        ),
        justify="center",
        padding_top="2em",
    )


app = rx.App(
    theme=rx.theme(accent_color="iris"),
)
