### PROVO A MANDARE SOLO LA DATA DI OGGI, IL RESTO LO LASCIO FARE AL MODELLO


from PyQt5 import QtWidgets, QtCore, QtGui
import sys
from collections import OrderedDict as Od
from traceback import format_exc as fex
from gui import Ui_Dialog as MyDialog2


class Mytable(QtWidgets.QTableView):
    resized = QtCore.pyqtSignal()
    def __init__(self,parent=None):
        super(Mytable, self).__init__(parent)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.setSizePolicy(sizePolicy)
        self.verticalHeader().setVisible(False)
        self.resized.connect(self.resizing)
        self.horizontalHeader().setDefaultSectionSize(5)
        # self.horizontalHeader().setStretchLastSection(True)
        # self.setMinimumSize(QtCore.QSize(600, 480))
        # self.setMaximumHeight(500)
        # self.setMaximumWidth(500)
        # self.setMinimumHeight(300)
        # self.setMinimumWidth(300)
    def resizing(self):
        # secSizeW = int(self.parent().size().width() / self.ro
        print('#########  children')

        try:
            # print(int(self.horizontalHeader().size().width()/7))
            # print(self.rowHeight(1))
            # print(self.columnWidth(1))
            # colWid = int(self.horizontalHeader().size().width() / 7)
            colWid = int(self.parent().size().width() / 7)-4
            self.horizontalHeader().setDefaultSectionSize(colWid)
            # self.horizontalHeader().setMaximumWidth(int(self.parent().size().width() / 7))
            rowH = colWid*7 - (self.horizontalHeader().height()-(self.horizontalHeader().defaultSectionSize()*2))
            # rowH = colWid*7 - (self.horizontalHeader().height()-(self.horizontalHeader().defaultSectionSize()*2))
            print('colwidth ', colWid)
            print('rowH ', rowH)
            print('horizontal header height',self.horizontalHeader().height())
            print('vertical count',self.verticalHeader().count())

            self.verticalHeader().setDefaultSectionSize(colWid)
            self.verticalHeader().count()
            self.resize(QtCore.QSize(colWid*7+2, colWid*6+25))

        except:
            print(fex())
        print('######### end children')


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
        # self.setMinimumSize(QtCore.QSize(600, 480))
        # self.setMaximumHeight(500)
        # self.setMaximumWidth(500)
        # self.setMinimumHeight(300)
        # self.setMinimumWidth(300)


