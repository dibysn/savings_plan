# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtWidgets, QtGui, QtChart

from src.workareas.passive_income.ui_mainbody_passive_income import Ui_Form as Ui_Form_Mainbody
from src.workareas.passive_income.ui_slidemenu_passive_income import Ui_Form as Ui_Form_Slidemenu
from src.workareas.passive_income.ui_dialog_booking import Ui_Dialog as Ui_Dialog_Booking
from src.workareas.passive_income.ui_dialog_category import Ui_Dialog as Ui_Dialog_Category
from src.workareas.passive_income.ui_dialog_table_settings import Ui_Dialog as Ui_Dialog_Table_Settings

import math
from datetime import date as dt
from src.workareas.passive_income.model.passive_income import PassiveIncome

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
            QtGui.QPixmap(':/icons/icons/hand-coin-outline.svg'),
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
        
        self.ui_mainbody.chart_dashboard = QtChart.QChart()
        self.ui_mainbody.chart_dashboard.setTheme(
            QtChart.QChart.ChartThemeDark
            )
        self.ui_mainbody.chart_dashboard.setAnimationOptions(
            QtChart.QChart.SeriesAnimations
            )
        self.ui_mainbody.chartview_dashboard.setChart(
            self.ui_mainbody.chart_dashboard
            )
        
        for _w in [
                self.ui_slidemenu.frame_header,
                self.ui_mainbody.frame_11, self.ui_mainbody.frame_12,
                self.ui_mainbody.chart_dashboard
                ]:
            shadow = QtWidgets.QGraphicsDropShadowEffect()
            shadow.setBlurRadius(8)
            shadow.setXOffset(0)
            shadow.setYOffset(0)
            shadow.setColor(QtGui.QColor(0, 0, 0, 255))
            _w.setGraphicsEffect(shadow)
        
        self.passive_income = PassiveIncome()
        
        self.ui_mainbody.spin_box_end_year.valueChanged.connect(
            lambda n: self.ui_mainbody.spin_box_start_year.setMaximum(n)
            )
        self.ui_mainbody.spin_box_start_year.valueChanged.connect(
            lambda n: self.ui_mainbody.spin_box_end_year.setMinimum(n)
            )
        
        self.chart_dashboard_annotation = QtWidgets.QGraphicsSimpleTextItem(
            self.ui_mainbody.chart_dashboard
            )
        self.chart_dashboard_rect = QtWidgets.QGraphicsRectItem(
            self.ui_mainbody.chart_dashboard)
        self.chart_dashboard_rect.setBrush(QtCore.Qt.white)
        self.chart_dashboard_rect.setPen(QtCore.Qt.black)
        
        self._update_staked_bar_chart()
        
        self.ui_mainbody.check_box_tax.stateChanged.connect(
            self._update_staked_bar_chart
            )
        self.ui_mainbody.check_box_fee.stateChanged.connect(
            self._update_staked_bar_chart
            )
        self.ui_mainbody.spin_box_start_year.valueChanged.connect(
            self._update_staked_bar_chart
            )
        self.ui_mainbody.spin_box_end_year.valueChanged.connect(
            self._update_staked_bar_chart
            )
        
        self.ui_slidemenu.button_categories.clicked.connect(
            self.open_dialog_category
            )
        self.ui_slidemenu.button_new_booking.clicked.connect(
            self.open_dialog_new_booking
            )
        self.ui_mainbody.button_edit_booking.clicked.connect(
            self.open_dialog_edit_booking
            )
        self.ui_mainbody.table_view_all_bookings.doubleClicked.connect(
            self.open_dialog_edit_booking
            )
        self.ui_mainbody.button_delete_booking.clicked.connect(
            self.delete_booking
            )
        self.ui_mainbody.button_table_settings_booking.clicked.connect(
            self.open_dialog_table_settings_booking
            )
        
        self.table_model_all_bookings = PassiveIncomeTableModel(
            self.passive_income
            )
        self.sort_bookings_proxy_model = QtCore.QSortFilterProxyModel()
        self.sort_bookings_proxy_model.setSourceModel(self.table_model_all_bookings)
        self.sort_bookings_proxy_model.setSortRole(PassiveIncomeTableModel.SORT_ROLE)
        self.ui_mainbody.table_view_all_bookings.setModel(
            self.sort_bookings_proxy_model
            )
        self.ui_mainbody.table_view_all_bookings.setSortingEnabled(True)
        self.sort_bookings_proxy_model.sort(0, QtCore.Qt.DescendingOrder)
        
        self.ui_mainbody.table_view_all_bookings.setSelectionBehavior(
            QtWidgets.QTableView.SelectRows
            )
        self.ui_mainbody.table_view_all_bookings.setSelectionMode(
            QtWidgets.QTableView.SingleSelection
            )
        self.ui_mainbody.table_view_all_bookings.horizontalHeader().setStretchLastSection(True)
        
        self._update_table()
        self._update_all_portfolio_specific_values()
        self._update_staked_bar_chart()
    
    def register_change_observer(self, change_observer_callback):
        self._change_observer_callbacks.append(change_observer_callback)
    
    def _notify_change_observer(self):
        for callback in self._change_observer_callbacks:
            callback()
    
    def get_name_of_workarea(self):
        return 'Passive Income'
    
    def set_default_values(self):
        self.passive_income = PassiveIncome()
        self.table_model_all_bookings.passive_income = self.passive_income
        PassiveIncomeTableModel.USED_COLUMNS = list(
            PassiveIncomeTableModel.COLUMN_INFO.keys()
            )
        
        self._update_table()
        self._update_all_portfolio_specific_values()
        self._update_staked_bar_chart()
        self._notify_change_observer()
    
    def get_json_data_for_saving(self):
        return {
            'Columns': PassiveIncomeTableModel.USED_COLUMNS,
            'Bookings': self.passive_income.get_json_data_for_saving()
            }
    
    def load_from_json_data(self, data):
        try:
            _passive_income = PassiveIncome.load_from_json_data(data['Bookings'])
            PassiveIncomeTableModel.USED_COLUMNS = data['Columns']
        except Exception as err:
            display_error(err)
            raise err
        
        self.passive_income = _passive_income
        self.table_model_all_bookings.passive_income = self.passive_income
        
        self._update_table()
        self._update_all_portfolio_specific_values()
        self._update_staked_bar_chart()
    
    def _update_all_portfolio_specific_values(self):
        _years = sorted(set(
            b.date.year \
            for _, bs in self.passive_income.bookings_by_category.items() \
            for b in bs
            ))
                
        if _years == []:
            _years = [9999]
            self.ui_mainbody.spin_box_start_year.setEnabled(False)
            self.ui_mainbody.spin_box_end_year.setEnabled(False)
        else:
            self.ui_mainbody.spin_box_start_year.setEnabled(True)
            self.ui_mainbody.spin_box_end_year.setEnabled(True)
        self.ui_mainbody.spin_box_start_year.setMinimum(_years[0])
        self.ui_mainbody.spin_box_start_year.setMaximum(_years[-1])
        self.ui_mainbody.spin_box_start_year.setValue(_years[0])
        self.ui_mainbody.spin_box_end_year.setMinimum(_years[0])
        self.ui_mainbody.spin_box_end_year.setMaximum(_years[-1])
        self.ui_mainbody.spin_box_end_year.setValue(_years[-1])
    
    def _update_staked_bar_chart(self):
        _start_year = self.ui_mainbody.spin_box_start_year.value()
        _end_year = self.ui_mainbody.spin_box_end_year.value()
        _years = list(range(_start_year, _end_year + 1))
        
        if _years == [9999]:
            self.ui_mainbody.chart_dashboard.removeAllSeries()
            for ax in self.ui_mainbody.chart_dashboard.axes():
                self.ui_mainbody.chart_dashboard.removeAxis(ax)
            return
        
        passive_income_fee_by_year = [
            sum(v for _,v in self.passive_income.get_total_fee_by_category(
                dt(_y, 1, 1), dt(_y, 12, 31)
                ).items()) for _y in _years
            ]
        passive_income_tax_by_year = [
            sum(v for _,v in self.passive_income.get_total_tax_by_category(
                dt(_y, 1, 1), dt(_y, 12, 31)
                ).items()) for _y in _years
            ]
        passive_income_amount_by_year = [
            sum(v for _,v in self.passive_income.get_total_amount_by_category(
                dt(_y, 1, 1), dt(_y, 12, 31)
                ).items()) for _y in _years
            ]
        net_passive_income_by_year = [
            p-t-f for p,t,f in zip(
                passive_income_amount_by_year,
                passive_income_tax_by_year,
                passive_income_fee_by_year
                )
            ]
        
        series = QtChart.QStackedBarSeries()
        
        _max_value = max(net_passive_income_by_year)
        set_passive_income = QtChart.QBarSet('Net passive income')
        set_passive_income.append(net_passive_income_by_year)
        set_passive_income.setColor(QtGui.QColor(0x25B92E))
        set_passive_income.hovered.connect(self._show_info_label_on_hover)
        series.append(set_passive_income)
        
        if self.ui_mainbody.check_box_tax.isChecked():
            _max_value += max(passive_income_tax_by_year)
            set_passive_income_tax = QtChart.QBarSet('Tax')
            set_passive_income_tax.append(passive_income_tax_by_year)
            set_passive_income_tax.setColor(QtGui.QColor(0xBA2539))
            set_passive_income_tax.hovered.connect(self._show_info_label_on_hover)
            series.append(set_passive_income_tax)
        
        if self.ui_mainbody.check_box_fee.isChecked():
            _max_value += max(passive_income_fee_by_year)
            set_passive_income_fee = QtChart.QBarSet('Fee')
            set_passive_income_fee.append(passive_income_fee_by_year)
            set_passive_income_fee.setColor(QtGui.QColor(0x2952B3))
            set_passive_income_fee.hovered.connect(self._show_info_label_on_hover)
            series.append(set_passive_income_fee)
        
        self.ui_mainbody.chart_dashboard.setLocalizeNumbers(True)
        self.ui_mainbody.chart_dashboard.removeAllSeries()
        self.ui_mainbody.chart_dashboard.addSeries(series)
        
        year_axis = QtChart.QBarCategoryAxis()
        year_axis.append(['{}'.format(_y) for _y in _years])
        year_axis.setTitleText('Year')
        
        _max = math.ceil(_max_value / 100) * 100
        _tick_interval = 100 * (_max // 500 + 1)
        value_axis = QtChart.QValueAxis()
        value_axis.setTickType(QtChart.QValueAxis.TicksDynamic)
        value_axis.setMin(0)
        value_axis.setMax(_max)
        value_axis.setTickAnchor(min(0, min(passive_income_amount_by_year)))
        value_axis.setTickInterval(_tick_interval)
        value_axis.setMinorTickCount(1)
        value_axis.setLabelFormat('%.0f €')
        value_axis.setTitleText('Amount')
        
        for ax in self.ui_mainbody.chart_dashboard.axes():
            self.ui_mainbody.chart_dashboard.removeAxis(ax)
        self.ui_mainbody.chart_dashboard.setAxisX(year_axis, series)
        self.ui_mainbody.chart_dashboard.setAxisY(value_axis, series)
    
    def _show_info_label_on_hover(self, status, index):
        # TODO
        # categories = self.passive_income.categories
        
        chart = self.ui_mainbody.chart_dashboard
        chart_annotation = self.chart_dashboard_annotation
        chart_rect = self.chart_dashboard_rect
        
        chart_rect.setVisible(status)
        chart_annotation.setBrush(
            QtGui.QBrush(QtCore.Qt.black)
            )
        
        _sets = chart.series()[0].barSets()
        
        _labels = ['{:>11,.2f} € (Net passive income)']
        if self.ui_mainbody.check_box_tax.isChecked():
            _labels.append('{:>11,.2f} € (Tax)')
        if self.ui_mainbody.check_box_fee.isChecked():
            _labels.append('{:>11,.2f} € (Fee)')
        
        x_axis_categories = chart.axes(QtCore.Qt.Horizontal)[0].categories()
        year = x_axis_categories[index]
        annotation_text = 'Year {}:'.format(year)
        _sum = 0.0
        for _l, _s in zip(_labels, _sets):
            annotation_text += '\n'
            annotation_text += _l.format(_s[index])
            _sum += _s[index]
        annotation_text += '\n{:>11,.2f} € (per month)'.format(_sum/12)
        ndays = (dt(int(year)+1,1,1) - dt(int(year),1,1)).days
        annotation_text += '\n{:>11,.2f} € (per day)'.format(_sum/ndays)
        chart_annotation.setText(annotation_text)
        
        y_axis = chart.axes(QtCore.Qt.Vertical)[0]
        p1 = chart.mapToPosition(
            QtCore.QPointF(-0.42, y_axis.max()*0.99)
            )
        
        chart_annotation.setPos(p1)
        chart_annotation.setZValue(20)
        chart_annotation.setVisible(status)
        
        r = chart_annotation.boundingRect()
        p2 = chart.mapToPosition(QtCore.QPointF(-0.45, y_axis.max()))
        p3 = p1-p2
        chart_rect.setRect(
            p2.x(), p2.y(),
            r.width()+2*p3.x(), r.height()+2*p3.y())
        chart_rect.setZValue(10)
        chart_rect.setVisible(status)
    
    def _get_selected_booking(self):
        booking = None
        r = self.ui_mainbody.table_view_all_bookings.selectionModel().selectedRows()
        if r:
            row = self.sort_bookings_proxy_model.mapToSource(r[0]).row()
            index = self.table_model_all_bookings.createIndex(row, 0)
            booking = self.table_model_all_bookings.data(
                index, PassiveIncomeTableModel.GET_DATA_ROLE
                )
        return booking
    
    def _update_table(self):
        self.table_model_all_bookings.layoutChanged.emit()
        self.sort_bookings_proxy_model.layoutChanged.emit()
        for i in range(self.table_model_all_bookings.columnCount(None)):
            self.ui_mainbody.table_view_all_bookings.resizeColumnToContents(i)
    
    def open_dialog_new_booking(self):
        if self.passive_income.categories == []:
            message = ('There are no categories available. '
                       'Please add a new category first.')
            
            QtWidgets.QMessageBox.information(
                self.slidemenu, 'No categories available', message,
                QtWidgets.QMessageBox.Ok
                )
            return
        
        self.table_model_all_bookings.layoutAboutToBeChanged.emit()
        dialog_booking = DialogBooking(
            self.passive_income,
            is_new_booking = True,
            booking = None
            )
        dialog_booking.exec()
        if dialog_booking.accepted:
            self._update_table()
            self._update_all_portfolio_specific_values()
            self._update_staked_bar_chart()
            self._notify_change_observer()
    
    def open_dialog_edit_booking(self):
        booking = self._get_selected_booking()
        
        if booking:
            self.table_model_all_bookings.layoutAboutToBeChanged.emit()
            dialog_booking = DialogBooking(
                self.passive_income,
                is_new_booking = False,
                booking = booking
                )
            dialog_booking.exec()
            if dialog_booking.accepted:
                self._update_table()
                self._update_all_portfolio_specific_values()
                self._update_staked_bar_chart()
                self._notify_change_observer()
    
    def delete_booking(self):
        booking = self._get_selected_booking()
        
        if booking:
            message = ('Do you really want to delete booking\n'
                       '"{}: {:,.2f} € (from {})"?\n\n').format(
                           booking.category, booking.amount, booking.date
                           )
            button = QtWidgets.QMessageBox.question(
                self.slidemenu, 'Delete booking', message,
                QtWidgets.QMessageBox.Cancel | QtWidgets.QMessageBox.Yes
                )
            if button == QtWidgets.QMessageBox.Cancel:
                return
            
            try:
                self.table_model_all_bookings.layoutAboutToBeChanged.emit()
                self.passive_income.delete_booking(booking)
            except Exception as err:
                display_error(err)
                return
            
            self._update_table()
            self.ui_mainbody.table_view_all_bookings.clearSelection()
            self._update_all_portfolio_specific_values()
            self._update_staked_bar_chart()
            self._notify_change_observer()
    
    def open_dialog_category(self):
        self.table_model_all_bookings.layoutAboutToBeChanged.emit()
        
        dialog_category = DialogCategory(
            self.passive_income
            )
        dialog_category.exec()
        
        self._update_table()
        self._update_all_portfolio_specific_values()
        self._update_staked_bar_chart()
        self._notify_change_observer()
    
    def open_dialog_table_settings_booking(self):
        dialog_table_settings = DialogTableSettings(
            PassiveIncomeTableModel.COLUMN_INFO,
            PassiveIncomeTableModel.USED_COLUMNS
            )
        dialog_table_settings.exec()
        if dialog_table_settings.accepted:
            PassiveIncomeTableModel.USED_COLUMNS = dialog_table_settings.used_columns
            self._update_table()
            self._notify_change_observer()

class PassiveIncomeTableModel(QtCore.QAbstractTableModel):
    
    COLUMN_INFO = {
        0: ['date', 'Date', ' {} ', str],
        1: ['category', 'Category', ' {} ', str],
        2: ['amount', 'Amount', ' {:,.2f} €', float],
        3: ['fee', 'Fee', ' {:,.2f} €', float],
        4: ['tax', 'Tax', ' {:,.2f} €', float]
        }
    
    USED_COLUMNS = list(COLUMN_INFO.keys())
    
    GET_DATA_ROLE = QtCore.Qt.UserRole
    SORT_ROLE = QtCore.Qt.UserRole + 1
    
    def __init__(self, passive_income):
        super(PassiveIncomeTableModel, self).__init__()
        self.passive_income = passive_income
    
    def _get_booking(self, index):
        booking = [
            b \
            for _, bs in self.passive_income.bookings_by_category.items() \
            for b in bs
            ][index.row()]
        return booking
    
    def data(self, index, role):
        if role == QtCore.Qt.DisplayRole:
            
            booking = self._get_booking(index)
            
            col = self.USED_COLUMNS[index.column()]
            
            attr_name = self.COLUMN_INFO[col][0]
            attr_format = self.COLUMN_INFO[col][2]
            
            value = getattr(booking, attr_name)
            value_str = attr_format.format(value)
            
            return value_str
        
        if role == QtCore.Qt.TextAlignmentRole:
            col = index.column()
            attr_format = self.COLUMN_INFO[col][2]
            if attr_format != ' {} ':
                return QtCore.Qt.AlignVCenter + QtCore.Qt.AlignRight
            else:
                return QtCore.Qt.AlignVCenter + QtCore.Qt.AlignLeft
        
        if role == self.GET_DATA_ROLE:
            booking = self._get_booking(index)
            return booking
        
        if role == self.SORT_ROLE:
            booking = self._get_booking(index)
            
            col = self.USED_COLUMNS[index.column()]
            
            attr_name = self.COLUMN_INFO[col][0]
            attr_type = self.COLUMN_INFO[col][3]
            
            value = getattr(booking, attr_name)
            r_value = attr_type(value)
            
            return r_value
    
    def rowCount(self, index):
        return sum(
            len(bs) for _, bs in self.passive_income.bookings_by_category.items()
            )
    
    def columnCount(self, index):
        return len(self.USED_COLUMNS)
    
    def headerData(self, section, orientation, role):
        if role == QtCore.Qt.DisplayRole:
            if orientation == QtCore.Qt.Horizontal:
                _s = self.USED_COLUMNS[section]
                header_str = '  {}  '.format(
                    self.COLUMN_INFO[_s][1]
                    )
                return header_str

class DialogBooking(QtWidgets.QDialog):
    def __init__(self, passive_income, is_new_booking = False, booking = None):
        super(DialogBooking, self).__init__()
        
        self.passive_income = passive_income
        self.is_new_booking = is_new_booking
        self.booking = booking
        self.accepted = False
        
        if self.is_new_booking:
            self.setup_gui_new()
        else:
            self.setup_gui_edit()
    
    def _setup_gui(self):
        self.ui_dialog = Ui_Dialog_Booking()
        self.ui_dialog.setupUi(self)
        
        shadow = QtWidgets.QGraphicsDropShadowEffect()
        shadow.setBlurRadius(8)
        shadow.setXOffset(0)
        shadow.setYOffset(0)
        shadow.setColor(QtGui.QColor(0, 0, 0, 255))
        self.ui_dialog.frame_header.setGraphicsEffect(shadow)
        
        self.ui_dialog.amount_gross.valueChanged.connect(
            self._update_total_amount_net
            )
        self.ui_dialog.fee.valueChanged.connect(
            self._update_total_amount_net
            )
        self.ui_dialog.tax.valueChanged.connect(
            self._update_total_amount_net
            )
        
        for category in self.passive_income.categories:
            self.ui_dialog.combo_box_category.addItem(category)
    
    def _update_total_amount_net(self):
        self.ui_dialog.amount_net.setText(
            '{:,.2f} €'.format(
                self.ui_dialog.amount_gross.value() - \
                self.ui_dialog.fee.value() - \
                self.ui_dialog.tax.value()
                )
            )
    
    def setup_gui_new(self):
        self._setup_gui()
        self.setWindowTitle('New')
    
        self.ui_dialog.date_booking.setDate(dt.today())
        
        self.ui_dialog.amount_net.setText('{:,.2f} €'.format(0))
    
    def setup_gui_edit(self):
        self._setup_gui()
        self.setWindowTitle('Edit')
        
        self.ui_dialog.combo_box_category.setCurrentText(
            '{}'.format(self.booking.category)
            )
        
        self.ui_dialog.date_booking.setDate(self.booking.date)
        self.ui_dialog.amount_gross.setValue(self.booking.amount)
        self.ui_dialog.fee.setValue(self.booking.fee)
        self.ui_dialog.tax.setValue(self.booking.tax)
        self.ui_dialog.amount_net.setText(
            '{:,.2f} €'.format(
                self.booking.amount - \
                self.ui_dialog.fee.value() - \
                self.ui_dialog.tax.value()
                )
            )
    
    def accept(self):
        new_category = self.ui_dialog.combo_box_category.currentText()
        new_date = self.ui_dialog.date_booking.date().toPyDate()
        new_amount_gross = self.ui_dialog.amount_gross.value()
        new_fee = self.ui_dialog.fee.value()
        new_tax = self.ui_dialog.tax.value()
        
        try:
            if self.is_new_booking:
                self.passive_income.create_booking(
                    new_category, new_date,
                    new_amount_gross, new_fee, new_tax
                    )
            else:
                self.passive_income.update_booking(
                    self.booking, new_category, new_date,
                    new_amount_gross, new_fee, new_tax
                    )
        except Exception as err:
            display_error(err)
            return
        
        self.accepted = True
        self.close()

class DialogCategory(QtWidgets.QDialog):
    def __init__(self, passive_income):
        super(DialogCategory, self).__init__()
        self.passive_income = passive_income
        self.setup_gui()
    
    def setup_gui(self):
        self.setWindowTitle('Category')
        self.ui_dialog = Ui_Dialog_Category()
        self.ui_dialog.setupUi(self)
        
        shadow = QtWidgets.QGraphicsDropShadowEffect()
        shadow.setBlurRadius(8)
        shadow.setXOffset(0)
        shadow.setYOffset(0)
        shadow.setColor(QtGui.QColor(0, 0, 0, 255))
        self.ui_dialog.frame_header.setGraphicsEffect(shadow)
        
        self._reload_categories()
        
        self.ui_dialog.list_categories.currentTextChanged.connect(
            lambda v: self.ui_dialog.line_edit_name.setText(v)
            )
        self.ui_dialog.button_create.clicked.connect(
            self.create_category
            )
        self.ui_dialog.button_update.clicked.connect(
            self.update_category
            )
        self.ui_dialog.button_delete.clicked.connect(
            self.delete_category
            )
        
        self.ui_dialog.list_categories.setCurrentRow(0)
    
    def _reload_categories(self):
        self.ui_dialog.list_categories.clear()
        self.ui_dialog.list_categories.addItems(
            self.passive_income.categories
            )
    
    def create_category(self):
        category = self.ui_dialog.line_edit_name.text()
        try:
            self.passive_income.create_category(category)
        except Exception as err:
            display_error(err)
            return
        self._reload_categories()
    
    def update_category(self):
        category = self.ui_dialog.list_categories.selectedItems()
        if category != []:
            category = category[0]
            new_category = self.ui_dialog.line_edit_name.text()
            try:
                self.passive_income.update_category(category.text(), new_category)
            except Exception as err:
                display_error(err)
                return
            self._reload_categories()
    
    def delete_category(self):
        category = self.ui_dialog.list_categories.selectedItems()
        if category != []:
            category = category[0]
            
            message = ('Do you really want to delete the category "{}"?\n\n'
                       'You will also delete all bookings '
                       'for this category.\n\n').format(category.text())
            button = QtWidgets.QMessageBox.question(
                self, 'Delete category', message,
                QtWidgets.QMessageBox.Cancel | QtWidgets.QMessageBox.Yes
                )
            if button == QtWidgets.QMessageBox.Cancel:
                return
            
            try:
                self.passive_income.delete_category(category.text())
            except Exception as err:
                display_error(err)
                return
            self._reload_categories()

class DialogTableSettings(QtWidgets.QDialog):
    def __init__(self, all_column_data, used_columns):
        super(DialogTableSettings, self).__init__()
        self.all_column_data = all_column_data
        
        self.id_to_name = {i: v[1] for i, v in all_column_data.items()}
        self.name_to_id = {v[1]: i for i, v in all_column_data.items()}
        
        self.used_columns = used_columns
        self.accepted = False
        
        self.setup_gui()
    
    def setup_gui(self):
        self.ui_dialog = Ui_Dialog_Table_Settings()
        self.ui_dialog.setupUi(self)
        self.setWindowTitle('Settings')
        
        self.ui_dialog.button_reset_to_default.clicked.connect(
            self.reset_used_columns_to_default
            )
        
        all_header_displayed = [
            self.id_to_name[i] for i in self.used_columns
            ]
        
        all_header_not_displayed = [
            v for i, v in self.id_to_name.items() if i not in self.used_columns
            ]
            
        self.ui_dialog.list_displayed.addItems(all_header_displayed)
        self.ui_dialog.list_not_displayed.addItems(all_header_not_displayed)
    
    def reset_used_columns_to_default(self):
        self.used_columns = list(self.all_column_data.keys())
        self.ui_dialog.list_displayed.clear()
        self.ui_dialog.list_displayed.addItems(
            [self.id_to_name[i] for i in self.used_columns]
            )
        self.ui_dialog.list_not_displayed.clear()
        self.ui_dialog.list_not_displayed.addItems([])
    
    def accept(self):
        self.used_columns = [
            self.name_to_id[self.ui_dialog.list_displayed.item(i).text()] \
                for i in range(self.ui_dialog.list_displayed.count())
                ]
        
        self.accepted = True
        self.close()

def get_workarea_icon_and_widgets():
    icon = IconWorkarea().icon
    workarea = Workarea()
    slidemenu_widget = workarea.slidemenu
    mainbody_widget  = workarea.mainbody
    return workarea, icon, slidemenu_widget, mainbody_widget