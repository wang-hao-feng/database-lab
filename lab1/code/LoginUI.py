import re
import ERROR
from SQLAPI import SQLSocket
from Ui_Login import Ui_MainWindow
from PyQt5.QtSql import QSqlDatabase
from PyQt5.QtWidgets import QMainWindow, QMessageBox

from MainUI import MainUI

class LoginUI(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.socket = SQLSocket()
        self.db = QSqlDatabase.addDatabase("QMYSQL")

        self.login_button.clicked.connect(self.__Login)
    
    def __Login(self):
        self.socket.host = self.IP_text.text()
        self.socket.user = self.user_text.text()
        self.socket.password = self.password_text.text()
        self.socket.database = self.database_text.text()

        if self.socket.host == '':
            self.__Critial('服务器IP不能为空')
            return
        elif not self.__IsIPv4(self.socket.host) and self.socket.host != 'localhost':
            self.__Critial('服务器IP必须为localhost或点分十进制形式')
            return
        elif self.socket.user == '':
            self.__Critial('用户名不能为空')
            return
        elif self.socket.database == '':
            self.__Critial('数据库名称不能为空')
            return
        

        error = self.socket.Connect()

        if error == ERROR.HOST_ERROR:
            self.__Critial('连接超时，请检查服务器ip是否正确')
            return
        elif error == ERROR.USER_OR_PASSWORD_ERROR:
            self.__Critial('用户名或密码错误')
            return
        elif error == ERROR.DATABASE_ERROR:
            self.__Critial('数据库不存在')
            return
        
        self.main_ui = MainUI(self.db)
        self.main_ui.show()
        self.close()

    
    def __Critial(self, message):
        QMessageBox.critical(self, "错误", message, QMessageBox.Ok)
    
    def __IsIPv4(self, ip):
        pattern = r'((0|1\d{0,2}|[3-9]\d?|2([6-9]|[0-4]\d?|5[0-5]?)?)\.){3}(0|1\d{0,2}|[3-9]\d?|2([6-9]|[0-4]\d?|5[0-5]?)?)'
        if re.match(pattern, ip) == None:
            return False
        return True