class MyDialog(QtWidgets.QDialog):
    def __init__(self,parent=None):
        super(MyDialog, self).__init__(parent)
        self.setWindowTitle('TableView v 0.1')
        self.setMinimumSize(QtCore.QSize(540, 500))
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
        self.currentDate = self.setCurrentDate(oggi)





    def data(self, index: QtCore.QModelIndex, role: int = ...):
        try:
            date = GiorniDelMese.sendList(self._oggi)
            row = index.row()
            col = index.column()
            dato = date[col][row].day()
            if role == QtCore.Qt.DisplayRole:
               return dato
            elif role == QtCore.Qt.TextAlignmentRole:
               return QtCore.Qt.AlignHCenter
        except:
            print(fex())
    def data_old(self, index: QtCore.QModelIndex, role: int = ...) :
        try:
            row = index.row()
            col = index.column()
            dato = self._days[col+1][row].day()
            if role == QtCore.Qt.DisplayRole:
                return dato
            elif role == QtCore.Qt.TextAlignmentRole:
                return QtCore.Qt.AlignHCenter
        except IndexError: pass
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

    def headerData(self, section: int, orientation: QtCore.Qt.Orientation, role: int = ...) :
        giorno = self._oggi
        nomeGiorno = giorno.shortDayName(giorno.dayOfWeek())
        if role == QtCore.Qt.DisplayRole:
            if orientation == QtCore.Qt.Horizontal:
                return nomeGiorno



    def setCurrentDate(self,dato: QtCore.QDate = ...) -> QtCore.QDate:
        self.currentDate = dato
        return  self.currentDate

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
        # listaGiorni = [[for r in range(rows)] for c in range(cols)]
    @staticmethod
    def sendList_old(dataDaLavorare) -> list:
        giorniLista = [d for d in dataDaLavorare.daysInMont()]
        return giorniLista

    @staticmethod
    def sendDict_old(dataDaLavorare) -> dict:
        tot = dataDaLavorare.daysInMonth()
        primoDelMese = QtCore.QDate(dataDaLavorare.year(),dataDaLavorare.month(),1)
        giorniLista = [d for d in range(1,tot+1)]
        def colDict(lista=[]):
            """deve ritornare un dizionario"""
            listaCopiata = lista.copy()
            listaTemp = []
            diz = {}
            while len(listaCopiata):
                try:
                    # print('len listaCopiata: ', len(listaCopiata))
                    listaTroncata = listaCopiata[:7]
                    # print('listaTroncata: ', listaTroncata)
                    for x in listaTroncata:
                        ind = listaCopiata.index(x)
                        # print('valore: ', x, ' indice: ', ind)
                        if x not in listaTemp:
                            estratto = listaCopiata.pop(ind)
                            # print('estratto: ', estratto)
                            chiave = estratto % 7
                            if chiave == 0:
                                chiave = 7
                            if chiave not in diz.keys():
                                diz[chiave] = []
                            # print('             chiave: ', chiave)
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
        primoDelMese = QtCore.QDate(dataDaLavorare.year(), dataDaLavorare.month(), 1)
        giorniLista = [getQDate(d) for d in range(1, tot + 1)]
        # giorniLista = [d for d in range(1, tot + 1)]

        def colDict(lista=[]):
            """deve ritornare un dizionario"""
            listaCopiata = lista.copy()
            listaTemp = []
            diz = {}
            while len(listaCopiata):
                try:
                    # print('len listaCopiata: ', len(listaCopiata))
                    listaTroncata = listaCopiata[:7]
                    # print('listaTroncata: ', listaTroncata)
                    for x in listaTroncata:
                        ind = listaCopiata.index(x)
                        # print('valore: ', x, ' indice: ', ind)
                        if x not in listaTemp:
                            estratto = listaCopiata.pop(ind)
                            # print('estratto: ', estratto)
                            estrattoInt = estratto.day()
                            chiave = estrattoInt % 7
                            if chiave == 0:
                                chiave = 7
                            if chiave not in diz.keys():
                                diz[chiave] = []
                            # print('             chiave: ', chiave)
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
    def __init__(self,parent=None):
        super(Main, self).__init__(parent)
        # self.mainWid = MyWid(self)
        # self.table = Mytable(self.mainWid)
        self.tableView = Mytable(self)
        self.settaData()
        # self.tableView.resized.connect(self.resizing)
        hBox1 = QtWidgets.QHBoxLayout()
        hBox1.addWidget(self.tableView)
        # # self.mainWid.setLayout(hBox1)
        # hBox = QtWidgets.QHBoxLayout()
        # # hBox.addWidget(self.mainWid)
        self.setLayout(hBox1)
        self.modellogiorni(self.oggi)
        # self.tableView.size()

        # self.settingTable()

        print(self.tableView.size())
        print('prima:',self.size())
        # newSize = QtCore.QSize(self.mainWid.size().height()+150, self.mainWid.size().width()+150)
        # self.resize(newSize)
        # self.setMinimumSize(newSize)
        # print('dopo:',self.size())

    def resizing(self):
        newsize = QtCore.QSize(self.tableView.size().width()+100, self.tableView.size().height()+10)
        self.resize(newsize)
        print("dopo",self.size())

    def settingTable(self):
        # self.table.horizontalHeader().setVisible(False)
        # self.table.verticalHeader().setVisible(False)
        quadrato = 50
        # self.table.verticalHeader().setDefaultSectionSize(quadrato)
        # self.table.horizontalHeader().setDefaultSectionSize(quadrato)

    def settaData(self,data=QtCore.QDate().currentDate()) -> QtCore.QDate():
        d = QtCore.QDate().currentDate()
        d.daysInMonth()
        self.oggi = data
        print('********test*********')
        print(self.oggi.shortDayName(self.oggi.dayOfWeek()))
        print('******** fine test*********')
        return self.oggi

    def getAllDates(self, annoIniziale:QtCore.QDate().currentDate().year()):
        dataOggi = QtCore.QDate().currentDate()
        annoFinale = annoIniziale + 10
        mesi = dataOggi.daysInMonth()

    # def giorni_nel_mese(self,dt=QtCore.QDate().currentDate()) -> list:
    #     lista = [d for d in range(dt.daysInMonth()+1)]
    #     giorni = []
    #     diz = {colonna:giorni for colonna, giorni in zip(range(lista),lista)}
    #     for colonna, giorni in zip(range(lista), lista):
    #
    #     for giorno in lista:
    #         if giorno % 7:
    #             pass
    #     diz = Od(diz)
    #     return diz

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

    def modellogiorni_old(self, *args, **kwargs):
        return MyModel(oggi=kwargs, parent=self)

    def modelloOggi(self):
        return MyModel(oggi=self.oggi, parent=self)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ui = Main()
    ui.show()
    sys.exit(app.exec_())