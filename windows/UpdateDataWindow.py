from PyQt5 import QtWidgets
from windows.WarningWindow import WarningEmptyFieldWindow
from base_windows import update_data_w_2
from utils import preparation_data, query


class UpdateDataWindow(QtWidgets.QMainWindow, update_data_w_2.Ui_MainWindow):

    def __init__(self, window, connection):
        super(UpdateDataWindow, self).__init__()
        self.setupUi(self)
        self.conn = connection
        self.cursor = self.conn.cursor()
        self.OkButton.clicked.connect(self.update_data)
        self.ExitButton.clicked.connect(self.close)
        self.main_window = window
        self.warning_window = WarningEmptyFieldWindow()
        self.table = None

    def update_window(self, table):
        self.table = table
        self.UpdateDataBox.clear()
        self.UpdateDataEdit.clear()
        data = query.select(table=self.table, columns='*', connection=self.conn)
        data = data[data.iloc[:, 1] != '']
        self.UpdateDataBox.addItems([''] + list(data.iloc[:, 1].drop_duplicates().values))
        table_text_dict = {'surnames': 'фамилию', 'names': 'имя', 'streets': 'улицу', 'middle_names': 'отчество'}
        text = f'Выберите {table_text_dict[table]} и введите новые данные*'
        self.label.setText(text)

    def update_data(self):
        try:
            current_value = preparation_data.get_text_from_box_w(self.UpdateDataBox)
            new_value = preparation_data.get_text_from_edit_w(self.UpdateDataEdit)
        except ValueError:
            self.warning_window.show()
            return 0
        column = self.table[:-1] + '_value'
        new_values = f"{column} = '{new_value}'"
        condition = f"{column} = '{current_value}'"
        try:
            query.update(table=self.table, new_values=new_values, condition=condition, cursor=self.cursor,
                         connection=self.conn)
        except Exception as err:
            print(err)
        self.main_window.update_combo_box()
        self.close()
