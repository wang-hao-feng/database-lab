# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'd:\实验\数据库\lab1\code\ui\Login.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(369, 260)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.formLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.formLayoutWidget.setGeometry(QtCore.QRect(40, 40, 291, 131))
        self.formLayoutWidget.setObjectName("formLayoutWidget")
        self.formLayout = QtWidgets.QFormLayout(self.formLayoutWidget)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setObjectName("formLayout")
        self.IP_label = QtWidgets.QLabel(self.formLayoutWidget)
        self.IP_label.setObjectName("IP_label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.IP_label)
        self.user_label = QtWidgets.QLabel(self.formLayoutWidget)
        self.user_label.setObjectName("user_label")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.user_label)
        self.password_label = QtWidgets.QLabel(self.formLayoutWidget)
        self.password_label.setObjectName("password_label")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.password_label)
        self.database_label = QtWidgets.QLabel(self.formLayoutWidget)
        self.database_label.setObjectName("database_label")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.database_label)
        self.user_text = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.user_text.setObjectName("user_text")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.user_text)
        self.password_text = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.password_text.setObjectName("password_text")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.password_text)
        self.database_text = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.database_text.setObjectName("database_text")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.database_text)
        self.IP_text = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.IP_text.setObjectName("IP_text")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.IP_text)
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(40, 170, 291, 31))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.login_button = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.login_button.setObjectName("login_button")
        self.verticalLayout_4.addWidget(self.login_button, 0, QtCore.Qt.AlignHCenter)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "登录页面"))
        self.IP_label.setText(_translate("MainWindow", "服务器IP"))
        self.user_label.setText(_translate("MainWindow", "用户名"))
        self.password_label.setText(_translate("MainWindow", "密码"))
        self.database_label.setText(_translate("MainWindow", "数据库名"))
        self.user_text.setText(_translate("MainWindow", "root"))
        self.IP_text.setText(_translate("MainWindow", "localhost"))
        self.login_button.setText(_translate("MainWindow", "登录"))