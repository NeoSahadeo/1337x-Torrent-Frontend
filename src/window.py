import webbrowser
import PyQt6.QtCore as QtCore
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QFrame, QLabel, QCheckBox
from qtgen.main_window import Ui_MainWindow
from qtgen.list_item import Ui_Frame
from qtgen.loading import Ui_Loading
from src.utils import EventListener
from src.database import Item, Database
from src.networking import Categories


class ListItem(Ui_Frame, QWidget):
    item: Item
    clicked = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.setFixedHeight(50)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit()
        super().mousePressEvent(event)


class Window(QMainWindow, Ui_MainWindow):
    __list_elements__: list[QCheckBox] = []
    __select_all: bool = False

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        self.current_page = 1
        self.EventHandler = EventListener()
        self.db = Database()

        self.container = QWidget()
        self.layout = QVBoxLayout(self.container)
        self.scrollArea.setWidget(self.container)

        # self.loading_widget = QWidget()
        # loading_ui = Ui_Loading()
        # loading_ui.setupUi(self.loading_widget)
        # self.layout.addWidget(self.loading_widget)
        # self.loading_widget.hide()

        self.EventHandler.subscribe("scan_search_page", self.populate_list)

        self.search.clicked.connect(self.search_button)
        self.searchBox.returnPressed.connect(self.search_button)
        self.categoryButton.currentIndexChanged.connect(self.search_button)
        self.nextPage.clicked.connect(self.next_page)
        self.prevPage.clicked.connect(self.prev_page)
        self.queueSelected.clicked.connect(self.queue_selected)
        self.closeButton.clicked.connect(self.close_window)
        self.githubButton.clicked.connect(self.github_link)
        self.selectAllButton.clicked.connect(self.select_all)

    def search_button(self):
        self.loading_widget.show()
        return
        for x in self.__list_elements__:
            x.deleteLater()
        self.__list_elements__ = []
        for x in self.db.getall():
            item: Item = self.db.get(x)
            self.create_list_item(item, True)
        self.EventHandler.dispatch("query_request", self.searchBox.text(), self.current_page, list(Categories)[self.categoryButton.currentIndex()])

    def create_list_item(self, item: Item, is_checked=False):
        def callback():
            if frame.checkbox.isChecked():
                self.db.update(item.id, item)
            else:
                self.db.delete(item.id)

        frame = ListItem()
        frame.item = item
        frame.label.setText(f"{item.name} | {item.size} | Seeds {item.seeds} | Leeches {item.leeches}")
        frame.checkbox.setChecked(is_checked)
        frame.checkbox.clicked.connect(callback)
        frame.clicked.connect(lambda: frame.checkbox.setChecked(not frame.checkbox.isChecked()) or callback())
        self.layout.addWidget(frame)
        self.__list_elements__.append(frame)

    def populate_list(self, item: Item):
        if not self.db.get(item.id):
            self.create_list_item(item)

    def next_page(self):
        self.current_page += 1
        self.search_button()

    def prev_page(self):
        if self.current_page > 1:
            self.current_page -= 1
        self.search_button()

    def queue_selected(self):
        links = []
        for x in self.db.getall():
            item: Item = self.db.get(x)
            links.append(item.link)
        self.EventHandler.dispatch("follow_links_request", links)

    def github_link(self):
        webbrowser.open("https://github.com/NeoSahadeo/1337x-Torrent-Frontend")

    def select_all(self):
        if self.__select_all:
            self.selectAllButton.setText('Select All')
            for x in self.__list_elements__:
                x.checkbox.setChecked(False)
                self.db.delete(x.item.id)
            self.__select_all = False
        else:
            self.selectAllButton.setText('Deselect All')
            for x in self.__list_elements__:
                x.checkbox.setChecked(True)
                self.db.update(x.item.id, x.item)
            self.__select_all = True

    def close_window(self):
        self.close()
