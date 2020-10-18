from PyQt5 import QtWidgets
from AddDataWindow import AddDataWindow
from DeleteDataWindow import DeleteDataWindow
import main_window
import query
import pyodbc


class MainWindow(QtWidgets.QMainWindow, main_window.Ui_MainWindow):

    def __init__(self):
        super().__init__()
        self.conn = pyodbc.connect('DSN=mydb')
        self.setupUi(self)
        self.setWindowTitle('Телефонный справочник')
        self.FindButton.clicked.connect(self.find_function)
        self.AddButton.clicked.connect(self.add_function)
        self.DeleteButton.clicked.connect(self.delete_function)
        self.PrintButton.clicked.connect(self.print_function)
        self.add_window = AddDataWindow(self, self.conn)
        self.delete_window = DeleteDataWindow(self, self.conn)
        self._update_combo_box()

    def find_function(self):
        self.tableWidget.setRowCount(0)
        data = self._get_data()
        box_text_list = [self.NameBox.currentText(), self.SurnameBox.currentText(), self.MiddleNameBox.currentText(),
                         self.StreetBox.currentText(), self.HouseEdit.text(), self.CorpusEdit.text(),
                         self.ApartamentEdit.text(), self.TelephoneEdit.text()
                         ]
        columns_name = list(data.columns)
        query_text = ''
        for col_name, box_text in zip(columns_name, box_text_list):
            if box_text == '':
                continue
            else:
                query_part = f"({col_name} == '{box_text}')"
                query_text += query_part + '&'
        if len(query_text) > 0:
            target_data = data.query(query_text[:-1])
        else:
            target_data = data
        self._view_table(target_data)

    def add_function(self):
        self.add_window.show()

    def delete_function(self):
        self.delete_window.show()

    def print_function(self):
        pass

    def _update_combo_box(self):
        data = self._get_data()
        self.NameBox.addItems([''] + list(data['name_value'].drop_duplicates().values))
        self.SurnameBox.addItems([''] + list(data['surname_value'].drop_duplicates().values))
        self.StreetBox.addItems([''] + list(data['street_value'].drop_duplicates().values))
        self.MiddleNameBox.addItems([''] + list(data['middle_name_value'].drop_duplicates().values))

    def _get_data(self):
        table = """ main
                    join names on main.name = names.name_id
                    join surnames on main.surname = surnames.surname_id
                    join middle_names on main.middle_name = middle_names.middle_name_id
                    join streets on main.street = streets.street_id
                """
        columns = """name_value, surname_value, middle_name_value, street_value, house, apartment,corp, telephone"""
        data = query.select(table, columns, self.conn)
        data.drop_duplicates(subset=['telephone'], inplace=True)
        data = data[(data.surname_value != '') & (data.name_value != '') & (data.middle_name_value != '') \
                    & (data.street_value != '') & (data.telephone != '')]
        return data

    def _view_table(self, data):
        for n, row in zip(range(0, data.shape[0]), data.values):
            self.tableWidget.insertRow(self.tableWidget.rowCount())
            for m in range(0, 8):
                item = QtWidgets.QTableWidgetItem(str(row[m]).replace(' ', ''))
                self.tableWidget.setItem(int(n), int(m), item)
