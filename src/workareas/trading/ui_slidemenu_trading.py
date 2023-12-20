# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_slidemenu_trading.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(376, 408)
        Form.setStyleSheet("#frame_header,\n"
"#frame_header_2 {\n"
"background-color: #E9EDF1;\n"
"border-radius: 8px;\n"
"}")
        self.horizontalLayout = QtWidgets.QHBoxLayout(Form)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.main_body_left_frame = QtWidgets.QFrame(Form)
        self.main_body_left_frame.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.main_body_left_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.main_body_left_frame.setObjectName("main_body_left_frame")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.main_body_left_frame)
        self.verticalLayout.setContentsMargins(0, 0, 0, 3)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.frame = QtWidgets.QFrame(self.main_body_left_frame)
        self.frame.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.frame)
        self.verticalLayout_2.setContentsMargins(9, 9, 9, 9)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.frame_header = QtWidgets.QFrame(self.frame)
        self.frame_header.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_header.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_header.setObjectName("frame_header")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.frame_header)
        self.horizontalLayout_2.setContentsMargins(6, -1, -1, -1)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label = QtWidgets.QLabel(self.frame_header)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.horizontalLayout_2.addWidget(self.label)
        self.verticalLayout_2.addWidget(self.frame_header)
        self.verticalLayout.addWidget(self.frame)
        self.frame_3 = QtWidgets.QFrame(self.main_body_left_frame)
        self.frame_3.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.frame_3)
        self.verticalLayout_5.setContentsMargins(9, -1, 9, -1)
        self.verticalLayout_5.setSpacing(6)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.button_new_portfolio = QtWidgets.QPushButton(self.frame_3)
        self.button_new_portfolio.setObjectName("button_new_portfolio")
        self.verticalLayout_5.addWidget(self.button_new_portfolio)
        self.button_edit_portfolio = QtWidgets.QPushButton(self.frame_3)
        self.button_edit_portfolio.setObjectName("button_edit_portfolio")
        self.verticalLayout_5.addWidget(self.button_edit_portfolio)
        self.verticalLayout.addWidget(self.frame_3)
        self.frame_2 = QtWidgets.QFrame(self.main_body_left_frame)
        self.frame_2.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.frame_2)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.frame_header_2 = QtWidgets.QFrame(self.frame_2)
        self.frame_header_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_header_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_header_2.setObjectName("frame_header_2")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.frame_header_2)
        self.horizontalLayout_3.setContentsMargins(6, -1, -1, -1)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_2 = QtWidgets.QLabel(self.frame_header_2)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_3.addWidget(self.label_2)
        self.verticalLayout_4.addWidget(self.frame_header_2)
        self.verticalLayout.addWidget(self.frame_2)
        self.frame_5 = QtWidgets.QFrame(self.main_body_left_frame)
        self.frame_5.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_5.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_5.setObjectName("frame_5")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.frame_5)
        self.verticalLayout_3.setContentsMargins(15, -1, -1, -1)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.button_new_trade = QtWidgets.QPushButton(self.frame_5)
        self.button_new_trade.setIconSize(QtCore.QSize(16, 16))
        self.button_new_trade.setObjectName("button_new_trade")
        self.verticalLayout_3.addWidget(self.button_new_trade)
        self.button_edit_trade = QtWidgets.QPushButton(self.frame_5)
        self.button_edit_trade.setObjectName("button_edit_trade")
        self.verticalLayout_3.addWidget(self.button_edit_trade)
        self.button_delete_trade = QtWidgets.QPushButton(self.frame_5)
        self.button_delete_trade.setObjectName("button_delete_trade")
        self.verticalLayout_3.addWidget(self.button_delete_trade)
        self.button_get_latest_price = QtWidgets.QPushButton(self.frame_5)
        self.button_get_latest_price.setObjectName("button_get_latest_price")
        self.verticalLayout_3.addWidget(self.button_get_latest_price)
        self.verticalLayout.addWidget(self.frame_5)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout.addWidget(self.main_body_left_frame)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "PORTFOLIO"))
        self.button_new_portfolio.setText(_translate("Form", "New portfolio..."))
        self.button_new_portfolio.setProperty("class", _translate("Form", "btn_slidemenu"))
        self.button_edit_portfolio.setText(_translate("Form", "Edit portfolio..."))
        self.button_edit_portfolio.setProperty("class", _translate("Form", "btn_slidemenu"))
        self.label_2.setText(_translate("Form", "TRADES"))
        self.button_new_trade.setText(_translate("Form", "New trade..."))
        self.button_new_trade.setProperty("class", _translate("Form", "btn_slidemenu"))
        self.button_edit_trade.setText(_translate("Form", "Edit trade..."))
        self.button_edit_trade.setProperty("class", _translate("Form", "btn_slidemenu"))
        self.button_delete_trade.setText(_translate("Form", "Delete trade..."))
        self.button_delete_trade.setProperty("class", _translate("Form", "btn_slidemenu"))
        self.button_get_latest_price.setText(_translate("Form", "Latest price"))
        self.button_get_latest_price.setProperty("class", _translate("Form", "btn_slidemenu"))
