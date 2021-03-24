from PyQt5 import QtWidgets
from windows.WarningWindow import WarningEmptyFieldWindow
from base_windows import update_data_w_3
from utils import preparation_data, query


class UpdateDataWithTableWindow(QtWidgets.QMainWindow, update_data_w_3.Ui_MainWindow):

    def __init__(self, window, connection):
        super(UpdateDataWithTableWindow, self).__init__()
        self.setupUi(self)
        self.conn = connection
        self.cursor = self.conn.cursor()
        self.OkButton.clicked.connect(self.update_data)
        self.ExitButton.clicked.connect(self.close)
        self.main_window = window
        self.warning_window = WarningEmptyFieldWindow()
        self.table = None
        self.id_value = None
        self.column = None

    def update_window(self, column, value, id_value):

        self.column = column
        self.table = self.column.split('_value')[0] + 's'
        self.id_value = id_value
        table_text_dict = {'surnames': 'фамилию', 'names': 'имя', 'streets': 'улицу', 'middle_names': 'отчество'}
        text = f'Выберите {table_text_dict[self.table]} и введите новые данные*'
        self.UpdateDataBox.clear()
        self.CurrentValueLabel.setText(value)
        self.label.setText(text)
        data = query.select(table=self.table, columns='*', connection=self.conn)
        data = data[data.iloc[:, 1] != '']
        self.UpdateDataBox.addItems([''] + list(data.iloc[:, 1].drop_duplicates().values))

    def update_data(self):
        try:
            new_value = preparation_data.get_text_from_box_w(self.UpdateDataBox)
        except ValueError:
            self.warning_window.show()
            return 0
        try:
            new_value = query.select(table=self.table, columns='*', condition=f"{self.column} = '{new_value}'",
                                     connection=self.conn).iloc[0, 0]
            column_in_main = self.column.split('_value')[0]
            query.update(table='main', new_values=f"{column_in_main}={new_value}", condition=f"id = {self.id_value}",
                         cursor=self.cursor, connection=self.conn)
        except Exception as err:
            print(err)
        data = self.main_window._get_data()
        self.main_window._view_table(data)
        self.close()