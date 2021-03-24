from PyQt5 import QtWidgets
from widgets import WarningEmptyWidget


class WarningEmptyFieldWindow(QtWidgets.QDialog, WarningEmptyWidget.Ui_Dialog):

    def __init__(self):
        super(WarningEmptyFieldWindow, self).__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.close)

    def close(self):
        self.done(0)
        self.accept()