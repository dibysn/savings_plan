# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_dialog_portfolio.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(473, 235)
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
        self.frame_5.setFrameShadow(QtWidgets.QFrame.Raised)
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
        self.frame_4 = QtWidgets.QFrame(self.frame_5)
        self.frame_4.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_4.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_4.setObjectName("frame_4")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.frame_4)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.allowed_risk_portfolio = QtWidgets.QDoubleSpinBox(self.frame_4)
        self.allowed_risk_portfolio.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.allowed_risk_portfolio.setMaximum(10.0)
        self.allowed_risk_portfolio.setSingleStep(0.1)
        self.allowed_risk_portfolio.setProperty("value", 0.0)
        self.allowed_risk_portfolio.setObjectName("allowed_risk_portfolio")
        self.gridLayout_3.addWidget(self.allowed_risk_portfolio, 1, 1, 1, 1)
        self.allowed_risk_trade = QtWidgets.QDoubleSpinBox(self.frame_4)
        self.allowed_risk_trade.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.allowed_risk_trade.setMaximum(10.0)
        self.allowed_risk_trade.setSingleStep(0.1)
        self.allowed_risk_trade.setProperty("value", 0.0)
        self.allowed_risk_trade.setObjectName("allowed_risk_trade")
        self.gridLayout_3.addWidget(self.allowed_risk_trade, 2, 1, 1, 1)
        self.label_6 = QtWidgets.QLabel(self.frame_4)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.gridLayout_3.addWidget(self.label_6, 0, 0, 1, 1)
        self.label_8 = QtWidgets.QLabel(self.frame_4)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_8.setFont(font)
        self.label_8.setObjectName("label_8")
        self.gridLayout_3.addWidget(self.label_8, 1, 0, 1, 1)
        self.initial_deposit = QtWidgets.QDoubleSpinBox(self.frame_4)
        self.initial_deposit.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.initial_deposit.setProperty("showGroupSeparator", True)
        self.initial_deposit.setMaximum(100000.0)
        self.initial_deposit.setSingleStep(100.0)
        self.initial_deposit.setProperty("value", 0.0)
        self.initial_deposit.setObjectName("initial_deposit")
        self.gridLayout_3.addWidget(self.initial_deposit, 0, 1, 1, 1)
        self.label_7 = QtWidgets.QLabel(self.frame_4)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_7.setFont(font)
        self.label_7.setObjectName("label_7")
        self.gridLayout_3.addWidget(self.label_7, 2, 0, 1, 1)
        self.label_total_allowed_risk_portfolio = QtWidgets.QLabel(self.frame_4)
        self.label_total_allowed_risk_portfolio.setObjectName("label_total_allowed_risk_portfolio")
        self.gridLayout_3.addWidget(self.label_total_allowed_risk_portfolio, 1, 2, 1, 1)
        self.label_total_allowed_risk_trade = QtWidgets.QLabel(self.frame_4)
        self.label_total_allowed_risk_trade.setObjectName("label_total_allowed_risk_trade")
        self.gridLayout_3.addWidget(self.label_total_allowed_risk_trade, 2, 2, 1, 1)
        self.label_total_amount_portfolio = QtWidgets.QLabel(self.frame_4)
        self.label_total_amount_portfolio.setObjectName("label_total_amount_portfolio")
        self.gridLayout_3.addWidget(self.label_total_amount_portfolio, 0, 2, 1, 1)
        self.verticalLayout_3.addWidget(self.frame_4, 0, QtCore.Qt.AlignTop)
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
        Dialog.setTabOrder(self.initial_deposit, self.allowed_risk_portfolio)
        Dialog.setTabOrder(self.allowed_risk_portfolio, self.allowed_risk_trade)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label_12.setText(_translate("Dialog", "PORTFOLIO"))
        self.allowed_risk_portfolio.setSuffix(_translate("Dialog", " %"))
        self.allowed_risk_trade.setSuffix(_translate("Dialog", " %"))
        self.label_6.setText(_translate("Dialog", "Initial deposit"))
        self.label_8.setText(_translate("Dialog", "Allowed risk portfolio"))
        self.initial_deposit.setSuffix(_translate("Dialog", " €"))
        self.label_7.setText(_translate("Dialog", "Allowed risk trade"))
        self.label_total_allowed_risk_portfolio.setText(_translate("Dialog", "(max N/A)"))
        self.label_total_allowed_risk_trade.setText(_translate("Dialog", "(max N/A)"))
        self.label_total_amount_portfolio.setText(_translate("Dialog", "(total N/A)"))
