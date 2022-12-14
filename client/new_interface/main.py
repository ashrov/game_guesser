import sys
from client import Client
from PyQt5 import QtWidgets, QtCore

from window_1 import UiWindow1
from window_2 import UiWindow2
from window_3 import UiWindow3
client = Client()


class Win3(QtWidgets.QMainWindow):
    def __init__(self):

        super(Win3, self).__init__()
        self.ui = UiWindow3()
        self.ui.setupUi(self)


class Win2(QtWidgets.QMainWindow):
    def __init__(self):
        super(Win2, self).__init__()
        self.ui = UiWindow2()
        self.ui.setupUi(self)
        global client
        response = client.start_guessing()
        self.ui.label_2.setText(response["new_tag"]["question"])
        self.ui.pushButton1.clicked.connect(lambda: self.change_text("yes"))
        self.ui.pushButton_2.clicked.connect(lambda: self.change_text("no"))
        self.ui.pushButton_4.clicked.connect(lambda: self.change_text("dn"))
        self.win_3 = Win3()
        self.ui.pushButton_3.clicked.connect(self.swicth_window)

    def swicth_window(self):
        self.close()

        self.win_3.show()

    def change_text(self, answer):
        global client
        response = client.answer(answer)
        self.ui.label_2.setText(response["new_tag"]["question"])
        self.ui.label_4.setText(f"Games count: {response['games_count']}")

    def get_games(self):
        print(client.get_current_games())

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
