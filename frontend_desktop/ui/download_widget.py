from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QLineEdit, QWidget, QHBoxLayout, QLabel, QPushButton


class UrlWidget(QWidget):
    download = pyqtSignal(str)
    
    def __init__(self, parent: QWidget | None = None, flags: Qt.WindowFlags | Qt.WindowType = Qt.WindowFlags()) -> None:
        super().__init__(parent, flags)

        self.__layout = QHBoxLayout()
        self.setLayout(self.__layout)

        self.__layout.addWidget(QLabel("Введите ссылку на видео:"))

        self.__url_line_edit = QLineEdit()
        self.__download_button = QPushButton("Скачать")
        self.__download_button.clicked.connect(self.download_clicked)

        self.__layout.addWidget(self.__url_line_edit)
        self.__layout.addWidget(self.__download_button)

    def download_clicked(self) -> None:
        url = self.__url_line_edit.text()
        if url == '':
            return

        self.download.emit(url)
