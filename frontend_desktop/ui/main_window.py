from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QListWidget, QListWidgetItem, QSplitter

import pyqtgraph as pg

from ui.download_widget import UrlWidget
from ui.left_panel import LeftPanel
from ui.requests_table import RequestsTable

from core.data_updater import DataUpdater

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.__main_layout = QVBoxLayout()
        self.__url_widget = UrlWidget()
        self.__data_updater = DataUpdater()
        self.__left_panel = LeftPanel()
        self.__requests_table = RequestsTable()
        
        self.__plot_graph = pg.PlotWidget()
        self.__plot_graph.setBackground("w")
        pen = pg.mkPen(color=(255, 0, 0))
        time = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        temperature = [30, 32, 34, 32, 33, 31, 29, 32, 35, 45]
        self.__plot_graph.plot(time, temperature, pen=pen)
        
        self.__left_panel.update_button_click.connect(self.__data_updater.fetch_data)
        
        self.__main_layout.addWidget(self.__url_widget)
        self.__main_layout.addWidget(self.__plot_graph)
        
        splitter = QSplitter()
        
        widget = QWidget()
        widget.setLayout(self.__main_layout)
        
        splitter.addWidget(self.__left_panel)
        splitter.addWidget(widget)
        splitter.addWidget(self.__requests_table)
        self.setCentralWidget(splitter)
        
        self.__data_updater.channels_videos_fetch.connect(
            self.__left_panel.fill_videos_tree
        )
        
        self.__data_updater.requests_fetch.connect(
            self.__requests_table.fill
        )
        
        self.__data_updater.fetch_data()
