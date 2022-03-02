# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'delete.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from connection import db

class AddWindow(QtWidgets.QDialog):
    """Creates window to add new entities
    """
    finished = QtCore.pyqtSignal(str)

    def __init__(self, fields, entity):
        super().__init__()
        self.fields = fields
        self.entity = entity
        self.setupUi()

    def setupUi(self):
        self.setObjectName("Delete " + self.entity)
        self.setWindowTitle("Add " + self.entity)
        self.resize(480, 111)
        self.Delete = QtWidgets.QDialogButtonBox(self)

        self.Delete.setOrientation(QtCore.Qt.Horizontal)
        self.Delete.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.Delete.setObjectName("Удалить")


        self.lineEdits = []
        self.labels = []

        for i, field in enumerate(self.fields):
            self.labels.append(QtWidgets.QLabel(self))
            self.labels[i].setGeometry(QtCore.QRect(20, 10 + i * 40, 150, 20))
            self.labels[i].setText(field)

            self.lineEdits.append(QtWidgets.QLineEdit(self))
            self.lineEdits[i].setGeometry(QtCore.QRect(20, 30 + i * 40, 150, 20))

        self.resize(480, 110 + i * 40)
        self.Delete.setGeometry(QtCore.QRect(10, 70 + i * 40, 161, 32))

        self.Delete.accepted.connect(self.accept_but)
        self.Delete.button(QtWidgets.QDialogButtonBox.Ok).setText("Добавить")
        self.Delete.rejected.connect(self.reject_but)
        QtCore.QMetaObject.connectSlotsByName(self)

        # self.setWindowTitle(_translate("Dialog", "Dialog"))

    def accept_but(self):
        res = db.add(self.lineEdits, self.entity)
        if (res is not None):
            if (res == -1):
                QtWidgets.QMessageBox.about(self, "Error", "Производитель не существует")
            else:
                self.close()
        else:
            QtWidgets.QMessageBox.about(self, "Error", "Error")
            self.close()

    def reject_but(self):
        self.close()

    def closeEvent(self, event: QtGui.QCloseEvent):
        """Calles when window is closed"""
        self.finished.emit("Edit")
        event.accept()