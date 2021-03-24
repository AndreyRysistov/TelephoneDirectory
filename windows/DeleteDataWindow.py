from PyQt5 import QtWidgets
from windows.WarningWindow import WarningEmptyFieldWindow
from base_windows import delete_data_w
from utils import preparation_data, query


class DeleteDataWindow(QtWidgets.QMainWindow, delete_data_w.Ui_MainWindow):

    def __init__(self, window, connection):
        super().__init__()
        self.setupUi(self)
        self.conn = connection
        self.cursor = self.conn.cursor()
        self.OkButton.clicked.connect(self.delete_data)
        self.ExitButton.clicked.connect(self.close)
        self.main_window = window
        self.warning_window = WarningEmptyFieldWindow()
        self.table = None

    def update_window(self, table):
        self.table = table
        self.DeleteDataBox.clear()
        data = query.select(table=self.table, columns='*', connection=self.conn)
        data = data[data.iloc[:, 1] != '']
        self.DeleteDataBox.addItems([''] + list(data.iloc[:, 1].drop_duplicates().values))
        table_text_dict = {'surnames': 'фамилию', 'names': 'имя', 'streets': 'улицу', 'middle_names': 'отчество'}
        text = f'Выберите {table_text_dict[table]} для удаления*'
        self.label.setText(text)

    def delete_data(self):
        try:
            data = preparation_data.get_text_from_box_w(self.DeleteDataBox)
        except ValueError:
            self.warning_window.show()
            return 0
        column = self.table[:-1] + '_value'

        condition = f"{column} = '{data}'"
        try:
            query.delete(table=self.table, condition=condition, cursor=self.cursor, connection=self.conn)
        except Exception as err:
            print(err)
        self.main_window.update_combo_box()
        self.close()