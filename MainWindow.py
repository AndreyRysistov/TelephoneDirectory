from PyQt5 import QtWidgets
from AddDataWindow import AddDataWindow
from DeleteDataWindow import DeleteDataWindow
from UpdateDataWindow import UpdateDataWindow
from WarningWindow import WarningEmptyFieldWindow
import main_window
import query
import pyodbc
import preparation_data


class MainWindow(QtWidgets.QMainWindow, main_window.Ui_MainWindow):

    def __init__(self):
        super().__init__()
        self.conn = pyodbc.connect('DSN=mydb')
        self.cursor = self.conn.cursor()
        self.setupUi(self)
        self.setWindowTitle('Телефонный справочник')

        self.add_window = AddDataWindow(window=self, connection=self.conn)
        self.delete_window = DeleteDataWindow(window=self, connection=self.conn)
        self.update_window = UpdateDataWindow(window=self, connection=self.conn)
        self.warning_window = WarningEmptyFieldWindow()

        self.FindButton.clicked.connect(self.find_function)
        self.AddButton.clicked.connect(self.add_function)
        self.DeleteButton.clicked.connect(self.delete_function)
        self.UpdateButton.clicked.connect(self.update_function)
        self.ClearButton.clicked.connect(self.clear_function)

        self.SurnameAddButton.clicked.connect(lambda x, table='surnames': self.plus_function(table))
        self.NameAddButton.clicked.connect(lambda x, table='names': self.plus_function(table))
        self.MiddleNameAddButton.clicked.connect(lambda x, table='middle_names': self.plus_function(table))
        self.StreetAddButton.clicked.connect(lambda x, table='streets': self.plus_function(table))

        self.SurnameDeleteButton.clicked.connect(lambda x, table='surnames': self.minus_function(table))
        self.NameDeleteButton.clicked.connect(lambda x, table='names': self.minus_function(table))
        self.MiddleNameDeleteButton.clicked.connect(lambda x, table='middle_names': self.minus_function(table))
        self.StreetDeleteButton.clicked.connect(lambda x, table='streets': self.minus_function(table))

        self.SurnameUpdateButton.clicked.connect(lambda x, table='surnames': self.change_function(table))
        self.NameUpdateButton.clicked.connect(lambda x, table='names': self.change_function(table))
        self.MiddleNameUpdateButton.clicked.connect(lambda x, table='middle_names': self.change_function(table))
        self.StreetUpdateButton.clicked.connect(lambda x, table='streets': self.change_function(table))
        self.update_combo_box()

    def plus_function(self, table):
        self.add_window.update_window(table)
        self.add_window.show()

    def minus_function(self, table):
        self.delete_window.update_window(table)
        self.delete_window.show()

    def change_function(self, table):
        self.update_window.update_window(table)
        self.update_window.show()

    def update_function(self):
        pass

    def find_function(self):
        data = self._get_data()
        name = preparation_data.get_text_from_box(self.NameBox)
        surname = preparation_data.get_text_from_box(self.SurnameBox)
        middle_name = preparation_data.get_text_from_box(self.MiddleNameBox)
        street = preparation_data.get_text_from_box(self.StreetBox)
        telephone = preparation_data.get_text_from_edit(self.TelephoneEdit)
        house = int(self.HouseEdit.text()) if len(self.HouseEdit.text()) > 0 else 'NULL'
        corpus = int(self.CorpusEdit.text()) if len(self.CorpusEdit.text()) > 0 else 'NULL'
        apartment = int(self.ApartamentEdit.text()) if len(self.ApartamentEdit.text()) > 0 else 'NULL'
        box_text_list = [name, surname, middle_name, street, house, apartment, corpus, telephone]
        columns_name = list(data.columns)
        query_text = ''
        for col_name, box_text in zip(columns_name, box_text_list):
            if box_text is '' or box_text is 'NULL':
                continue
            else:
                if type(box_text) is str:
                    query_part = f"({col_name} == '{box_text}')"
                else:
                    query_part = f"({col_name} == {box_text})"
                query_text += query_part + '&'
        if len(query_text) > 0:
            target_data = data.query(query_text[:-1])
        else:
            target_data = data
        self._view_table(target_data)

    def add_function(self):
        try:
            name = preparation_data.get_text_from_box_w(self.NameBox)
            surname = preparation_data.get_text_from_box_w(self.SurnameBox)
            middle_name = preparation_data.get_text_from_box_w(self.MiddleNameBox)
            street = preparation_data.get_text_from_box_w(self.StreetBox)
            telephone = preparation_data.get_text_from_edit_w(self.TelephoneEdit)
            house = preparation_data.get_text_from_edit_w(self.HouseEdit)
            corpus = preparation_data.get_text_from_edit(self.CorpusEdit)
            apartment = preparation_data.get_text_from_edit(self.ApartamentEdit)
        except ValueError:
            self.warning_window.show()
            return 0
        try:
            surnames = query.select(table='surnames', columns='*', connection=self.conn)
            surname_id = surnames[surnames.surname_value == surname].surname_id.values[0]
            names = query.select(table='names', columns='*', connection=self.conn)
            name_id = names[names.name_value == name].name_id.values[0]
            middle_names = query.select(table='middle_names', columns='*', connection=self.conn)
            middle_name_id = middle_names[middle_names.middle_name_value == middle_name].middle_name_id.values[0]
            streets = query.select(table='streets', columns='*', connection=self.conn)
            street_id = streets[streets.street_value == street].street_id.values[0]
            query.insert(table='main (id, surname, name, middle_name, street, house, corp, apartment, telephone)',
                         values=f"""(default, {surname_id}, {name_id}, {middle_name_id}, {street_id}, {house}, {corpus}, {apartment},{telephone})""",
                         cursor=self.cursor,
                         connection=self.conn)
        except Exception as err:
            print(err)

    def delete_function(self):
        try:
            row = self.tableWidget.currentRow()
            items = [self.tableWidget.item(row, col).text() for col in range(0, 8)]
            name_id = query.select(table='names', columns='name_id', condition=f"name_value = '{items[0]}'", connection=self.conn).values[0,0]
            surname_id = query.select(table='surnames', columns='surname_id', condition=f"surname_value = '{items[1]}'", connection=self.conn).values[0,0]
            middle_name_id = query.select(table='middle_names', columns='middle_name_id', condition=f"middle_name_value = '{items[2]}'", connection=self.conn).values[0,0]
            street_id = query.select(table='streets', columns='street_id', condition=f"street_value = '{items[3]}'", connection=self.conn).values[0,0]
            house = int(items[4]) if items[4] is not '' else 'NULL'
            apartment = int(items[5]) if items[5] is not '' else 'NULL'
            corp = int(items[6]) if items[6] is not '' else 'NULL'
            telephone = items[7]
            condition = f"""name = {name_id} and surname = {surname_id} and middle_name = {middle_name_id}
                            and street = {street_id} and house = {house} and corp = {corp}
                            and apartment = {apartment} and telephone = '{telephone}' """
            query.delete(table='main', condition=condition, cursor=self.cursor, connection=self.conn)
            data = self._get_data()
            self._view_table(data)
        except Exception as err:
            print(err)

    def clear_function(self):
        self.HouseEdit.clear()
        self.ApartamentEdit.clear()
        self.CorpusEdit.clear()
        self.TelephoneEdit.clear()
        self.update_combo_box()

    def update_combo_box(self):
        self.NameBox.clear()
        self.SurnameBox.clear()
        self.MiddleNameBox.clear()
        self.StreetBox.clear()
        try:
            names = query.select(table='names', columns='*', connection=self.conn)
            names = names[names.name_value != '']
            self.NameBox.addItems([''] + list(names.name_value.drop_duplicates().values))
            surnames = query.select(table='surnames', columns='*', connection=self.conn)
            surnames = surnames[surnames.surname_value != '']
            self.SurnameBox.addItems([''] + list(surnames.surname_value.drop_duplicates().values))
            middle_names = query.select(table='middle_names', columns='*', connection=self.conn)
            middle_names = middle_names[middle_names.middle_name_value != '']
            self.MiddleNameBox.addItems([''] + list(middle_names.middle_name_value.drop_duplicates().values))
            streets = query.select(table='streets', columns='*', connection=self.conn)
            streets = streets[streets.street_value != '']
            self.StreetBox.addItems([''] + list(streets.street_value.drop_duplicates().values))
        except Exception as err:
            print(err)

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
        self.tableWidget.setRowCount(0)
        for n, row in zip(range(0, data.shape[0]), data.values):
            self.tableWidget.insertRow(self.tableWidget.rowCount())
            for m in range(0, 8):
                item = QtWidgets.QTableWidgetItem(str(row[m]))
                self.tableWidget.setItem(int(n), int(m), item)