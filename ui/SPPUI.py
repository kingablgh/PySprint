# -*- coding: utf-8 -*-



from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QAbstractItemView, QTreeWidget
import numpy as np

# xcoords = []
# ycoords = []

class Ui_SPP(object):
## ez is átmegy majd

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1302, 832)

        ##
        self.xData = []
        self.yData = []
        self.ySam = []
        self.yRef = []
        self.xtemporal = []
        self.ytemporal = []
        self.xpoints = [[None]]*20
        self.ypoints = [[None]]*20
        self.delays = np.array([None]*20)
        self.cid = None
        ##
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.loadButton = QtWidgets.QPushButton(self.centralwidget)
        self.loadButton.setMinimumSize(QtCore.QSize(150, 30))
        self.loadButton.setObjectName("loadButton")
        self.horizontalLayout_2.addWidget(self.loadButton)
        self.pushButton_7 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_7.setObjectName("pushButton_7")
        self.horizontalLayout_2.addWidget(self.pushButton_7)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.treeWidget = QtWidgets.QTreeWidget(self.centralwidget)
        self.treeWidget.setExpandsOnDoubleClick(False)
        self.treeWidget.setObjectName("treeWidget")
        font = QtGui.QFont()
        font.setBold(False)
        font.setUnderline(True)
        font.setWeight(50)
        font.setStrikeOut(False)
        self.treeWidget.headerItem().setFont(0, font)
        self.verticalLayout.addWidget(self.treeWidget)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 3, 1)
        self.widget = PlotWidget(self.centralwidget)
        self.widget.setMinimumSize(QtCore.QSize(500, 450))
        self.widget.setObjectName("widget")
        self.gridLayout.addWidget(self.widget, 0, 1, 1, 3)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.delayLine = QtWidgets.QLineEdit(self.centralwidget)
        self.delayLine.setMinimumSize(QtCore.QSize(0, 30))
        self.delayLine.setObjectName("delayLine")
        self.horizontalLayout.addWidget(self.delayLine)
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setMinimumSize(QtCore.QSize(0, 30))
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.pushButton)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.SPP1 = QtWidgets.QLineEdit(self.centralwidget)
        self.SPP1.setMinimumSize(QtCore.QSize(0, 30))
        self.SPP1.setText("")
        self.SPP1.setObjectName("SPP1")
        self.SPP1.setStyleSheet("""QLineEdit { color: blue }""")
        self.verticalLayout_2.addWidget(self.SPP1)
        self.SPP2 = QtWidgets.QLineEdit(self.centralwidget)
        self.SPP2.setMinimumSize(QtCore.QSize(0, 30))
        self.SPP2.setObjectName("SPP2")
        self.SPP2.setStyleSheet("""QLineEdit { color: orange }""")
        self.verticalLayout_2.addWidget(self.SPP2)
        self.SPP3 = QtWidgets.QLineEdit(self.centralwidget)
        self.SPP3.setMinimumSize(QtCore.QSize(0, 30))
        self.SPP3.setObjectName("SPP3")
        self.SPP3.setStyleSheet("""QLineEdit { color: green }""")
        self.verticalLayout_2.addWidget(self.SPP3)
        self.SPP4 = QtWidgets.QLineEdit(self.centralwidget)
        self.SPP4.setMinimumSize(QtCore.QSize(0, 20))
        self.SPP4.setObjectName("SPP4")
        self.SPP4.setStyleSheet("""QLineEdit { color: purple }""")
        self.SPP4.setMinimumSize(QtCore.QSize(0, 30))
        self.verticalLayout_2.addWidget(self.SPP4)
        self.pushButton_4 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_4.setObjectName("pushButton_4")
        self.verticalLayout_2.addWidget(self.pushButton_4)
        self.verticalLayout_4.addLayout(self.verticalLayout_2)
        self.gridLayout.addLayout(self.verticalLayout_4, 1, 1, 2, 1)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setObjectName("pushButton_2")
        self.horizontalLayout_4.addWidget(self.pushButton_2)
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setObjectName("pushButton_3")
        self.horizontalLayout_4.addWidget(self.pushButton_3)
        self.gridLayout.addLayout(self.horizontalLayout_4, 1, 2, 1, 1)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.GDSPP = QtWidgets.QLineEdit(self.centralwidget)
        self.GDSPP.setObjectName("GDSPP")
        self.verticalLayout_3.addWidget(self.GDSPP)
        self.GDDSPP = QtWidgets.QLineEdit(self.centralwidget)
        self.GDDSPP.setObjectName("GDDSPP")
        self.verticalLayout_3.addWidget(self.GDDSPP)
        self.TODSPP = QtWidgets.QLineEdit(self.centralwidget)
        self.TODSPP.setObjectName("TODSPP")
        self.verticalLayout_3.addWidget(self.TODSPP)
        self.FODSPP = QtWidgets.QLineEdit(self.centralwidget)
        self.FODSPP.setObjectName("FODSPP")
        self.verticalLayout_3.addWidget(self.FODSPP)
        self.QODSPP = QtWidgets.QLineEdit(self.centralwidget)
        self.QODSPP.setObjectName("QODSPP")
        self.verticalLayout_3.addWidget(self.QODSPP),
        self.messageBox = QtWidgets.QTextEdit(self.centralwidget)
        self.messageBox.setReadOnly(True)
        self.messageBox.setObjectName("messageBox")

        self.verticalLayout_3.addWidget(self.messageBox)
        self.gridLayout.addLayout(self.verticalLayout_3, 1, 3, 2, 1)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.pushButton_5 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_5.setObjectName("pushButton_5")
        self.horizontalLayout_3.addWidget(self.pushButton_5)
        self.fitOrderLine = QtWidgets.QLineEdit(self.centralwidget)
        self.fitOrderLine.setMinimumSize(QtCore.QSize(0, 30))
        self.fitOrderLine.setObjectName("fitOrderLine")
        self.horizontalLayout_3.addWidget(self.fitOrderLine)
        self.pushButton_6 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_6.setMinimumSize(QtCore.QSize(0, 30))
        self.pushButton_6.setObjectName("pushButton_6")
        self.horizontalLayout_3.addWidget(self.pushButton_6)
        self.gridLayout.addLayout(self.horizontalLayout_3, 2, 2, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1302, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "SPP Method"))
        self.loadButton.setText(_translate("MainWindow", "Load file"))
        self.pushButton_7.setText(_translate("MainWindow", "Delete item"))
        self.treeWidget.headerItem().setText(0, _translate("MainWindow", "Loaded files"))
        __sortingEnabled = self.treeWidget.isSortingEnabled()
        self.treeWidget.setSortingEnabled(False)
        self.treeWidget.setSortingEnabled(__sortingEnabled)
        self.delayLine.setPlaceholderText(_translate("MainWindow", "delay (fs)"))
        self.pushButton.setText(_translate("MainWindow", "Set delay"))
        self.SPP1.setPlaceholderText(_translate("MainWindow", "SPP1"))
        self.SPP2.setPlaceholderText(_translate("MainWindow", "SPP2"))
        self.SPP3.setPlaceholderText(_translate("MainWindow", "SPP3"))
        self.SPP4.setPlaceholderText(_translate("MainWindow", "SPP4"))
        self.pushButton_4.setText(_translate("MainWindow", "Set SPP"))
        self.pushButton_2.setText(_translate("MainWindow", "Clickable SPP"))
        self.pushButton_3.setText(_translate("MainWindow", "Stop and record"))
        self.GDSPP.setPlaceholderText(_translate("MainWindow", "GD "))
        self.GDDSPP.setPlaceholderText(_translate("MainWindow", "GDD"))
        self.TODSPP.setPlaceholderText(_translate("MainWindow", "TOD"))
        self.FODSPP.setPlaceholderText(_translate("MainWindow", "FOD"))
        self.QODSPP.setPlaceholderText(_translate("MainWindow", "QOD"))
        self.pushButton_5.setText(_translate("MainWindow", "Reset all"))
        self.fitOrderLine.setPlaceholderText(_translate("MainWindow", "Fit order "))
        self.pushButton_6.setText(_translate("MainWindow", "Fit and report"))

from ui.plotwidget import PlotWidget

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_SPP()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

