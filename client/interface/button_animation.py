from PyQt5.QtWidgets import QPushButton
from PyQt5.QtCore import QPropertyAnimation, QEasingCurve, QMargins

class JumpButton(QPushButton):
    def __init__(self, *args, **kwargs):
        QPushButton.__init__(self, *args, **kwargs)
        self.marginsAnim = QPropertyAnimation(self, b'geometry')
        self.marginsAnim.setDuration(150)
        self.marginsAnim.setEasingCurve(QEasingCurve.OutElastic)

    def enterEvent(self,event):
        self.marginsAnim.setDirection(self.marginsAnim.Forward)
        if self.marginsAnim.state() == self.marginsAnim.State.Stopped:
            rect = self.geometry()
            self.marginsAnim.setStartValue(rect)
            rect += QMargins(10,10,10,10)
            self.marginsAnim.setEndValue(rect)
            self.marginsAnim.start()
        QPushButton.enterEvent(self, event)

    def leaveEvent(self,event):
        self.marginsAnim.setDirection(self.marginsAnim.Backward)
        if self.marginsAnim.state() == self.marginsAnim.State.Stopped: self.marginsAnim.start()
        QPushButton.leaveEvent(self, event)
