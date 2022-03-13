import window
import sys, os
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog, QSizePolicy, QComboBox, QPushButton, QVBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

from fedot.core.pipelines.pipeline import Pipeline
from fedot.core.pipelines.node import PrimaryNode, SecondaryNode

# Data 
from fedot.core.data.data import InputData
from fedot.core.data.data_split import train_test_data_setup
from fedot.core.repository.dataset_types import DataTypesEnum

# Tasks
from fedot.core.repository.tasks import Task, TaskTypesEnum, TsForecastingParams


class WaterPredictor(QtWidgets.QMainWindow, window.Ui_MainWindow):
    directory = ''
    data = ''

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.actionQuit.triggered.connect(self.close)
        self.actionSelect_Data.triggered.connect(self.openFile)
        self.actionPredict.triggered.connect(self.makePredict)
            

    def openFile(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "",".csv Files (*.csv)", options=options)
        if fileName:
            print(fileName)
            with open(fileName) as file:
                df = pd.read_csv(file)
                self.data = df
                sc = MplCanvas(self, width=5, height=4, dpi=100)
                sc.axes.plot(self.data['data'], self.data['water_level'])
                self.setCentralWidget(sc)
                print(self.data)
                
    def makePredict(self):
        md = PredictModel(self.data)
        act, pred, size = md.get_results()
        #print(act, pred, size)
        #print(self.data)
        sc = MplCanvas(self, width=5, height=4, dpi=100)
        sc.axes.plot(np.arange(0, len(act)), 
             act, label = 'Actual values', c = 'green')
        sc.axes.plot(np.arange(size, size + len(pred)), 
                 pred, label = 'Predicted', c = 'blue')
        sc.axes.set_ylabel('Water Level', fontsize = 15)
        sc.axes.set_xlabel('Time index', fontsize = 15)
        sc.axes.legend(fontsize = 15, loc='upper left')
        # Plot black line which divide our array into train and test
        sc.axes.plot([size, size],
                 [min(act), max(act)], c = 'black', linewidth = 1)
        self.setCentralWidget(sc)


class MplCanvas(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)

class PredictModel():
    _actual_time_series = ''
    _predicted_values = ''
    _len_train_data = ''
    
    #def plot_results(self, actual_time_series, predicted_values, len_train_data, y_name = 'Parameter'):
    #    plt.plot(np.arange(0, len(actual_time_series)), 
    #             actual_time_series, label = 'Actual values', c = 'green')
    #    plt.plot(np.arange(len_train_data, len_train_data + len(predicted_values)), 
    #             predicted_values, label = 'Predicted', c = 'blue')
    #    # Plot black line which divide our array into train and test
    #    plt.plot([len_train_data, len_train_data],
    #             [min(actual_time_series), max(actual_time_series)], c = 'black', linewidth = 1)
    #    plt.ylabel(y_name, fontsize = 15)
    #    plt.xlabel('Time index', fontsize = 15)
    #    plt.legend(fontsize = 15, loc='upper left')
    #    plt.grid()
    #    plt.show()
        
    def get_results(self):
        return self._actual_time_series, self._predicted_values, self._len_train_data
    
    def get_pipeline(self):
        node_lagged_1 = PrimaryNode('lagged')
        node_lagged_1.custom_params = {'window_size': 120}
        node_lagged_2 = PrimaryNode('lagged')
        node_lagged_2.custom_params = {'window_size': 10}

        node_first = SecondaryNode('ridge', nodes_from=[node_lagged_1])
        node_second = SecondaryNode('dtreg', nodes_from=[node_lagged_2])
        node_final = SecondaryNode('ridge', nodes_from=[node_first, node_second])
        pipeline = Pipeline(node_final)

        return pipeline
    
    def __init__(self, inputData):
        df = inputData
        df['data'] = pd.to_datetime(df['data'], format='%d-%m-%Y')
        act_data = df[:730]
        # Specify forecast length
        forecast_length = 200

        # Got univariate time series as numpy array
        time_series = np.array(act_data['water_level'])

        # Wrapp data into InputData
        task = Task(TaskTypesEnum.ts_forecasting,
                    TsForecastingParams(forecast_length=forecast_length))
        input_data = InputData(idx=np.arange(0, len(time_series)),
                               features=time_series,
                               target=time_series,
                               task=task,
                               data_type=DataTypesEnum.ts)

        # Split data into train and test
        train_input, predict_input = train_test_data_setup(input_data)
        pipeline = self.get_pipeline()
        # Fit pipeline
        pipeline.fit(train_input)

        # Make forecast
        output = pipeline.predict(predict_input)
        forecast = np.ravel(np.array(output.predict))

        # Plot the graph
        #self.plot_results(actual_time_series = time_series,
        #             predicted_values = forecast, 
        #             len_train_data = len(time_series)-forecast_length)

        from fedot.core.pipelines.ts_wrappers import out_of_sample_ts_forecast

        # Make forecast
        ts_predicted = out_of_sample_ts_forecast(pipeline=pipeline,
                                                 input_data=predict_input,
                                                 horizon=300)
        
        # Plot the graph
        #self.plot_results(actual_time_series = time_series,
        #             predicted_values = ts_predicted, 
        #             len_train_data = len(time_series)-forecast_length)
        
        self._actual_time_series = time_series
        self._predicted_values = ts_predicted
        self._len_train_data = len(time_series) - forecast_length
        

    

def main():
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = WaterPredictor()  # Создаём объект класса ExampleApp
    window.show()  # Показываем окно
    app.exec_()  # и запускаем приложение


if __name__ == '__main__':  # Если запускаем файл напрямую, а не импортируем
    main()  # то запускаем функцию main()