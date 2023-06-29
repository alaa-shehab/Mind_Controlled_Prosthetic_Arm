import sys

from PyQt5 import QtWidgets

from Backend.ProstheticsWindowBackend import ProstheticsBackend
from Backend.SerialBackend import SerialBackend

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    ui = ProstheticsBackend()
    serial = SerialBackend()
    ui.get_ports_signal.connect(serial.get_all_ports)
    serial.portsAvailable_signal.connect(ui.scan_button_action)
    ui.port_signal.connect(serial.set_port)
    ui.command_signal.connect(serial.send)

    ui.show()
    sys.exit(app.exec_())

