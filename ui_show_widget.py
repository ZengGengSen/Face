# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_show_widget.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Show_Widget(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(907, 559)
        self.gridLayout_2 = QtWidgets.QGridLayout(Form)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.widget = QtWidgets.QWidget(Form)
        self.widget.setObjectName("widget")
        self.gridLayout = QtWidgets.QGridLayout(self.widget)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(self.widget)
        self.label.setText("")
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.gridLayout_2.addWidget(self.widget, 1, 0, 1, 2)
        self.add_data = QtWidgets.QPushButton(Form)
        self.add_data.setObjectName("add_data")
        self.gridLayout_2.addWidget(self.add_data, 0, 0, 1, 1)
        self.delete_data = QtWidgets.QPushButton(Form)
        self.delete_data.setObjectName("delete_data")
        self.gridLayout_2.addWidget(self.delete_data, 0, 1, 1, 1)
        self.listWidget = QtWidgets.QListWidget(Form)
        self.listWidget.setObjectName("listWidget")
        self.gridLayout_2.addWidget(self.listWidget, 1, 2, 1, 1)
        self.gridLayout_2.setColumnStretch(0, 3)
        self.gridLayout_2.setColumnStretch(1, 3)
        self.gridLayout_2.setColumnStretch(2, 2)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.add_data.setText(_translate("Form", "添加数据"))
        self.delete_data.setText(_translate("Form", "删除数据"))