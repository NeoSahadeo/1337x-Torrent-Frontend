from enum import Enum
from dataclasses import dataclass
from src.utils import Singleton


class Categories(Enum):
    TV = "TV Only"
    Movies = "Movies Only"
    Games = "Games Only"
    Music = "Music Only"
    Apps = "Applications Only"
    Documentaries = "Documentaries Only"
    Anime = "Anime Only"
    Other = "Other Only"
    XXX = "XXX Only"


@dataclass
class Item:
    link: str = ""
    name: str = ""
    seeds: str = ""
    leeches: str = ""
    size: str = ""
    id: str = ""


@dataclass
class SearchState(metaclass=Singleton):
    category = Categories.TV
    page = 1

    def set_category(self, category: Categories):
        self.category = category

    def get_category(self):
        return self.category.value

    def set_page(self, number):
        self.page = number

    def get_page(self):
        return self.page


@dataclass
class Database(metaclass=Singleton):
    data = {}

    def get(self, key):
        if self.data.get(key):
            return self.data.get(key)

    def getall(self):
        return self.data.keys()

    # def insert(self, key, value):
    #     if not self.data.get(key):
    #         self.data[key] = value

    def update(self, key, value):
        self.data[key] = value

    def delete(self, key):
        if self.data.get(key):
            del self.data[key]

    def clear(self):
        self.data = {}


if __name__ == "__main__":
    db = Database()
    db.insert("Neo", 123456)
    db = Database()
    print(db.get("Neo"))
