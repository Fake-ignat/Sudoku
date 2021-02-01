from PyQt5 import QtCore, QtGui, QtWidgets, QtPrintSupport
import re
from modules.widget import Widget
from modules.previewdialog import Previewdialog

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
            ],
            "copy": [
                "К&опировать",
                self.onCopyData,
                QtCore.Qt.CTRL + QtCore.Qt.Key_C,
                "Копирование головоломки в буфер обмена",
                QtGui.QIcon('..\\images\\copy.png')
            ],
            "compact_copy": [
                "&Копировать компактно",
                self.onCopyDataMini,
                None,
                "Копирование в компактном формате"
            ],
            "copy_excel": [
                "Копировать &для Excel",
                self.onCopyDataExcel,
                None,
                "Копирование в формате MS Excel"
            ],
            "paste": [
                "&Вставить",
                self.onPasteData,
                QtCore.Qt.CTRL + QtCore.Qt.Key_V,
                "Вставка головоломки из буфера обмена",
                QtGui.QIcon('..\\images\\paste.png')
            ],
            "paste_excel": [
                "Вставить &из Excel",
                self.onPasteDataExcel,
                None,
                "Вставка головоломки из MS Excel"
            ],
            "open": [
                "&Открыть...",
                self.onOpenFile,
                QtCore.Qt.CTRL + QtCore.Qt.Key_O,
                "Загрузка головоломки из файла",
                QtGui.QIcon('..\\images\\open.png')
            ],
            "save": [
                "Со&хранить...",
                self.onSave,
                QtCore.Qt.CTRL + QtCore.Qt.Key_S,
                "Сохранение головоломки в файле",
                QtGui.QIcon('..\\images\\save.png')
            ],
            "save_mini": [
                "&Сохранить компактно...",
                self.onSave,
                None,
                "Сохранение головоломки в компактном формате"
            ],
            "print": [
                "&Печать...",
                self.onPrint,
                QtCore.Qt.CTRL + QtCore.Qt.Key_P,
                "Печать головоломки",
                QtGui.QIcon('..\\images\\print.png')
            ],
            "preview": [
                "П&редварительный просмотр...",
                self.onPreview,
                None,
                "Печать головоломки",
                QtGui.QIcon('..\\images\\preview.png')
            ],
            "page_setup": [
                "П&араметры страницы...",
                self.onPageSetup,
                None,
                "Задание параметров страницы",
            ]
        }

        myMenuFile = menuBar.addMenu("&Файл")

        action = add_menu_action(myMenuFile, *menu_actions["new"])
        toolBar.addAction(action)

        action = add_menu_action(myMenuFile, *menu_actions["open"])
        toolBar.addAction(action)

        action = add_menu_action(myMenuFile, *menu_actions["save"])
        toolBar.addAction(action)

        add_menu_action(myMenuFile, *menu_actions["save_mini"])

        action = add_menu_action(myMenuFile, *menu_actions["print"])
        toolBar.addAction(action)

        action = add_menu_action(myMenuFile, *menu_actions["preview"])
        toolBar.addAction(action)

        add_menu_action(myMenuFile, *menu_actions["page_setup"])

        # ----------------------------------------------
        myMenuFile.addSeparator()
        toolBar.addSeparator()

        add_menu_action(myMenuFile, *menu_actions["exit"])

        myMenuEdit = menuBar.addMenu("&Правка")

        action = add_menu_action(myMenuEdit, *menu_actions["copy"])
        toolBar.addAction(action)
        add_menu_action(myMenuEdit, *menu_actions["compact_copy"])
        add_menu_action(myMenuEdit, *menu_actions["copy_excel"])
        action = add_menu_action(myMenuEdit, *menu_actions["paste"])
        toolBar.addAction(action)
        add_menu_action(myMenuEdit, *menu_actions["paste_excel"])

        # ----------------------------------------------
        myMenuEdit.addSeparator()
        toolBar.addSeparator()

        add_menu_action(myMenuEdit, *menu_actions["lock"])

        action = add_menu_action(myMenuEdit, *menu_actions["lock_all"])
        toolBar.addAction(action)

        add_menu_action(myMenuEdit, *menu_actions["unlock"])
        action = add_menu_action(myMenuEdit, *menu_actions["unlock_all"])
        toolBar.addAction(action)

        myMenuAbout = menuBar.addMenu("&Справка")
        add_menu_action(myMenuAbout, *menu_actions["about_program"])
        add_menu_action(myMenuAbout, *menu_actions["about_Qt"])

        # ----------------------------------------------
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

    def onCopyData(self):
        state = self.sudoku.getDataAllCells()
        QtWidgets.QApplication.clipboard().setText(state)

    def onCopyDataMini(self):
        state = self.sudoku.getDataAllCellsMini()
        QtWidgets.QApplication.clipboard().setText(state)

    def onCopyDataExcel(self):
        state = self.sudoku.getDataAllCellExcel()
        QtWidgets.QApplication.clipboard().setText(state)

    def onPasteData(self):
        data = QtWidgets.QApplication.clipboard().text()
        if data:
            if len(data) == 81 or len(data) == 162:
                r = re.compile(r'[^0-9]')
                if not r.match(data):
                    self.sudoku.setDataAllCells(data)
                    return
        self.dataErrorMsg()

    def onPasteDataExcel(self):
        data = QtWidgets.QApplication.clipboard().text()
        if data:
            data = data.replace('\r', '')
            r = re.compile(r'([0-9]?[\t\n]){81}')
            if r.match(data):
                result = []
                if data[-1] == '\n':
                    data = data[:-1]
                lines = data.split('\n')
                for line in lines:
                    cells_state = line.split('\t')
                    for cell_state in cells_state:
                        if len(cell_state) == 0:
                            result.append('00')
                        else:
                            result.append('0' + cell_state[0])
                data = ''.join(result)
                self.sudoku.setDataAllCells(data)
                return
        self.dataErrorMsg()

    def dataErrorMsg(self):
        QtWidgets.QMessageBox.information(self, 'Судоку',
                                          'Данные имеют неправильный формат')

    def onOpenFile(self):
        filename = QtWidgets.QFileDialog.getOpenFileName(
            self, "Выберите файл", QtCore.QDir.homePath(), "Судоку (*.svd)"
        )[0]
        if filename:
            data = ''
            try:
                with open(filename, newline='') as f:
                    data = f.read()
            except:
                QtWidgets.QMessageBox.information(self, "Судоку",
                                                  "Не удалось открыть файл")
                return
            if len(data) > 2:
                if data[-1] == '\n':
                    data = data[:-1]
                if len(data) in (81, 162):
                    r = re.compile(r'[^0-9]')
                    if not  r.match(data):
                        self.sudoku.setDataAllCells(data)
                        return
            self.dataErrorMsg()

    def onSave(self):
        self.saveSVDFile(self.sudoku.getDataAllCells())

    def onSaveMini(self):
        self.saveSVDFile(self.sudoku.getDataAllCellsMini())

    def saveSVDFile(self, data):
        filename = QtWidgets.QFileDialog.getSaveFileName(
            self, "Выберите файл", QtCore.QDir.homePath(), "Судоку (*.svd)"
        )[0]
        if filename:
            try:
                with open(filename, mode='w', newline='') as f:
                     f.write(data)
                self.statusBar().showMessage("Файл сохранен", 10000)
            except:
                QtWidgets.QMessageBox.information(self, "Судоку",
                                                  "Не удалось сохранить файл")

    def onPrint(self):
        pd = QtPrintSupport.QPrintDialog(self.printer, parent=self)
        pd.setOptions(QtPrintSupport.QAbstractPrintDialog.PrintToFile |
                      QtPrintSupport.QAbstractPrintDialog.PrintSelection)
        if pd.exec() == QtWidgets.QDialog.Accepted:
            self.sudoku.print(self.printer)

    def onPreview(self):
        pd = Previewdialog(self)
        pd.exec()

    def onPageSetup(self):
        pd = QtPrintSupport.QPageSetupDialog(self.printer, parent=self)
        pd.exec()



def add_menu_action(menu_item, title, listener, key, status_tip, icon=None):
    if icon:
        if key:
            action = menu_item.addAction(icon, title, listener, key)
        else:
            action = menu_item.addAction(icon, title, listener)
    else:
        if key:
            action = menu_item.addAction(title, listener, key)
        else:
            action = menu_item.addAction(title, listener)

    action.setStatusTip(status_tip)
    return action


