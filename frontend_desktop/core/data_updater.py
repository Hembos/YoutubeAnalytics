from PyQt5.QtCore import pyqtSignal, QObject
import requests
from config import API_URL


class DataUpdater(QObject):
    channels_videos_fetch = pyqtSignal(list)
    requests_fetch = pyqtSignal(list)

    def __init__(self, parent: QObject | None = None) -> None:
        super().__init__(parent)

    def fetch_data(self):
        channels_response = requests.get(f'{API_URL}channels/')
        requests_response = requests.get(f'{API_URL}requests/?count=1000')

        self.channels_videos_fetch.emit(channels_response.json())
        self.requests_fetch.emit(requests_response.json())
