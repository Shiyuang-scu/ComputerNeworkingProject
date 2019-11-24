from SHOW.MainWindow_SLOT import MainWindow_SLOT
from PyQt5 import QtWidgets
import sys

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow_SLOT()
    window.show()
    sys.exit(app.exec_())
