import os
import sys
import ERROR
from Ui_Main import Ui_MainWindow
from PyQt5.QtGui import QIcon, QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QHeaderView

class MainUI(QMainWindow, Ui_MainWindow):
    def __init__(self, sql_socket):
        super().__init__()
        self.setupUi(self)
        self.__sql_socket = sql_socket
        self.updated = False

        ico_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), './images/avatar_32x32.ico')
        self.setWindowIcon(QIcon(ico_path))

        self.student_insert_button.clicked.connect(self.__InsertStudent)
        self.student_delete_button.clicked.connect(self.__DeleteStudent)

        self.course_insert_button.clicked.connect(self.__InsertCourse)
        self.course_delete_button.clicked.connect(self.__DeleteCourse)

        self.take_insert_button.clicked.connect(self.__InsertTake)
        self.take_delete_button.clicked.connect(self.__DeleteTake)

        self.join_query_button.clicked.connect(self.__QueryJoin)
        self.nested_query_button.clicked.connect(self.__QueryNested)
        self.group_query_button.clicked.connect(self.__QueryGroup)

        self.commit.triggered.connect(self.__Commit)
        self.rollback.triggered.connect(self.__Rollback)

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
        number = self.student_number_text.text()
        name = self.student_name_text.text()
        age = self.student_age_text.text()
        sex = self.student_sex_text.text()
        grade = self.student_grade_text.text()

        if number == '':
            self.__Critial('学号不能为空')
            return
        elif name == '':
            self.__Critial('姓名不能为空')
            return
        if age != '':
            try:
                age = int(age)
            except Exception:
                self.__Critial('年龄必须为数字')
                return
            if age < 0 or age > 150:
                self.__Critial('年龄必须介于0到150之间')
                return
        if sex != '' and sex != '男' and sex != '女':
            self.__Critial('性别必须为‘男’或者‘女’')
        if grade != '' and grade != '大一' and grade != '大二' and grade != '大三' and grade != '大四':
            self.__Critial('年纪必须为‘大一’、‘大二’、‘大三’、‘大四’中的一个')
        
        attr_list = '学号, 姓名'
        value = '\"{0}\", \"{1}\"'.format(number, name)

        if age != '':
            attr_list += ', 年龄'
            value += ', \"{0}\"'.format(age)
        if sex != '':
            attr_list += ', 性别'
            value += ', \"{0}\"'.format(sex)
        if grade != '':
            attr_list += ', 年级'
            value += ', \"{0}\"'.format(grade)

        query = 'INSERT INTO 学生({0}) VALUES ({1})'.format(attr_list, value)
        
        error = self.__sql_socket.Insert(query)

        if error == ERROR.TABELE_NOT_EXIST:
            self.__Critial('插入的表不存在')
        elif error == ERROR.INSERT_VALUE_ERROR:
            self.__Critial('插入数据有误')
        elif error == ERROR.DUPLICATE_ENTRY_ERROR:
            self.__Critial('该记录已存在')
        elif error == ERROR.ACCEPT:
            self.updated = True

        result = self.__sql_socket.Query('SELECT * FROM 学生')

        self.__ShowQueryResult(True, result)

    def __DeleteStudent(self):
        number = self.student_number_text.text()

        if number == '':
            self.__Critial('学号不能为空')
            return
        
        query = 'DELETE FROM {0} WHERE {1}'.format('学生',
                                                    '学号 = \"{0}\"'.format(number))
        
        error = self.__sql_socket.Delete(query)

        if error == ERROR.DELETE_OR_UPDATE_PARENT_ROW:
            self.__Critial('此记录与其他表相关联，请先删除关联记录')
        elif error == ERROR.ACCEPT:
            self.updated = True

        result = self.__sql_socket.Query('SELECT * FROM 学生')

        self.__ShowQueryResult(True, result)

    def __InsertCourse(self):
        number = self.course_number_text.text()
        name = self.course_name_text.text()

        if number == '':
            self.__Critial('课程号不能为空')
            return
        elif name == '':
            self.__Critial('课程名不能为空')
            return

        query = 'INSERT INTO 课程 VALUES (\"{0}\", \"{1}\")'.format(number, name)
        
        error = self.__sql_socket.Insert(query)

        if error == ERROR.TABELE_NOT_EXIST:
            self.__Critial('插入的表不存在')
        elif error == ERROR.INSERT_VALUE_ERROR:
            self.__Critial('插入数据有误')
        elif error == ERROR.DUPLICATE_ENTRY_ERROR:
            self.__Critial('该记录已存在')
        elif error == ERROR.ACCEPT:
            self.updated = True

        result = self.__sql_socket.Query('SELECT * FROM 课程')

        self.__ShowQueryResult(True, result)

    def __DeleteCourse(self):
        number = self.course_number_text.text()

        if number == '':
            self.__Critial('课程号不能为空')
            return
        
        query = 'DELETE FROM {0} WHERE {1}'.format('课程',
                                                    '课程号 = \"{0}\"'.format(number))
        
        error = self.__sql_socket.Delete(query)

        if error == ERROR.DELETE_OR_UPDATE_PARENT_ROW:
            self.__Critial('此记录与其他表相关联，请先删除关联记录')
        elif error == ERROR.ACCEPT:
            self.updated = True

        result = self.__sql_socket.Query('SELECT * FROM 课程')

        self.__ShowQueryResult(True, result)
    
    def __InsertTake(self):
        student = self.take_student_text.text()
        course = self.take_course_text.text()
        grade = self.take_grade_text.text()

        if student == '':
            self.__Critial('学号不能为空')
            return
        elif course == '':
            self.__Critial('课程号不能为空')
            return
        elif grade != '':
            try:
                grade = int(grade)
            except Exception:
                self.__Critial('成绩必须为数字')
                return
            if grade < 0 or grade > 100:
                self.__Critial('成绩必须介于0到100之间')
                return
        
        query = 'INSERT INTO 选修 VALUES (\"{0}\", \"{1}\", \"{2}\")'.format(student, course, grade)
        
        error = self.__sql_socket.Insert(query)

        if error == ERROR.TABELE_NOT_EXIST:
            self.__Critial('插入的表不存在')
        elif error == ERROR.INSERT_VALUE_ERROR:
            self.__Critial('插入数据有误')
        elif error == ERROR.DUPLICATE_ENTRY_ERROR:
            self.__Critial('该记录已存在')
        elif error == ERROR.FOREGIN_KEY_NOT_SATISFY_ERROR:
            self.__Critial('学号和课程号不满足外键约束')
        elif error == ERROR.ACCEPT:
            self.updated = True

        result = self.__sql_socket.Query('SELECT * FROM 选修')

        self.__ShowQueryResult(True, result)

    def __DeleteTake(self):
        student = self.take_student_text.text()
        course = self.take_course_text.text()

        if student == '':
            self.__Critial('学号不能为空')
            return
        elif course == '':
            self.__Critial('课程号不能为空')
            return

        query = 'DELETE FROM {0} WHERE {1}'.format('选修',
                                                    '学号 = \"{0}\" AND 课程号 = \"{1}\"'.format(student, course))
        
        error = self.__sql_socket.Delete(query)

        if error == ERROR.DELETE_OR_UPDATE_PARENT_ROW:
            self.__Critial('此记录与其他表相关联，请先删除关联记录')
        elif error == ERROR.ACCEPT:
            self.updated = True

        result = self.__sql_socket.Query('SELECT * FROM 选修')

        self.__ShowQueryResult(True, result)


    #查询相关
    def __QueryJoin(self):
        student_number = self.join_text.text()
        if student_number == '':
            self.__Critial('学号不能为空')
        query = 'SELECT {0} FROM {1} WHERE {2}'.format('学号, 姓名, 课程号, 课程名',
                                                        '学生 NATURAL JOIN 选修 NATURAL JOIN 课程', 
                                                        '学号 = \"{0}\"'.format(student_number))
        result = self.__sql_socket.Query(query)
        if len(result) == 0:
            self.__Critial('学号不存在')
        self.__ShowQueryResult(False, result)

    def __QueryNested(self):
        in_school_query = 'SELECT {0} FROM {1}'.format('学号',
                                                        '学生 NATURAL JOIN 住宿')
        query = 'SELECT {0} FROM {1} WHERE {2}'.format('学号, 姓名, 性别, 年级',
                                                        '学生',
                                                        '学号 NOT IN ({0})'.format(in_school_query))
        result = self.sql_socket.Query(query)
        self.__ShowQueryResult(False, result)

    def __QueryGroup(self):
        number_of_student = self.group_text.text()
        if number_of_student == '':
            self.__Critial('人数不能为空')
            return
        try:
            number_of_student = int(number_of_student)
        except Exception:
            self.__Critial('非法数字')
        query = 'SELECT {0} FROM {1} GROUP BY {2} HAVING {3}'.format('社团代码, 社团名',
                                                                    '参加 NATURAL JOIN 社团',
                                                                    '社团代码', 
                                                                    'COUNT(学号) > {0}'.format(number_of_student))
        result = self.__sql_socket.Query(query)
        self.__ShowQueryResult(False, result)

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
                self.mode.setItem(i, j, QStandardItem(str(result[i][keys[j]])))
        
        table.setModel(self.mode)
    
    def __Commit(self):
        self.__sql_socket.Commit()
        self.insert_delete_table.setModel(self.zeromode)
        self.query_table.setModel(self.zeromode)
        self.updated = False
    
    def __Rollback(self):
        self.__sql_socket.Rollback()
        self.insert_delete_table.setModel(self.zeromode)
        self.query_table.setModel(self.zeromode)
        self.updated = False
    
    def closeEvent(self, event):
        if self.updated:
            quitMsgBox = QMessageBox()
            quitMsgBox.setWindowTitle('提示')
            quitMsgBox.setText('有尚未保存的事物，是否直接退出？')
            quitMsgBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
            buttonY = quitMsgBox.button(QMessageBox.Yes)
            buttonY.setText('保存')
            buttonN = quitMsgBox.button(QMessageBox.No)
            buttonN.setText('退出')
            buttonC = quitMsgBox.button(QMessageBox.Cancel)
            buttonC.setText('取消')
            quitMsgBox.exec_()
            if quitMsgBox.clickedButton() == buttonY:
                self.__Commit()
                event.accept()
            elif quitMsgBox.clickedButton() == buttonN:
                event.accept()
            elif quitMsgBox.clickedButton() == buttonC:
                event.ignore()
        else:
            self.__sql_socket.Close()