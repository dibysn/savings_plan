# -*- coding: utf-8 -*-

import os
import sys
import math
from PyQt5 import QtCore, QtWidgets, QtChart, QtGui

from src.model.savings_plan_simulation import SavingsSimulation
from src.savings_plan_ui import Ui_MainWindow

def round_up(n, decimals = 0):
    multiplier = 10 ** decimals
    return math.ceil(2 * n * multiplier) / multiplier / 2

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
    
    def setup_gui(self):
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        QtWidgets.QSizeGrip(self.ui.size_grip)
        
        QtCore.QLocale.setDefault(
            QtCore.QLocale(
                QtCore.QLocale.English, QtCore.QLocale.UnitedStates
                )
            )
        
        self._set_default_values()
        self.savings_sim = SavingsSimulation(
            self.ui.current_age.value(),
            self.ui.retirement_age.value(),
            self.ui.expected_age.value(),
            self.ui.initial_invest.value(),
            self.ui.monthly_withdrawal_nominal.value(),
            self.ui.rate_of_return.value() / 100.0,
            self.ui.rate_of_inflation.value() / 100.0,
            self.ui.flat_tax_rate.value() / 100.0,
            self.ui.solidarity_tax.value() / 100.0,
            self.ui.church_tax.value() / 100.0
            )
        self.setWindowTitle('SAVINGS PLAN - New savings plan*')
        
        self.ui.chart_without_tax = QtChart.QChart()
        self.ui.chart_without_tax.setTheme(QtChart.QChart.ChartThemeDark)
        self.ui.chart_without_tax.setAnimationOptions(QtChart.QChart.SeriesAnimations)
        self.ui.chartview_without_tax.setChart(self.ui.chart_without_tax)
        
        self.ui.chart_with_tax = QtChart.QChart()
        self.ui.chart_with_tax.setTheme(QtChart.QChart.ChartThemeDark)
        self.ui.chart_with_tax.setAnimationOptions(QtChart.QChart.SeriesAnimations)
        self.ui.chartview_with_tax.setChart(self.ui.chart_with_tax)
        
        for _w in [self.ui.chart_without_tax, self.ui.chart_with_tax,
                   self.ui.frame_3, self.ui.frame_4,
                   self.ui.frame_5, self.ui.frame_6,
                   self.ui.data_input_header_frame]:
            shadow = QtWidgets.QGraphicsDropShadowEffect(self)
            shadow.setBlurRadius(8)
            shadow.setXOffset(0)
            shadow.setYOffset(0)
            shadow.setColor(QtGui.QColor(0, 0, 0, 255))
            _w.setGraphicsEffect(shadow)
        
        self._update_text_all_labels()
        self._update_stacked_bar_chart(
            self.ui.chart_without_tax, self.savings_sim.yearly_savings_amount_without_tax)
        self._update_stacked_bar_chart(
            self.ui.chart_with_tax, self.savings_sim.yearly_savings_amount_with_tax)
        
        self.ui.retirement_age.valueChanged.connect(
            lambda n: self.ui.current_age.setMaximum(n-1)
            )
        self.ui.retirement_age.valueChanged.connect(
            lambda n: self.ui.expected_age.setMinimum(n+1)
            )
        self.ui.current_age.valueChanged.connect(
            lambda n: self.ui.retirement_age.setMinimum(n+1)
            )
        self.ui.expected_age.valueChanged.connect(
            lambda n: self.ui.retirement_age.setMaximum(n-1)
            )
        
        self.ui.btn_open_close_side_bar.clicked.connect(
            lambda: self.slide_left_menu()
            )
        
        self.chart_without_tax_annotation = QtWidgets.QGraphicsSimpleTextItem(
            self.ui.chart_without_tax)
        self.chart_without_tax_rect = QtWidgets.QGraphicsRectItem(
            self.ui.chart_without_tax)
        self.chart_without_tax_rect.setBrush(QtCore.Qt.white)
        self.chart_without_tax_rect.setPen(QtCore.Qt.black)
        
        self.chart_with_tax_annotation = QtWidgets.QGraphicsSimpleTextItem(
            self.ui.chart_with_tax
            )
        self.chart_with_tax_rect = QtWidgets.QGraphicsRectItem(
            self.ui.chart_with_tax)
        self.chart_with_tax_rect.setBrush(QtCore.Qt.white)
        self.chart_with_tax_rect.setPen(QtCore.Qt.black)
        
        self.show()
    
    def _savings_plan_changed(self):
        if self.windowTitle()[-1] != '*':
            self.setWindowTitle('{}*'.format(self.windowTitle()))
    
    def _set_default_values(self):
        self.ui.expected_age.setValue(90)
        self.ui.retirement_age.setValue(67)
        self.ui.current_age.setValue(30)
        self.ui.initial_invest.setValue(2000)
        self.ui.monthly_withdrawal_nominal.setValue(500)
        self.ui.rate_of_return.setValue(5.0)
        self.ui.rate_of_inflation.setValue(2.2)
        self.ui.flat_tax_rate.setValue(25)
        self.ui.solidarity_tax.setValue(5.5)
        self.ui.church_tax.setValue(8)
        self.ui.notes.clear()
        self.ui.include_tax_check_box.setChecked(False)
        self.ui.include_tax_check_box.clicked.emit(False)
        self._savings_plan_changed()
    
    def restore_or_maximize_window(self):
        if self.isMaximized():
            self.showNormal()
            self.ui.restore_window_button.setIcon(
                QtGui.QIcon(':/icons/icons/window-maximize.svg')
                )
        else:
            self.showMaximized()
            self.ui.restore_window_button.setIcon(
                QtGui.QIcon(':/icons/icons/window-restore.svg')
                )
    
    def slide_left_menu(self):
        width = self.ui.main_body_left_frame.width()
        
        if width == 0:
            new_width = 390
            self.ui.btn_open_close_side_bar.setIcon(
                QtGui.QIcon(':/icons/icons/menu-open.svg')
                )
        else:
            new_width = 0
            self.ui.btn_open_close_side_bar.setIcon(
                QtGui.QIcon(':/icons/icons/menu.svg')
                )
        
        self.animation = QtCore.QPropertyAnimation(
            self.ui.main_body_left_margin_frame, b'maximumWidth'
            )
        self.animation.setDuration(250)
        self.animation.setStartValue(width)
        self.animation.setEndValue(new_width)
        self.animation.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
        self.animation.start()
    
    def switch_stacked_widget(self, with_tax):
        if with_tax:
            self.ui.stackedWidget.setCurrentIndex(1)
        else:
            self.ui.stackedWidget.setCurrentIndex(0)
    
    def new_savings_plan(self):
        if not self.savings_sim.is_saved:
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
        
        self._set_default_values()
        self.setWindowTitle('SAVINGS PLAN - New savings plan*')
    
    def save_savings_plan_as(self):
        filename, _filter = QtWidgets.QFileDialog.getSaveFileName(
            self, 'Save savings plan as', './New savings plan.json', 'JSON files (*.json)',
            options = QtWidgets.QFileDialog.DontUseNativeDialog)
        if filename:
            try:
                self.savings_sim.save_to_file(filename, force = True)
            except Exception as err:
                display_error(err)
                return
            
            _name = os.path.splitext(os.path.basename(filename))[0]
            self.setWindowTitle('SAVINGS PLAN - {}'.format(_name))
    
    def load_savings_plan(self):
        if not self.savings_sim.is_saved:
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
            try:
                _savings_sim = SavingsSimulation.load_from_file(filename)
            except Exception as err:
                display_error(err)
                return
            
            self.ui.current_age.setValue(_savings_sim.current_age)
            self.ui.retirement_age.setValue(_savings_sim.retirement_age)
            self.ui.expected_age.setValue(_savings_sim.expected_age)
            self.ui.initial_invest.setValue(_savings_sim.initial_invest)
            self.ui.monthly_withdrawal_nominal.setValue(_savings_sim.monthly_withdrawal_nominal)
            self.ui.rate_of_return.setValue(_savings_sim.rate_of_return * 100.0)
            self.ui.rate_of_inflation.setValue(_savings_sim.rate_of_inflation * 100.0)
            self.ui.flat_tax_rate.setValue(_savings_sim.flat_tax_rate * 100.0)
            self.ui.solidarity_tax.setValue(_savings_sim.solidarity_tax * 100.0)
            self.ui.church_tax.setValue(_savings_sim.church_tax * 100.0)
            self.ui.notes.clear()
            self.ui.notes.insertPlainText(_savings_sim.notes)
            
            self.savings_sim = _savings_sim
            
            _name = os.path.splitext(os.path.basename(filename))[0]
            self.setWindowTitle('SAVINGS PLAN - {}'.format(_name))
            
            self._update_text_all_labels()
            self._update_stacked_bar_chart(
                self.ui.chart_without_tax, self.savings_sim.yearly_savings_amount_without_tax)
            self._update_stacked_bar_chart(
                self.ui.chart_with_tax, self.savings_sim.yearly_savings_amount_with_tax)
    
    def show_information(self):
        QtWidgets.QMessageBox.information(
            self,
            'Savings plan - Information',
            ('For more information please visit my GitHub repository:'
             '<br><center><a href=https://github.com/dibysn/savings_plan> https://github.com/dibysn/savings_plan </a>'),
            QtWidgets.QMessageBox.Close
            )
    
    def notes_changed(self):
        try:
            self.savings_sim.notes = self.ui.notes.toPlainText()
            self._savings_plan_changed()
        except:
            pass
    
    def _update_text_all_labels(self):
        self.ui.label_years_saving_1.setText(
            '{} years'.format(self.savings_sim.years_saving)
            )
        self.ui.label_years_saving_2.setText(
            '{} years'.format(self.savings_sim.years_saving)
            )
        self.ui.label_years_withdrawal_1.setText(
            '{} years'.format(self.savings_sim.years_withdrawal)
            )
        self.ui.label_years_withdrawal_2.setText(
            '{} years'.format(self.savings_sim.years_withdrawal)
            )
        self.ui.label_yearly_withdrawal_real_1.setText(
            '{:,.2f} €'.format(self.savings_sim.yearly_withdrawal_real)
            )
        self.ui.label_yearly_withdrawal_real_2.setText(
            '{:,.2f} €'.format(self.savings_sim.yearly_withdrawal_real)
            )
        self.ui.label_monthly_withdrawal_real_1.setText(
            '{:,.2f} €'.format(self.savings_sim.monthly_withdrawal_real)
            )
        self.ui.label_monthly_withdrawal_real_2.setText(
            '{:,.2f} €'.format(self.savings_sim.monthly_withdrawal_real)
            )
        self.ui.label_target_amount_without_tax.setText(
            '{:,.2f} €'.format(self.savings_sim.target_amount_without_tax)
            )
        self.ui.label_yearly_savings_amount_without_tax.setText(
            '{:,.2f} €'.format(self.savings_sim.yearly_savings_amount_without_tax)
            )
        self.ui.label_monthly_savings_amount_without_tax.setText(
            '{:,.2f} €'.format(self.savings_sim.monthly_savings_amount_without_tax)
            )
        self.ui.label_target_amount_with_tax.setText(
            '{:,.2f} €'.format(self.savings_sim.target_amount_with_tax)
            )
        self.ui.label_yearly_savings_amount_with_tax.setText(
            '{:,.2f} €'.format(self.savings_sim.yearly_savings_amount_with_tax)
            )
        self.ui.label_monthly_savings_amount_with_tax.setText(
            '{:,.2f} €'.format(self.savings_sim.monthly_savings_amount_with_tax)
            )
        self.ui.label_total_tax_rate.setText(
            '{:.2f}%'.format(self.savings_sim.total_tax_rate * 100.0)
            )
    
    def _update_stacked_bar_chart(self, chart, yearly_savings_amount):
        savings, portfolio_value = self.savings_sim.sample_portfolio(
            self.savings_sim.initial_invest,
            self.savings_sim.rate_of_return,
            yearly_savings_amount,
            list(range(int(self.savings_sim.years_saving+1)))
            )
        growth = [p - s for p, s in zip(portfolio_value, savings)]
        
        set_savings = QtChart.QBarSet('Savings')
        set_savings.append(savings)
        set_savings.setColor(QtGui.QColor(0x25A18E))
        set_growth = QtChart.QBarSet('Growth')
        set_growth.append(growth)
        set_savings.setColor(QtGui.QColor(0x25B92E))
        series = QtChart.QStackedBarSeries()
        series.append(set_savings)
        series.append(set_growth)
        
        set_savings.hovered.connect(self.show_info_label_on_hover)
        set_growth.hovered.connect(self.show_info_label_on_hover)
        
        chart.setLocalizeNumbers(True)
        chart.removeAllSeries()
        chart.addSeries(series)
        
        year_axis = QtChart.QValueAxis()
        year_axis.setTickType(QtChart.QValueAxis.TicksDynamic)
        year_axis.setMin(0)
        year_axis.setTickAnchor(0)
        year_axis.setTickInterval(4)
        year_axis.setLabelFormat('%.0d')
        year_axis.setTitleText('# Years saving')
        
        _max = round_up(portfolio_value[-1], -5)
        _tick_interval = 50000 * (_max // 500000 + 1)
        value_axis = QtChart.QValueAxis()
        value_axis.setTickType(QtChart.QValueAxis.TicksDynamic)
        value_axis.setMin(0)
        value_axis.setMax(_max)
        value_axis.setTickAnchor(min(0, min(savings)))
        value_axis.setTickInterval(_tick_interval)
        value_axis.setMinorTickCount(1)
        value_axis.setLabelFormat('%.0f €')
        value_axis.setTitleText('Portfolio value')
        
        for ax in chart.axes():
            chart.removeAxis(ax)
        chart.setAxisX(year_axis, series)
        chart.setAxisY(value_axis, series)
    
    def show_info_label_on_hover(self, status, index):
        if self.ui.include_tax_check_box.isChecked():
            chart = self.ui.chart_with_tax
            chart_annotation = self.chart_with_tax_annotation
            chart_rect = self.chart_with_tax_rect
        else:
            chart = self.ui.chart_without_tax
            chart_annotation = self.chart_without_tax_annotation
            chart_rect = self.chart_without_tax_rect
        
        chart_rect.setVisible(status)
        chart_annotation.setBrush(
            QtGui.QBrush(QtCore.Qt.black)
            )
        set_savings, set_growth = chart.series()[0].barSets()
        chart_annotation.setText(
            ('Value after {} years:\n'
             '{:>16,.2f} € (total)\n'
             '{:>16,.2f} € (savings)\n'
             '{:>16,.2f} € (growth)').format(
                  index,
                  set_savings[index] + set_growth[index],
                  set_savings[index],
                  set_growth[index]))
        
        x_axis = chart.axes(QtCore.Qt.Horizontal)[0]
        y_axis = chart.axes(QtCore.Qt.Vertical)[0]
        p1 = chart.mapToPosition(
            QtCore.QPointF(x_axis.max()*0.01, y_axis.max()*0.99)
            )
        
        chart_annotation.setPos(p1)
        chart_annotation.setZValue(20)
        chart_annotation.setVisible(status)
        
        r = chart_annotation.boundingRect()
        p2 = chart.mapToPosition(QtCore.QPointF(0, y_axis.max()))
        p3 = p1-p2
        chart_rect.setRect(
            p2.x(), p2.y(),
            r.width()+2*p3.x(), r.height()+2*p3.y())
        chart_rect.setZValue(10)
        chart_rect.setVisible(status)
    
    def update_simulation(self, value):
        _name = self.sender().objectName()
        if _name in [
                'rate_of_return', 'rate_of_inflation',
                'flat_tax_rate', 'solidarity_tax', 'church_tax'
                ]:
            value = value / 100.0
        
        setattr(self.savings_sim, _name, value)
        self._update_text_all_labels()
        self._update_stacked_bar_chart(
            self.ui.chart_without_tax, self.savings_sim.yearly_savings_amount_without_tax)
        self._update_stacked_bar_chart(
            self.ui.chart_with_tax, self.savings_sim.yearly_savings_amount_with_tax)
        
        self._savings_plan_changed()
    
    def closeEvent(self, event):
        if not self.savings_sim.is_saved:
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