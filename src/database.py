from dataclasses import dataclass
from src.utils import Singleton


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
