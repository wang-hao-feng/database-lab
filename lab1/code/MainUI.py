import sys
import ERROR
from SQLAPI import SQLSocket
from Ui_Main import Ui_MainWindow
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class MainUI(QMainWindow, Ui_MainWindow):
    def __init__(self, db):
        super().__init__()
        self.setupUi(self)
        self.db = db

        self.student_insert_button.clicked.connect(self.__InsertStudent)
        self.student_delete_button.clicked.connect(self.__DeleteStudent)

        self.course_insert_button.clicked.connect(self.__InsertCourse)
        self.course_delete_button.clicked.connect(self.__DeleteCourse)

        self.take_insert_button.clicked.connect(self.__InsertTake)
        self.take_delete_button.clicked.connect(self.__DeleteTake)

        self.join_query_button.clicked.connect(self.__QueryJoin)
        self.nested_query_button.clicked.connect(self.__QueryNested)
        self.group_query_button.clicked.connect(self.__QueryGroup)

        self.zeromode = QStandardItemModel(0, 0)
        self.mode = None

        self.insert_delete_table.setModel(self.zeromode)
        self.insert_delete_table.horizontalHeader().setStretchLastSection(True)
        self.insert_delete_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
        self.query_table.setModel(self.zeromode)
        self.query_table.horizontalHeader().setStretchLastSection(True)
        self.query_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
    
    def __Critial(self, message):
        QMessageBox.critical(self, "错误", message, QMessageBox.Ok)
    
    #插入删除相关
    def __InsertStudent(self):
        pass

    def __DeleteStudent(self):
        pass

    def __InsertCourse(self):
        pass

    def __DeleteCourse(self):
        pass
    
    def __InsertTake(self):
        pass

    def __DeleteTake(self):
        pass

    #查询相关
    def __QueryJoin(self):
        pass

    def __QueryNested(self):
        pass

    def __QueryGroup(self):
        pass

    #显示
    def __ShowQueryResult(self, table_name:bool, result:list):
        table = self.insert_delete_table if table_name else self.query_table
        if len(result) == 0:
            table.setModel(self.zeromode)
            return
        keys = list(result[0].keys())
        self.mode = QStandardItemModel(len(result), len(keys))
        self.mode.setHorizontalHeaderLabels(keys)

        for i in range(len(result)):
            for j in range(len(keys)):
                self.mode.setItem(i, j, QStandardItem(result[i][keys[j]]))
        
        table.setModel(self.mode)
    
if __name__ == '__main__':
    sql_socket = SQLSocket(password='whf020304', database='school')
    app = QApplication(sys.argv)
    gui = MainUI(sql_socket)
    gui.show()
    sys.exit(app.exec_())