from PyQt5 import QtWidgets
from login_form import LoginForm
from main_window import MainWindow
from connection import db

import sys




def main():
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication

    # показываем окно
    login_window = LoginForm()
    main = MainWindow()
    # подключаем функцию обработчик, запускающий окно, к сигналу, когда логин произойдет
    login_window.logined.connect(lambda x: main.init())
    login_window.show()  # Показываем окно

    app.exec_()  # и запускаем приложение



if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    main()  # то запускаем функцию main()
