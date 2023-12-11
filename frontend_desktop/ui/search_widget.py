from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QLineEdit, QWidget, QHBoxLayout, QLabel, QPushButton


class SearchWidget(QWidget):
    def __init__(self, parent: QWidget | None = None, flags: Qt.WindowFlags | Qt.WindowType = Qt.WindowFlags()) -> None:
        super().__init__(parent, flags)
        
        self.__layout = QHBoxLayout()
        self.setLayout(self.__layout)
        
        self.__layout.addWidget(QLabel("Введите ссылку на видео:"))
        
        self.__item_search_line_edit = QLineEdit()
        self.__search_button = QPushButton("Проанализировать")
        
        self.__layout.addWidget(self.__item_search_line_edit)
        self.__layout.addWidget(self.__search_button)
