### PROVO A MANDARE SOLO LA DATA DI OGGI, IL RESTO LO LASCIO FARE AL MODELLO

import sys
from traceback import format_exc as fex

from PyQt5.QtCore import (QDate, QObject, pyqtSignal, QSize, QAbstractItemModel, QModelIndex, QByteArray, Qt,
                          QStringListModel, pyqtProperty)
from PyQt5.QtWidgets import (QTableView, QWidget, QSizePolicy, QAbstractItemView, QHBoxLayout, QDialog, QPushButton,
                             QComboBox, QVBoxLayout, QSpacerItem, QDataWidgetMapper, QLineEdit,QApplication, QLabel, QFrame)
from PyQt5.QtGui import (QFont, QColor, QBrush, QStandardItemModel, QStandardItem, QResizeEvent)
from meseGiorniDictGen import MeseGiorniDictGen
from models import MyModel
class MyCalendarCore(QWidget):
    cellClicked = pyqtSignal(QDate)
    def __init__(self,parent=None):
        super(MyCalendarCore, self).__init__(parent)
        self.setObjectName('MyCalendarCore')
        self.setMinimumSize(QSize(int(680 * 1.5), int(600 * 1.5)))
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        sizePolicy.setWidthForHeight(self.sizePolicy().hasWidthForHeight())
        self.setSizePolicy(sizePolicy)
        self.tableView = Mytable(self)
        # self.tableView = QTableView(self)
        self.settaData()
        hBox1 = QHBoxLayout()
        hBox1.addWidget(self.tableView)
        self.setLayout(hBox1)
        # self.modellogiorni(self.oggi)
        # self.tableView.cellClickedMyTable.connect(lambda x:self.cellClicked.emit(x))

    def settaData(self,data=QDate().currentDate()) -> QDate():
        data.daysInMonth()
        self.oggi = data
        return self.oggi

    def setDataView(self, data:QDate()= ...) -> QDate():
        self.dataView = data
        return self.dataView

    def nextMonth(self):
        year =self.oggi.year()
        daysInMonth = self.oggi.daysInMonth()
        nextMonth = self.oggi.addDays(daysInMonth - self.oggi.day()+1)
        print(nextMonth)
        self.settaData(nextMonth)

    # def modellogiorni(self, oggi):        lista = GiorniDelMese.sendList(oggi)
    #     dati = GiorniDelMese.sendDict(oggi)
    #     try:
    #         model = MyModel(oggi=oggi, parent=self)
    #         self.tableView.setModel(model)
    #     except:
    #         print(fex())
    #
    # def modelloOggi(self):
    #     return MyModel(oggi=self.oggi, parent=self)

    def modelloOnTheRun(self,model,dati):
        self.tableView.setModel(model(oggi=dati,parent=self))


class Mytable(QTableView):
    resized = pyqtSignal()
    cellClickedMyTable = pyqtSignal(QDate)
    whoIsComing = pyqtSignal(QWidget)
    sigModel = pyqtSignal(int)

    def __init__(self,parent=None, mese=None):
        if mese is None:
            self._mese = mese
        super(Mytable, self).__init__(parent)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setSizePolicy(sizePolicy)
        self.verticalHeader().setVisible(False)
        self.setFrameShape(QFrame.NoFrame)
        self.setFrameShadow(QFrame.Plain)
        self.horizontalHeader().setDefaultAlignment(Qt.AlignCenter)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.frameRect()
        # self.resized.connect(self.resizing)
        self.oggi = QDate().currentDate()
        # self.pagine = MeseGiorniDictGen.genDict(self.oggi,num=True)
        self.pagine = MeseGiorniDictGen.bigList(self.oggi)

        self.horizontalHeader().setMinimumHeight(30)
        font = QFont('Arial', 20)
        font2 = QFont('Arial', 17)
        self.horizontalHeader().setFont(font2)
        self.setFont(font)
        self.setSelectionMode(QAbstractItemView.SingleSelection)
        self.setSelectionBehavior(QAbstractItemView.SelectItems)
        # self.doubleClicked.connect(self.dClick)
        self.clicked.connect(self.dClick)
        self.sigModel.connect(lambda x: print('sig',x, self._mese,self.model().setDate(x)))
        self.setModel(MyModel(self.pagine,parent=parent))
        self.setSizeAdjustPolicy(self.AdjustToContentsOnFirstShow)
        # print('frame',self.frameRect(),'wid ', self.rect())
        self.resized.connect(self.resizing)
        self._sizeSection = self.genSizes()

    def getMese(self):
        return self._mese
    def setMese(self,m):
        self._mese = m

    def dClick(self,ind):
        return
        self.cellClickedMyTable.emit(data)
        return data

    def genSizes(self,m=150,M=200):
        size = m
        while True:
            yield size
            print('gen size ',size)
            size +=10

    def resizingFromParent(self,size):
        self.verticalHeader().setDefaultSectionSize(size)
        self.horizontalHeader().setDefaultSectionSize(size)

    def resizing(self,size=None):

        # print(type(_size))
        try:
            if size is None:
                # size =  next(self._sizeSection)
                size =  int(self.horizontalHeader().size().width()/7)
            print('resizing size:',size)
            # print('frame', self.frameRect(), 'wid ', self.rect())
            # self.horizontalHeader().setDefaultSectionSize(size)
            self.verticalHeader().setDefaultSectionSize(size)
            self.setSizeAdjustPolicy(self.AdjustToContents)
            # print(size, 'size  ', self.size())
        except :
                print(fex())



    def resizeEvent(self, event):
        self.resized.emit()
        return super(Mytable, self).resizeEvent(event)
    #
    # def setModel(self, model: QAbstractItemModel) -> None:
    #     # self.whoIsComing.emit(self)
    #     model.setFromList(self)
    #     super(Mytable, self).setModel(model)

    def update(self) -> None:
        print(self.objectName())
        self.whoIsComing.emit(self)
        super(Mytable, self).update(self)

    mese = pyqtProperty(str, fget=getMese, fset=setMese, notify=sigModel)


