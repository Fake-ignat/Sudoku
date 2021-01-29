from PyQt5 import QtGui, QtWidgets
import sys

from modules.mainwindow import MainWindow

app = QtWidgets.QApplication(sys.argv)
app.setWindowIcon(QtGui.QIcon('..\\images\\svd.png'))
window = MainWindow()
window.show()
sys.exit(app.exec_())


# page 782
