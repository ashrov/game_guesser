import sys
from client import Client
from PyQt5 import QtWidgets, QtCore

from window_1 import UiWindow1
from window_2 import UiWindow2

client = Client()

message = {'intent': 'get_all_tags'}
tags = client.send_message(message)['all_tags']
questions = [question["question"] for question in tags]

count = 0


class Win2(QtWidgets.QWidget):
    def __init__(self):
        super(Win2, self).__init__()
        self.ui = UiWindow2()
        self.ui.setupUi(self)
        self.ui.pushButton_2.clicked.connect(self.change_text)
        self.ui.pushButton.clicked.connect(self.change_text)


    def change_text(self):
        global count
        self.ui.label_2.setGeometry(QtCore.QRect(210, 130, 15 * len(questions[count]), 231))
        if questions[count]:
            self.ui.label_2.setText(questions[count])
        count += 1

class Win1(QtWidgets.QMainWindow):
    def __init__(self):

        super(Win1, self).__init__()
        self.ui = UiWindow1()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.swicth_window)

        self.win_2 = Win2()



    def swicth_window(self):
        self.close()
        self.win_2.show()





if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    application_1 = Win1()
    application_1.show()

    sys.exit(app.exec())
