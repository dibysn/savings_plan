# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtWidgets, QtGui, QtChart

from src.workareas.savings_simulation.ui_mainbody_savings_simulation import Ui_Form as Ui_Form_Mainbody
from src.workareas.savings_simulation.ui_slidemenu_savings_simulation import Ui_Form as Ui_Form_Slidemenu

from src.workareas.savings_simulation.ui_dialog_savings import Ui_Dialog as Ui_Dialog_Savings
from src.workareas.savings_simulation.ui_dialog_new_update_saving import Ui_Dialog as Ui_Dialog_New_Update_Saving

import math
from src.workareas.savings_simulation.model.savings_simulation import SavingsSimulation

def round_up(n, decimals = 0):
    multiplier = 10 ** decimals
    return math.ceil(2 * n * multiplier) / multiplier / 2

def display_error(err):
    msg_box = QtWidgets.QMessageBox()
    msg_box.setIcon(QtWidgets.QMessageBox.Critical)
    msg_box.setText(str(err))
    msg_box.setStandardButtons(QtWidgets.QMessageBox.Ok)
    msg_box.exec()

class IconWorkarea:
    def __init__(self):
        self.icon = QtGui.QIcon()
        self.icon.addPixmap(
            QtGui.QPixmap(':/icons/icons/calculator.svg'),
            QtGui.QIcon.Normal,
            QtGui.QIcon.Off
            )

