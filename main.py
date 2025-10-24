from typing import Union, Dict, Any
from tkinter import ttk, Tk, StringVar, BooleanVar, Grid, Canvas
import threading
import re
from bs4 import BeautifulSoup
import urllib
import requests
from qbittorrent import Client


qb = Client('http://localhost:8080/')
qb.login('admin', 'admin1234')

lock = threading.Lock()


class ObservableList(list):
    def __init__(self, *args, callback=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.callback = callback

    def append(self, item):
        super().append(item)
        if self.callback:
            self.callback('append', item)

    def remove(self, item):
        super().remove(item)
        if self.callback:
            self.callback('remove', item)

    def __setitem__(self, index, value):
        super().__setitem__(index, value)
        if self.callback:
            self.callback('setitem', index, value)


class Methods():
    render_list_data = ObservableList()
    postfix = "https://www.1377x.to"

    def __init__(self):
        pass

    def can_run(self) -> bool:
        if not lock.acquire(blocking=False):
            return False
        return True

    def clear_queries(self):
        for x in self.render_list_data:
            del self.render_list_data[x]

    def run_query(self, query, button):
        button.config(state="disabled")
        if not self.can_run():
            return
        print(f"Running query: {query}")
        encoded_query = urllib.parse.quote_plus(query)
        response = requests.get(f"{self.postfix}/sort-category-search/{encoded_query}/TV/seeders/desc/1/")
        # print(response.text)
        iterator = re.finditer(r"(?<=<tr>)(?P<table_row>(.|\n)*?)(?=<\/tr>)", response.text, re.MULTILINE)
        index = 0
        for match in iterator:
            if index == 0:
                index += 1  # INFO: Skip first iteration
                continue
            groups = match.groupdict()
            results = re.finditer(r"(?P<name>name(.|\n)*?(?<=</td>))|(?P<seeds>seeds(.|\n)*?(?<=</td>))|(?P<leeches>leeches(.|\n)*?(?<=</td>))|(?P<size>size(.|\n)*?(?<=</td>))|(?P<uploader>uploader(.|\n)*?(?<=</td>))", groups['table_row'], re.MULTILINE)

            item = {}
            for m in results:
                if (m.group("name")):
                    item["link"] = re.search(r"(?<=\")/torrent.*(?=\")", m.group("name")).group(0)
                    item["name"] = re.search(r"(?<=>)\w.*(?=</a></td>)", m.group("name")).group(0)
                    continue
                if (m.group("seeds")):
                    item["seeds"] = re.search(r"(?<=>)\w.*(?=</td>)", m.group("seeds")).group(0)
                    continue
                if (m.group("leeches")):
                    item["leeches"] = re.search(r"(?<=>)\w.*(?=</td>)", m.group("leeches")).group(0)
                    continue
                if (m.group("size")):
                    item["size"] = re.search(r"(?<=>)\w.*(?=</td>)", m.group("size")).group(0)
                    continue
                # if (m.group("uploader")):
                #     item["uploader"] = re.search(r"(? <= >)\w.*(?=</a>)", m.group("uploader")).group(0)
                #     continue
            item["id"] = urllib.parse.quote_plus(item["name"] + item["size"] + item["leeches"] + item["seeds"])
            self.render_list_data.append(item)
        lock.release()
        button.config(state="normal")

    def follow_links(self, links, button):
        button.config(state="disabled")
        if not self.can_run():
            return
        for _link in links:
            response = requests.get(f"{self.postfix}{_link}")
            soup = BeautifulSoup(response.text, "html.parser")
            anchors = soup.find_all('a')
            for x in anchors:
                if (x.decode_contents().__contains__("Magnet Download")):
                    qb.download_from_link(x.get("href"))
        lock.release()
        button.config(state="normal")


class ScrollableFrame(ttk.Frame):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        canvas = Canvas(self)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        self.scrollable_frame = ttk.Frame(canvas)

        # Update scroll region when the size of scrollable_frame changes
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")


class Window(Tk, Methods):
    render_list_checkboxes: Dict[str, ttk.Checkbutton] = {}

    def __init__(self):
        self.root = super().__init__()
        self.geometry("1280x720")
        self.title('App 1337x')
        self.columnconfigure(0, weight=1)

        self.render_list_data.callback = self.render_list
        _s = ScrollableFrame(self.root)
        self.render_list_frame = _s.scrollable_frame
        _s.scrollable_frame.columnconfigure(0, weight=1)
        _s.scrollable_frame.rowconfigure(0, weight=1)
        _s.grid(row=1, column=0, sticky="news")

        self.query = StringVar()
        self.search_frame = self._produce_frame()
        # Register UI
        self.close_button()
        self.search_ui()
        self.clear_button()
        self.scan_button()

        self.mainloop()

    def render_list(self, action, *args):
        checked = BooleanVar()
        c = self.generate_checkbox(self.render_list_frame,
                                   checked,
                                   f"{args[0]['name']} | {args[0]['size']} | {args[0]['seeds']} | {args[0]['leeches']}")
        c.grid(sticky="w")

        # def callback():
        #     print("clicked!", args[0]["id"], checked.get(), args[0]["link"])
        # c.configure(command=callback)
        self.render_list_checkboxes[args[0]["id"]] = (c, checked, args[0])

    def _produce_frame(self, **kwargs: Union[Grid, None]) -> ttk.Frame:
        frame = ttk.Frame(self.root)
        frame.grid(kwargs)
        return frame

    def _produce_button(self, parent: ttk.Frame, text, callback):
        button = ttk.Button(parent, text=text)
        button.bind("<ButtonPress-1>", callback)
        return button

    def generate_checkbox(self, parent: ttk.Frame, value: Any, text: str) -> ttk.Checkbutton:
        return ttk.Checkbutton(parent, text=text, variable=value, onvalue=True, offvalue=False)

    def close_button(self):
        frame = self._produce_frame()
        frame.columnconfigure(0, weight=1)
        frame.grid(row=0, column=0, sticky="ne")
        button = self._produce_button(frame, text="Close", callback=lambda _: self.destroy())
        button.grid(column=5, columnspan=1)

    def clear_button(self):
        def callback(_):
            self.query.set("")
            for x in self.render_list_checkboxes:
                self.render_list_checkboxes[x][0].destroy()

        button = self._produce_button(self.search_frame, text="Clear All", callback=callback)
        button.grid(row=0, column=6, columnspan=1)
        self.clear_queries()

    def scan_button(self):
        button = None

        def callback(_):
            links = []
            for x in self.render_list_checkboxes:
                if (self.render_list_checkboxes[x][1].get()):
                    links.append(self.render_list_checkboxes[x][2].get("link"))
            self.follow_links(links, button)

        button = self._produce_button(self.search_frame, text="Start Scan", callback=callback)
        button.grid(row=0, column=7, columnspan=1)

    def search_ui(self):
        self.search_frame.grid(row=0, column=0, sticky="nw")
        name = ttk.Entry(self.search_frame, textvariable=self.query)
        name.grid(row=0, column=2)
        ttk.Label(self.search_frame, text="Search").grid(row=0)

        button = self._produce_button(self.search_frame, text="🔍", callback=lambda _:
                                      threading.Thread(target=self.run_query, args=(self.query.get(), button)).start())
        button.grid(row=0, column=5, columnspan=1, rowspan=1)


class App(Window):
    def __init__(self):
        super().__init__()


if __name__ == "__main__":
    App()
