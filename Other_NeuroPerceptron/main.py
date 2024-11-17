from PyQt5 import QtWidgets
from controller import WindowController

if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = WindowController()
    window.show()
    sys.exit(app.exec_())
