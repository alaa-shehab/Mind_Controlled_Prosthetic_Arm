import threading

from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot
import numpy as np
from tensorflow import keras
from PyQt5 import QtWidgets
import pandas as pd
import keras
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Bidirectional, LSTM, BatchNormalization, Conv1D, Flatten, MaxPooling1D, \
    Dropout, TimeDistributed
from keras.optimizers import Adam, SGD

from Backend.SerialBackend import SerialBackend
from UI.prosthetic import Prosthetic_Window


class ProstheticsBackend(QtWidgets.QMainWindow):
    port_signal = pyqtSignal(str)
    get_ports_signal = pyqtSignal()
    command_signal = pyqtSignal(str)

    def _set_thread_name(self):
        # print(threading.currentThread().name)
        if threading.currentThread().name != "MainThread":
            threading.currentThread().name = self._thread_name

    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)
        self.ui = Prosthetic_Window()
        self.serial = SerialBackend()
        self.ui.setupUi(self)
        self.thread_name = "Model Thread"
        self.thread = QThread()
        self.moveToThread(self.thread)
        self.thread.started.connect(self._set_thread_name)
        self.thread.start()

        self.model = self.create_model()

        # self.model.build(input_shape= (1,100,32))
        self.model.load_weights('Models/model.h5')
        self.data = 0
        self.prediction = 0
        self.arr = 0
        self.test = 0
        self.test_arr = 0
        self.raw = []
        self.command = None
        self.ui.predictions_button.clicked.connect(self.test_dataset)
        self.ui.scan_button.clicked.connect(self.get_ports)
        self.ui.connect_button.clicked.connect(self.select_port)
        self.ui.open_button.clicked.connect(self.grasp_command)
        self.ui.close_button.clicked.connect(self.release_command)

    def test_dataset(self):
        print("in")
        self.data = pd.read_csv("test/test/subj1_series9_data.csv").drop(['id'], axis=1)
        self.raw.append(self.data)
        self.arr = np.asarray(pd.concat(self.raw).astype(float))
        self.reshape = np.resize(self.arr[2], (1, 100, 32))
        self.prediction = self.model.predict(self.reshape)
        index = np.argmax(self.prediction)
        if index == 0:
            self.ui.arm_state.setText("Grasp")
            self.command_signal.emit('G')
            print('grasp')

        else:
            self.ui.arm_state.setText("Release")
            self.command_signal.emit('R')
            print('release')

    def create_model(self):
        time_steps = 1000
        subsample = 10
        model3 = Sequential()
        model3.add(Conv1D(128, 7, input_shape=(time_steps // subsample, 32), activation='relu',
                          kernel_regularizer=keras.regularizers.l1_l2(0.001, 0.01)))
        model3.add(BatchNormalization())
        model3.add(MaxPooling1D(pool_size=2))
        model3.add(Dropout(0.25))
        model3.add(Conv1D(128, 5, activation='relu', kernel_regularizer=keras.regularizers.l1_l2(0.001, 0.01)))
        model3.add(BatchNormalization())
        model3.add(MaxPooling1D(pool_size=2))
        model3.add(Dropout(0.25))
        model3.add(
            Bidirectional(LSTM(256, kernel_regularizer=keras.regularizers.l1_l2(0.001, 0.01), return_sequences=True)))
        model3.add(BatchNormalization())
        model3.add(Dropout(0.25))
        model3.add(Flatten())
        model3.add(Dense(12, activation='relu'))
        model3.add(BatchNormalization())
        model3.add(Dropout(0.5))
        model3.add(Dense(12, activation='relu'))
        model3.add(BatchNormalization())
        model3.add(Dropout(0.5))
        model3.add(Dense(2, activation='sigmoid'))

        learning_rate = 0.1
        epochs = 50
        momentum = 0.8

        decay_rate = learning_rate / epochs
        ada = keras.optimizers.Adagrad(learning_rate=0.001, epsilon=1e-08, decay=decay_rate)
        sgd = SGD(learning_rate=learning_rate, momentum=momentum, decay=decay_rate, nesterov=False)

        model3.compile(loss='binary_crossentropy', optimizer=sgd, metrics=['accuracy'])
        return model3

    def create_lstm(self):
        model1 = Sequential()
        model1.add(TimeDistributed(Conv1D(filters=128, kernel_size=7, activation='relu',
                                          kernel_regularizer=keras.regularizers.l1_l2(0.001, 0.001),
                                          input_shape=(None, 100, 32))))
        model1.add(BatchNormalization())
        # model1.add(TimeDistributed(MaxPooling1D(pool_size=2)))
        model1.add(TimeDistributed(Conv1D(filters=64, kernel_size=5, activation='relu',
                                          kernel_regularizer=keras.regularizers.l1_l2(0.001, 0.001))))
        model1.add(BatchNormalization())
        model1.add(TimeDistributed(Conv1D(filters=32, kernel_size=3, activation='relu',
                                          kernel_regularizer=keras.regularizers.l1_l2(0.001, 0.001))))
        model1.add(BatchNormalization())
        model1.add(TimeDistributed(MaxPooling1D(pool_size=2)))
        # model1.add(BatchNormalization())
        model1.add(TimeDistributed(Flatten()))
        model1.add(LSTM(512))
        model1.add(Dense(12, activation='relu', kernel_regularizer=keras.regularizers.l1_l2(0.001, 0.001)))
        model1.add(Dense(2, activation='sigmoid'))
        # ad = adam(lr = 0.001)
        learning_rate = 0.1
        epochs = 50
        momentum = 0.8

        decay_rate = learning_rate / epochs
        ada = keras.optimizers.Adagrad(learning_rate=0.001, epsilon=1e-08, decay=decay_rate)

        model1.compile(optimizer=ada, loss="binary_crossentropy", metrics=["accuracy"])
        return model1

    @pyqtSlot(list)
    def scan_button_action(self, ports: list):
        self.ui.ports_comboBox.clear()
        self.ui.ports_comboBox.addItems(ports)

    def get_ports(self):
        self.get_ports_signal.emit()

    def select_port(self):
        self.port_signal.emit(self.ui.ports_comboBox.currentText())
        print(self.ui.ports_comboBox.currentText())

    def grasp_command(self):
        self.command_signal.emit('G')
        print('grasp')

    def release_command(self):
        self.command_signal.emit('R')
        print('release')
