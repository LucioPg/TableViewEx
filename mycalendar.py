### PROVO A MANDARE SOLO LA DATA DI OGGI, IL RESTO LO LASCIO FARE AL MODELLO

from PyQt5 import QtWidgets, QtCore, QtGui
import sys
from traceback import format_exc as fex


class Mytable(QtWidgets.QTableView):
    resized = QtCore.pyqtSignal()
    cellClickedMyTable = QtCore.pyqtSignal(QtCore.QDate)
    whoIsComing = QtCore.pyqtSignal(QtWidgets.QWidget)
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

    def setModel(self, model: QtCore.QAbstractItemModel) -> None:
        # self.whoIsComing.emit(self)
        model.setFromList(self)
        super(Mytable, self).setModel(model)

    def update(self) -> None:
        print(self.objectName())
        self.whoIsComing.emit(self)
        super(Mytable, self).update(self)


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

    listaMesi = ['Gennaio',
                 'Febbraio',
                 'Marzo',
                 'Aprile',
                 'Maggio',
                 'Giugno',
                 'Luglio',
                 'Agosto',
                 'Settembre',
                 'Ottobre',
                 'Novembre',
                 'Dicembre']

    def __init__(self, oggi=None, parent=None):
        super(MyModel, self).__init__(parent)
        print(self.parent().objectName())
        self.roleNames()
        self.fromList = []
        if oggi is None:
            oggi = QtCore.QDate().currentDate()
        self._oggi = oggi
        # self.date = GiorniDelMese.sendList(self._oggi)
        self.date = GiorniDelMese.sendList(self._oggi)
        self.currentDate = self.setCurrentDate(oggi)



    def getCurrentSelected(self, index):
        pass

    def itsMe(self,me):
        self.me = me
        print('its me, ',me)
        return self.me

    def setFromList(self,who):
        if who not in self.fromList:
            self.fromList.append(who)
            who.whoIsComing.connect(self.itsMe)
            print(who,' added')
    def setCurrentDate(self,dato: QtCore.QDate = ...) -> QtCore.QDate:
        self.currentDate = dato
        return  self.currentDate

    def data(self, index: QtCore.QModelIndex, role: int = ...):
        try:
            row = index.row()
            col = index.column()
            # print("type parent ", type(self.fromWho))
            # for w in self.fromList:
            w = 0
            # w = self.me
            if role == QtCore.QByteArray(b'peppe'):
                pass
                # print('peppe!!!',index.isValid())
                # # mese = self.date[col][row].month()
                # mese = self.currentDate.month()
                # dato = self.listaMesi[mese]
                # print(dato.upper())
                # return dato
            # else:
            #     dato = self.date[col][row].day()

            if role == QtCore.Qt.DisplayRole:
                if col == 12:
                    mese = self.currentDate.month()
                    dato = self.listaMesi[mese-1]
                    print(dato.upper())
                    print('dato', row, col)
                else:
                    dato = self.date[row][col].day()

                return dato

            elif role == QtCore.Qt.TextAlignmentRole:

               # return QtCore.Qt.AlignHCenter | QtCore.Qt.AlignBottom
                return QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter

        # except AttributeError:
        #     pass
        # except IndexError:
        #     mese = self.currentDate.month()
        #     dato = self.listaMesi[mese]
        #     print(dato.upper())
        #     return dato
        except:
            print(fex())
            print()
            print()
            print(row,col)

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

    def lastRoleName(self) -> int:
        last = max([r for r in self.roleNames.keys()])
        return last

    def setRoleNames(self,roleName):
        last = self.lastRoleName() + QtCore.Qt.UserRole
        self.roleNames()[last] = roleName



class GiorniDelMese(QtCore.QObject):
    def __init__(self,data:QtCore.QDate):
        super(GiorniDelMese, self).__init__()
        self.dataDaLavorare = data

    @staticmethod
    def sendList(dataDaLavorare) -> list:
        """ la lista deve essere [ [] ]
            la tabella sempre piena, quindi rows = 6 ; cols = 7
            il primo giorno deve essere un lunedì"""
        rows = 7
        cols = 6
        primoDelMese = QtCore.QDate(dataDaLavorare.year(), dataDaLavorare.month(), 1)
        lun = GiorniDelMese.iLunedi(primoDelMese)[0]
        corrente = lun
        listaGiorni = []
        for c in range(cols):
            listaGiorni.append([])
            for r in range(rows):
                listaGiorni[c].append(corrente)
                corrente = corrente.addDays(1)
        print(listaGiorni)
        return listaGiorni

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

class MyCalendarCore(QtWidgets.QWidget):
    cellClicked = QtCore.pyqtSignal(QtCore.QDate)


    def __init__(self,parent=None):
        super(MyCalendarCore, self).__init__(parent)
        self.setObjectName('MyCalendarCore')
        self.setMinimumSize(QtCore.QSize(int(680 * 1.5), int(600 * 1.5)))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        sizePolicy.setWidthForHeight(self.sizePolicy().hasWidthForHeight())
        self.setSizePolicy(sizePolicy)
        self.tableView = Mytable(self)
        self.settaData()
        hBox1 = QtWidgets.QHBoxLayout()
        hBox1.addWidget(self.tableView)
        self.setLayout(hBox1)
        # self.modellogiorni(self.oggi)
        self.tableView.cellClickedMyTable.connect(lambda x:self.cellClicked.emit(x))

    def settaData(self,data=QtCore.QDate().currentDate()) -> QtCore.QDate():
        data.daysInMonth()
        self.oggi = data
        return self.oggi
    def setDataView(self, data:QtCore.QDate()= ...) -> QtCore.QDate():
        self.dataView = data
        return self.dataView

    def nextMonth(self):
        year =self.oggi.year()
        daysInMonth = self.oggi.daysInMonth()
        nextMonth = self.oggi.addDays(daysInMonth - self.oggi.day()+1)
        print(nextMonth)
        self.settaData(nextMonth)

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

    def modelloOnTheRun(self,model,dati):
        self.tableView.setModel(model(oggi=dati,parent=self))





if __name__ == '__main__':
    from combosenzafreccia import ComboSenzaFreccia
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('fusion')
    ui = QtWidgets.QDialog()
    cal = MyCalendarCore(ui)
    model = MyModel(oggi=QtCore.QDate().currentDate(), parent=ui)
    cal.tableView.setModel(model)
    combo = ComboSenzaFreccia(ui)
    # combo = QtWidgets.QComboBox(ui)
    combo.setObjectName('comboBox')
    combo.setModel(model)
    hbox = QtWidgets.QVBoxLayout()
    hbox.addWidget(combo)
    hbox.addWidget(cal)
    ui.setLayout(hbox)
    bot = QtWidgets.QPushButton('click me')
    bot.clicked.connect(cal.nextMonth)
    combo.setRole()
    ui.show()
    bot.show()
    sys.exit(app.exec_())