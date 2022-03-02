from PyQt5 import QtWidgets, QtCore
from connection import db

class ExistOrderTable(QtWidgets.QTableWidget):
    """
    Table of existing order details
    """
    def __init__(self, parent):
        super().__init__(parent)

        self.resizeColumnsToContents()
        self.setRowCount(0)
        columns = ["ID", "Тип", "Позиция", "Цена", "Количество"]
        self.setColumnCount(len(columns))
        self.setHorizontalHeaderLabels(columns)


    def fill(self, res, order_id):
        """Fills table with res list of lists"""
        self.order_id = order_id
        self.setRowCount(0)
        for row_number, row_data in enumerate(res):
            self.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                new_cell = QtWidgets.QTableWidgetItem(str(data))
                new_cell.setFlags(QtCore.Qt.ItemIsEnabled)
                self.setItem(row_number, column_number, new_cell)


    def add_detail(self, new_odrer, new_order_ids):
        """Add position(detail) to order"""
        self.insertRow(self.rowCount())
        detail_id = db.insertDetail(self.order_id, new_order_ids)
        new_odrer = [detail_id] + new_odrer
        for column_number, data in enumerate(new_odrer):
            new_cell = QtWidgets.QTableWidgetItem(str(data))
            self.setItem(self.rowCount() - 1, column_number, new_cell)




    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Delete:
            row = self.currentRow()
            detail_id = self.item(self.currentRow(), 0).text()
            self.removeRow(row)
            db.deleteById(detail_id, "detail")
        else:
            super().keyPressEvent(event)
