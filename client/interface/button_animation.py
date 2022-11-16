"""
Теперь Иван главный дизайнер
"""

# from PyQt5.QtWidgets import QPushButton, QLabel, QGraphicsOpacityEffect
# from PyQt5.QtCore import QPropertyAnimation, QEasingCurve, QMargins
# from pyqt5_plugins.examplebutton import QtWidgets
#
#
# class JumpButton(QPushButton):
#     def __init__(self, *args, **kwargs):
#         QPushButton.__init__(self, *args, **kwargs)
#         self.marginsAnim = QPropertyAnimation(self, b'geometry')
#         self.marginsAnim.setDuration(150)
#         self.marginsAnim.setEasingCurve(QEasingCurve.OutElastic)
#
#     def enterEvent(self, event):
#         self.marginsAnim.setDirection(self.marginsAnim.Forward)
#         if self.marginsAnim.state() == self.marginsAnim.State.Stopped:
#             rect = self.geometry()
#             self.marginsAnim.setStartValue(rect)
#             rect += QMargins(10,10,10,10)
#             self.marginsAnim.setEndValue(rect)
#             self.marginsAnim.start()
#         QPushButton.enterEvent(self, event)
#
#     def leaveEvent(self, event):
#         self.marginsAnim.setDirection(self.marginsAnim.Backward)
#         if self.marginsAnim.state() == self.marginsAnim.State.Stopped: self.marginsAnim.start()
#         QPushButton.leaveEvent(self, event)
#
# # class TextOpacity(QLabel):
# #     def __init__(self, *args, **kwargs):
# #         QLabel.__init__(self, *args, **kwargs)
# #         self.eff = QGraphicsOpacityEffect()
# #         self.eff.setOpacity(0.0)
# #         self.animation = QPropertyAnimation(self.eff, b'opacity')
# #         self.animation.setDuration(4000)
# #
# #     def enterEvent(self, event):
# #         self.animation.setStartValue(0)
# #         self.animation.setEndValue(1)
# #         self.animation.setGraphicsEffect(self.eff)
# #         self.animation.start()
# #
# #         QLabel.enterEvent(self, event)
#
