# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Widget(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(765, 506)
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.gridLayout.setContentsMargins(2, 2, 2, 2)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName("gridLayout")
        self.show_face_button = QtWidgets.QPushButton(Form)
        self.show_face_button.setObjectName("show_face_button")
        self.gridLayout.addWidget(self.show_face_button, 1, 1, 1, 1)
        self.pic_rec_button = QtWidgets.QPushButton(Form)
        self.pic_rec_button.setObjectName("pic_rec_button")
        self.gridLayout.addWidget(self.pic_rec_button, 2, 1, 1, 1)
        self.widget = QtWidgets.QWidget(Form)
        self.widget.setObjectName("widget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.widget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.picture = QtWidgets.QLabel(self.widget)
        self.picture.setText("")
        self.picture.setObjectName("picture")
        self.gridLayout_2.addWidget(self.picture, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.widget, 0, 0, 6, 1)
        self.quit = QtWidgets.QPushButton(Form)
        self.quit.setObjectName("quit")
        self.gridLayout.addWidget(self.quit, 4, 1, 1, 1)
        self.cap_rec_button = QtWidgets.QPushButton(Form)
        self.cap_rec_button.setObjectName("cap_rec_button")
        self.gridLayout.addWidget(self.cap_rec_button, 3, 1, 1, 1)
        self.gridLayout.setColumnStretch(0, 9)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.show_face_button.setText(_translate("Form", "显示人脸数据"))
        self.pic_rec_button.setText(_translate("Form", "图像识别人脸"))
        self.quit.setText(_translate("Form", "退出"))
        self.cap_rec_button.setText(_translate("Form", "相机识别人脸"))