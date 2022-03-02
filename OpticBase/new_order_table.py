from PyQt5 import QtWidgets, QtCore


class NewOrderTable(QtWidgets.QTableWidget):
    """Table for details of new order"""
    def __init__(self, parent):
        super().__init__(parent)

        self.resizeColumnsToContents()
        columns = ["Тип", "Позиция", "Цена", "Количество"]
        self.setColumnCount(len(columns))
        self.setHorizontalHeaderLabels(columns)

        self.data_ids = []


    def add_detail(self, new_odrer, new_order_ids):
        """Add position(detail) to order"""
        self.data_ids.append(new_order_ids)

        self.insertRow(self.rowCount())
        for column_number, data in enumerate(new_odrer):
            new_cell = QtWidgets.QTableWidgetItem(str(data))
            self.setItem(self.rowCount() - 1, column_number, new_cell)


    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Delete:
            row = self.currentRow()
            self.removeRow(row)
            self.data_ids.pop(row)
        else:
            super().keyPressEvent(event)
