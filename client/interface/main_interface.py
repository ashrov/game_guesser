from PyQt5 import QtCore, QtGui, QtWidgets
import sys
from time import sleep
from PyQt5.QtGui import QIcon, QColor, QPainter
from interface import Ui_MainWindow

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    application_1 = MainWindow()
    application_1.show()

    sys.exit(app.exec())
