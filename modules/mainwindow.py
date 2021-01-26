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

        menu_actions = {
            "new": [
                "&Новый",
                self.sudoku.onClearAllCells,
                QtCore.Qt.CTRL + QtCore.Qt.Key_N,
                "Создание новой, пустой головоломки",
                QtGui.QIcon('..\\images\\new.png')
            ],
            "exit": [
                "&Выход",
                QtWidgets.qApp.quit,
                QtCore.Qt.CTRL + QtCore.Qt.Key_Q,
                "Завершение работы приложения"
            ],
            "lock": [
                "&Блокировать",
                self.sudoku.onBlockCell,
                QtCore.Qt.Key_F2,
                "Блокирование активной ячейки"
            ],
            "lock_all": [
                "Б&локировать все",
                self.sudoku.onBlockCells,
                QtCore.Qt.Key_F3,
                "Блокирование всех ячеек",
                QtGui.QIcon('..\\images\\lock.png')
            ],
            "unlock": [
                "&Разблокировать",
                self.sudoku.onClearBlockCell,
                QtCore.Qt.Key_F4,
                "Разблокирование активной ячейки"
            ],
            "unlock_all": [
                "Р&азблокировать все",
                self.sudoku.onClearBlockCells,
                QtCore.Qt.Key_F5,
                "Разблокирование всех ячеек",
                QtGui.QIcon('..\\images\\unlock.png')
            ],
            "about_program": [
                "О &программе...",
                self.aboutInfo,
                None,
                "Получение сведений о приложении",
            ],
            "about_Qt": [
                "О &Qt...",
                QtWidgets.qApp.aboutQt,
                None,
                "Получение сведений о библиотеке Qt",
            ]
        }

        myMenuFile = menuBar.addMenu("&Файл")
        action = add_menu_action(myMenuFile, *menu_actions["new"])
        toolBar.addAction(action)

        myMenuFile.addSeparator()
        toolBar.addSeparator()

        add_menu_action(myMenuFile, *menu_actions["exit"])

        myMenuEdit = menuBar.addMenu("&Правка")

        add_menu_action(myMenuEdit, *menu_actions["lock"])
        action = add_menu_action(myMenuEdit, *menu_actions["lock_all"])
        toolBar.addAction(action)

        add_menu_action(myMenuEdit, *menu_actions["unlock"])
        action = add_menu_action(myMenuEdit, *menu_actions["unlock_all"])
        toolBar.addAction(action)

        myMenuAbout = menuBar.addMenu("&Справка")
        add_menu_action(myMenuAbout, *menu_actions["about_program"])
        add_menu_action(myMenuAbout, *menu_actions["about_Qt"])

        toolBar.setMovable(False)
        toolBar.setFloatable(False)
        self.addToolBar(toolBar)

        statusBar = self.statusBar()
        statusBar.setSizeGripEnabled(False)
        statusBar.showMessage("\"Судоку\" приветствует вас", 20000)

        if self.settings.contains("X") and self.settings.contains("Y"):
            self.move(self.settings.value("X"), self.settings.value("Y"))

    def closeEvent(self, event):
        g = self.geometry()
        self.settings.setValue("X", g.left())
        self.settings.setValue("Y", g.top())

    def aboutInfo(self):
        QtWidgets.QMessageBox.about(self, "О программе",
                                    "<center>\"Судоку\" v2.0.0<br><br>"
                                    "Программа для просмотра и редактирования судоку<br><br>")


def add_menu_action(menu_item, title, listener, key, status_tip, icon=None):
    if icon:
        action = menu_item.addAction(icon, title, listener, key)
    else:
        if key:
            action = menu_item.addAction(title, listener, key)
        else:
            action = menu_item.addAction(title, listener)

    action.setStatusTip(status_tip)
    return action
