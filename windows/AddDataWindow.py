from PyQt5 import QtWidgets
from windows.WarningWindow import WarningEmptyFieldWindow
from base_windows import add_data_w
from utils import preparation_data, query


class AddDataWindow(QtWidgets.QMainWindow, add_data_w.Ui_MainWindow):

    def __init__(self, window, connection):
        super(AddDataWindow, self).__init__()
        self.setupUi(self)
        self.conn = connection
        self.cursor = self.conn.cursor()
        self.OkButton.clicked.connect(self.add_data)
        self.ExitButton.clicked.connect(self.close)
        self.main_window = window
        self.warning_window = WarningEmptyFieldWindow()
        self.table = None

    def update_window(self, table):
        self.table = table
        table_text_dict = {'surnames': 'фамилию', 'names': 'имя', 'streets': 'улицу', 'middle_names': 'отчество'}
        text = f'Введите {table_text_dict[table]} для добавления*'
        self.label.setText(text)

    def add_data(self):
        try:
            data = preparation_data.get_text_from_edit_w(self.AddDataEdit).capitalize()
        except ValueError:
            self.warning_window.show()
            return 0
        df = query.select(table=self.table, columns='*', connection=self.conn).iloc[:, 1:]
        if data not in df.values:
            try:
                query.insert(table=self.table, values=f"(default, '{data}')", cursor=self.cursor, connection=self.conn)
            except Exception as err:
                print(err)
        self.main_window.update_combo_box()
        self.close()
