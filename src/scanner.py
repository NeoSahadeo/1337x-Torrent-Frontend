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
            results = re.finditer(r"(?P<name>name(.|\n)*?(?<=</td>))|(?P<seeds><td class=\".* seeds.*?<)|(?P<leeches><td class=\".* leeches.*?<)|(?P<size><td class=\".*size.*?<)|(?P<uploader>uploader(.|\n)*?(?<=</td>))", groups['table_row'], re.MULTILINE)

            item: Item = {}
            for m in results:
                if (m.group("name")):
                    b = BeautifulSoup(m.group("name"), "html.parser")
                    for x in b.find_all("a"):
                        if str(x.get("href")).startswith("/torrent"):
                            item["name"] = x.decode_contents()
                            item["link"] = x.get("href")
                    continue
                if (m.group("seeds")):
                    item["seeds"] = re.search(r"(?<=>)\d+", m.group("seeds")).group(0)
                    continue
                if (m.group("leeches")):
                    item["leeches"] = re.search(r"(?<=>)\d+", m.group("leeches")).group(0)
                    continue
                if (m.group("size")):
                    item["size"] = re.search(r"(?<=>)[a-zA-Z0-9. ]+", m.group("size")).group(0)
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
