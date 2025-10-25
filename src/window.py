import customtkinter
from typing import Union, Callable
from tkinter import Tk, ttk, Grid, StringVar, IntVar, BooleanVar
from src.scanner import Item
from src.database import Database
from src.utils import EventListener


class BaseClass():
    def create_frame(self, master="default", **kwargs: Union[Grid, None]) -> ttk.Frame:
        frame = ttk.Frame(master=self.root if master == "default" else master, **kwargs)
        return frame

    def search_callback(self, e):
        for x in self.__list_elements__:
            x.destroy()
        self.__list_elements__ = []
        for x in self.db.getall():
            item: Item = self.db.get(x)
            self.create_list_item(item, True)
        EventListener().dispatch("query_request", self.query_string.get(), self.page_number.get())
        EventListener().dispatch("page_change")


class Dependencies(Tk, BaseClass):
    pass


class FormElements(Dependencies):
    __list_elements__: list[customtkinter.CTkCheckBox] = []

    def search_input(self):
        def callback(e):
            self.page_number.set(1)
            self.search_callback(e)
        entry: ttk.Entry = customtkinter.CTkEntry(self.search_parent,
                                                  width=400,
                                                  placeholder_text="Search 1337x",
                                                  textvariable=self.query_string)
        entry.bind("<Return>", callback)
        entry.pack(side='left')

    def create_list_item(self, item: Item, value=False):
        refVal = BooleanVar(value=value)
        checkbox = customtkinter.CTkCheckBox(self.scroll_parent, text=f"{item.name} | {item.size} | Seeds {item.seeds} | Leeches {item.leeches}", variable=refVal)
        checkbox.grid(column=0, padx=10, pady=(10, 0), sticky="w")

        def callback():
            if refVal.get():
                Database().update(item.id, item)
            else:
                Database().delete(item.id)
        checkbox.configure(command=callback)
        self.__list_elements__.append(checkbox)


class Buttons(Dependencies):
    def create_default_button(self,
                              parent: ttk.Frame,
                              text: str,
                              callback: Callable,
                              bind="<ButtonPress-1>",
                              color="#d63600",
                              width=140) -> ttk.Button:
        button = customtkinter.CTkButton(master=parent,
                                         text=text,
                                         width=width,
                                         corner_radius=5,
                                         border_width=4,
                                         border_color=color,
                                         fg_color=color,
                                         hover_color=color)
        button.bind(bind, callback)
        return button

    def close_button(self):
        button = self.create_default_button(self.root, text="x", width=50, callback=lambda _: self.destroy())
        button.place(rely=0.01, relx=0.99, anchor="ne")

    def search_button(self):
        def callback(e):
            self.page_number.set(1)
            self.search_callback(e)
        button = self.create_default_button(self.search_parent, text="🔍", width=50, callback=self.search_callback)
        button.pack_configure(padx=6)
        button.pack(side="right")

    def search_left_button(self):
        def callback(e):
            # Check thread lock
            self.page_number.set(self.page_number.get() + 1)
            self.search_callback(e)
        button = self.create_default_button(self.search_parent, text=">", width=50, callback=callback)
        button.pack(side="right")

    def search_right_button(self):
        def callback(e):
            # Check thread lock
            if (self.page_number.get() > 1):
                self.page_number.set(self.page_number.get() - 1)
            self.search_callback(e)
        button = self.create_default_button(self.search_parent, text="<", width=50, callback=callback)
        button.pack(side="right")

    def scan_button(self):
        def callback(e):
            links = []
            for x in self.db.getall():
                item: Item = self.db.get(x)
                links.append(item.link)
            EventListener().dispatch("follow_links_request", links)
        button = self.create_default_button(self.parent, text="Queue Selected", callback=callback)
        button.pack(side="right")

    def clear_button(self):
        button = self.create_default_button(self.parent, text="Clear All", color="red", callback=lambda _: print("I do nothing!"))
        button.pack(side="right")


class Labels(Dependencies):
    def logo_label(self):
        label = ttk.Label(self.root, text="1337x Frontend (Unofficial)")
        label.place(rely=0.01, relx=0.01, anchor="nw")

    def page_label(self):
        text = f"Page {self.page_number.get()}"
        label = ttk.Label(self.parent, text=text)
        label.pack()

        def callback():
            text = f"Page {self.page_number.get()}"
            label.config(text=text)

        EventListener().subscribe("page_change", callback)

    def selected(self):
        ...


class ScrollFrame(customtkinter.CTkScrollableFrame):
    def __init__(self, master):
        super().__init__(master)
        self.grid_columnconfigure(0, weight=1)


class Window(Buttons, FormElements, Labels):

    def __init__(self, custom_elements=[]):
        self.root = super().__init__()
        self.parent = self.create_frame(padding=10)

        self.query_string = StringVar()
        self.page_number = IntVar(value=1)

        self.db = Database()

        import os
        self.tk.call("lappend", "auto_path", os.path.join(os.getcwd(), "themes", "awthemes-10.4.0"))
        self.tk.call('package', 'require', 'awdark')
        ttk.Style().theme_use("awdark")

        self.geometry("1280x720")
        self.title("1337x App")
        self.configure(bg="#121212")
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.parent.columnconfigure(0, weight=1)
        self.parent.rowconfigure(0, weight=1)
        self.parent.grid(sticky="news")
        self.search_parent = self.create_frame(master=self.parent)
        self.search_parent.pack()
        self.search_parent.rowconfigure(0, weight=1)
        self.scroll_parent = ScrollFrame(self.parent)
        self.scroll_parent.rowconfigure(0, weight=99)
        self.scroll_parent.columnconfigure(0, weight=99)
        self.scroll_parent.pack(fill="both", expand=True)

        elements = [
            self.logo_label,
            self.page_label,
            self.close_button,
            self.search_input,
            self.search_left_button,
            self.search_right_button,
            self.search_button,
            self.scan_button,
            self.clear_button,
        ]
        for x in [*elements, *custom_elements]:
            x()

        EventListener().subscribe("scan_search_page", self.populate_list)

    def populate_list(self, item: Item):
        if not self.db.get(item.id):
            self.create_list_item(item)


if __name__ == "__main__":
    Window()
