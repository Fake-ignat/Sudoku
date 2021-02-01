from PyQt5 import QtCore, QtWidgets, QtPrintSupport

class Previewdialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        QtWidgets.QDialog.__init__(self, parent)
        self.setWindowTitle("Предварительный просмотр")
        self.resize(600, 400)
        vBox = QtWidgets.QVBoxLayout()
        hBox1 = QtWidgets.QHBoxLayout()

        btnZoomIn = addButton(hBox1, '&+')
        btnZoomOut = addButton(hBox1, '&-')
        btnZoomReset = addButton(hBox1, '&Сброс')

        hBox1.addStretch()
        vBox.addLayout(hBox1)

        hBox2 = QtWidgets.QHBoxLayout()
        self.ppw = QtPrintSupport.QPrintPreviewWidget(parent.printer)
        self.ppw.paintRequested.connect(parent.sudoku.print)
        hBox2.addWidget(self.ppw)

        btnZoomIn.clicked.connect(self.ppw.zoomIn)
        btnZoomOut.clicked.connect(self.ppw.zoomOut)
        btnZoomReset.clicked.connect(self.zoomReset)

        box = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.Close, QtCore.Qt.Vertical
        )
        btnClose = box.button(QtWidgets.QDialogButtonBox.Close)
        btnClose.setText('&Закрыть')
        btnClose.setFixedSize(96, 64)
        btnClose.clicked.connect(self.accept)
        hBox2.addWidget(box, alignment=QtCore.Qt.AlignRight | QtCore.Qt.AlignTop)

        vBox.addLayout(hBox2)
        self.setLayout(vBox)

        self.zoomReset()

    def zoomReset(self):
        self.ppw.setZoomFactor(1)

def addButton(hbox, name):
    btn = QtWidgets.QPushButton(name)
    btn.setFocusPolicy(QtCore.Qt.NoFocus)
    hbox.addWidget(btn, alignment=QtCore.Qt.AlignLeft)
    return btn
