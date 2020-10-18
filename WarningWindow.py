from PyQt5 import QtWidgets
import warning_empty_fields_widget


class WarningEmptyFieldWindow(QtWidgets.QDialog, warning_empty_fields_widget.Ui_Dialog):

    def __init__(self):
        super(WarningEmptyFieldWindow, self).__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.close)

    def close(self):
        self.done(0)
        self.accept()