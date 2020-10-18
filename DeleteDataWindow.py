from PyQt5 import QtWidgets
import delete_window
import query


class DeleteDataWindow(QtWidgets.QMainWindow, delete_window.Ui_MainWindow):

    def __init__(self, window, connection):
        super().__init__()
        self.setupUi(self)
        self.conn = connection
        self.cursor = self.conn.cursor()
        self.setWindowTitle('Удаление данных')
        self.OkButton.clicked.connect(self.delete_data)
        self.ExitButton.clicked.connect(self.close)
        self.main_window = window

    def delete_data(self):
        self.surname = self.SurnameBox.currentText()
        self.name = self.NameBox.currentText()
        self.middle_name = self.MiddleNameBox.currentText()
        self.telephone = self.TelephoneBox.currentText()
