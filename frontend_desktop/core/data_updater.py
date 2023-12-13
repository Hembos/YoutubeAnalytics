from PyQt5.QtCore import pyqtSignal, QObject
import requests
from config import API_URL


class DataUpdater(QObject):
    channels_videos_fetch = pyqtSignal(list)
    requests_fetch = pyqtSignal(list)
    analytic_fetch = pyqtSignal(dict)

    def __init__(self, parent: QObject | None = None) -> None:
        super().__init__(parent)

    def fetch_data(self):
        channels_response = requests.get(f'{API_URL}channels/')
        requests_response = requests.get(f'{API_URL}requests/1000')

        self.channels_videos_fetch.emit(channels_response.json())
        self.requests_fetch.emit(requests_response.json())

        print(channels_response)
        print(requests_response)

    def send_analyze_request(self, id: str, is_channel: bool) -> None:
        # if is_channel:
        #     resp = requests.post(f'{API_URL}build-channel-analytics/{id}')
        # else:
        #     resp = requests.post(f'{API_URL}build-video-analytics/{id}')
        
        if not is_channel:
            resp = requests.post(f'{API_URL}build-video-analytics/{id}')
            print(resp)

    def send_download_data_request(self, url: str) -> None:
        resp = requests.post(f'{API_URL}channel-by-video-url/', json={"video_url": url})

        print(resp, url)

    def get_analytics(self, id: str, is_channel: bool, type: int) -> None:
        if is_channel:
            return

        resp = requests.get(f'{API_URL}get-analytics/{type}/{id}')

        self.analytic_fetch.emit(resp.json())

        print(resp, id, type)
