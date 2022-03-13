import window
import sys, os
import pandas as pd 
import matplotlib
matplotlib.use('Qt5Agg')

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog, QSizePolicy, QComboBox, QPushButton, QVBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

class WaterPredictor(QtWidgets.QMainWindow, window.Ui_MainWindow):
    directory = ''
    data = ''

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.actionQuit.triggered.connect(self.close)
        self.actionSelect_Data.triggered.connect(self.openFile)
            

    def openFile(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "",".csv Files (*.csv)", options=options)
        if fileName:
            print(fileName)
            with open(fileName) as file:
                df = pd.read_csv(file)
                data = df
                sc = MplCanvas(self, width=5, height=4, dpi=100)
                data[:731].plot(ax=sc.axes)
                self.setCentralWidget(sc)
                print(data)


class MplCanvas(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)



def main():
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = WaterPredictor()  # Создаём объект класса ExampleApp
    window.show()  # Показываем окно
    app.exec_()  # и запускаем приложение


if __name__ == '__main__':  # Если запускаем файл напрямую, а не импортируем
    main()  # то запускаем функцию main()