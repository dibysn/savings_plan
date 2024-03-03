# -*- coding: utf-8 -*-

import sys
import os
import json
from PyQt5 import QtCore, QtWidgets, QtGui

from src.savings_plan_ui import Ui_MainWindow

from src.workareas.savings_simulation import workarea_savings_simulation
from src.workareas.trading import workarea_trading
from src.workareas.dividend_tracker import workarea_dividend_tracker

def display_error(err):
    msg_box = QtWidgets.QMessageBox()
    msg_box.setIcon(QtWidgets.QMessageBox.Critical)
    msg_box.setText(str(err))
    msg_box.setStandardButtons(QtWidgets.QMessageBox.Ok)
    msg_box.exec()

class MainWindow(QtWidgets.QMainWindow):
    
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setup_gui()
        self._is_saved = False
        self._filename = None
    
    def setup_gui(self):
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        QtWidgets.QSizeGrip(self.ui.frame_footer_right)
        
        QtCore.QLocale.setDefault(
            QtCore.QLocale(
                QtCore.QLocale.English, QtCore.QLocale.UnitedStates
                )
            )
        
        self.setWindowTitle('SAVINGS PLAN - New savings plan*')
        self.ui.lbl_version.setText('Version 2.0')
        
        self.ui.btn_new.clicked.connect(
            self.new_savings_plan
            )
        
        self.ui.btn_save.clicked.connect(
            self.save_savings_plan
            )
        
        self.ui.btn_save_as.clicked.connect(
            self.save_savings_plan_as
            )
        
        self.ui.btn_open.clicked.connect(
            self.load_savings_plan
            )
        
        self.ui.btn_slidemenu.clicked.connect(
            self.slide_left_menu
            )
        
        self.ui.btn_info.clicked.connect(
            self.show_information
            )
        
        self.shortcut = QtWidgets.QShortcut(
            QtGui.QKeySequence(QtCore.Qt.CTRL + QtCore.Qt.Key_S), self
            )
        self.shortcut.activated.connect(self.shortcut_save_savings_plan)
        
        #################
        # Registration of workareas
        
        wa_savings_plan, \
        icon_workarea_savings_plan, \
        slidemenu_workarea_savings_plan, \
        mainbody_workarea_savings_plan = workarea_savings_simulation.get_workarea_icon_and_widgets()
        
        wa_dividend_tracker, \
        icon_workarea_dividend_tracker, \
        slidemenu_workarea_dividend_tracker, \
        mainbody_workarea_dividend_tracker = workarea_dividend_tracker.get_workarea_icon_and_widgets()
        
        wa_trading, \
        icon_workarea_trading, \
        slidemenu_workarea_trading, \
        mainbody_workarea_trading = workarea_trading.get_workarea_icon_and_widgets()
        
        self.workareas = {
            wa_savings_plan.get_name_of_workarea(): wa_savings_plan,
            wa_dividend_tracker.get_name_of_workarea(): wa_dividend_tracker,
            wa_trading.get_name_of_workarea(): wa_trading
            }
        
        self.slidemenu_workareas = [
            slidemenu_workarea_savings_plan,
            slidemenu_workarea_dividend_tracker,
            slidemenu_workarea_trading
            ]
        self.mainbody_workareas = [
            mainbody_workarea_savings_plan,
            mainbody_workarea_dividend_tracker,
            mainbody_workarea_trading
            ]
        self.icons_workareas = [
            icon_workarea_savings_plan,
            icon_workarea_dividend_tracker,
            icon_workarea_trading
            ]
        
        self.register_workareas()
        
        #################
        
        self.show()
    
    def register_workareas(self):
        
        def activate_workarea(n):
            def a():
                self.ui.stackedWidget_slidemenu.setCurrentIndex(n)
                self.ui.stackedWidget_mainbody.setCurrentIndex(n)
            return a
        
        for s_workarea in self.slidemenu_workareas:
            self.ui.stackedWidget_slidemenu.addWidget(s_workarea)
        
        for m_workarea in self.mainbody_workareas:
            self.ui.stackedWidget_mainbody.addWidget(m_workarea)
        
        for n, icon in enumerate(self.icons_workareas):
            button = QtWidgets.QPushButton(self.ui.frame_workareas_buttons)
            button.setText('')
            
            button.setIcon(icon)
            button.setIconSize(QtCore.QSize(30, 30))
            button.setFlat(True)
            button.setObjectName('btn_workarea_{}'.format(n))
            button.setProperty('class', 'btn_mainwindow')
            self.ui.verticalLayoutWorkareaButtons.addWidget(button)
            
            button.clicked.connect(activate_workarea(n))
        
        for _, wa in self.workareas.items():
            wa.register_change_observer(self.savings_plan_changed)
    
    def slide_left_menu(self):
        width = self.ui.frame_body_slidemenu.width()
        
        if width == 0:
            new_width = 390
            self.ui.btn_slidemenu.setIcon(
                QtGui.QIcon(':/icons/icons/menu-open.svg')
                )
        else:
            new_width = 0
            self.ui.btn_slidemenu.setIcon(
                QtGui.QIcon(':/icons/icons/menu.svg')
                )
        
        self.animation = QtCore.QPropertyAnimation(
            self.ui.frame_body_slidemenu, b'maximumWidth'
            )
        self.animation.setDuration(250)
        self.animation.setStartValue(width)
        self.animation.setEndValue(new_width)
        self.animation.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
        self.animation.start()
    
    def new_savings_plan(self):
        if not self._is_saved:
            message = ('The current savings plan has been modified. '
                       'If you continue, all changes to the current plan '
                       'will be lost.\n\n'
                       'Do you want to continue?')
        else:
            message = ('If you creeate a new savings plan, '
                       'the current plan will be closed.\n\n'
                       'Do you want to continue?')
            
        button = QtWidgets.QMessageBox.question(
            self, 'Savings plan - New', message,
            QtWidgets.QMessageBox.Cancel | QtWidgets.QMessageBox.Yes
            )
        if button == QtWidgets.QMessageBox.Cancel:
            return
        
        for _, wa in self.workareas.items():
            wa.set_default_values()
        
        self.setWindowTitle('SAVINGS PLAN - New savings plan*')
        
        self._is_saved = False
        self._filename = None
        self.ui.btn_save.setEnabled(False)
    
    def _save(self, filename):
        _data = []
        for wa_name, wa in self.workareas.items():
            _data.append(
                (wa_name, wa.get_json_data_for_saving())
                )
        with open(filename, 'w') as f:
            json.dump(_data, f)
    
    def save_savings_plan(self):
        try:
            if not os.path.isfile(self._filename):
                raise Exception(
                    ('File\n'
                     '"{}"\n'
                     'does not exist').format(self._filename)
                    )
            self._save(self._filename)
        except Exception as err:
            display_error(err)
        else:
            _name = os.path.splitext(os.path.basename(self._filename))[0]
            self.setWindowTitle('SAVINGS PLAN - {}'.format(_name))
            self._is_saved = True
            self.ui.btn_save.setEnabled(False)
    
    def save_savings_plan_as(self):
        filename, _filter = QtWidgets.QFileDialog.getSaveFileName(
            self, 'Save savings plan as', './New savings plan.json', 'JSON files (*.json)',
            options = QtWidgets.QFileDialog.DontUseNativeDialog)
        if filename:
            try:
                self._save(filename)
            except Exception as err:
                display_error(err)
            else:
                _name = os.path.splitext(os.path.basename(filename))[0]
                self.setWindowTitle('SAVINGS PLAN - {}'.format(_name))
                self._is_saved = True
                self._filename = filename
                self.ui.btn_save.setEnabled(False)
    
    def shortcut_save_savings_plan(self):
        if self._filename != None:
            self.save_savings_plan()
        else:
            self.save_savings_plan_as()
    
    def load_savings_plan(self):
        if not self._is_saved:
            button = QtWidgets.QMessageBox.question(
                self,
                'Savings plan - Open',
                ('The current savings plan has been modified. '
                 'If you continue, all changes to the current plan '
                 'will be lost.\n\n'
                 'Do you want to continue?'),
                QtWidgets.QMessageBox.Cancel | 
                QtWidgets.QMessageBox.Yes
                )
            if button == QtWidgets.QMessageBox.Cancel:
                return
        
        filename, _filter = QtWidgets.QFileDialog.getOpenFileName(
            self, 'Open savings plan', './', 'JSON files (*.json)',
            options = QtWidgets.QFileDialog.DontUseNativeDialog)
        
        if filename:
            self._filename = filename
            _name = os.path.splitext(os.path.basename(filename))[0]
            _cursor = self.cursor()
            self.setCursor(QtCore.Qt.WaitCursor)
            try:
                try:
                    with open(filename, 'r') as f:
                        _l = json.load(f)
                except Exception as e:
                    raise Exception(
                        ('Data in "{}" not readale '
                         '({})'.format(filename, e))
                        )
                
                if not isinstance(_l, list):
                    raise Exception(
                        ('Data in "{}" not readale '
                         '(wrong instance)').format(filename)
                        )
                
                for _wa_name, _ in _l:
                    if _wa_name not in self.workareas.keys():
                        raise Exception(
                            ('Data in "{}" not readale '
                             '(wrong workareas)').format(filename)
                            )
            except Exception as err:
                display_error(err)
            else:
                errors = []
                for _wa_name, _wa_data in _l:
                    try:
                        if not isinstance(_wa_data, dict):
                            raise Exception('Data in "{}" not readale'.format(filename))
                        self.workareas[_wa_name].load_from_json_data(_wa_data)
                    except:
                        self.workareas[_wa_name].set_default_values()
                        errors.append(
                            Exception(
                                ('Loading failed (data for workarea "{}" caused an error)\n'
                                 'Default values will be used for this workarea'
                                 ).format(_wa_name)
                                )
                            )
                if errors != []:
                    self._is_saved = False
                    self.ui.btn_save.setEnabled(True)
                    self.setWindowTitle('SAVINGS PLAN - {}*'.format(_name))
                    for err in errors:
                        display_error(err)
                else:
                    self._is_saved = True
                    self.ui.btn_save.setEnabled(False)
                    self.setWindowTitle('SAVINGS PLAN - {}'.format(_name))
            finally:
                self.setCursor(_cursor)
    
    def savings_plan_changed(self):
        self._is_saved = False
        if self._filename != None:
            self.ui.btn_save.setEnabled(True)
        if self.windowTitle()[-1] != '*':
            self.setWindowTitle('{}*'.format(self.windowTitle()))
    
    def show_information(self):
        QtWidgets.QMessageBox.information(
            self,
            'Savings plan - Information',
            ('For more information please visit my GitHub repository:'
              '<br><center><a href=https://github.com/dibysn> https://github.com/dibysn </a>'),
            QtWidgets.QMessageBox.Close
            )
    
    def closeEvent(self, event):
        if not self._is_saved:
            button = QtWidgets.QMessageBox.question(
                self,
                'Savings plan - Close application',
                ('The current savings plan has been modified. '
                 'If you close the application, '
                 'all changes to the current plan '
                 'will be lost.\n\n'
                 'Do you want to close the application anyway?'),
                QtWidgets.QMessageBox.Cancel | 
                QtWidgets.QMessageBox.Yes
                )
            if button == QtWidgets.QMessageBox.Cancel:
                event.ignore()
            elif button == QtWidgets.QMessageBox.Yes:
                event.accept()

def execute():
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())
    