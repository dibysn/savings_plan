# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_dialog_category.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(367, 396)
        Dialog.setStyleSheet("#frame_5 {\n"
"border-radius: 8px;\n"
"background-color: #BFCBD9;\n"
"}\n"
"\n"
"#frame_header {\n"
"background-color: #E9EDF1;\n"
"border-radius: 8px;\n"
"}")
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.frame_5 = QtWidgets.QFrame(Dialog)
        self.frame_5.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_5.setFrameShadow(QtWidgets.QFrame.Plain)
        self.frame_5.setObjectName("frame_5")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.frame_5)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.frame = QtWidgets.QFrame(self.frame_5)
        self.frame.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.frame)
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.frame_header = QtWidgets.QFrame(self.frame)
        self.frame_header.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_header.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_header.setObjectName("frame_header")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.frame_header)
        self.horizontalLayout_3.setContentsMargins(6, -1, -1, -1)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_12 = QtWidgets.QLabel(self.frame_header)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_12.setFont(font)
        self.label_12.setObjectName("label_12")
        self.horizontalLayout_3.addWidget(self.label_12)
        self.verticalLayout_4.addWidget(self.frame_header)
        self.verticalLayout_3.addWidget(self.frame)
        self.frame_3 = QtWidgets.QFrame(self.frame_5)
        self.frame_3.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Plain)
        self.frame_3.setObjectName("frame_3")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.frame_3)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.list_categories = QtWidgets.QListWidget(self.frame_3)
        self.list_categories.setObjectName("list_categories")
        self.verticalLayout_2.addWidget(self.list_categories)
        self.verticalLayout_3.addWidget(self.frame_3)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem)
        self.frame_4 = QtWidgets.QFrame(self.frame_5)
        self.frame_4.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_4.setFrameShadow(QtWidgets.QFrame.Plain)
        self.frame_4.setObjectName("frame_4")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.frame_4)
        self.horizontalLayout.setContentsMargins(-1, 0, -1, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.line_edit_name = QtWidgets.QLineEdit(self.frame_4)
        self.line_edit_name.setObjectName("line_edit_name")
        self.horizontalLayout.addWidget(self.line_edit_name)
        self.label_color = QtWidgets.QLabel(self.frame_4)
        self.label_color.setStyleSheet("background-color: #3911ed")
        self.label_color.setText("")
        self.label_color.setObjectName("label_color")
        self.horizontalLayout.addWidget(self.label_color)
        self.button_color = QtWidgets.QPushButton(self.frame_4)
        self.button_color.setObjectName("button_color")
        self.horizontalLayout.addWidget(self.button_color)
        self.verticalLayout_3.addWidget(self.frame_4)
        self.frame_2 = QtWidgets.QFrame(self.frame_5)
        self.frame_2.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Plain)
        self.frame_2.setObjectName("frame_2")
        self.gridLayout = QtWidgets.QGridLayout(self.frame_2)
        self.gridLayout.setObjectName("gridLayout")
        self.button_create = QtWidgets.QPushButton(self.frame_2)
        self.button_create.setObjectName("button_create")
        self.gridLayout.addWidget(self.button_create, 0, 1, 1, 1)
        self.button_delete = QtWidgets.QPushButton(self.frame_2)
        self.button_delete.setObjectName("button_delete")
        self.gridLayout.addWidget(self.button_delete, 0, 3, 1, 1)
        self.button_update = QtWidgets.QPushButton(self.frame_2)
        self.button_update.setObjectName("button_update")
        self.gridLayout.addWidget(self.button_update, 0, 2, 1, 1)
        self.verticalLayout_3.addWidget(self.frame_2)
        self.verticalLayout.addWidget(self.frame_5)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Close)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept) # type: ignore
        self.buttonBox.rejected.connect(Dialog.reject) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        Dialog.setTabOrder(self.list_categories, self.line_edit_name)
        Dialog.setTabOrder(self.line_edit_name, self.button_color)
        Dialog.setTabOrder(self.button_color, self.button_create)
        Dialog.setTabOrder(self.button_create, self.button_update)
        Dialog.setTabOrder(self.button_update, self.button_delete)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label_12.setText(_translate("Dialog", "CATEGORY"))
        self.button_color.setText(_translate("Dialog", "Color..."))
        self.button_create.setText(_translate("Dialog", "Add"))
        self.button_delete.setText(_translate("Dialog", "Delete"))
        self.button_update.setText(_translate("Dialog", "Update"))
