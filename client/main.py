import sys
import webbrowser

from PyQt5 import QtWidgets, QtCore

from client import Client
from interface.window_1 import UiWindow1
from interface.window_2 import UiWindow2
from interface.window_3 import UiWindow3


class Win3(QtWidgets.QMainWindow):
    def __init__(self, client: Client, parent_window):
        super(Win3, self).__init__()
        self.ui = UiWindow3()
        self.ui.setupUi(self)
        self.ui.listWidget.itemClicked.connect(self.handle_clicked_item)
        self.ui.pushButton.clicked.connect(self.back)

        self.client = client
        self.parent_window = parent_window

    def fill_games_list(self):
        self.ui.listWidget.clear()

        response = self.client.get_current_games()
        for game in response.get("current_games"):
            item = QtWidgets.QListWidgetItem()
            item.setText(game.get("game_name"))
            item.setData(1, game.get("steam_url"))
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.ui.listWidget.addItem(item)

    def show(self) -> None:
        self.fill_games_list()
        super().show()

    def handle_clicked_item(self, item: QtWidgets.QListWidgetItem):
        webbrowser.open(item.data(1))

    def back(self):
        self.close()
        self.parent_window.show()


class Win2(QtWidgets.QMainWindow):
    def __init__(self):
        super(Win2, self).__init__()
        self.ui = UiWindow2()
        self.ui.setupUi(self)

        self.client = Client()
        self.win_3 = Win3(self.client, self)

        self.ui.pushButton.clicked.connect(lambda: self.handle_answer("yes"))
        self.ui.pushButton_2.clicked.connect(lambda: self.handle_answer("no"))
        self.ui.pushButton_4.clicked.connect(lambda: self.handle_answer("dn"))
        self.ui.pushButton_3.clicked.connect(self.get_games)
        self.ui.pushButton_5.clicked.connect(self.restart)

        self.response = self.client.start_guessing()
        self.ui.label_2.setText(self.response["new_tag"]["question"])

    def handle_answer(self, answer):
        response = self.client.answer(answer)
        if response['games_count'] == 1:
            self.one_game_left_warning_messagebox()
        elif response['games_count'] == 0:
            self.zero_games_left_warning_messagebox()
        else:
            self.ui.label_2.setText(response["new_tag"]["question"])
            self.ui.label_4.setText(f"Games count: {response['games_count']}")

    def get_games(self):
        self.hide()
        self.win_3.show()

    def restart(self):
        self.response = self.client.start_guessing()
        self.ui.label_2.setText(self.response["new_tag"]["question"])
        self.ui.label_4.setText("Games count: ...")

    def one_game_left_warning_messagebox(self):
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Warning)

        msg.setText("Games left: 1\nDo You want to get this?")
        msg.setWindowTitle("Warning MessageBox")

        msg.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        button = msg.exec()
        if button == QtWidgets.QMessageBox.Yes:
            self.get_games()
        else:
            self.restart()

    def zero_games_left_warning_messagebox(self):
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Warning)

        msg.setText("Games left: 0\nDo You want to restart?")
        msg.setWindowTitle("Warning MessageBox")

        msg.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        button = msg.exec()
        if button == QtWidgets.QMessageBox.Yes:
            self.restart()


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
