from PyQt5 import QtWidgets, QtCore
from WarningWindow import WarningEmptyFieldWindow
import update_data_without_table_window
import query
import preparation_data


class UpdateDataWithoutTableWindow(QtWidgets.QMainWindow, update_data_without_table_window.Ui_MainWindow):

    def __init__(self, window, connection):
        super(UpdateDataWithoutTableWindow, self).__init__()
        self.setupUi(self)
        self.conn = connection
        self.cursor = self.conn.cursor()
        self.OkButton.clicked.connect(self.update_data)
        self.ExitButton.clicked.connect(self.close)
        self.main_window = window
        self.warning_window = WarningEmptyFieldWindow()
        self.column = None
        self.id_value = None

    def update_window(self, column, value, id_value):
        self.column = column
        self.id_value = id_value
        columns_text_dict = {'house': 'дом', 'corp': 'корпус', 'apartment': 'квартиру', 'telephone': 'телефон'}
        text = f'Выберите {columns_text_dict[column]} и введите новые данные*'
        self.NewValueEdit.clear()
        self.CurrentValueLabel.setText(value)
        self.label.setText(text)

    def update_data(self):
        try:
            new_value = preparation_data.get_text_from_edit_w(self.NewValueEdit)
        except ValueError:
            self.warning_window.show()
            return 0
        try:
            query.update(table='main', new_values=f"{self.column}={new_value}", condition=f"id = '{self.id_value}'",
                         cursor=self.cursor, connection=self.conn)
        except Exception as err:
            print(err)
        data = self.main_window._get_data()
        self.main_window._view_table(data)
        self.close()