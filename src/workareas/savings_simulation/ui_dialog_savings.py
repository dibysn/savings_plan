# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_dialog_savings.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(316, 441)
        Dialog.setStyleSheet("#main_frame{\n"
"border-radius: 8px;\n"
"background-color: #BFCBD9;\n"
"}")
        self.horizontalLayout = QtWidgets.QHBoxLayout(Dialog)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.main_frame = QtWidgets.QFrame(Dialog)
        self.main_frame.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.main_frame.setFrameShadow(QtWidgets.QFrame.Plain)
        self.main_frame.setObjectName("main_frame")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.main_frame)
        self.verticalLayout.setContentsMargins(0, 4, 0, 0)
        self.verticalLayout.setSpacing(4)
        self.verticalLayout.setObjectName("verticalLayout")
        self.frame = QtWidgets.QFrame(self.main_frame)
        self.frame.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame.setFrameShadow(QtWidgets.QFrame.Plain)
        self.frame.setObjectName("frame")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.frame)
        self.horizontalLayout_2.setContentsMargins(4, 0, 0, 0)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.frame_3 = QtWidgets.QFrame(self.frame)
        self.frame_3.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Plain)
        self.frame_3.setObjectName("frame_3")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.frame_3)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setSpacing(4)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.button_new = QtWidgets.QPushButton(self.frame_3)
        self.button_new.setObjectName("button_new")
        self.horizontalLayout_3.addWidget(self.button_new)
        self.button_edit = QtWidgets.QPushButton(self.frame_3)
        self.button_edit.setObjectName("button_edit")
        self.horizontalLayout_3.addWidget(self.button_edit)
        self.button_delete = QtWidgets.QPushButton(self.frame_3)
        self.button_delete.setObjectName("button_delete")
        self.horizontalLayout_3.addWidget(self.button_delete)
        self.horizontalLayout_2.addWidget(self.frame_3, 0, QtCore.Qt.AlignLeft)
        self.verticalLayout.addWidget(self.frame)
        self.table_view_savings = QtWidgets.QTableView(self.main_frame)
        self.table_view_savings.setObjectName("table_view_savings")
        self.verticalLayout.addWidget(self.table_view_savings)
        self.horizontalLayout.addWidget(self.main_frame)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.button_new.setText(_translate("Dialog", "New..."))
        self.button_new.setProperty("class", _translate("Dialog", "btn_slidemenu"))
        self.button_edit.setText(_translate("Dialog", "Edit..."))
        self.button_edit.setProperty("class", _translate("Dialog", "btn_slidemenu"))
        self.button_delete.setText(_translate("Dialog", "Delete..."))
        self.button_delete.setProperty("class", _translate("Dialog", "btn_slidemenu"))