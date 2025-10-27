from dataclasses import dataclass
from typing import Callable, ClassVar, Dict, List


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


@dataclass
class EventListener(metaclass=Singleton):
    __events__: ClassVar[Dict[str, List[Callable]]] = {}

    def subscribe(self, event_name: str, callback: Callable) -> None:
        events = self.__events__.get(event_name)
        if events:
            events.append(callback)
        else:
            self.__events__[event_name] = []
            self.__events__[event_name].append(callback)

    def unsubscribe(self, event_name: str, callback: Callable) -> None:
        events = self.__events__.get(event_name)
        if not events:
            return
        events.remove(callback)
        if events.__len__() == 0:
            self.__events__.pop(event_name)

    def dispatch(self, event_name: str, *args, **kwargs):
        for event in self.__events__.get(event_name, []):
            event(*args, **kwargs)
