from PyQt5.QtWidgets import QApplication
from ui.main_window import MainWindow


app = QApplication([])
main = MainWindow()
main.show()
app.exec()


# import pyqtgraph as pg
# from PyQt5.QtGui import QPen, QPainter
# from PyQt5.QtWidgets import QWidget, QApplication
# import sys
# from PyQt5.QtCore import Qt


# class PieChartWidget(QWidget):
#     def __init__(self, data):
#         super(PieChartWidget, self).__init__()
#         self.data = data
#         self.colors = [pg.Color(255, 0, 0), pg.Color(0, 255, 0), pg.Color(0, 0, 255)]  # Example colors
#         self.setMinimumSize(300, 300)

#     def paintEvent(self, event):
#         painter = QPainter(self)
#         painter.setRenderHint(QPainter.Antialiasing)

#         total = sum(self.data)
#         start_angle = 0

#         for value, color in zip(self.data, self.colors):
#             span_angle = int(value / total * 16 * 360)
#             painter.setBrush(color)
#             painter.drawPie(self.rect(), start_angle, span_angle)
#             start_angle += span_angle

#         painter.end()


# def main():
#     app = QApplication(sys.argv)

#     data = [30, 100, 20]  # Example data

#     pie_chart_widget = PieChartWidget(data)
#     pie_chart_widget.setWindowTitle('PyQtGraph Pie Chart')

#     pie_chart_widget.show()

#     if sys.flags.interactive != 1 or not hasattr(Qt, 'PYQT_VERSION'):
#         sys.exit(app.exec_())


# if __name__ == '__main__':
#     main()
