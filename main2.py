### PROVO A MANDARE SOLO LA DATA DI OGGI, IL RESTO LO LASCIO FARE AL MODELLO


from PyQt5 import QtWidgets, QtCore, QtGui
import sys
from collections import OrderedDict as Od
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
        self.mainWid = MyWid(self)
        # self.table = Mytable(self.mainWid)
        self.settaData()
        hBox = QtWidgets.QHBoxLayout()
        hBox.addWidget(self.mainWid)
        self.setLayout(hBox)
        hBox = QtWidgets.QHBoxLayout()

        self.table = QtWidgets.QTreeView(self.mainWid)
        model = QtGui.QStandardItemModel(self.table)

        # AGGIUNTA COMBOBOX
        ############################################################################################################
        self.table.setModel(model)

        combobox = QtWidgets.QComboBox()
        combobox.addItems(['a','b','c'])

        child1 = QtGui.QStandardItem('test1')
        child2 = QtGui.QStandardItem('test2')
        child3 = QtGui.QStandardItem('test3')
        model.appendRow([child1, child2, child3])
        a = model.index(0, 2)
        self.table.setIndexWidget(a, combobox)
        ############################################################################################################
        # self.settingTable()
        # self.modellogiorni(self.oggi)
        hBox.addWidget(self.table)
        self.mainWid.setLayout(hBox)

    def settingTable(self):
        # self.table.horizontalHeader().setVisible(False)
        self.table.verticalHeader().setVisible(False)
        self.table

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
            self.table.setModel(model)
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