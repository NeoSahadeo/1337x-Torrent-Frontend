import sys
from qbittorrent import Client
from src import Networking, EventListener, Database, Scanner, Window
from PyQt6.QtWidgets import QApplication
from requests.exceptions import ConnectionError


def qBittorrentProcess(links):
    for x in links:
        qb.download_from_link(x)


def main():
    e = EventListener()
    Networking()
    Database()
    scanner = Scanner()

    # Link scanner to networking modules
    e.subscribe("query_response", scanner.scan_search_page)

    # Subscribe to link response
    e.subscribe("follow_links_response", qBittorrentProcess)

    app = QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    try:
        qb = Client('http://localhost:8080/')
        qb.login('admin', 'admin1234')
        main()
    except ConnectionError:
        print("Qbittorent is not open!")
