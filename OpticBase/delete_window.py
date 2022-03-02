# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'delete.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from connection import db

class DeleteWindow(QtWidgets.QDialog):
    """
        creates window for editing/seraching entities
    """
    finished = QtCore.pyqtSignal(str)

    def __init__(self, fields, entity):
        super().__init__()
        self.fields = fields
        self.entity = entity
        self.setupUi()

    def setupUi(self):
        self.setObjectName("Delete " + self.entity)
        self.resize(480, 111)
        self.Delete = QtWidgets.QDialogButtonBox(self)
        self.setWindowTitle("Edit " + self.entity)

        self.Delete.setOrientation(QtCore.Qt.Horizontal)
        self.Delete.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.Delete.button(QtWidgets.QDialogButtonBox.Ok).setText("Поиск")
        self.Delete.setObjectName("Поиск")


        self.lineEdits = []
        self.labels = []

        for i, field in enumerate(self.fields):
            self.labels.append(QtWidgets.QLabel(self))
            self.labels[i].setGeometry(QtCore.QRect(20, 10 + i * 40, 150, 20))
            self.labels[i].setText(field)

            self.lineEdits.append(QtWidgets.QLineEdit(self))
            self.lineEdits[i].setGeometry(QtCore.QRect(20, 30 + i * 40, 150, 20))


        self.Delete.setGeometry(QtCore.QRect(10, 70 + i * 40, 161, 32))

        self.Delete.accepted.connect(self.search_but)
        self.Delete.rejected.connect(self.reject_but)

        self.tableWidget = QtWidgets.QTableWidget(self)
        self.tableWidget.setGeometry(QtCore.QRect(10, 130 + i * 40, 780, 500))
        self.tableWidget.setObjectName("tableWidget")

        self.resize(800, 510 + 130 + i * 40)

        self.tableWidget.setSizeAdjustPolicy(
            QtWidgets.QAbstractScrollArea.AdjustToContents)

        QtCore.QMetaObject.connectSlotsByName(self)


    def deleteRow(self, ent_id):
        db.deleteById(ent_id, self.entity)
        self.updateTable()

    def updateTable(self):
        """Updates table by user input (lineEdits)"""
        res = db.select(self.lineEdits, self.entity)
        if (res is not None):
            self.fillTable(res)
        else:
            QtWidgets.QMessageBox.about(self, "Error", "Error")
            self.close()

    def updateRow(self, row_index):
        """Sends to database updated row"""
        res = [self.tableWidget.item(row_index, j).text() for j in range(self.tableWidget.columnCount() - 2)]
        res = db.updateRow(res, self.entity)
        if (res == None):
            QtWidgets.QMessageBox.about(self, "Error", "Error")
        if (res == -1):
            QtWidgets.QMessageBox.about(self, "Error", "Нет такого производителя. Производитель не сохранен")


    def fillTable(self, res):
        """Creates and fills table with search results based on select result"""

        self.res = res
        columns = res[0]
        res = res[1]

        self.tableWidget.setRowCount(0)
        self.tableWidget.setColumnCount(len(columns) + 2)
        self.tableWidget.setHorizontalHeaderLabels(columns)
        delete_buttons = []
        for row_number, row_data in enumerate(res):
            self.tableWidget.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                new_cell = QtWidgets.QTableWidgetItem(str(data))
                if (column_number == 0):
                    new_cell.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
                self.tableWidget.setItem(row_number, column_number, new_cell)


            delete_button = QtWidgets.QPushButton(self.tableWidget)
            delete_button.clicked.connect(lambda state, x=row_data[0]: self.deleteRow(x))
            delete_button.setText("Delete")
            self.tableWidget.setCellWidget(row_number, column_number + 1, delete_button)

            update_button = QtWidgets.QPushButton(self.tableWidget)
            update_button.clicked.connect(lambda state, x=row_number: self.updateRow(x))
            update_button.setText("Save")
            self.tableWidget.setCellWidget(row_number, column_number + 2, update_button)

        self.tableWidget.resizeColumnsToContents()

    def search_but(self):
        self.updateTable()

    def reject_but(self):
        self.close()

    def closeEvent(self, event: QtGui.QCloseEvent):
        """called when window is closed"""
        self.finished.emit("Edit")
        event.accept()
