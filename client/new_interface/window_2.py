# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/Users/sliwmen/Downloads/quetsions_page.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.

from client import Client
from PyQt5 import QtCore, QtGui, QtWidgets

client = Client()

message = {'intent': 'get_all_tags'}
tags = client.send_message(message)['all_tags']
questions = [question["question"] for question in tags]

class UiWindow2(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setFixedSize(1920, 1080)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(0, 0, 1920, 1080))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap("images/sppr_win_main_without_text.png"))
        self.label.setScaledContents(True)
        self.label.setObjectName("label")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(600, 650, 93, 28))
        self.pushButton.setStyleSheet("QPushButton{\n"
"    background-color: white;\n"
"}")
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(1100, 650, 93, 28))
        self.pushButton_2.setStyleSheet("QPushButton{\n"
"    background-color: white;\n"
"}")
        self.pushButton_2.setObjectName("pushButton_2")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(700, 250, 450, 100))
        self.label_2.setStyleSheet("QLabel{\n"
"    color: black;\n"
"    font: 75 8pt \"MS Shell Dlg 2\";\n"
"    background-color: white;\n"
"    border-radius: 20px;\n"
"    font-weight: bold;\n"  
"    text-align: center;\n"
"}")
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton.setText(_translate("MainWindow", "Да"))
        self.pushButton_2.setText(_translate("MainWindow", "Нет"))
        self.label_2.setText(_translate("MainWindow", questions[0]))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = UiWindow2()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())