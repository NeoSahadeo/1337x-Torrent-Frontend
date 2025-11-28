import sys
from PyQt6.QtWidgets import QApplication
from requests.exceptions import ConnectionError
from qbittorrent import Client
from src import Networking, EventListener, Database, Scanner, Window, SeleniumAgent, Logger


def qBittorrentProcess(links):
    for x in links:
        qb.download_from_link(x)


def close_all():
    raise Exception("Encountered Fatal Error!")


def main():
    Logger()
    e = EventListener()
    e.subscribe("error_close", close_all)
    e.dispatch("log_info", "EventListener Setup")
    e.dispatch("log_info", "Logger Setup")

    # gen user data before setting up network
    e.dispatch("log_info", "Loading Selenium Agent...")
    SeleniumAgent()
    e.dispatch("log_info", "Selenium Agent Setup")
    Networking()
    e.dispatch("log_info", "Networking Setup")

    Database()
    e.dispatch("log_info", "Database Setup")
    scanner = Scanner()
    e.dispatch("log_info", "Scanner Setup")

    # Link scanner to networking modules
    e.subscribe("query_response", scanner.scan_search_page)
    e.dispatch("log_debug", "Subscribed to query_response")

    # Subscribe to link response
    e.subscribe("follow_links_response", qBittorrentProcess)
    e.dispatch("log_debug", "Subscribed to follow_links_response")

    app = QApplication(sys.argv)
    e.dispatch("log_info", "QApplication Setup")
    win = Window()
    e.dispatch("log_info", "Window Setup")
    win.show()
    e.dispatch("log_info", "Displaying Window")

    sys.exit(app.exec())


if __name__ == "__main__":
    try:
        qb = Client('http://localhost:8080/')
        qb.login('admin', 'admin1234')
        main()
    except ConnectionError:
        print("Qbittorrent is not open!")
