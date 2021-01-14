from PyQt5 import  QtCore, QtGui, QtWidgets
from modules.mylabel import MyLabel


class Widget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.setFocusPolicy(QtCore.Qt.StrongFocus)