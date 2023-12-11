from PyQt5.QtWidgets import QMainWindow, QGridLayout, QWidget, QComboBox, QListWidget, QListWidgetItem

import pyqtgraph as pg

from ui.search_widget import SearchWidget
from ui.videos_tree import VideosTree

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.__main_layout = QGridLayout()
        
        self.__search_widget = SearchWidget()
        
        self.__videos_tree = VideosTree()
        
        self.__statistics_combobox = QComboBox()
        self.__statistics_combobox.addItem("Graph 1")
        self.__statistics_combobox.addItem("Graph 2")
        
        self.__requests_list = QListWidget()
        QListWidgetItem("request 1", self.__requests_list)
        QListWidgetItem("request 2", self.__requests_list)
        QListWidgetItem("request 3", self.__requests_list)
        
        self.__plot_graph = pg.PlotWidget()
        self.__plot_graph.setBackground("w")
        pen = pg.mkPen(color=(255, 0, 0))
        time = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        temperature = [30, 32, 34, 32, 33, 31, 29, 32, 35, 45]
        self.__plot_graph.plot(time, temperature, pen=pen)
        
        self.__main_layout.addWidget(self.__search_widget, 0, 0, 1, 20)
        self.__main_layout.addWidget(self.__statistics_combobox, 1, 0, 1, 2)
        self.__main_layout.addWidget(self.__videos_tree, 2, 0, 18, 2)
        self.__main_layout.addWidget(self.__plot_graph, 1, 2, 19, 16)
        self.__main_layout.addWidget(self.__requests_list, 1, 18, 19, 2)
        
        widget = QWidget()
        widget.setLayout(self.__main_layout)
        self.setCentralWidget(widget)
        