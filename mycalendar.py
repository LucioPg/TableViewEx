### PROVO A MANDARE SOLO LA DATA DI OGGI, IL RESTO LO LASCIO FARE AL MODELLO

import sys
from traceback import format_exc as fex

from PyQt5.QtCore import (QDate, QObject, pyqtSignal, QSize, QAbstractItemModel, QModelIndex, QByteArray, Qt,
                          QStringListModel, pyqtProperty)
from PyQt5.QtWidgets import (QTableView, QWidget, QSizePolicy, QAbstractItemView, QHBoxLayout, QDialog, QPushButton,
                             QComboBox, QVBoxLayout, QSpacerItem, QDataWidgetMapper, QLineEdit,QApplication,
                             QLabel, QFrame, QGridLayout)
from PyQt5.QtGui import (QFont, QColor, QBrush, QStandardItemModel, QStandardItem, QResizeEvent)
from meseGiorniDictGen import MeseGiorniDictGen
from models import MyModel



class Mytable(QTableView):
    resized = pyqtSignal()
    cellClickedMyTable = pyqtSignal(QDate)
    whoIsComing = pyqtSignal(QWidget)
    sigModel = pyqtSignal(int)

    def __init__(self,parent=None, mesi=None):
        if mesi is None:
            self._mesi = mesi
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
        self.clicked.connect(self.click)
        # self.doubleClicked.connect()
        self.sigModel.connect(lambda x: self.model().setDate(x))
        self.setModel(MyModel(self.pagine,parent=parent))
        self.setSizeAdjustPolicy(self.AdjustToContentsOnFirstShow)
        # print('frame',self.frameRect(),'wid ', self.rect())
        self.resized.connect(self.resizing)
        self._sizeSection = self.genSizes()

    def getMese(self):
        return self._mesi
    def setMese(self,m):
        self._mesi = m
        self.model()

    def click(self, ind):
        # data = self.model().date[ind.row()][ind.column()]
        data = self.model()._date[ind.row()][ind.column()]
        self.cellClickedMyTable.emit(data)
        # return data

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
            # print('resizing size:',size)
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

    mesi = pyqtProperty(str, fget=getMese, fset=setMese, notify=sigModel)


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
    doubleClicked = pyqtSignal(QDate)
    def __init__(self,parent=None):
        super(MyDialog, self).__init__(parent)
        self.datas()
        self.selfSetUp()
        self.setUpWidgets()
        self.setUpModels()
        self.setUpMapper()
        self.setUpConnections()
        self.setUpLayouts()
        self.setCurrentDate(QDate().currentDate())

    def datas(self,annoNuovo: int=None):
        # self.pagine = ['vegetale', 'animale']
        self.oggi = QDate().currentDate()
        if annoNuovo is not None:
            self.oggi = QDate(annoNuovo,1,1)
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
        self.table.setMinimumSize(QSize(0, 0))
        self.table.setFrameShape(QFrame.NoFrame)
        self.table.setFrameShadow(QFrame.Plain)
        self.table.setLineWidth(0)
        self.table.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.table.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.table.setObjectName("table")
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

        self.combo.setMinimumSize(QSize(30, 40))
        self.combo.setMaxVisibleItems(12)
        self.combo.setMaxCount(12)
        self.combo.setModelColumn(0)
        self.combo.setObjectName("combo")
        # self.combo.setEditable(True)
        # self.combo.lineEdit().setAlignment(Qt.AlignCenter)
        # self.combo = QComboBox(self)
        # try:
        #     self.combo.lineEdit().setAlignment(Qt.AlignCenter)
        # except AttributeError:
        #     pass

        botSize = QSize(40,40)
        self.bot_next = QPushButton(text='Next', parent=self)
        self.bot_prev = QPushButton(text='Prev', parent=self)
        self.bot_prev.setMinimumSize(QSize(40, 40))
        self.bot_prev.setMaximumSize(QSize(40, 40))
        self.bot_prev.setSizePolicy(sizePolicy)
        self.bot_prev.setObjectName("bot_prev")
        self.bot_next.setMinimumSize(QSize(40, 40))
        self.bot_next.setMaximumSize(QSize(40, 40))
        self.bot_next.setObjectName("bot_next")

    def setUpLayouts_old(self):
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


    def setUpLayouts(self):
        self.gridLayout = QGridLayout(self)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setContentsMargins(-1, -1, -1, -1)
        self.horizontalLayout.setObjectName("horizontalLayout")
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.bot_prev.sizePolicy().hasHeightForWidth())
        self.bot_prev.setSizePolicy(sizePolicy)
        self.horizontalLayout.addWidget(self.bot_prev)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.combo.sizePolicy().hasHeightForWidth())
        self.combo.setSizePolicy(sizePolicy)
        # self.combo.setStyleSheet("")

        self.horizontalLayout.setSpacing(-15)
        self.horizontalLayout.addWidget(self.combo)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.bot_next.sizePolicy().hasHeightForWidth())
        self.bot_next.setSizePolicy(sizePolicy)

        self.horizontalLayout.addWidget(self.bot_next)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.table.horizontalHeader().setStretchLastSection(False)
        # self.verticalLayout.setContentsMargins(-1, -1, -1, 10)
        self.verticalLayout.addWidget(self.table)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)

        self.setLayout(self.gridLayout)

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
        self.mapper.addMapping(self.table,1,b'mesi')
        # self.mapper.addMapping(self.combo,0,b'currentIndex')
        self.mapper.addMapping(self.combo,0)
        # self.mapper.currentIndexChanged.connect(self.updateButtons)
        self.mapper.currentIndexChanged.connect(lambda x: self.table.sigModel.emit(x))
        # self.mapper.toFirst()
        # self.mapper.toLast()
        self.mapper.setCurrentIndex(QDate().currentDate().month()-1)
    def setUpConnections(self):
        self.resized.connect(self.tableAndComboResizing)
        self.bot_next.clicked.connect(self.toNext)
        self.bot_prev.clicked.connect(self.toPrevious)
        self.combo.currentIndexChanged.connect(lambda x: self.mapper.setCurrentIndex(x))
        self.table.cellClickedMyTable.connect(self.setCurrentDate)
        self.table.doubleClicked.connect(self.doubleClickSignal)
        # self.combo.currentIndexChanged.connect(lambda x: self.mapper.model().c)

    def doubleClickSignal(self,ind):
        data = self.model()._date[ind.row()][ind.column()]
        self.doubleClicked.emit(data)

    def toPrevious(self):
        currentIndex = self.mapper.currentIndex()
        try:
            self.mapper.setCurrentIndex(currentIndex - 1)
            afterIndex = self.mapper.currentIndex()
            if afterIndex == currentIndex:
                self.datas(self.oggi.year() - 1)
                self.table.model()._mesi = self.pagine
                self.mapper.toLast()
        except:
            print(fex())
    def toNext(self):
        currentIndex = self.mapper.currentIndex()
        try:
            self.mapper.setCurrentIndex(currentIndex+1)
            afterIndex = self.mapper.currentIndex()
            if afterIndex == currentIndex:
                self.datas(self.oggi.year() + 1)
                self.table.model()._mesi = self.pagine
                self.mapper.toFirst()
        except:
            print(fex())

    def setCurrentDate(self,data):
        self.currentDate = data

    def resizeEvent(self, a0: QResizeEvent) -> None:
        self.resized.emit()
    def tableAndComboResizing(self):
        sizeD = self.size().height()
        self.table.resizingFromParent(int(sizeD /8))
if __name__ == '__main__':
    from combosenzafreccia import ComboSenzaFreccia
    app = QApplication(sys.argv)
    app.setStyle('fusion')
    ui = MyDialog()
    ui.show()
    sys.exit(app.exec_())