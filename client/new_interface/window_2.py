# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\questions_page.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class UiWindow2(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(900, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(0, 0, 900, 600))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap("images/sppr_win_main_without_text.png"))
        self.label.setScaledContents(True)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(190, 130, 501, 121))
        self.label_2.setStyleSheet("QLabel{\n"
"    text-align: center;\n"
"    background-color: white;\n"
"    border-radius: 20px;\n"
"    font: 10pt \"Times New Roman\";\n"
"     font-weight: bold;"
"}")
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.pushButton1 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton1.setGeometry(QtCore.QRect(200, 440, 130, 40))
        self.pushButton1.setStyleSheet("QPushButton{\n"
"    \n"
"    \n"
"    font: 12pt \"Terminal\";\n"
"    background-color: white;\n"
"    border-radius: 10px;\n"
"\n"
"}")
        self.pushButton1.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(560, 440, 130, 40))
        self.pushButton_2.setStyleSheet("QPushButton{\n"
"    \n"
"    \n"
"    font: 12pt \"Terminal\";\n"
"    background-color: white;\n"
"    border-radius: 10px;\n"
"}")
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(760, 60, 130, 40))
        self.pushButton_3.setStyleSheet("QPushButton{\n"
"    \n"
"    \n"
"    font: 12pt \"Terminal\";\n"
"    background-color: white;\n"
"    border-radius: 10px;\n"
"}")
        self.pushButton_3.setObjectName("pushButton_3")
        # self.label_3 = QtWidgets.QLabel(self.centralwidget)
        # self.label_3.setGeometry(QtCore.QRect(-70, 170, 421, 441))
        # self.label_3.setText("")
        # self.label_3.setPixmap(QtGui.QPixmap("images/human.png"))
        # self.label_3.setScaledContents(True)
        # self.label_3.setObjectName("label_3")
        self.pushButton_4 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_4.setGeometry(QtCore.QRect(380, 490, 130, 40))
        self.pushButton_4.setStyleSheet("QPushButton{\n"
"    \n"
"    \n"
"    font: 12pt \"Terminal\";\n"
"    background-color: white;\n"
"    border-radius: 10px;\n"
"}")
        self.pushButton_4.setObjectName("pushButton_4")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(630, 10, 261, 41))
        self.label_4.setStyleSheet("QLabel{\n"
"    font: 14pt \"Terminal\";\n"
"    border-radius: 10px;\n"
"    background-color: white;\n"
"}")
        self.label_4.setScaledContents(True)
        self.label_4.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_4.setObjectName("label_4")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_2.setText(_translate("MainWindow", "Question"))
        self.pushButton1.setText(_translate("MainWindow", "Yes"))
        self.pushButton_2.setText(_translate("MainWindow", "No"))
        self.pushButton_3.setText(_translate("MainWindow", "Get games"))
        self.pushButton_4.setText(_translate("MainWindow", "Don\'t know"))
        self.label_4.setText(_translate("MainWindow", "Games found:"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = UiWindow2()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
