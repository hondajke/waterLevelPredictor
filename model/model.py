# Additional imports 
import matplotlib.pyplot as plt
import pandas as pd 
import numpy as np

# Imports for creating plots
from pylab import rcParams
rcParams['figure.figsize'] = 18, 7

# Pipeline and nodes
from fedot.core.pipelines.pipeline import Pipeline
from fedot.core.pipelines.node import PrimaryNode, SecondaryNode

# Data 
from fedot.core.data.data import InputData
from fedot.core.data.data_split import train_test_data_setup
from fedot.core.repository.dataset_types import DataTypesEnum

# Tasks
from fedot.core.repository.tasks import Task, TaskTypesEnum, TsForecastingParams

# Read the file
df = pd.read_csv('/content/data.csv')
df['data'] = pd.to_datetime(df['data'], format='%d-%m-%Y')
act_data = df[:730]
plt.plot(act_data['data'], act_data['water_level'])
plt.show()

def plot_results(actual_time_series, predicted_values, len_train_data, y_name = 'Parameter'):
    """
    Function for drawing plot with predictions
    
    :param actual_time_series: the entire array with one-dimensional data
    :param predicted_values: array with predicted values
    :param len_train_data: number of elements in the training sample
    :param y_name: name of the y axis
    """
    
    plt.plot(np.arange(0, len(actual_time_series)), 
             actual_time_series, label = 'Actual values', c = 'green')
    plt.plot(np.arange(len_train_data, len_train_data + len(predicted_values)), 
             predicted_values, label = 'Predicted', c = 'blue')
    # Plot black line which divide our array into train and test
    plt.plot([len_train_data, len_train_data],
             [min(actual_time_series), max(actual_time_series)], c = 'black', linewidth = 1)
    plt.ylabel(y_name, fontsize = 15)
    plt.xlabel('Time index', fontsize = 15)
    plt.legend(fontsize = 15, loc='upper left')
    plt.grid()
    plt.show()

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
def get_pipeline():
    node_lagged_1 = PrimaryNode('lagged')
    node_lagged_1.custom_params = {'window_size': 120}
    node_lagged_2 = PrimaryNode('lagged')
    node_lagged_2.custom_params = {'window_size': 10}

    node_first = SecondaryNode('ridge', nodes_from=[node_lagged_1])
    node_second = SecondaryNode('dtreg', nodes_from=[node_lagged_2])
    node_final = SecondaryNode('ridge', nodes_from=[node_first, node_second])
    pipeline = Pipeline(node_final)

    return pipeline

pipeline = get_pipeline()
# Fit pipeline
pipeline.fit(train_input)

# Make forecast
output = pipeline.predict(predict_input)
forecast = np.ravel(np.array(output.predict))

# Plot the graph
plot_results(actual_time_series = time_series,
             predicted_values = forecast, 
             len_train_data = len(time_series)-forecast_length)

from fedot.core.pipelines.ts_wrappers import out_of_sample_ts_forecast

# Make forecast
ts_predicted = out_of_sample_ts_forecast(pipeline=pipeline,
                                         input_data=predict_input,
                                         horizon=300)

# Plot the graph
plot_results(actual_time_series = time_series,
             predicted_values = ts_predicted, 
             len_train_data = len(time_series)-forecast_length)