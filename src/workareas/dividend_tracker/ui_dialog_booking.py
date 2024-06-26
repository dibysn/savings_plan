# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_dialog_booking.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(349, 448)
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
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.gridLayout = QtWidgets.QGridLayout(self.frame_3)
        self.gridLayout.setObjectName("gridLayout")
        self.label_name = QtWidgets.QLabel(self.frame_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_name.sizePolicy().hasHeightForWidth())
        self.label_name.setSizePolicy(sizePolicy)
        self.label_name.setObjectName("label_name")
        self.gridLayout.addWidget(self.label_name, 2, 1, 1, 1)
        self.label_10 = QtWidgets.QLabel(self.frame_3)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_10.setFont(font)
        self.label_10.setObjectName("label_10")
        self.gridLayout.addWidget(self.label_10, 1, 0, 1, 1)
        self.label_isin = QtWidgets.QLabel(self.frame_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_isin.sizePolicy().hasHeightForWidth())
        self.label_isin.setSizePolicy(sizePolicy)
        self.label_isin.setObjectName("label_isin")
        self.gridLayout.addWidget(self.label_isin, 3, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.frame_3)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 2, 0, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.frame_3)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 3, 0, 1, 1)
        self.combo_box_share = QtWidgets.QComboBox(self.frame_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.combo_box_share.sizePolicy().hasHeightForWidth())
        self.combo_box_share.setSizePolicy(sizePolicy)
        self.combo_box_share.setObjectName("combo_box_share")
        self.gridLayout.addWidget(self.combo_box_share, 1, 1, 1, 1)
        self.combo_box_type = QtWidgets.QComboBox(self.frame_3)
        self.combo_box_type.setObjectName("combo_box_type")
        self.gridLayout.addWidget(self.combo_box_type, 0, 1, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.frame_3)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 0, 0, 1, 1)
        self.verticalLayout_3.addWidget(self.frame_3)
        self.frame_4 = QtWidgets.QFrame(self.frame_5)
        self.frame_4.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_4.setFrameShadow(QtWidgets.QFrame.Plain)
        self.frame_4.setObjectName("frame_4")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.frame_4)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.frame_7 = QtWidgets.QFrame(self.frame_4)
        self.frame_7.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_7.setFrameShadow(QtWidgets.QFrame.Plain)
        self.frame_7.setObjectName("frame_7")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.frame_7)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.label_4 = QtWidgets.QLabel(self.frame_7)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.gridLayout_5.addWidget(self.label_4, 4, 0, 1, 1)
        self.fee = QtWidgets.QDoubleSpinBox(self.frame_7)
        self.fee.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.fee.setProperty("showGroupSeparator", True)
        self.fee.setMinimum(-90000.0)
        self.fee.setMaximum(90000.0)
        self.fee.setObjectName("fee")
        self.gridLayout_5.addWidget(self.fee, 8, 1, 1, 1)
        self.label_11 = QtWidgets.QLabel(self.frame_7)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_11.setFont(font)
        self.label_11.setObjectName("label_11")
        self.gridLayout_5.addWidget(self.label_11, 7, 0, 1, 1)
        self.tax = QtWidgets.QDoubleSpinBox(self.frame_7)
        self.tax.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.tax.setProperty("showGroupSeparator", True)
        self.tax.setMinimum(-90000.0)
        self.tax.setMaximum(90000.0)
        self.tax.setObjectName("tax")
        self.gridLayout_5.addWidget(self.tax, 9, 1, 1, 1)
        self.total_amount = QtWidgets.QLabel(self.frame_7)
        self.total_amount.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.total_amount.setObjectName("total_amount")
        self.gridLayout_5.addWidget(self.total_amount, 7, 1, 1, 1)
        self.amount_per_share = QtWidgets.QDoubleSpinBox(self.frame_7)
        self.amount_per_share.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.amount_per_share.setProperty("showGroupSeparator", True)
        self.amount_per_share.setDecimals(4)
        self.amount_per_share.setMinimum(-90000.0)
        self.amount_per_share.setMaximum(90000.0)
        self.amount_per_share.setObjectName("amount_per_share")
        self.gridLayout_5.addWidget(self.amount_per_share, 6, 1, 1, 1)
        self.label_6 = QtWidgets.QLabel(self.frame_7)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.gridLayout_5.addWidget(self.label_6, 8, 0, 1, 1)
        self.date_booking = QtWidgets.QDateEdit(self.frame_7)
        self.date_booking.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.date_booking.setDateTime(QtCore.QDateTime(QtCore.QDate(2024, 1, 1), QtCore.QTime(0, 0, 0)))
        self.date_booking.setCalendarPopup(True)
        self.date_booking.setObjectName("date_booking")
        self.gridLayout_5.addWidget(self.date_booking, 4, 1, 1, 1)
        self.label_8 = QtWidgets.QLabel(self.frame_7)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_8.setFont(font)
        self.label_8.setObjectName("label_8")
        self.gridLayout_5.addWidget(self.label_8, 9, 0, 1, 1)
        self.label_7 = QtWidgets.QLabel(self.frame_7)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_7.setFont(font)
        self.label_7.setObjectName("label_7")
        self.gridLayout_5.addWidget(self.label_7, 6, 0, 1, 1)
        self.label_9 = QtWidgets.QLabel(self.frame_7)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_9.setFont(font)
        self.label_9.setObjectName("label_9")
        self.gridLayout_5.addWidget(self.label_9, 5, 0, 1, 1)
        self.label_13 = QtWidgets.QLabel(self.frame_7)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_13.setFont(font)
        self.label_13.setObjectName("label_13")
        self.gridLayout_5.addWidget(self.label_13, 10, 0, 1, 1)
        self.total_value = QtWidgets.QLabel(self.frame_7)
        self.total_value.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.total_value.setObjectName("total_value")
        self.gridLayout_5.addWidget(self.total_value, 10, 1, 1, 1)
        self.number_of_shares = QtWidgets.QDoubleSpinBox(self.frame_7)
        self.number_of_shares.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.number_of_shares.setDecimals(5)
        self.number_of_shares.setMaximum(100000.0)
        self.number_of_shares.setObjectName("number_of_shares")
        self.gridLayout_5.addWidget(self.number_of_shares, 5, 1, 1, 1)
        self.horizontalLayout.addWidget(self.frame_7, 0, QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.verticalLayout_3.addWidget(self.frame_4)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem)
        self.verticalLayout.addWidget(self.frame_5)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Save)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept) # type: ignore
        self.buttonBox.rejected.connect(Dialog.reject) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        Dialog.setTabOrder(self.combo_box_share, self.date_booking)
        Dialog.setTabOrder(self.date_booking, self.number_of_shares)
        Dialog.setTabOrder(self.number_of_shares, self.amount_per_share)
        Dialog.setTabOrder(self.amount_per_share, self.fee)
        Dialog.setTabOrder(self.fee, self.tax)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label_12.setText(_translate("Dialog", "BOOKING"))
        self.label_name.setText(_translate("Dialog", "N/A"))
        self.label_10.setText(_translate("Dialog", "Share"))
        self.label_isin.setText(_translate("Dialog", "N/A"))
        self.label_2.setText(_translate("Dialog", "Name"))
        self.label_3.setText(_translate("Dialog", "ISIN"))
        self.label_5.setText(_translate("Dialog", "Type"))
        self.label_4.setText(_translate("Dialog", "Date"))
        self.fee.setSuffix(_translate("Dialog", " €"))
        self.label_11.setText(_translate("Dialog", "Amount"))
        self.tax.setSuffix(_translate("Dialog", " €"))
        self.total_amount.setText(_translate("Dialog", "N/A €"))
        self.amount_per_share.setSuffix(_translate("Dialog", " €"))
        self.label_6.setText(_translate("Dialog", "Fee"))
        self.date_booking.setDisplayFormat(_translate("Dialog", "dd.MM.yyyy"))
        self.label_8.setText(_translate("Dialog", "Tax"))
        self.label_7.setText(_translate("Dialog", "Amount/share"))
        self.label_9.setText(_translate("Dialog", "Number of shares"))
        self.label_13.setText(_translate("Dialog", "Total"))
        self.total_value.setText(_translate("Dialog", "N/A €"))
