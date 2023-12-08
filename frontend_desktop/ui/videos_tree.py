from PyQt5.QtWidgets import QApplication, QTreeWidget, QTreeWidgetItem, QVBoxLayout, QWidget

class VideosTree(QWidget):
    def __init__(self):
        super().__init__()
        
        self.__tree = QTreeWidget(self)
        self.__tree.setHeaderHidden(True)

        rootItem = QTreeWidgetItem(self.__tree)
        rootItem.setText(0, 'Channel 1')

        # Add child items to the root
        child1 = QTreeWidgetItem(rootItem)
        child1.setText(0, 'Video 1')

        child2 = QTreeWidgetItem(rootItem)
        child2.setText(0, 'Video 2')
        
        self.__layout = QVBoxLayout()
        self.setLayout(self.__layout)
        self.__layout.addWidget(self.__tree)
        self.__layout.setSpacing(0)
        self.__layout.setContentsMargins(0, 0, 0, 0)