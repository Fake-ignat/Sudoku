from PyQt5 import QtCore, QtGui, QtWidgets, QtPrintSupport
from modules.widget import Widget

qpushbutton_style = 'font-size:10pt; font-family:Verdana; color:black;font-weight:bold;'
mylabel_style = 'font-size:14pt; font-family:Verdana; border:1px solid #9AA6A7;'


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent,
                                       flags=QtCore.Qt.Window |
                                       QtCore.Qt.MSWindowsFixedSizeDialogHint)
        self.setWindowTitle('Судоку 2.0.0')

        self.setStyleSheet(
            f"QFrame QPushButton {qpushbutton_style}"
            f"MyLabel {mylabel_style}"
        )

        self.settings = QtCore.QSettings('Прохоренок и Дронов', "Судоку")
        self.printer = QtPrintSupport.QPrinter()

        self.sudoku = Widget()
        self.setCentralWidget(self.sudoku)

        menuBar = self.menuBar()
        toolBar = QtWidgets.QToolBar()
        myMenuFile = menuBar.addMenu("&Файл")
        action = myMenuFile.addAction(QtGui.QIcon(r'images/new.png'),
                                      "&Новый", self.sudoku.onClearAllCells,
                                      QtCore.Qt.CTRL + QtCore.Qt.Key_N)
        toolBar.addAction(action)
        toolBar.addSeparator()
        action = myMenuFile.addAction("&Выход", QtWidgets.qApp.quit,
                                      QtCore.Qt.CTRL + QtCore.Qt.Key_Q)
        action.setStatusTip("Завершение работы приложения")

        # page 769
