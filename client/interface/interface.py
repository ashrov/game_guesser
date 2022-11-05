# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/Users/sliwmen/Desktop/SPPR.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.Qt import *


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(0, 0, 800, 600))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap("res/sppr_win_main_without_text.png"))
        self.label.setScaledContents(True)
        self.label.setObjectName("label")
        self.Start = QtWidgets.QPushButton(self.centralwidget)
        self.Start.setGeometry(QtCore.QRect(700, 530, 151, 81))
        font = QtGui.QFont()
        font.setFamily("Apple SD Gothic Neo")
        font.setPointSize(24)
        font.setBold(False)
        font.setWeight(50)
        self.Start.setFont(font)
        self.Start.setStyleSheet("QPushButton {\n"
                                 "    background-color: rgb(255, 128, 90);\n"
                                 "    color: rgb(255, 255, 255);\n"
                                 "    border-radius: 17px;\n"
                                 "    padding-left: -45px;\n"
                                 "    padding-top: -0px;\n"
                                 "    outline: none;\n"
                                 "}\n"
                                 "\n"
                                 "QPushButton:hover {\n"
                                 "    \n"
                                 "    \n"
                                 "    background-color: rgb(255, 175, 130);\n"
                                 "}    ")
        self.Start.setObjectName("Start")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(-80, 190, 550, 550))
        self.label_2.setText("")
        self.label_2.setPixmap(QtGui.QPixmap(
            "res/human.png"))
        self.label_2.setScaledContents(True)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(0, 140, 801, 141))
        font = QtGui.QFont()
        font.setFamily("Apple SD Gothic Neo")
        font.setPointSize(30)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setStyleSheet("color: rgb(255, 255, 255);\n"
                                   "font: 81 30pt \"Apple SD Gothic Neo\";\n"
                                   "font-weight: bold;\n"
                                   "text-align: center;")
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(0, 170, 801, 141))
        font = QtGui.QFont()
        font.setFamily("Apple SD Gothic Neo")
        font.setPointSize(23)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(10)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color: rgba(255, 255, 255, 0.5);\n"
                                   "font: 81 23pt \"Apple SD Gothic Neo\";\n"
                                   "font-weight: light;\n"
                                   "text-align: center;\n"
                                   "")
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName("label_4")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.eff = QGraphicsOpacityEffect()
        self.eff.setOpacity(0.0)
        self.label_4.setGraphicsEffect(self.eff)

        self.Start.setCheckable(True)

        self.animation = QPropertyAnimation(self.eff, b'opacity')

        self.animation.setDuration(3500)

        self.animation.setStartValue(0)
        self.animation.setEndValue(1)

        self.animation.start()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.Start.setText(_translate("MainWindow", "Start"))
        self.label_3.setText(_translate("MainWindow", "Fucking Bullshit"))
        self.label_4.setText(_translate("MainWindow", "we will help you choose a game"))


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())