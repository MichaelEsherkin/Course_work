

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtWidgets import QMessageBox
import pyodbc

from connection import db

class LoginForm(QtWidgets.QWidget):

    # Signal emitted when login succeeded
    logined = QtCore.pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.setupUi(self)

    def setupUi(self, Dialog):
        """Initialization of interface"""

        Dialog.resize(270, 200)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(50, 140, 161, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)

        self.lineEdit = QtWidgets.QLineEdit(Dialog)
        self.lineEdit.setGeometry(QtCore.QRect(70, 10, 191, 20))

        self.lineEdit_2 = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_2.setGeometry(QtCore.QRect(70, 40, 191, 20))

        self.lineEdit_3 = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_3.setGeometry(QtCore.QRect(70, 70, 191, 20))

        self.lineEdit_4 = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_4.setGeometry(QtCore.QRect(70, 100, 191, 20))

        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(20, 10, 47, 13))

        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(20, 40, 47, 13))

        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(20, 70, 47, 13))

        self.label_4 = QtWidgets.QLabel(Dialog)
        self.label_4.setGeometry(QtCore.QRect(20, 100, 47, 13))


        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label.setText(_translate("Dialog", "Login"))
        self.label_2.setText(_translate("Dialog", "Password"))
        self.label_3.setText(_translate("Dialog", "Connect"))
        self.label_4.setText(_translate("Dialog", "Schema"))

        self.lineEdit.setText("testuser1")
        self.lineEdit_2.setText("testpass1")
        self.lineEdit_3.setText("THIRTYTHIRDPC\\SQLEXPRESS")
        self.lineEdit_4.setText("testbase1")

        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)



    def accept(self):
        """Processing Login button (trying to connect with login)"""
        try:

            db.connect(self.lineEdit_3.text(), self.lineEdit_4.text(),
                       self.lineEdit.text(), self.lineEdit_2.text())
        except pyodbc.InterfaceError as e:
            QMessageBox.about(self, "Error", str(e))
        else:
            self.logined.emit("Success")
            self.close()

    def reject(self):
        QCoreApplication.instance().quit()