class MyDialog(QWidget):
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
    resized = pyqtSignal()
    def __init__(self,parent=None):
        super(MyDialog, self).__init__(parent)
        self.datas()
        self.selfSetUp()
        self.setUpWidgets()
        self.setUpModels()
        self.setUpMapper()
        self.setUpConnections()
        self.setUpLayouts()


    def datas(self):
        # self.pagine = ['vegetale', 'animale']
        self.oggi = QDate().currentDate()
        # self.pagine = MeseGiorniDictGen.genDict(self.oggi,num=True)
        self.pagine = MeseGiorniDictGen.bigList(self.oggi)


    def selfSetUp(self):
        self.setWindowTitle('TableView v 0.2')
        # self.setMinimumSize(QSize(int(800), int(800)))
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasWidthForHeight())
        sizePolicy.setWidthForHeight(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)

    def setUpWidgets(self):
        # self.table = Mytable(self)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        sizePolicy.setWidthForHeight(self.sizePolicy().hasWidthForHeight())
        # self.cal = MyCalendarCore(self)
        # self.table =self.cal.tableView
        self.table =Mytable(self)
        # sizeD = self.size().width()
        # print('primodi size',)
        # self.table.resizing(int(sizeD/10))
        # self.table.setStyleSheet("background-color: rgb(255, 255, 127)")
        # labSize = QSize(100,30)
        # self.table.setFixedSize(labSize)
        self.table.setSizePolicy(sizePolicy)
        # self.table.sizePolicy().horizontalStretch()
        self.combo = QComboBox()
        self.combo = ComboSenzaFreccia(self)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.combo.setSizePolicy(sizePolicy)
        self.combo.setMinimumHeight(40)
        # self.combo.setEditable(True)
        # self.combo.lineEdit().setAlignment(Qt.AlignCenter)
        # self.combo = QComboBox(self)
        # try:
        #     self.combo.lineEdit().setAlignment(Qt.AlignCenter)
        # except AttributeError:
        #     pass
        botSize = QSize(30,30)
        self.bot_next = QPushButton(text='Next', parent=self)
        self.bot_prev = QPushButton(text='Prev', parent=self)
        self.bot_prev.setSizePolicy(sizePolicy)
        self.bot_next.setSizePolicy(sizePolicy)
        self.bot_prev.setFixedSize(botSize)
        self.bot_next.setFixedSize(botSize)

    def setUpLayouts(self):
        self.finalLay = QVBoxLayout()
        self.finalLay.setObjectName("finalLay")
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.bot_prev.setObjectName("bot_prev")
        spacerItem3 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        spacerItem4 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.horizontalLayout_3.addItem(spacerItem3)
        self.horizontalLayout_3.addWidget(self.bot_prev)
        self.combo.setObjectName("ComboSenzaFreccia")
        self.horizontalLayout_3.addWidget(self.combo)
        self.bot_next.setObjectName("bot_next")
        self.horizontalLayout_3.addWidget(self.bot_next)
        self.horizontalLayout_3.addItem(spacerItem4)
        self.finalLay.addLayout(self.horizontalLayout_3)
        spacerItem1 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        spacerItem2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        # self.horizontalLayout.addItem(spacerItem1)
        self.horizontalLayout.addWidget(self.table)
        # self.horizontalLayout.addItem(spacerItem2)
        self.finalLay.addLayout(self.horizontalLayout)
        self.setLayout(self.finalLay)


    def setUpLayouts_old(self):
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.finalLay = QHBoxLayout()
        self.finalLay.setObjectName("finalLay")
        self.prevLay = QVBoxLayout()
        self.prevLay.setObjectName("prevLay")
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        spacerItem = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.bot_prev.setObjectName("bot_prev")
        self.horizontalLayout_3.addWidget(self.bot_prev)
        self.prevLay.addLayout(self.horizontalLayout_3)
        spacerItem1 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.prevLay.addItem(spacerItem1)
        self.finalLay.addLayout(self.prevLay)
        self.centLay = QVBoxLayout()
        self.centLay.setObjectName("centLay")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.combo.setMaxVisibleItems(12)
        self.combo.setMaxCount(12)
        self.combo.setObjectName("ComboSenzaFreccia")
        self.verticalLayout_2.addWidget(self.combo)
        # self.table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.table.setObjectName("table")
        # self.table.horizontalHeader().setStretchLastSection(True)
        # self.verticalLayout_2.addWidget(self.cal)
        hor = QHBoxLayout()
        sp1 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        sp2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        hor.addItem(sp1)
        hor.addItem(sp2)
        hor.addWidget(self.table)
        self.verticalLayout_2.addLayout(hor)
        spacerItem13 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.centLay.addLayout(self.verticalLayout_2)
        self.verticalLayout_2.addItem(spacerItem13)
        self.finalLay.addLayout(self.centLay)
        self.nextLay = QVBoxLayout()
        self.nextLay.setObjectName("nextLay")
        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.bot_next.setObjectName("bot_next")
        self.horizontalLayout_4.addWidget(self.bot_next)
        spacerItem2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem2)
        self.nextLay.addLayout(self.horizontalLayout_4)
        spacerItem3 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.nextLay.addItem(spacerItem3)
        self.finalLay.addLayout(self.nextLay)
        # self.horizontalLayout.addLayout(self.finalLay)
        self.setLayout(self.finalLay)

    def setUpModels(self):
        ## sono gli items che devo essere nella combo (es: i mesi)
        # items = ['cane', 'gatto', 'melo', 'pero']
        items = self.listaMesi
        #i numeri 4 e 2 passati come argomenti per il modello base indicano le righe e le colonne del modello
        # basate sulla len di items e di self.pagine
        self.model = QStandardItemModel(len(items), len(items), self)
        # questo è il modello passato alla combo, che ha come elementi gli items
        self.typeModel = QStringListModel(items, self)
        # self.typeModel.dataChanged.connect(self.typeModel.setData(self.typeModel.index(),Qt.AlignCenter, Qt.TextAlignmentRole))
        self.combo.setModel(self.typeModel)
        #setto il modello per la tableView
        self.tableModel = MyModel(self.pagine,parent=self)
        self.table.setModel(self.tableModel)
        # a ogni elemento di items deve corrispondere un valore, self.pagine, ricavato dall'indice
        # types = ("1", "1", "0", "0")
        typesList = [str(x) for x in range(1,13)]
        types = tuple(typesList)
        # per ogni item viene assegnato il valore nel modello matrice
        # la mappatura ha nella colonna 0 la combobox e gli viene assegnato un item
        # alla colonna 1 del modello viene assegnato il riferimento a self.pagine passato attraverso types
        for row, item in enumerate(items):
            self.model.setItem(row, 0, QStandardItem(item))
            self.model.setItem(row, 1, QStandardItem(types[row]))
            # self.model.setItem(row, 1, QStandardItem(types[2]))
            # self.model.setItem(row, 1, QStandardItem(types[row]))
        # for row, col in enumerate()
        # self.combo.setEditable(

        # self.model.itemChanged.connect(lambda x: print('DATACHANGED',dir(x),end='\n'))

    def setUpMapper(self):
        self.mapper = QDataWidgetMapper(self)
        self.mapper.setModel(self.model)
        # self.mapper.addMapping(self.table,1,b'currentIndex')
        self.mapper.addMapping(self.table,1,b'mese')
        # self.mapper.addMapping(self.combo,0,b'currentIndex')
        self.mapper.addMapping(self.combo,0)
        self.mapper.currentIndexChanged.connect(self.updateButtons)
        self.mapper.currentIndexChanged.connect(lambda x: self.table.sigModel.emit(x))
        # self.mapper.toFirst()
        # self.mapper.toLast()
        self.mapper.setCurrentIndex(QDate().currentDate().month()-1)
    def setUpConnections(self):
        self.resized.connect(self.tableAndComboResizing)
        self.bot_next.clicked.connect(self.mapper.toNext)
        self.bot_prev.clicked.connect(self.mapper.toPrevious)
        try:
            self.combo.currentIndexChanged.connect(lambda x: self.mapper.setCurrentIndex(x))
            pass
        except:
            print(fex())
        # self.combo.currentIndexChanged.connect(lambda x: self.mapper.model().c)
    def updateButtons(self, row):
        self.bot_prev.setEnabled(row > 0)
        self.bot_next.setEnabled(row < self.model.rowCount() - 1)
        # print('mapper current index', self.mapper.currentIndex())
        # print('combo current index', self.combo.currentIndex())
        # # print('mapper model rows count', self.mapper.model().rowCount())
        # print('-'*20)

    def resizeEvent(self, a0: QResizeEvent) -> None:
        self.resized.emit()
    def tableAndComboResizing(self):
        sizeD = self.size().height()
        self.table.resizingFromParent(int(sizeD /8))
        tableWidth = self.table.size().width()
        botWid = self.bot_next.size().width() *2
        finalWid = tableWidth -botWid
        self.combo.setFixedWidth(finalWid)
if __name__ == '__main__':
    from combosenzafreccia import ComboSenzaFreccia
    app = QApplication(sys.argv)
    app.setStyle('fusion')
    ui = MyDialog()
    ui.show()
    sys.exit(app.exec_())