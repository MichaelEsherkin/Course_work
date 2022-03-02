# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

from add_window import AddWindow
from delete_window import DeleteWindow
from connection import db
from exist_order_table import ExistOrderTable
from new_order_table import NewOrderTable


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

    def init(self):
        self.setupUi(self)
        self.updateLists()
        self.show()


    def updateLists(self):
        """Updates lists for autocomplete"""
        self.product_list, self.product_ids = db.selectForList("product")
        self.service_list, self.service_ids = db.selectForList("service")
        self.seller_list, self.seller_ids = db.selectForList("seller")
        self.client_list, self.client_ids = db.selectForList("client")

        self.service_list_model.setStringList(self.service_list)
        self.product_list_model.setStringList(self.product_list)
        self.seller_list_model.setStringList(self.seller_list)
        self.client_list_model.setStringList(self.client_list)
        self.service_list_model_2.setStringList(self.service_list)
        self.product_list_model_2.setStringList(self.product_list)


    def addProduct(self):
        """Add new product to new order"""
        if (self.lineEditProduct.text() not in self.product_list):
            print("No such product")
            return
        product_idx = self.product_list.index(self.lineEditProduct.text())

        self.tableView.add_detail(["Товар", self.lineEditProduct.text(), self.product_ids[product_idx][2], self.spinBox.text()],
                                  [None, None, self.product_ids[product_idx][0], self.product_ids[product_idx][1], self.spinBox.text()])

    def addService(self):
        """Add new service to new order"""
        if (self.lineEditService.text() not in self.service_list):
            print("No such service")
            return
        service_idx = self.service_list.index(self.lineEditService.text())

        self.tableView.add_detail(
            ["Услуга", self.lineEditService.text(), self.service_ids[service_idx][2], self.spinBox_2.text()],
            [self.service_ids[service_idx][0], self.service_ids[service_idx][1], None, None, self.spinBox_2.text()])

    def addProductToExist(self):
        """Add new product to existing order (tab2)"""
        if (self.lineEditProduct_2.text() not in self.product_list):
            print("No such product")
            return
        product_idx = self.product_list.index(self.lineEditProduct_2.text())

        self.tableWidgetDetailed.add_detail(["Товар", self.lineEditProduct_2.text(), self.product_ids[product_idx][2], self.spinBox_3.text()],
                                  [None, None, self.product_ids[product_idx][0], self.product_ids[product_idx][1], self.spinBox_3.text()])

    def addServiceToExist(self):
        """Add new service to existing order (tab2)"""
        if (self.lineEditService_2.text() not in self.service_list):
            print("No such service")
            return
        service_idx = self.service_list.index(self.lineEditService_2.text())

        self.tableWidgetDetailed.add_detail(
            ["Услуга", self.lineEditService_2.text(), self.service_ids[service_idx][2], self.spinBox_4.text()],
            [self.service_ids[service_idx][0], self.service_ids[service_idx][1], None, None, self.spinBox_4.text()])

    def registerOrder(self):
        """Registers order"""
        if (self.lineEditClient.text() not in self.client_list):
            print("No such product")
            return
        client_idx = self.client_list.index(self.lineEditClient.text())

        if (self.lineEditSeller.text() not in self.seller_list):
            print("No such product")
            return
        seller_idx = self.seller_list.index(self.lineEditSeller.text())

        order_id, details_ids = db.insertOrder(self.client_ids[client_idx], self.seller_ids[seller_idx],
                                               self.dateEdit.text(), self.tableView.data_ids)
        QtWidgets.QMessageBox.about(self, "Заказ Зарегистрирован", "Номер заказа: " + str(order_id))

    def searchExisting(self):
        """Searches existing orders and fills table with them"""
        res = db.searchExistingOrder(self.lineEditId.text(), self.lineEditSur.text())
        columns = ["id_order", "surname_client", "name_client", "phone_number_client", "date_order"]

        self.tableWidgetSearch.setRowCount(0)
        self.tableWidgetSearch.setColumnCount(len(columns))
        self.tableWidgetSearch.setHorizontalHeaderLabels(columns)

        for row_number, row_data in enumerate(res):
            self.tableWidgetSearch.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                new_cell = QtWidgets.QTableWidgetItem(str(data))

                self.tableWidgetSearch.setItem(row_number, column_number, new_cell)

        self.tableWidgetSearch.resizeColumnsToContents()

        self.tableWidgetSearch.clicked.connect(lambda item: self.getSearchDetailed(self.tableWidgetSearch
                                                                                       .item(item.row(), 0)
                                                                                       .text()))

    def getSearchDetailed(self, order_id):
        """Searches for details of order_id and creates table with them"""
        details = db.searchExistingOrderDetailed(order_id)
        self.tableWidgetDetailed.fill(details, order_id)


    def setupUi(self, MainWindow):
        """Creates buttons/fields/etc"""
        MainWindow.resize(685, 715)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(0, 0, 691, 691))
        self.tab = QtWidgets.QWidget()

        self.lineEditProduct = QtWidgets.QLineEdit(self.tab)
        self.lineEditProduct.setGeometry(QtCore.QRect(70, 10, 200, 22))
        self.completerProduct = QtWidgets.QCompleter(self)
        self.completerProduct.setCaseSensitivity(QtCore.Qt.CaseInsensitive)
        self.lineEditProduct.setCompleter(self.completerProduct)
        self.product_list_model = QtCore.QStringListModel()
        self.completerProduct.setModel(self.product_list_model)

        self.lineEditService = QtWidgets.QLineEdit(self.tab)
        self.lineEditService.setGeometry(QtCore.QRect(70, 40, 200, 22))
        self.completerService = QtWidgets.QCompleter(self)
        self.completerService.setCaseSensitivity(QtCore.Qt.CaseInsensitive)
        self.lineEditService.setCompleter(self.completerService)
        self.service_list_model = QtCore.QStringListModel()
        self.completerService.setModel(self.service_list_model)

        self.label = QtWidgets.QLabel(self.tab)
        self.label.setGeometry(QtCore.QRect(10, 10, 51, 21))
        self.label_2 = QtWidgets.QLabel(self.tab)
        self.label_2.setGeometry(QtCore.QRect(290, 10, 61, 21))
        self.label_3 = QtWidgets.QLabel(self.tab)
        self.label_3.setGeometry(QtCore.QRect(10, 40, 47, 21))
        self.label_5 = QtWidgets.QLabel(self.tab)
        self.label_5.setGeometry(QtCore.QRect(290, 40, 61, 21))

        self.dateEdit = QtWidgets.QDateEdit(self.tab)
        self.dateEdit.setGeometry(QtCore.QRect(450, 620, 110, 22))

        self.spinBox = QtWidgets.QSpinBox(self.tab)
        self.spinBox.setGeometry(QtCore.QRect(360, 10, 71, 22))
        self.spinBox.setMaximum(1000000000)
        self.spinBox.setProperty("value", 1)

        self.spinBox_2 = QtWidgets.QSpinBox(self.tab)
        self.spinBox_2.setGeometry(QtCore.QRect(360, 40, 71, 22))
        self.spinBox_2.setMaximum(100000000)
        self.spinBox_2.setProperty("value", 1)

        self.pushButton = QtWidgets.QPushButton(self.tab)
        self.pushButton.setGeometry(QtCore.QRect(440, 10, 75, 23))
        self.pushButton.clicked.connect(self.addProduct)

        self.pushButton_2 = QtWidgets.QPushButton(self.tab)
        self.pushButton_2.setGeometry(QtCore.QRect(440, 40, 75, 23))
        self.pushButton_2.clicked.connect(self.addService)

        self.pushButton_3 = QtWidgets.QPushButton(self.tab)
        self.pushButton_3.setGeometry(QtCore.QRect(590, 620, 75, 23))
        self.pushButton_3.clicked.connect(self.registerOrder)

        self.lineEditSeller = QtWidgets.QLineEdit(self.tab)
        self.lineEditSeller.setGeometry(QtCore.QRect(240, 620, 181, 22))
        self.completerSeller = QtWidgets.QCompleter(self)
        self.completerSeller.setCaseSensitivity(QtCore.Qt.CaseInsensitive)
        self.lineEditSeller.setCompleter(self.completerSeller)
        self.seller_list_model = QtCore.QStringListModel()
        self.completerSeller.setModel(self.seller_list_model)

        self.lineEditClient = QtWidgets.QLineEdit(self.tab)
        self.lineEditClient.setGeometry(QtCore.QRect(20, 620, 191, 22))
        self.completerClient = QtWidgets.QCompleter(self)
        self.completerClient.setCaseSensitivity(QtCore.Qt.CaseInsensitive)
        self.lineEditClient.setCompleter(self.completerClient)
        self.client_list_model = QtCore.QStringListModel()
        self.completerClient.setModel(self.client_list_model)

        self.label_4 = QtWidgets.QLabel(self.tab)
        self.label_4.setGeometry(QtCore.QRect(20, 590, 191, 20))
        self.label_6 = QtWidgets.QLabel(self.tab)
        self.label_6.setGeometry(QtCore.QRect(240, 590, 181, 20))
        self.label_7 = QtWidgets.QLabel(self.tab)
        self.label_7.setGeometry(QtCore.QRect(450, 590, 111, 16))

        self.tableView = NewOrderTable(self.tab)
        self.tableView.setGeometry(QtCore.QRect(10, 80, 661, 501))

        self.tabWidget.addTab(self.tab, "")
        self.tab_3 = QtWidgets.QWidget()

        self.lineEditId = QtWidgets.QLineEdit(self.tab_3)
        self.lineEditId.setGeometry(QtCore.QRect(50, 10, 150, 21))

        self.lineEditSur = QtWidgets.QLineEdit(self.tab_3)
        self.lineEditSur.setGeometry(QtCore.QRect(270, 10, 150, 21))

        self.label_8 = QtWidgets.QLabel(self.tab_3)
        self.label_8.setGeometry(QtCore.QRect(10, 10, 50, 21))
        self.label_9 = QtWidgets.QLabel(self.tab_3)
        self.label_9.setGeometry(QtCore.QRect(220, 10, 50, 21))

        self.pushButton_4 = QtWidgets.QPushButton(self.tab_3)
        self.pushButton_4.setGeometry(QtCore.QRect(450, 10, 75, 21))
        self.pushButton_4.clicked.connect(self.searchExisting)

        self.tableWidgetSearch = QtWidgets.QTableWidget(self.tab_3)
        self.tableWidgetSearch.setGeometry(QtCore.QRect(10, 50, 661, 161))

        self.tableWidgetDetailed = ExistOrderTable(self.tab_3)
        self.tableWidgetDetailed.setGeometry(QtCore.QRect(10, 300, 661, 281))

        self.label_13 = QtWidgets.QLabel(self.tab_3)
        self.label_13.setGeometry(QtCore.QRect(230, 230, 61, 21))

        self.lineEditProduct_2 = QtWidgets.QLineEdit(self.tab_3)
        self.lineEditProduct_2.setGeometry(QtCore.QRect(80, 230, 121, 22))
        self.completerProduct_2 = QtWidgets.QCompleter(self)
        self.completerProduct_2.setCaseSensitivity(QtCore.Qt.CaseInsensitive)
        self.lineEditProduct_2.setCompleter(self.completerProduct_2)
        self.product_list_model_2 = QtCore.QStringListModel()
        self.completerProduct_2.setModel(self.product_list_model_2)

        self.lineEditService_2 = QtWidgets.QLineEdit(self.tab_3)
        self.lineEditService_2.setGeometry(QtCore.QRect(80, 260, 121, 22))
        self.completerService_2 = QtWidgets.QCompleter(self)
        self.completerService_2.setCaseSensitivity(QtCore.Qt.CaseInsensitive)
        self.lineEditService_2.setCompleter(self.completerService_2)
        self.service_list_model_2 = QtCore.QStringListModel()
        self.completerService_2.setModel(self.service_list_model_2)

        self.pushButton_5 = QtWidgets.QPushButton(self.tab_3)
        self.pushButton_5.setGeometry(QtCore.QRect(540, 230, 75, 23))
        self.pushButton_5.setObjectName("ExistAddProduct")
        self.pushButton_5.clicked.connect(self.addProductToExist)

        self.pushButton_7 = QtWidgets.QPushButton(self.tab_3)
        self.pushButton_7.setGeometry(QtCore.QRect(540, 260, 75, 23))
        self.pushButton_7.setObjectName("ExistAddService")
        self.pushButton_7.clicked.connect(self.addServiceToExist)

        self.spinBox_3 = QtWidgets.QSpinBox(self.tab_3)
        self.spinBox_3.setGeometry(QtCore.QRect(300, 230, 71, 22))
        self.spinBox_3.setMaximum(100000000)
        self.spinBox_3.setProperty("value", 1)

        self.spinBox_4 = QtWidgets.QSpinBox(self.tab_3)
        self.spinBox_4.setGeometry(QtCore.QRect(301, 260, 71, 22))
        self.spinBox_4.setMaximum(1000000000)
        self.spinBox_4.setProperty("value", 1)

        self.label_14 = QtWidgets.QLabel(self.tab_3)
        self.label_14.setGeometry(QtCore.QRect(20, 260, 47, 21))
        self.label_15 = QtWidgets.QLabel(self.tab_3)
        self.label_15.setGeometry(QtCore.QRect(20, 230, 51, 21))
        self.label_16 = QtWidgets.QLabel(self.tab_3)
        self.label_16.setGeometry(QtCore.QRect(230, 260, 61, 21))
        self.tabWidget.addTab(self.tab_3, "")

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 685, 21))
        self.menu = QtWidgets.QMenu(self.menubar)
        self.menu_2 = QtWidgets.QMenu(self.menubar)

        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)

        MainWindow.setStatusBar(self.statusbar)
        self.action = QtWidgets.QAction(MainWindow)
        self.action.triggered.connect(lambda x: self.showMenuWindow("add", ["Производитель", "Страна"],
                                                                    "manufacturer"))
        self.action_2 = QtWidgets.QAction(MainWindow)
        self.action_2.triggered.connect(lambda x: self.showMenuWindow("add", ["Материалы(через запятую)", "Производитель", "Название", "Количество", "Цена"],
                                                                      "product"))
        self.action_3 = QtWidgets.QAction(MainWindow)
        self.action_3.triggered.connect(lambda x: self.showMenuWindow("add", ["Фамилия", "Имя", "Отчество", "Номер"],
                                                                      "client"))
        self.action_4 = QtWidgets.QAction(MainWindow)
        self.action_4.triggered.connect(lambda x: self.showMenuWindow("add", ["Фамилия", "Имя", "Отчество", "Номер", "Позиция"],
                                                                      "seller"))
        self.action_5 = QtWidgets.QAction(MainWindow)
        self.action_5.triggered.connect(lambda x: self.showMenuWindow("add", ["Имя Сервиса", "Цена"],
                                                                      "service"))

        self.action_6 = QtWidgets.QAction(MainWindow)
        self.action_6.triggered.connect(lambda x: self.showMenuWindow("remove", ["Производитель"],
                                                                      "manufacturer"))
        self.action_7 = QtWidgets.QAction(MainWindow)
        self.action_7.triggered.connect(lambda x: self.showMenuWindow("remove", ["Название"],
                                                                      "product"))
        self.action_8 = QtWidgets.QAction(MainWindow)
        self.action_8.triggered.connect(lambda x: self.showMenuWindow("remove", ["Фамилия", "Имя", "Отчество"],
                                                                      "client"))
        self.action_9 = QtWidgets.QAction(MainWindow)
        self.action_9.triggered.connect(lambda x: self.showMenuWindow("remove", ["Фамилия", "Имя", "Отчество"],
                                                                      "seller"))
        self.action_10 = QtWidgets.QAction(MainWindow)
        self.action_10.triggered.connect(lambda x: self.showMenuWindow("remove", ["Название"],
                                                                       "service"))

        self.menu.addAction(self.action)
        self.menu.addAction(self.action_2)
        self.menu.addAction(self.action_3)
        self.menu.addAction(self.action_4)
        self.menu.addAction(self.action_5)
        self.menu_2.addAction(self.action_6)
        self.menu_2.addAction(self.action_7)
        self.menu_2.addAction(self.action_8)
        self.menu_2.addAction(self.action_9)
        self.menu_2.addAction(self.action_10)
        self.menubar.addAction(self.menu.menuAction())
        self.menubar.addAction(self.menu_2.menuAction())

        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "Товар"))
        self.label_2.setText(_translate("MainWindow", "Количество"))
        self.label_3.setText(_translate("MainWindow", "Услуга"))
        self.label_5.setText(_translate("MainWindow", "Количество"))
        self.pushButton.setText(_translate("MainWindow", "Добавить"))
        self.pushButton_2.setText(_translate("MainWindow", "Добавить"))
        self.pushButton_3.setText(_translate("MainWindow", "Оформить"))
        self.label_4.setText(_translate("MainWindow", "Клиент"))
        self.label_6.setText(_translate("MainWindow", "Сотрудник"))
        self.label_7.setText(_translate("MainWindow", "Дата"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "Новый заказ"))
        self.label_8.setText(_translate("MainWindow", "Номер"))
        self.pushButton_4.setText(_translate("MainWindow", "Поиск"))
        self.label_9.setText(_translate("MainWindow", "Фамилия"))
        self.pushButton_5.setText(_translate("MainWindow", "Добавить"))
        self.label_13.setText(_translate("MainWindow", "Количество"))
        self.pushButton_7.setText(_translate("MainWindow", "Добавить"))
        self.label_14.setText(_translate("MainWindow", "Услуга"))
        self.label_15.setText(_translate("MainWindow", "Товар"))
        self.label_16.setText(_translate("MainWindow", "Количество"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("MainWindow", "Редактировать заказ"))

        self.menu.setTitle(_translate("MainWindow", "Добавить"))
        self.menu_2.setTitle(_translate("MainWindow", "Редактировать"))

        self.action.setText(_translate("MainWindow", "Производитель"))
        self.action_2.setText(_translate("MainWindow", "Продукт"))
        self.action_3.setText(_translate("MainWindow", "Клиент"))
        self.action_4.setText(_translate("MainWindow", "Продавец"))
        self.action_5.setText(_translate("MainWindow", "Сервис"))
        self.action_6.setText(_translate("MainWindow", "Производитель"))
        self.action_7.setText(_translate("MainWindow", "Продукт"))
        self.action_8.setText(_translate("MainWindow", "Клиент"))
        self.action_9.setText(_translate("MainWindow", "Продавец"))
        self.action_10.setText(_translate("MainWindow", "Сервис"))

        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)


    def showMenuWindow(self, type, fields, entity):
        """Shows window for adding or editing"""
        if (type == "add"):
            self.window = AddWindow(fields, entity)

        else:
            self.window = DeleteWindow(fields, entity)
        self.window.finished.connect(lambda x: self.updateLists())
        self.window.show()