class Workarea:
    def __init__(self):
        self.slidemenu = QtWidgets.QWidget()
        self.ui_slidemenu = Ui_Form_Slidemenu()
        self.ui_slidemenu.setupUi(self.slidemenu)
        self.mainbody = QtWidgets.QWidget()
        self.ui_mainbody = Ui_Form_Mainbody()
        self.ui_mainbody.setupUi(self.mainbody)
        
        self._change_observer_callbacks = []
        
        self.set_default_values()
        self.savings_sim = SavingsSimulation(
            self.ui_slidemenu.current_age.value(),
            self.ui_slidemenu.retirement_age.value(),
            self.ui_slidemenu.expected_age.value(),
            self.ui_slidemenu.initial_invest.value(),
            self.ui_slidemenu.monthly_withdrawal_nominal.value(),
            self.ui_slidemenu.rate_of_return.value() / 100.0,
            self.ui_slidemenu.rate_of_inflation.value() / 100.0,
            self.ui_slidemenu.flat_tax_rate.value() / 100.0,
            self.ui_slidemenu.solidarity_tax.value() / 100.0,
            self.ui_slidemenu.church_tax.value() / 100.0
            )
        
        self.ui_mainbody.chart_without_tax = QtChart.QChart()
        self.ui_mainbody.chart_without_tax.setTheme(QtChart.QChart.ChartThemeDark)
        self.ui_mainbody.chart_without_tax.setAnimationOptions(QtChart.QChart.SeriesAnimations)
        self.ui_mainbody.chartview_without_tax.setChart(self.ui_mainbody.chart_without_tax)
        
        self.ui_mainbody.chart_with_tax = QtChart.QChart()
        self.ui_mainbody.chart_with_tax.setTheme(QtChart.QChart.ChartThemeDark)
        self.ui_mainbody.chart_with_tax.setAnimationOptions(QtChart.QChart.SeriesAnimations)
        self.ui_mainbody.chartview_with_tax.setChart(self.ui_mainbody.chart_with_tax)
        
        for _w in [self.ui_mainbody.chart_without_tax, self.ui_mainbody.chart_with_tax,
                    self.ui_mainbody.frame_3, self.ui_mainbody.frame_4,
                    self.ui_mainbody.frame_5, self.ui_mainbody.frame_6,
                    self.ui_slidemenu.data_input_header_frame]:
            shadow = QtWidgets.QGraphicsDropShadowEffect()
            shadow.setBlurRadius(8)
            shadow.setXOffset(0)
            shadow.setYOffset(0)
            shadow.setColor(QtGui.QColor(0, 0, 0, 255))
            _w.setGraphicsEffect(shadow)
        
        self._update_text_all_labels()
        
        self._update_all_charts()
        
        self.ui_slidemenu.retirement_age.valueChanged.connect(
            lambda n: self.ui_slidemenu.current_age.setMaximum(n-1)
            )
        self.ui_slidemenu.retirement_age.valueChanged.connect(
            lambda n: self.ui_slidemenu.expected_age.setMinimum(n+1)
            )
        self.ui_slidemenu.current_age.valueChanged.connect(
            lambda n: self.ui_slidemenu.retirement_age.setMinimum(n+1)
            )
        self.ui_slidemenu.expected_age.valueChanged.connect(
            lambda n: self.ui_slidemenu.retirement_age.setMaximum(n-1)
            )
        
        self.ui_slidemenu.button_savings.clicked.connect(
            self.open_dialog_savings
            )
        
        self.ui_slidemenu.solidarity_tax.valueChanged['double'].connect(self.update_simulation)
        self.ui_slidemenu.retirement_age.valueChanged['int'].connect(self.update_simulation)
        self.ui_slidemenu.rate_of_return.valueChanged['double'].connect(self.update_simulation)
        self.ui_slidemenu.rate_of_inflation.valueChanged['double'].connect(self.update_simulation)
        self.ui_slidemenu.notes.textChanged.connect(self.notes_changed)
        self.ui_slidemenu.monthly_withdrawal_nominal.valueChanged['double'].connect(self.update_simulation)
        self.ui_slidemenu.initial_invest.valueChanged['double'].connect(self.update_simulation)
        self.ui_slidemenu.include_tax_check_box.clicked['bool'].connect(self.ui_slidemenu.flat_tax_rate.setEnabled)
        self.ui_slidemenu.include_tax_check_box.clicked['bool'].connect(self.ui_slidemenu.solidarity_tax.setEnabled)
        self.ui_slidemenu.include_tax_check_box.clicked['bool'].connect(self.ui_slidemenu.church_tax.setEnabled)
        self.ui_slidemenu.include_tax_check_box.clicked['bool'].connect(self.switch_stacked_widget)
        self.ui_slidemenu.flat_tax_rate.valueChanged['double'].connect(self.update_simulation)
        self.ui_slidemenu.expected_age.valueChanged['int'].connect(self.update_simulation)
        self.ui_slidemenu.current_age.valueChanged['int'].connect(self.update_simulation)
        self.ui_slidemenu.church_tax.valueChanged['double'].connect(self.update_simulation)
        self.ui_slidemenu.show_real_savings_check_box.clicked['bool'].connect(self._update_all_charts)
        
        self.chart_without_tax_annotation = QtWidgets.QGraphicsSimpleTextItem(
            self.ui_mainbody.chart_without_tax)
        self.chart_without_tax_rect = QtWidgets.QGraphicsRectItem(
            self.ui_mainbody.chart_without_tax)
        self.chart_without_tax_rect.setBrush(QtCore.Qt.white)
        self.chart_without_tax_rect.setPen(QtCore.Qt.black)
        
        self.chart_with_tax_annotation = QtWidgets.QGraphicsSimpleTextItem(
            self.ui_mainbody.chart_with_tax
            )
        self.chart_with_tax_rect = QtWidgets.QGraphicsRectItem(
            self.ui_mainbody.chart_with_tax)
        self.chart_with_tax_rect.setBrush(QtCore.Qt.white)
        self.chart_with_tax_rect.setPen(QtCore.Qt.black)
    
    def register_change_observer(self, change_observer_callback):
        self._change_observer_callbacks.append(change_observer_callback)
    
    def get_name_of_workarea(self):
        return 'Savings Simulation'
    
    def _notify_change_observer(self):
        for callback in self._change_observer_callbacks:
            callback()
    
    def set_default_values(self):
        self.ui_slidemenu.expected_age.setValue(99)
        self.ui_slidemenu.retirement_age.setValue(67)
        self.ui_slidemenu.current_age.setValue(30)
        self.ui_slidemenu.initial_invest.setValue(2000)
        self.ui_slidemenu.monthly_withdrawal_nominal.setValue(500)
        self.ui_slidemenu.rate_of_return.setValue(5.0)
        self.ui_slidemenu.rate_of_inflation.setValue(2.2)
        self.ui_slidemenu.flat_tax_rate.setValue(25)
        self.ui_slidemenu.solidarity_tax.setValue(5.5)
        self.ui_slidemenu.church_tax.setValue(8)
        self.ui_slidemenu.notes.clear()
        self.ui_slidemenu.include_tax_check_box.setChecked(False)
        self.ui_slidemenu.include_tax_check_box.clicked.emit(False)
        
        try:
            self.savings_sim.real_savings.clear_all()
            self._update_all_charts()
        except:
            pass
        
        self._notify_change_observer()
    
    def _update_text_all_labels(self):
        self.ui_mainbody.label_years_saving_1.setText(
            '{} years'.format(self.savings_sim.years_saving)
            )
        self.ui_mainbody.label_years_saving_2.setText(
            '{} years'.format(self.savings_sim.years_saving)
            )
        self.ui_mainbody.label_years_withdrawal_1.setText(
            '{} years'.format(self.savings_sim.years_withdrawal)
            )
        self.ui_mainbody.label_years_withdrawal_2.setText(
            '{} years'.format(self.savings_sim.years_withdrawal)
            )
        self.ui_mainbody.label_yearly_withdrawal_real_1.setText(
            '{:,.2f} €'.format(self.savings_sim.yearly_withdrawal_real)
            )
        self.ui_mainbody.label_yearly_withdrawal_real_2.setText(
            '{:,.2f} €'.format(self.savings_sim.yearly_withdrawal_real)
            )
        self.ui_mainbody.label_monthly_withdrawal_real_1.setText(
            '{:,.2f} €'.format(self.savings_sim.monthly_withdrawal_real)
            )
        self.ui_mainbody.label_monthly_withdrawal_real_2.setText(
            '{:,.2f} €'.format(self.savings_sim.monthly_withdrawal_real)
            )
        self.ui_mainbody.label_target_amount_without_tax.setText(
            '{:,.2f} €'.format(self.savings_sim.target_amount_without_tax)
            )
        self.ui_mainbody.label_yearly_savings_amount_without_tax.setText(
            '{:,.2f} €'.format(self.savings_sim.yearly_savings_amount_without_tax)
            )
        self.ui_mainbody.label_monthly_savings_amount_without_tax.setText(
            '{:,.2f} €'.format(self.savings_sim.monthly_savings_amount_without_tax)
            )
        self.ui_mainbody.label_target_amount_with_tax.setText(
            '{:,.2f} €'.format(self.savings_sim.target_amount_with_tax)
            )
        self.ui_mainbody.label_yearly_savings_amount_with_tax.setText(
            '{:,.2f} €'.format(self.savings_sim.yearly_savings_amount_with_tax)
            )
        self.ui_mainbody.label_monthly_savings_amount_with_tax.setText(
            '{:,.2f} €'.format(self.savings_sim.monthly_savings_amount_with_tax)
            )
        self.ui_mainbody.label_total_tax_rate.setText(
            '{:.2f}%'.format(self.savings_sim.total_tax_rate * 100.0)
            )
    
    def _update_all_charts(self):
        self._update_stacked_bar_chart(
            self.ui_mainbody.chart_without_tax, self.savings_sim.yearly_savings_amount_without_tax)
        self._update_stacked_bar_chart(
            self.ui_mainbody.chart_with_tax, self.savings_sim.yearly_savings_amount_with_tax)
    
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
        set_savings.setColor(QtGui.QColor(0x25B92E))
        set_growth = QtChart.QBarSet('Growth')
        set_growth.append(growth)
        set_growth.setColor(QtGui.QColor(0x4CA0C2))
        series = QtChart.QStackedBarSeries()
        series.append(set_savings)
        series.append(set_growth)
        
        set_savings.hovered.connect(self.show_info_label_on_hover)
        set_growth.hovered.connect(self.show_info_label_on_hover)
        
        if self.ui_slidemenu.show_real_savings_check_box.isChecked():
            savings_real = [0] * max(len(savings), len(self.savings_sim.real_savings.savings))
            growth_real = [0] * max(len(savings), len(self.savings_sim.real_savings.savings))
            for v in self.savings_sim.real_savings.savings:
                savings_real[v.year] = v.saving
                growth_real[v.year] = v.value - v.saving
            
            set_savings_real = QtChart.QBarSet('Savings (real)')
            set_savings_real.append(savings_real)
            set_savings_real.setColor(QtGui.QColor(0xA6A21F))
            set_growth_real = QtChart.QBarSet('Growth (real)')
            set_growth_real.append(growth_real)
            set_growth_real.setColor(QtGui.QColor(0xF7F019))
            series_real = QtChart.QStackedBarSeries()
            series_real.append(set_savings_real)
            series_real.append(set_growth_real)
            
            set_savings_real.hovered.connect(self.show_info_label_on_hover)
            set_growth_real.hovered.connect(self.show_info_label_on_hover)
        
        chart.setLocalizeNumbers(True)
        chart.removeAllSeries()
        chart.addSeries(series)        
        if self.ui_slidemenu.show_real_savings_check_box.isChecked():
            chart.addSeries(series_real)
        
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
        
        if self.ui_slidemenu.show_real_savings_check_box.isChecked():
            chart.setAxisX(year_axis, series_real)
            chart.setAxisY(value_axis, series_real)
    
    def show_info_label_on_hover(self, status, index):
        if self.ui_slidemenu.include_tax_check_box.isChecked():
            chart = self.ui_mainbody.chart_with_tax
            chart_annotation = self.chart_with_tax_annotation
            chart_rect = self.chart_with_tax_rect
        else:
            chart = self.ui_mainbody.chart_without_tax
            chart_annotation = self.chart_without_tax_annotation
            chart_rect = self.chart_without_tax_rect
        
        chart_rect.setVisible(status)
        chart_annotation.setBrush(
            QtGui.QBrush(QtCore.Qt.black)
            )
        
        set_savings, set_growth = chart.series()[0].barSets()
        
        if self.ui_slidemenu.show_real_savings_check_box.isChecked():
            set_savings_real, set_growth_real = chart.series()[1].barSets()
        
        if self.ui_slidemenu.show_real_savings_check_box.isChecked():
            chart_annotation.setText(
                ('Value after {} years:\n'
                 'Total:   {:,.2f} € ({:,.2f} € real)\n'
                 'Savings: {:,.2f} € ({:,.2f} € real)\n'
                 'Growth:  {:,.2f} € ({:,.2f} € real)').format(
                      index,
                      set_savings[index] + set_growth[index],
                      set_savings_real[index] + set_growth_real[index],
                      set_savings[index], set_savings_real[index],
                      set_growth[index], set_growth_real[index]))
        else:
            chart_annotation.setText(
                ('Value after {} years:\n'
                 'Total:   {:,.2f} €\n'
                 'Savings: {:,.2f} €\n'
                 'Growth:  {:,.2f} €').format(
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
    
    def switch_stacked_widget(self, with_tax):
        if with_tax:
            self.ui_mainbody.stackedWidget.setCurrentIndex(1)
        else:
            self.ui_mainbody.stackedWidget.setCurrentIndex(0)
    
    def notes_changed(self):
        try:
            self.savings_sim.notes = self.ui_slidemenu.notes.toPlainText()
            self._notify_change_observer()
        except:
            pass
    
    def update_simulation(self, value):
        _name = self.slidemenu.sender().objectName()
        if _name in [
                'rate_of_return', 'rate_of_inflation',
                'flat_tax_rate', 'solidarity_tax', 'church_tax'
                ]:
            value = value / 100.0
        
        setattr(self.savings_sim, _name, value)
        self._update_text_all_labels()
        self._update_all_charts()
        
        self._notify_change_observer()
    
    def get_json_data_for_saving(self):
        return self.savings_sim.get_json_data_for_saving()
    
    def load_from_json_data(self, data):
        try:
            _savings_sim = SavingsSimulation.load_from_json_data(data)
        except Exception as err:
            display_error(err)
            raise err
        
        self.ui_slidemenu.current_age.setValue(_savings_sim.current_age)
        self.ui_slidemenu.retirement_age.setValue(_savings_sim.retirement_age)
        self.ui_slidemenu.expected_age.setValue(_savings_sim.expected_age)
        self.ui_slidemenu.initial_invest.setValue(_savings_sim.initial_invest)
        self.ui_slidemenu.monthly_withdrawal_nominal.setValue(_savings_sim.monthly_withdrawal_nominal)
        self.ui_slidemenu.rate_of_return.setValue(_savings_sim.rate_of_return * 100.0)
        self.ui_slidemenu.rate_of_inflation.setValue(_savings_sim.rate_of_inflation * 100.0)
        self.ui_slidemenu.flat_tax_rate.setValue(_savings_sim.flat_tax_rate * 100.0)
        self.ui_slidemenu.solidarity_tax.setValue(_savings_sim.solidarity_tax * 100.0)
        self.ui_slidemenu.church_tax.setValue(_savings_sim.church_tax * 100.0)
        self.ui_slidemenu.notes.clear()
        self.ui_slidemenu.notes.insertPlainText(_savings_sim.notes)
        
        self.savings_sim = _savings_sim
        
        self._update_text_all_labels()
        self._update_all_charts()
    
    def open_dialog_savings(self):
        dialog_savings = DialogSavings(self.savings_sim.real_savings)
        dialog_savings.exec()
        if dialog_savings.changed:
            self._update_all_charts()
            self._notify_change_observer()
        
class DialogSavings(QtWidgets.QDialog):
    def __init__(self, real_savings):
        super(DialogSavings, self).__init__()
        self.real_savings = real_savings
        self.changed = False
        self.setup_gui()
    
    def setup_gui(self):
        self.ui_dialog = Ui_Dialog_Savings()
        self.ui_dialog.setupUi(self)
        self.setWindowTitle('Savings')
        
        self.table_model_savings = SavingsTableModel(
            self.real_savings
            )
        self.ui_dialog.table_view_savings.setModel(
            self.table_model_savings
            )
        self.ui_dialog.table_view_savings.setSelectionBehavior(
            QtWidgets.QTableView.SelectRows
            )
        self.ui_dialog.table_view_savings.setSelectionMode(
            QtWidgets.QTableView.SingleSelection
            )
        self.ui_dialog.table_view_savings.horizontalHeader().setStretchLastSection(True)
        
        self.ui_dialog.table_view_savings.doubleClicked.connect(
            self.edit_saving
            )
        
        self.ui_dialog.button_new.clicked.connect(
            self.new_saving
            )
        self.ui_dialog.button_edit.clicked.connect(
            self.edit_saving
            )
        self.ui_dialog.button_delete.clicked.connect(
            self.delete_saving
            )
        
        self._update_table()
        
    def _update_table(self):
        self.table_model_savings.layoutChanged.emit()
        for i in range(self.table_model_savings.columnCount(None)):
            self.ui_dialog.table_view_savings.resizeColumnToContents(i)
    
    def new_saving(self):
        dialog_new_update_saving = DialogNewUpdateSaving(
            self.real_savings, saving = None
            )
        dialog_new_update_saving.exec()
        if dialog_new_update_saving.accepted:
            self.changed = True
            self._update_table()
    
    def edit_saving(self):
        saving = self._get_selected_saving()
        if saving:
            dialog_new_update_saving = DialogNewUpdateSaving(
                self.real_savings, saving = saving
                )
            dialog_new_update_saving.exec()
            if dialog_new_update_saving.accepted:
                self.changed = True
                self._update_table()
    
    def delete_saving(self):
        saving = self._get_selected_saving()
        if saving:
            message = ('Do you really want to delete saving\n'
                       '"Year {}: saving {:,.2f} €, total {:,.2f} €"?\n\n').format(
                           saving.year, saving.saving, saving.value
                           )
            button = QtWidgets.QMessageBox.question(
                self, 'Delete saving', message,
                QtWidgets.QMessageBox.Cancel | QtWidgets.QMessageBox.Yes
                )
            if button == QtWidgets.QMessageBox.Cancel:
                return
            
            self.real_savings.delete_saving(saving)
            self.changed = True
            self._update_table()
    
    def _get_selected_saving(self):
        saving = None
        
        s = self.ui_dialog.table_view_savings.selectionModel().selectedRows()
        if s:
            row = s[0].row()
            index = self.table_model_savings.createIndex(row, 0)
            saving = self.table_model_savings.data(index, SavingsTableModel.GET_DATA_ROLE)
        return saving

class DialogNewUpdateSaving(QtWidgets.QDialog):
    def __init__(self, real_savings, saving = None):
        super(DialogNewUpdateSaving, self).__init__()
        self.real_savings = real_savings
        self.saving = saving
        self.accepted = False
        self.setup_gui()
    
    def setup_gui(self):
        self.ui_dialog = Ui_Dialog_New_Update_Saving()
        self.ui_dialog.setupUi(self)
        self.setWindowTitle('Saving')
        
        if self.saving != None:
            self.ui_dialog.spinbox_year.setValue(self.saving.year)
            self.ui_dialog.spinbox_saving.setValue(self.saving.saving)
            self.ui_dialog.spinbox_total.setValue(self.saving.value)
    
    def accept(self):
        year = self.ui_dialog.spinbox_year.value()
        saving = self.ui_dialog.spinbox_saving.value()
        value = self.ui_dialog.spinbox_total.value()
        
        try:
            if self.saving != None:
                self.real_savings.update_saving(self.saving, year, saving, value)
            else:
                self.real_savings.create_saving(year, saving, value)
        except Exception as err:
            display_error(err)
            return
        
        self.accepted = True
        self.close()

class SavingsTableModel(QtCore.QAbstractTableModel):
    
    GET_DATA_ROLE = QtCore.Qt.UserRole
    
    def __init__(self, real_savings):
        super(SavingsTableModel, self).__init__()
        self.real_savings = real_savings
    
    def data(self, index, role):
        if role == QtCore.Qt.DisplayRole:
            
            row = index.row()
            col = index.column()
            
            if col == 0:
                value_str = '{}'.format(self.real_savings.savings[row].year)
            elif col == 1:
                value_str = ' {:,.2f} €'.format(self.real_savings.savings[row].saving)
            elif col == 2:
                value_str = ' {:,.2f} €'.format(self.real_savings.savings[row].value)
            
            return value_str
        
        if role == QtCore.Qt.TextAlignmentRole:
            col = index.column()
            if col == 0:
                return QtCore.Qt.AlignVCenter + QtCore.Qt.AlignLeft
            else:
                return QtCore.Qt.AlignVCenter + QtCore.Qt.AlignRight
        
        if role == self.GET_DATA_ROLE:
            saving = self.real_savings.savings[index.row()]
            return saving
    
    def rowCount(self, index):
        return len(self.real_savings.savings)
    
    def columnCount(self, index):
        return 3
    
    def headerData(self, section, orientation, role):
        if role == QtCore.Qt.DisplayRole:
            if orientation == QtCore.Qt.Horizontal:
                if section == 0:
                    header_str = '  Year  '
                elif section == 1:
                    header_str = '  Savings  '
                elif section == 2:
                    header_str = '  Value  '
               
                return header_str

def get_workarea_icon_and_widgets():
    icon = IconWorkarea().icon
    workarea = Workarea()
    slidemenu_widget = workarea.slidemenu
    mainbody_widget  = workarea.mainbody
    return workarea, icon, slidemenu_widget, mainbody_widget