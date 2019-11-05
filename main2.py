### PROVO A MANDARE SOLO LA DATA DI OGGI, IL RESTO LO LASCIO FARE AL MODELLO

from PyQt5 import QtWidgets, QtCore, QtGui
import sys
from traceback import format_exc as fex


class Mytable(QtWidgets.QTableView):
    resized = QtCore.pyqtSignal()
    cellClickedMyTable = QtCore.pyqtSignal(QtCore.QDate)
    def __init__(self,parent=None):
        super(Mytable, self).__init__(parent)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.setSizePolicy(sizePolicy)
        self.verticalHeader().setVisible(False)
        self.resized.connect(self.resizing)
        self.horizontalHeader().setDefaultSectionSize(500)
        self.horizontalHeader().setMinimumHeight(30)
        font = QtGui.QFont('Arial', 20)
        font2 = QtGui.QFont('Arial', 17)
        self.horizontalHeader().setFont(font2)
        self.setFont(font)
        self.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectItems)
        # self.doubleClicked.connect(self.dClick)
        self.clicked.connect(self.dClick)

    def dClick(self,ind):
        data = self.model().date[ind.row()][ind.column()]
        self.cellClickedMyTable.emit(data)
        return data


                # return self.mouseDoubleClickEvent(e)
        # self.setStyleSheet("""QHeaderView::section::middle { background-color:lightGray; border-left:1px solid black;}
        # QHeaderView::section::first { background-color:lightGray; border:0px;}""")

#         self.setStyleSheet("""QHeaderView::section {
#     background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,
#                                       stop:0 #616161, stop: 0.5 #505050,
#                                       stop: 0.6 #434343, stop:1 #656565);
#     color: white;
#     border: 1px solid #6c6c6c;
# }""")

    def resizing(self):
        try:
            colWid = int(self.parent().size().width() / 7)-4
            self.horizontalHeader().setDefaultSectionSize(colWid)
            self.verticalHeader().setDefaultSectionSize(colWid)
            self.verticalHeader().count()
            self.resize(QtCore.QSize(colWid*7+3, colWid*6+34))

        except:
            print(fex())

        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.verticalHeader().setSizePolicy(sizePolicy)
    def resizeEvent(self, event):
        self.resized.emit()
        return super(Mytable, self).resizeEvent(event)


class MyWid(QtWidgets.QWidget):
    def __init__(self,parent=None):
        super(MyWid, self).__init__(parent)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.setSizePolicy(sizePolicy)


class MyDialog(QtWidgets.QDialog):
    def __init__(self,parent=None):
        super(MyDialog, self).__init__(parent)
        self.setWindowTitle('TableView v 0.1')
        self.setMinimumSize(QtCore.QSize(int(680*1.5), int(600*1.5)))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        sizePolicy.setWidthForHeight(self.sizePolicy().hasWidthForHeight())
        self.setSizePolicy(sizePolicy)

class MyModel(QtCore.QAbstractTableModel):
    def __init__(self, oggi=None, parent=None):
        super(MyModel, self).__init__(parent)
        if oggi is None:
            oggi = QtCore.QDate().currentDate()
        self._oggi = oggi
        # self.date = GiorniDelMese.sendList(self._oggi)
        self.date = GiorniDelMese.sendList(self._oggi)
        self.currentDate = self.setCurrentDate(oggi)


    def getCurrentSelected(self, index):
        pass


    def setCurrentDate(self,dato: QtCore.QDate = ...) -> QtCore.QDate:
        self.currentDate = dato
        return  self.currentDate

    def data(self, index: QtCore.QModelIndex, role: int = ...):
        try:

            row = index.row()
            col = index.column()
            dato = self.date[col][row].day()
            if role == QtCore.Qt.DisplayRole:
               return dato

            elif role == QtCore.Qt.TextAlignmentRole:
               # return QtCore.Qt.AlignHCenter | QtCore.Qt.AlignBottom
               return QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter

        except:
            print(fex())

    def flags(self, index: QtCore.QModelIndex):
        try:
            if index.isValid():
                return QtCore.Qt.ItemFlags() | QtCore.Qt.ItemIsEnabled
        except:
            print(fex())

    def rowCount(self, parent: QtCore.QModelIndex = ...) -> int:
        return 6

    def columnCount(self, parent: QtCore.QModelIndex = ...) -> int:
        return 7

    def headerData(self, section: int, orientation: QtCore.Qt.Orientation, role: int = ...):
        try:
            giorno = self.date[0][section]
            nomeGiorno = giorno.shortDayName(giorno.dayOfWeek())
        except IndexError:
            nomeGiorno = QtCore.QDate().shortDayName(7)

        weekEnd = [QtCore.QDate().shortDayName(6), QtCore.QDate().shortDayName(7)]
        if role == QtCore.Qt.DisplayRole:
            if orientation == QtCore.Qt.Horizontal:
                return nomeGiorno

        if role == QtCore.Qt.ForegroundRole:
            if nomeGiorno in weekEnd:

                return QtGui.QColor(QtCore.Qt.red)

        if role == QtCore.Qt.BackgroundRole: # necessario   CAMBIARE QAPPLICATION.SETSTYLE("FUSION")
            color = QtGui.QColor('darkGray')
            brush = QtGui.QBrush(color)
            return brush


