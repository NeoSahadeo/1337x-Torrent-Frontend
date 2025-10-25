from dataclasses import dataclass
import re
import urllib
from bs4 import BeautifulSoup
from src.utils import EventListener


@dataclass
class Item:
    link: str = ""
    name: str = ""
    seeds: str = ""
    leeches: str = ""
    size: str = ""
    id: str = ""


class Scanner():
    def scan_search_page(self, text) -> None:
        iterator = re.finditer(r"(?<=<tr>)(?P<table_row>(.|\n)*?)(?=<\/tr>)", text, re.MULTILINE)
        index = 0
        for match in iterator:
            if index == 0:
                index += 1  # INFO: Skip first iteration
                continue
            groups = match.groupdict()
            results = re.finditer(r"(?P<name>name(.|\n)*?(?<=</td>))|(?P<seeds>seeds(.|\n)*?(?<=</td>))|(?P<leeches>leeches(.|\n)*?(?<=</td>))|(?P<size>size(.|\n)*?(?<=</td>))|(?P<uploader>uploader(.|\n)*?(?<=</td>))", groups['table_row'], re.MULTILINE)

            item: Item = {}
            item["name"] = "error"
            for m in results:
                if (m.group("name")):
                    # b = BeautifulSoup(m.group("name"))
                    # print(m.group("name"))
                    # _link = re.search(r"(?<=\")/torrent.*(?=\")", m.group("name"))
                    # if _link:
                    #     item["link"] = _link.group(0)
                    # _name = re.search(r"(?<=>)\w.*(?=</a></td>)", m.group("name"))
                    # if _name:
                    #     item["name"] = _name.group(0)
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
            EventListener().dispatch("scan_search_page",
                                     Item(
                                         link=item["link"],
                                         name=item["name"],
                                         seeds=item["seeds"],
                                         leeches=item["leeches"],
                                         size=item["size"],
                                         id=item["id"],
                                     ))
