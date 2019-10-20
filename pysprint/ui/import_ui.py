# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'imp_ui.ui'
#
# Created by: PyQt5 UI code generator 5.13.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_ImportPage(object):
    def setupUi(self, ImportPage):
        ImportPage.setObjectName("ImportPage")
        ImportPage.resize(1024, 768)
        self.centralwidget = QtWidgets.QWidget(ImportPage)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.imp_path = QtWidgets.QLineEdit(self.centralwidget)
        self.imp_path.setReadOnly(True)
        self.imp_path.setObjectName("imp_path")
        self.horizontalLayout_2.addWidget(self.imp_path)
        self.imp_load = QtWidgets.QPushButton(self.centralwidget)
        self.imp_load.setObjectName("imp_load")
        self.horizontalLayout_2.addWidget(self.imp_load)
        self.gridLayout_2.addLayout(self.horizontalLayout_2, 0, 0, 1, 2)
        self.imp_table = QtWidgets.QTableWidget(self.centralwidget)
        self.imp_table.setObjectName("imp_table")
        self.imp_table.setColumnCount(4)
        self.imp_table.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.imp_table.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.imp_table.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.imp_table.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.imp_table.setHorizontalHeaderItem(3, item)
        self.gridLayout_2.addWidget(self.imp_table, 1, 0, 1, 1)
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout.setObjectName("gridLayout")
        self.label_3 = QtWidgets.QLabel(self.groupBox)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 1, 0, 1, 1)
        self.imp_header = QtWidgets.QComboBox(self.groupBox)
        self.imp_header.setObjectName("imp_header")
        self.imp_header.addItem("")
        self.imp_header.addItem("")
        self.gridLayout.addWidget(self.imp_header, 0, 1, 1, 1)
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.imp_commit = QtWidgets.QPushButton(self.groupBox)
        self.imp_commit.setObjectName("imp_commit")
        self.gridLayout.addWidget(self.imp_commit, 3, 1, 1, 1)
        self.imp_command = QtWidgets.QTextEdit(self.groupBox)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.imp_command.setFont(font)
        self.imp_command.setObjectName("imp_command")
        self.gridLayout.addWidget(self.imp_command, 1, 1, 1, 1)
        self.imp_put = QtWidgets.QTextEdit(self.groupBox)
        self.imp_put.setObjectName("imp_put")
        self.gridLayout.addWidget(self.imp_put, 2, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 2, 0, 1, 1)
        self.gridLayout_2.addWidget(self.groupBox, 1, 1, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.imp_close = QtWidgets.QPushButton(self.centralwidget)
        self.imp_close.setObjectName("imp_close")
        self.horizontalLayout.addWidget(self.imp_close)
        self.imp_import = QtWidgets.QPushButton(self.centralwidget)
        self.imp_import.setObjectName("imp_import")
        self.horizontalLayout.addWidget(self.imp_import)
        self.gridLayout_2.addLayout(self.horizontalLayout, 2, 0, 1, 2)
        ImportPage.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(ImportPage)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1024, 26))
        self.menubar.setObjectName("menubar")
        ImportPage.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(ImportPage)
        self.statusbar.setObjectName("statusbar")
        ImportPage.setStatusBar(self.statusbar)

        self.retranslateUi(ImportPage)
        QtCore.QMetaObject.connectSlotsByName(ImportPage)

    def retranslateUi(self, ImportPage):
        _translate = QtCore.QCoreApplication.translate
        ImportPage.setWindowTitle(_translate("ImportPage", "Import Data"))
        self.imp_path.setPlaceholderText(_translate("ImportPage", "File path"))
        self.imp_load.setText(_translate("ImportPage", "Load"))
        item = self.imp_table.horizontalHeaderItem(0)
        item.setText(_translate("ImportPage", "x"))
        item = self.imp_table.horizontalHeaderItem(1)
        item.setText(_translate("ImportPage", "y"))
        item = self.imp_table.horizontalHeaderItem(2)
        item.setText(_translate("ImportPage", "reference"))
        item = self.imp_table.horizontalHeaderItem(3)
        item.setText(_translate("ImportPage", "sample"))
        self.groupBox.setTitle(_translate("ImportPage", "Behaviour"))
        self.label_3.setText(_translate("ImportPage", "Command line"))
        self.imp_header.setItemText(0, _translate("ImportPage", "None"))
        self.imp_header.setItemText(1, _translate("ImportPage", "1st row"))
        self.label.setText(_translate("ImportPage", "Header mode(not implemented)"))
        self.imp_commit.setText(_translate("ImportPage", "Commit"))
#         self.imp_command.setHtml(_translate("ImportPage", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
# "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
# "p, li { white-space: pre-wrap; }\n"
# "</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
# "<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
        self.imp_command.setPlaceholderText(_translate("ImportPage", "Write your command here. Pressing CTRL+E will run the code. Type help or help() for details."))
        self.label_2.setText(_translate("ImportPage", "Output"))
        self.imp_close.setText(_translate("ImportPage", "Close"))
        self.imp_import.setText(_translate("ImportPage", "Import"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ImportPage = QtWidgets.QMainWindow()
    ui = Ui_ImportPage()
    ui.setupUi(ImportPage)
    ImportPage.show()
    sys.exit(app.exec_())
