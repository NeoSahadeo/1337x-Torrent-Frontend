import threading
from qbittorrent import Client
from src import Networking, EventListener, Database, Scanner, Window, Item


def qBittorrentProcess(links):
    for x in links:
        qb.download_from_link(x)


def main():
    e = EventListener()
    Networking()
    Database()
    scanner = Scanner()
    window = Window()

    # Link scanner to networking modules
    e.subscribe("query_response", scanner.scan_search_page)

    # Subscribe to link response
    e.subscribe("follow_links_response", qBittorrentProcess)

    window.mainloop()


if __name__ == "__main__":
    qb = Client('http://localhost:8080/')
    qb.login('admin', 'admin1234')
    main()
