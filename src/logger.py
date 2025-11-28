from src.utils import EventListener, Singleton


class Logger(EventListener, metaclass=Singleton):
    def __init__(self):
        self.subscribe("log_debug", self.print_debug)
        self.subscribe("log_error", self.print_error)
        self.subscribe("log_warning", self.print_warning)
        self.subscribe("log_info", self.print_info)

    def print_error(self, text):
        print("[Error]", text)

    def print_warning(self, text):
        print("[Warning]", text)

    def print_info(self, text):
        print("[INFO]", text)

    def print_debug(self, text):
        print("[DEBUG]", text)
