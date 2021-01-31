from PyQt5 import QtCore, QtGui, QtWidgets
from modules.mylabel import MyLabel
from utils import isNotValidId, makeValid

frameColor = '#9AA6A7'
idColor = (3, 4, 5, 12, 13, 14, 21, 22, 23, 27, 28, 29, 36, 37, 38, 45, 46, 47,
           33, 34, 35, 42, 43, 44, 51, 52, 53, 57, 58, 59, 66, 67, 68, 75, 76, 77)


class Widget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.setFocusPolicy(QtCore.Qt.StrongFocus)

        vBoxMain = QtWidgets.QVBoxLayout()
        frame1 = QtWidgets.QFrame()
        frame1.setStyleSheet(
            f'background-color:{frameColor};'
            f'border:1px solid {frameColor};'
        )

        grid = QtWidgets.QGridLayout()
        grid.setSpacing(0)

        self.cells = self.createCells(81)
        self.cells[0].setCellFocus()
        self.idCellInFocus = 0

        i = 0
        for j in range(0, 9):
            for k in range(0, 9):
                grid.addWidget(self.cells[i], j, k)
                i += 1

        for cell in self.cells:
            cell.changeCellFocus.connect(self.onChangeCellFocus)

        frame1.setLayout(grid)
        vBoxMain.addWidget(frame1, alignment=QtCore.Qt.AlignHCenter)

        frame2 = QtWidgets.QFrame()
        frame2.setFixedSize(272, 36)

        hbox = QtWidgets.QHBoxLayout()
        hbox.setSpacing(1)

        btns = self.createButtons(9)
        for btn in btns:
            hbox.addWidget(btn)

        btns[0].clicked.connect(self.onBtn1Clicked)
        btns[1].clicked.connect(self.onBtn2Clicked)
        btns[2].clicked.connect(self.onBtn3Clicked)
        btns[3].clicked.connect(self.onBtn4Clicked)
        btns[4].clicked.connect(self.onBtn5Clicked)
        btns[5].clicked.connect(self.onBtn6Clicked)
        btns[6].clicked.connect(self.onBtn7Clicked)
        btns[7].clicked.connect(self.onBtn8Clicked)
        btns[8].clicked.connect(self.onBtn9Clicked)
        btns[9].clicked.connect(self.onBtnXClicked)

        frame2.setLayout(hbox)
        vBoxMain.addWidget(frame2, alignment=QtCore.Qt.AlignHCenter)

        self.setLayout(vBoxMain)

    def onChangeCellFocus(self, id):
        if self.idCellInFocus != id and not isNotValidId(id):
            self.cells[self.idCellInFocus].clearCellFocus()
            self.idCellInFocus = id
            self.cells[id].setCellFocus()

    def createCells(self, amount):
        return [MyLabel(i,
                        MyLabel.colorGrey if i in idColor
                        else MyLabel.colorOrange)
                for i in range(amount)]

    def createButtons(self, amount):
        btns = []
        for i in range(amount):
            btn = QtWidgets.QPushButton(str(i+1))
            btn.setFixedSize(27, 27)
            btn.setFocusPolicy(QtCore.Qt.NoFocus)
            btns.append(btn)

        btn = QtWidgets.QPushButton("X")
        btn.setFixedSize(27, 27)
        btns.append(btn)

        return btns

    def keyPressEvent(self, evt):
        key = evt.key()
        if key == QtCore.Qt.Key_Up:
            tid = self.idCellInFocus - 9
            makeValid(tid)
            self.onChangeCellFocus(tid)
        elif key == QtCore.Qt.Key_Right:
            tid = self.idCellInFocus + 1
            makeValid(tid)
            self.onChangeCellFocus(tid)
        elif key == QtCore.Qt.Key_Down:
            tid = self.idCellInFocus + 9
            makeValid(tid)
            self.onChangeCellFocus(tid)
        elif key == QtCore.Qt.Key_Left:
            tid = self.idCellInFocus - 1
            makeValid(tid)
            self.onChangeCellFocus(tid)
        elif QtCore.Qt.Key_1 <= key <= QtCore.Qt.Key_9:
            self.cells[self.idCellInFocus].setNewText(chr(key))
        elif key in [QtCore.Qt.Key_Backspace, QtCore.Qt.Key_Space, QtCore.Qt.Key_Delete]:
            self.cells[self.idCellInFocus].setNewText("")
        QtWidgets.QWidget.keyPressEvent(self, evt)

    for x in range(1, 10):
        ex_string = f'def onBtn{x}Clicked(self): self.cells[self.idCellInFocus].setNewText("{x}")'
        exec(ex_string)



    def onBtnXClicked(self):
        self.cells[self.idCellInFocus].setNewText("")

    def onClearAllCells(self):
        for cell in self.cells:
            cell.setText("")
            cell.clearCellBlock()

    def onBlockCell(self):
        cell = self.cells[self.idCellInFocus]
        if not cell.text():
            QtWidgets.QMessageBox.information(self, "Судоку",
                                              "Нельзя блокировать пустую ячейку")
        else:
            if cell.isCellChange:
                cell.setCellBlock()

    def onBlockCells(self):
        for cell in self.cells:
            if cell.text() and cell.isCellChange:
                cell.setCellBlock()

    def onClearBlockCell(self):
        cell = self.cells[self.idCellInFocus]
        if not cell.isCellChange:
            cell.clearCellBlock()

    def onClearBlockCells(self):
        for cell in self.cells:
            if not cell.isCellChange:
                cell.clearCellBlock()

    def getDataAllCells(self):
        listAllData = []
        for cell in self.cells:
            listAllData.append('0' if cell.isCellChange else '1')
            s = cell.text()
            listAllData.append(s if len(s) == 1 else '0')
        return ''.join(listAllData)

    def getDataAllCellsMini(self):
        listAllData = []
        for cell in self.cells:
            s = cell.text()
            listAllData.append(s if len(s) == 1 else '0')
        return ''.join(listAllData)

    def getDataAllCellExcel(self):
        numbers = (9, 18, 27, 36, 45, 54, 63, 72)
        listAllData = [self.cells[0].text()]
        for i in range(1, 81):
            listAllData.append('\r\n' if i in numbers else '\t')
            listAllData.append(self.cells[i].text())
        listAllData.append('\r\n')
        return ''.join(listAllData)

    def setDataAllCells(self, data):
        size = len(data)
        if size == 81:
            for i in range(81):
                if data[i] == '0':
                    self.cells[i].setText('')
                    self.cells[i].clearCellBlock()
                else:
                    self.cells[i].setText(data[i])
                    self.cells[i].setCellBlock()
            self.onChangeCellFocus(0)
        elif size == 162:
            for i in range(0, 162, 2):
                id = i // 2
                if data[i] == '0':
                    self.cells[id].clearCellBlock()
                else:
                    self.cells[id].setCellBlock()
                self.cells[id].setText('' if data[i + 1] == '0' else data[i+1])
            self.onChangeCellFocus(0)

    def print(self, printer):
        penText = QtGui.QPen(QtGui.QColor(MyLabel.colorBlack), 1)
        penBorder = QtGui.QPen(QtGui.QColor(QtCore.Qt.darkGray), 1)
        brushOrange = QtGui.QBrush(QtGui.QColor(MyLabel.colorOrange))
        brushGrey = QtGui.QBrush(QtGui.QColor(MyLabel.colorGrey))

        painter = QtGui.QPainter()
        painter.begin(printer)

        painter.setFont(QtGui.QFont('Veranda', pointSize=14))
        i = 0
        for j in range(0, 9):
            for k in range(0, 9):
                x = j * 30
                y = k * 30
                target = self.cells[i]
                painter.setPen(penBorder)
                painter.setBrush(brushGrey if
                                 target.bgColorDefault == MyLabel.colorGrey
                                 else brushOrange)
                painter.drawRect(x, y, 30, 30)
                painter.setPen(penText)
                painter.drawText(x, y, 30, 30, QtCore.Qt.AlignCenter,
                                 target.text())
                i += 1
        painter.end()



