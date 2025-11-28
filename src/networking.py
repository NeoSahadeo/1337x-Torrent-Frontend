import threading
from enum import Enum
from dataclasses import dataclass
import urllib
from bs4 import BeautifulSoup
from src.utils import Singleton, EventListener
from src.selenium import SeleniumAgent
from selenium.webdriver.common.by import By


class Categories(Enum):
    TV = "TV"
    Movies = "Movies"
    Games = "Games"
    Music = "Music"
    Apps = "Apps"
    Documentaries = "Documentaries"
    Anime = "Anime"
    Other = "Other"
    XXX = "XXX"


@dataclass
class Networking(EventListener, metaclass=Singleton):
    lock = threading.Lock()
    postfix = "https://www.1377x.to"

    def __init__(self):
        self.agent = SeleniumAgent()
        self.subscribe("query_request", self.query)
        self.subscribe("follow_links_request", self.follow_links)

    def can_run(self) -> bool:
        self.dispatch("thread_lock")
        if not self.lock.acquire(blocking=False):
            return False
        return True

    def query(self, q: str, p=1, type: Categories = Categories.TV) -> None:
        if not self.can_run():
            return
        self.agent.search(q)
        self.dispatch("thread_unlock")
        self.lock.release()

    def follow_links(self, links):
        if not self.can_run():
            return
        # valid_links = []
        # for _link in links:
        #     response = self.session.get(f"{self.postfix}{_link}")
        #     soup = BeautifulSoup(response.text, "html.parser")
        #     anchors = soup.find_all('a')
        #     for x in anchors:
        #         if (x.decode_contents().__contains__("Magnet Download")):
        #             valid_links.append(x.get("href"))
        # self.dispatch("thread_unlock")
        # self.lock.release()
        # self.dispatch("follow_links_response", valid_links)


if __name__ == "__main__":
    n = Networking()
    # print(n.__events__)
    e = EventListener()
    # e.subscribe("query_response", callme)
    # e.dispatch("query_request", "Amazing Race")
