import threading

import serial
from serial import SerialException
from serial.tools import list_ports
from PyQt5.QtCore import QObject, QThread, QTimer, pyqtSlot, pyqtSignal


class SerialBackend(QObject):

    serialMessage_signal = pyqtSignal(str)
    portsAvailable_signal = pyqtSignal(list)


    def _thread_set(self):
        thread = threading.current_thread()
        thread.setName(self.thread.objectName())

    def __init__(self, device=None, baud_rate=9600):
        super().__init__()
        self.thread = QThread()
        self.thread.setObjectName("SerialWorkerThread")
        self.moveToThread(self.thread)
        self.thread.started.connect(self._thread_set)

        self.serialLoopTimer = QTimer()
        self.serialLoopTimer.timeout.connect(self.serial_loop)
        self.sampling_rate = 100
        self.serialLoopTimer.start(self.sampling_rate)

        self.thread.start()

        self.currentConnectedPortName = None
        self.openConnection = True
        self.device = None
        self.baud_rate = 9600
        self.portIsAvailable = False
        self.portWasAvailable = False
        self._configurationsChanged = False
        self.currentConnectedSerialPort = None
        self.currentConnectedPortName = None
        self.Last_Command = None
        self.Sent_MSGs = 0

    @pyqtSlot()
    def get_all_ports(self):
        ports = list_ports.comports()
        self.portsAvailable_signal.emit([port.device for port in ports])

    @pyqtSlot(str)
    def set_port(self, port: str):
        if self.currentConnectedPortName != port:
            self.device = port

    def serial_loop(self):
        # if we don't want to connect with serial port
        if not self.openConnection:
            if self.currentConnectedSerialPort != None:
                self.currentConnectedSerialPort.close()
        else:
            self.portIsAvailable = self.device
            if self.portIsAvailable != self.portWasAvailable:
                # if it is the first time that it becomes available
                if self.portIsAvailable:
                    pass
                # if it was available then it changed
                else:
                    self.currentConnectedSerialPort = None
                # If the port connection changed, then signal the user interface to update.
                self.portWasAvailable = self.portIsAvailable
            # if we are trying to connect for the first time and no ports are found or 1 time after disconnecting
            elif not self.portIsAvailable:
                self.currentConnectedSerialPort = None

            # if the port is available and no connection was opened before
            # or the configurations (port or baudRate were changed)
            if (self.portIsAvailable and not self.currentConnectedSerialPort) or self._configurationsChanged:
                # if the configurations changed and there is an opened a connection
                if self._configurationsChanged == True and self.currentConnectedSerialPort:
                    self.currentConnectedSerialPort.close()
                try:
                    self.open_connection()
                    # print("print")
                except:
                    self.currentConnectedSerialPort = None

    def open_connection(self):
        # portToConnect = self.get_port()
        portToConnect = self.device
        print("send thread:", portToConnect)
        portToConnect = str(portToConnect)
        # if there is ports that are connected
        #if True:
        #    self.currentConnectedSerialPort = serial.Serial(portToConnect, self.baudRate, timeout=3)
        if portToConnect:
            #self.currentConnectedSerialPort = serial.Serial(portToConnect, self.baudRate, timeout=90 / 1000)
            self.currentConnectedSerialPort = serial.Serial(portToConnect, self.baud_rate, timeout=3)
            self.currentConnectedPortName = portToConnect
            self._configurationsChanged = False
            print("Done connecting")


            if not self.currentConnectedSerialPort.is_open:
                self.currentConnectedSerialPort.open()

        if self.currentConnectedSerialPort.is_open:
            print("\n   Port Open Success")


        else:
            pass

    @pyqtSlot(str)
    def send(self, command: str):
        if self.portIsAvailable and self.openConnection:
            if command != self.Last_Command:
                self.Sent_MSGs = 0
            if self.Sent_MSGs < 3:
                try:
                    print("Sent :" + command)
                    if self.currentConnectedSerialPort:
                        self.currentConnectedSerialPort.write(str(command + "\n").encode())
                        print("Sent :" + command)
                    self.serialMessage_signal.emit(command)
                    self.Last_Command = command
                    self.Sent_MSGs += 1
                except SerialException:
                    pass

