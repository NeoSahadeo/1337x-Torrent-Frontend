import threading
from dataclasses import dataclass
import urllib
import requests
from bs4 import BeautifulSoup
from src.utils import Singleton, EventListener


@dataclass
class Networking(EventListener, metaclass=Singleton):
    lock = threading.Lock()
    postfix = "https://www.1377x.to"

    def __init__(self):
        self.subscribe("query_request", self.query)
        self.subscribe("follow_links_request", self.follow_links)

    def can_run(self) -> bool:
        self.dispatch("thread_lock")
        if not self.lock.acquire(blocking=False):
            return False
        return True

    def query(self, q: str, p=1) -> None:
        if not self.can_run():
            return
        # print(q, p)
        encoded_query = urllib.parse.quote_plus(q)
        response = requests.get(f"https://www.1337x.to/category-search/{encoded_query}/TV/{p}/")
        # response = requests.get(f"{self.postfix}/sort-category-search/{encoded_query}/TV/seeders/desc/{p}/")
        self.dispatch("thread_unlock")
        self.lock.release()
        self.dispatch("query_response", response.text)

    def follow_links(self, links):
        if not self.can_run():
            return
        valid_links = []
        for _link in links:
            response = requests.get(f"{self.postfix}{_link}")
            soup = BeautifulSoup(response.text, "html.parser")
            anchors = soup.find_all('a')
            for x in anchors:
                if (x.decode_contents().__contains__("Magnet Download")):
                    valid_links.append(x.get("href"))
        self.dispatch("thread_unlock")
        self.lock.release()
        self.dispatch("follow_links_response", valid_links)


if __name__ == "__main__":
    n = Networking()
    # print(n.__events__)
    e = EventListener()
    # e.subscribe("query_response", callme)
    # e.dispatch("query_request", "Amazing Race")
