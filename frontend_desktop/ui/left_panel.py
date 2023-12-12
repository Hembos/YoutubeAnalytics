from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QWidget, QComboBox, QVBoxLayout, QPushButton

from ui.videos_tree import VideosTree


class LeftPanel(QWidget):
    update_button_click = pyqtSignal()
    
    def __init__(self, parent: QWidget | None = None, flags: Qt.WindowFlags = Qt.WindowFlags()) -> None:
        super().__init__(parent, flags)
        
        self.__statistics_combobox = QComboBox()
        self.__statistics_combobox.addItem("Graph 1")
        self.__statistics_combobox.addItem("Graph 2")
        
        self.__update_button = QPushButton("Обновить")
        self.__update_button.clicked.connect(self.update_button_click)
        
        self.__videos_tree = VideosTree()
        
        self.__layout = QVBoxLayout(self)
        self.__layout.addWidget(self.__update_button)
        self.__layout.addWidget(self.__statistics_combobox)
        self.__layout.addWidget(self.__videos_tree)
        
    def fill_videos_tree(self, channels: list) -> None:
        self.__videos_tree.fill(channels)
        