import sys
from random import randint
from PyQt5.QtWidgets import QApplication

from LoginUI import LoginUI

if __name__ == '__main__':
    app = QApplication(sys.argv)
    gui = LoginUI()
    gui.show()
    sys.exit(app.exec_())