class GiorniDelMese(QtCore.QObject):
    def __init__(self,data:QtCore.QDate):
        super(GiorniDelMese, self).__init__()
        self.dataDaLavorare = data

    @staticmethod
    def sendList(dataDaLavorare) -> list:
        """ la lista deve essere [ [] ]
            la tabella sempre piena, quindi rows = 6 ; cols = 7
            il primo giorno deve essere un lunedì"""
        rows = 6
        cols = 7
        primoDelMese = QtCore.QDate(dataDaLavorare.year(), dataDaLavorare.month(), 1)
        lun = GiorniDelMese.iLunedi(primoDelMese)[0]
        corrente = lun
        listaGiorni = []
        for c in range(cols):
            listaGiorni.append([])
            for r in range(rows):
                listaGiorni[c].append(corrente)
                corrente = corrente.addDays(1)
        return listaGiorni

    @staticmethod
    def sendList_old(dataDaLavorare) -> list:
        giorniLista = [d for d in dataDaLavorare.daysInMont()]
        return giorniLista

    @staticmethod
    def sendDict_old(dataDaLavorare) -> dict:
        tot = dataDaLavorare.daysInMonth()
        giorniLista = [d for d in range(1,tot+1)]
        def colDict(lista=[]):
            """deve ritornare un dizionario"""
            listaCopiata = lista.copy()
            listaTemp = []
            diz = {}
            while len(listaCopiata):
                try:
                    listaTroncata = listaCopiata[:7]
                    for x in listaTroncata:
                        ind = listaCopiata.index(x)
                        if x not in listaTemp:
                            estratto = listaCopiata.pop(ind)
                            chiave = estratto % 7
                            if chiave == 0:
                                chiave = 7
                            if chiave not in diz.keys():
                                diz[chiave] = []
                            listaTemp.append(estratto)
                            diz[chiave].append(estratto)
                except:
                    print(fex())
            return diz
        return colDict(giorniLista)

    @staticmethod
    def sendDict(dataDaLavorare) -> dict:
        def getQDate(giorno):
            return QtCore.QDate(dataDaLavorare.year(), dataDaLavorare.month(), giorno)
        tot = dataDaLavorare.daysInMonth()
        giorniLista = [getQDate(d) for d in range(1, tot + 1)]

        def colDict(lista=[]):
            """deve ritornare un dizionario"""
            listaCopiata = lista.copy()
            listaTemp = []
            diz = {}
            while len(listaCopiata):
                try:
                    listaTroncata = listaCopiata[:7]
                    for x in listaTroncata:
                        ind = listaCopiata.index(x)
                        if x not in listaTemp:
                            estratto = listaCopiata.pop(ind)
                            estrattoInt = estratto.day()
                            chiave = estrattoInt % 7
                            if chiave == 0:
                                chiave = 7
                            if chiave not in diz.keys():
                                diz[chiave] = []
                            listaTemp.append(estratto)
                            diz[chiave].append(estratto)

                except:
                    print(fex())
            return diz

        return colDict(giorniLista)

    @staticmethod
    def iLunedi(oggi):
        dayWeek = oggi.dayOfWeek()
        if dayWeek > 1:
            indietro = dayWeek - 1
            lunediPrec = oggi.addDays(-indietro)
        else:
            lunediPrec = oggi
        lunediSucc = lunediPrec.addDays(7)

        return (lunediPrec, lunediSucc,)

class Main(MyDialog):
    cellClicked = QtCore.pyqtSignal(QtCore.QDate)


    def __init__(self,parent=None):
        super(Main, self).__init__(parent)
        self.tableView = Mytable(self)
        self.settaData()
        hBox1 = QtWidgets.QHBoxLayout()
        hBox1.addWidget(self.tableView)
        self.setLayout(hBox1)
        self.modellogiorni(self.oggi)
        self.tableView.cellClickedMyTable.connect(lambda x:self.cellClicked.emit(x))

    def settaData(self,data=QtCore.QDate().currentDate()) -> QtCore.QDate():
        d = QtCore.QDate().currentDate()
        d.daysInMonth()
        self.oggi = data
        return self.oggi

    def mese(self, dt: QtCore.QDate = ...) -> int:
        return dt.month()

    def modellogiorni(self, oggi):
        lista = GiorniDelMese.sendList(oggi)
        dati = GiorniDelMese.sendDict(oggi)
        try:
            model = MyModel(oggi=oggi, parent=self)
            self.tableView.setModel(model)
        except:
            print(fex())

    def modelloOggi(self):
        return MyModel(oggi=self.oggi, parent=self)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('fusion')
    ui = Main()
    ui.show()

    sys.exit(app.exec_())