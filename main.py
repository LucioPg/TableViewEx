from PyQt5 import QtWidgets, QtCore, QtGui
import sys
from traceback import format_exc as fex


class Mytable(QtWidgets.QTableView):
    def __init__(self,parent=None):
        super(Mytable, self).__init__(parent)
        self.setMaximumHeight(300)
        self.setMaximumWidth(300)
        self.setMinimumHeight(300)
        self.setMinimumWidth(300)


class MyWid(QtWidgets.QWidget):
    def __init__(self,parent=None):
        super(MyWid, self).__init__(parent)
        self.setMaximumHeight(350)
        self.setMaximumWidth(350)
        self.setMinimumHeight(300)
        self.setMinimumWidth(300)

class MyDialog(QtWidgets.QDialog):
    def __init__(self,parent=None):
        super(MyDialog, self).__init__(parent)
        self.setWindowTitle('TableView v 0.1')
        self.setMaximumHeight(400)
        self.setMaximumWidth(400)
        self.setMinimumHeight(350)
        self.setMinimumWidth(350)

class Main(MyDialog):
    def __init__(self,parent=None):
        super(Main, self).__init__(parent)
        self.mainWid = MyWid(self)
        self.table = Mytable(self.mainWid)
        hBox = QtWidgets.QHBoxLayout()
        hBox.addWidget(self.mainWid)
        self.setLayout(hBox)
        hBox = QtWidgets.QHBoxLayout()
        hBox.addWidget(self.table)
        self.mainWid.setLayout(hBox)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ui = Main()
    ui.show()
    sys.exit(app.exec_())