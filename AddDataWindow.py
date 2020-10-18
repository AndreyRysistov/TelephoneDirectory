from PyQt5 import QtWidgets, QtCore
from WarningWindow import WarningEmptyFieldWindow
import add_window
import query


class AddDataWindow(QtWidgets.QMainWindow, add_window.Ui_MainWindow):

    def __init__(self, window, conn):
        super(AddDataWindow, self).__init__()
        self.setupUi(self)
        self.conn = conn
        self.cursor = self.conn.cursor()
        self.setWindowTitle('Добавление новых данных')
        self.OkButton.clicked.connect(self.add_data)
        self.ExitButton.clicked.connect(self.close)
        self.main_window = window

    def add_data(self):
        try:
            surname = AddDataWindow.get_text_from_edit(self.AddSurnameEdit).capitalize()
            name = AddDataWindow.get_text_from_edit(self.AddNameEdit).capitalize()
            middle_name = AddDataWindow.get_text_from_edit(self.AddMiddleEdit).capitalize()
            street = AddDataWindow.get_text_from_edit(self.AddStreetEdit).capitalize()
            house = AddDataWindow.get_text_from_edit(self.AddHouseEdit)
            corpus = AddDataWindow.get_text_from_edit(self.AddCorpusEdit)
            apartment = AddDataWindow.get_text_from_edit(self.AddApartmentEdit)
            telephone = AddDataWindow.get_text_from_edit(self.AddTelephoneEdit)
        except ValueError:
            self.warning_window = WarningEmptyFieldWindow()
            self.warning_window.show()
            return 0

        query.insert(table='surnames', values=f"(default, '{surname}')", cursor=self.cursor, connection=self.conn)
        query.insert(table='names', values=f"(default, '{name}')", cursor=self.cursor, connection=self.conn)
        query.insert(table='middle_names', values=f"(default, '{middle_name}')", cursor=self.cursor, connection=self.conn)
        query.insert(table='streets', values=f"(default, '{street}')", cursor=self.cursor, connection=self.conn)

        surnames = query.select(table='surnames', columns='*', connection=self.conn)
        surname_id = surnames[surnames.surname_value == surname].surname_id.values[0]
        names = query.select(table='names', columns='*', connection=self.conn)
        name_id = names[names.name_value == name].name_id.values[0]
        middle_names = query.select(table='middle_names', columns='*', connection=self.conn)
        middle_name_id = middle_names[middle_names.middle_name_value == middle_name].middle_name_id.values[0]
        streets = query.select(table='streets', columns='*', connection=self.conn)
        street_id = streets[streets.street_value == street].street_id.values[0]
        try:
            query.insert(table='main (id, surname, name, middle_name, street, house, corp, apartment, telephone)',
                         values=f"""(default, {surname_id}, {name_id}, {middle_name_id}, {street_id}, {house}, {corpus}, {apartment},{telephone})""",
                         cursor=self.cursor,
                         connection=self.conn)
        except Exception:
            pass
        self.main_window.update_combo_box()


    @staticmethod
    def get_text_from_edit(box):
        text = box.text()
        if len(text) > 0:
            return text
        else:
            raise ValueError

