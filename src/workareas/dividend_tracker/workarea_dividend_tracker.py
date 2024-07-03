# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtWidgets, QtGui, QtChart

from src.workareas.dividend_tracker.ui_mainbody_dividend_tracker import Ui_Form as Ui_Form_Mainbody
from src.workareas.dividend_tracker.ui_slidemenu_dividend_tracker import Ui_Form as Ui_Form_Slidemenu
from src.workareas.dividend_tracker.ui_dialog_share import Ui_Dialog as Ui_Dialog_Share
from src.workareas.dividend_tracker.ui_dialog_booking import Ui_Dialog as Ui_Dialog_Booking
from src.workareas.dividend_tracker.ui_dialog_table_settings import Ui_Dialog as Ui_Dialog_Table_Settings

import math
from datetime import date as dt
from src.workareas.dividend_tracker.model.dividend_tracker import Share, Portfolio

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
            QtGui.QPixmap(':/icons/icons/cash-multiple.svg'),
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
                self.ui_mainbody.frame_3, self.ui_mainbody.frame_4,
                self.ui_mainbody.frame_11, self.ui_mainbody.frame_12,
                self.ui_mainbody.chart_dashboard
                ]:
            shadow = QtWidgets.QGraphicsDropShadowEffect()
            shadow.setBlurRadius(8)
            shadow.setXOffset(0)
            shadow.setYOffset(0)
            shadow.setColor(QtGui.QColor(0, 0, 0, 255))
            _w.setGraphicsEffect(shadow)
        
        self.dividend_portfolio = Portfolio()
        
        self.ui_mainbody.spin_box_end_year.valueChanged.connect(
            lambda n: self.ui_mainbody.spin_box_start_year.setMaximum(n)
            )
        self.ui_mainbody.spin_box_start_year.valueChanged.connect(
            lambda n: self.ui_mainbody.spin_box_end_year.setMinimum(n)
            )
        
        self.table_model_all_bookings = BookingsTableModel(
            self.dividend_portfolio
            )
        
        self.sort_bookings_proxy_model = QtCore.QSortFilterProxyModel()
        self.sort_bookings_proxy_model.setSourceModel(self.table_model_all_bookings)
        self.sort_bookings_proxy_model.setSortRole(BookingsTableModel.SORT_ROLE)
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
        
        
        self.table_model_all_shares = ShareTableModel(
            self.dividend_portfolio
            )
        
        self.sort_shares_proxy_model = QtCore.QSortFilterProxyModel()
        self.sort_shares_proxy_model.setSourceModel(self.table_model_all_shares)
        self.sort_shares_proxy_model.setSortRole(ShareTableModel.SORT_ROLE)
        self.ui_mainbody.table_view_all_shares.setModel(
            self.sort_shares_proxy_model
            )
        self.ui_mainbody.table_view_all_shares.setSortingEnabled(True)
        self.sort_shares_proxy_model.sort(0, QtCore.Qt.DescendingOrder)
        
        self.ui_mainbody.table_view_all_shares.setSelectionBehavior(
            QtWidgets.QTableView.SelectRows
            )
        self.ui_mainbody.table_view_all_shares.setSelectionMode(
            QtWidgets.QTableView.SingleSelection
            )
        self.ui_mainbody.table_view_all_shares.horizontalHeader().setStretchLastSection(True)
        
        self._update_tables()
        self._update_all_portfolio_specific_values()
        self._update_staked_bar_chart()
        
        self.ui_mainbody.button_edit_share.clicked.connect(
            self.open_dialog_edit_share
            )
        self.ui_mainbody.table_view_all_shares.doubleClicked.connect(
            self.open_dialog_edit_share
            )
        self.ui_mainbody.button_delete_share.clicked.connect(
            self.delete_share
            )
        self.ui_mainbody.button_table_settings_share.clicked.connect(
            self.open_dialog_table_settings_share
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
        
        self.ui_slidemenu.button_new_portfolio.clicked.connect(
            self.new_dividend_portfolio
            )
        self.ui_slidemenu.button_new_share.clicked.connect(
            self.open_dialog_new_share
            )
        self.ui_slidemenu.button_new_booking.clicked.connect(
            self.open_dialog_new_booking
            )
        
        self.chart_dashboard_annotation = QtWidgets.QGraphicsSimpleTextItem(
            self.ui_mainbody.chart_dashboard
            )
        self.chart_dashboard_rect = QtWidgets.QGraphicsRectItem(
            self.ui_mainbody.chart_dashboard)
        self.chart_dashboard_rect.setBrush(QtCore.Qt.white)
        self.chart_dashboard_rect.setPen(QtCore.Qt.black)
    
    def register_change_observer(self, change_observer_callback):
        self._change_observer_callbacks.append(change_observer_callback)
    
    def _notify_change_observer(self):
        for callback in self._change_observer_callbacks:
            callback()
    
    def get_name_of_workarea(self):
        return 'Dividend tracker'
    
    def get_json_data_for_saving(self):
        return {
            'Columns share': ShareTableModel.USED_COLUMNS,
            'Columns booking': BookingsTableModel.USED_COLUMNS,
            'Portfolio': self.dividend_portfolio.get_json_data_for_saving()
            }
    
    def load_from_json_data(self, data):
        try:
            _dividend_portfolio = Portfolio.load_from_json_data(data['Portfolio'])
            ShareTableModel.USED_COLUMNS = data['Columns share']
            BookingsTableModel.USED_COLUMNS = data['Columns booking']
        except Exception as err:
            display_error(err)
            raise err
        
        self.dividend_portfolio = _dividend_portfolio
        self.table_model_all_bookings.dividend_portfolio = self.dividend_portfolio
        self.table_model_all_shares.dividend_portfolio = self.dividend_portfolio
        
        self._update_tables()
        self._update_all_portfolio_specific_values()
        self._update_staked_bar_chart()
    
    def set_default_values(self):
        self.dividend_portfolio = Portfolio()
        self.table_model_all_bookings.dividend_portfolio = self.dividend_portfolio
        self.table_model_all_shares.dividend_portfolio = self.dividend_portfolio
        ShareTableModel.USED_COLUMNS = list(
            ShareTableModel.COLUMN_INFO.keys()
            )
        BookingsTableModel.USED_COLUMNS = list(
            BookingsTableModel.COLUMN_INFO.keys()
            )
        
        self._update_tables()
        self._update_all_portfolio_specific_values()
        self._update_staked_bar_chart()
        self._notify_change_observer()
    
    def _update_tables(self):
        self.table_model_all_bookings.layoutChanged.emit()
        self.sort_bookings_proxy_model.layoutChanged.emit()
        for i in range(self.table_model_all_bookings.columnCount(None)):
            self.ui_mainbody.table_view_all_bookings.resizeColumnToContents(i)
        
        self.table_model_all_shares.layoutChanged.emit()
        self.sort_shares_proxy_model.layoutChanged.emit()
        for i in range(self.table_model_all_shares.columnCount(None)):
            self.ui_mainbody.table_view_all_shares.resizeColumnToContents(i)
    
    def _update_all_portfolio_specific_values(self):
        _years = sorted(set(
            d.date.year \
            for s in self.dividend_portfolio.all_shares \
            for d in s.dividend_payments
            ))
        if _years == []:
            _years = [9999]
            self.ui_mainbody.spin_box_start_year.setEnabled(False)
            self.ui_mainbody.spin_box_end_year.setEnabled(False)
            net_dividends = 0.0
            gross_dividends = 0.0
        else:
            self.ui_mainbody.spin_box_start_year.setEnabled(True)
            self.ui_mainbody.spin_box_end_year.setEnabled(True)
            dividend_fee = self.dividend_portfolio.get_total_dividend_fee(
                dt(_years[0], 1, 1), dt(_years[-1], 12, 31)
                )
            dividend_tax = self.dividend_portfolio.get_total_dividend_tax(
                dt(_years[0], 1, 1), dt(_years[-1], 12, 31)
                )
            gross_dividends = self.dividend_portfolio.get_total_dividend_amount(
                dt(_years[0], 1, 1), dt(_years[-1], 12, 31)
                )
            net_dividends = gross_dividends - dividend_tax - dividend_fee
        self.ui_mainbody.spin_box_start_year.setMinimum(_years[0])
        self.ui_mainbody.spin_box_start_year.setMaximum(_years[-1])
        self.ui_mainbody.spin_box_start_year.setValue(_years[0])
        self.ui_mainbody.spin_box_end_year.setMinimum(_years[0])
        self.ui_mainbody.spin_box_end_year.setMaximum(_years[-1])
        self.ui_mainbody.spin_box_end_year.setValue(_years[-1])
        
        self.ui_mainbody.label_tied_capital.setText(
            '{:,.2f} €'.format(self.dividend_portfolio.tied_capital)
            )
        self.ui_mainbody.label_total_gross_dividends.setText(
            '{:,.2f} €'.format(gross_dividends)
            )
        self.ui_mainbody.label_total_net_dividends.setText(
            '{:,.2f} €'.format(net_dividends)
            )
        self.ui_mainbody.label_rotc_last_12_m.setText(
            '{:,.2f} %'.format(
                self.dividend_portfolio.dividend_return_on_tied_capital_12_months
                )
            )
        self.ui_mainbody.label_yoc_last_12_m.setText(
            '{:,.2f} %'.format(self.dividend_portfolio.yield_on_cost_12_months)
            )
        self.ui_mainbody.label_realized_profit_loss.setText(
            '{:,.2f} €'.format(self.dividend_portfolio.realized_profit_loss)
            )
    
    def _update_staked_bar_chart(self):
        _start_year = self.ui_mainbody.spin_box_start_year.value()
        _end_year = self.ui_mainbody.spin_box_end_year.value()
        _years = list(range(_start_year, _end_year + 1))
        if _years == [9999]:
            self.ui_mainbody.chart_dashboard.removeAllSeries()
            for ax in self.ui_mainbody.chart_dashboard.axes():
                self.ui_mainbody.chart_dashboard.removeAxis(ax)
            return
        
        dividend_fee_by_year = [
            self.dividend_portfolio.get_total_dividend_fee(
                dt(_y, 1, 1), dt(_y, 12, 31)
                ) for _y in _years
            ]
        dividend_tax_by_year = [
            self.dividend_portfolio.get_total_dividend_tax(
                dt(_y, 1, 1), dt(_y, 12, 31)
                ) for _y in _years
            ]
        dividends_by_year = [
            self.dividend_portfolio.get_total_dividend_amount(
                dt(_y, 1, 1), dt(_y, 12, 31)
                ) for _y in _years
            ]
        net_dividends_by_year = [
            d-t-f for d,t,f in zip(
                dividends_by_year, dividend_tax_by_year, dividend_fee_by_year
                )
            ]
        
        series = QtChart.QStackedBarSeries()
        
        _max_value = max(net_dividends_by_year)
        set_dividends = QtChart.QBarSet('Net dividends')
        set_dividends.append(net_dividends_by_year)
        set_dividends.setColor(QtGui.QColor(0x25B92E))
        set_dividends.hovered.connect(self._show_info_label_on_hover)
        series.append(set_dividends)
        
        if self.ui_mainbody.check_box_tax.isChecked():
            _max_value += max(dividend_tax_by_year)
            set_dividend_tax = QtChart.QBarSet('Tax')
            set_dividend_tax.append(dividend_tax_by_year)
            set_dividend_tax.setColor(QtGui.QColor(0xBA2539))
            set_dividend_tax.hovered.connect(self._show_info_label_on_hover)
            series.append(set_dividend_tax)
        
        if self.ui_mainbody.check_box_fee.isChecked():
            _max_value += max(dividend_fee_by_year)
            set_dividend_fee = QtChart.QBarSet('Fee')
            set_dividend_fee.append(dividend_fee_by_year)
            set_dividend_fee.setColor(QtGui.QColor(0x2952B3))
            set_dividend_fee.hovered.connect(self._show_info_label_on_hover)
            series.append(set_dividend_fee)
        
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
        value_axis.setTickAnchor(min(0, min(dividends_by_year)))
        value_axis.setTickInterval(_tick_interval)
        value_axis.setMinorTickCount(1)
        value_axis.setLabelFormat('%.0f €')
        value_axis.setTitleText('Amount')
        
        for ax in self.ui_mainbody.chart_dashboard.axes():
            self.ui_mainbody.chart_dashboard.removeAxis(ax)
        self.ui_mainbody.chart_dashboard.setAxisX(year_axis, series)
        self.ui_mainbody.chart_dashboard.setAxisY(value_axis, series)
    
    def _show_info_label_on_hover(self, status, index):
        chart = self.ui_mainbody.chart_dashboard
        chart_annotation = self.chart_dashboard_annotation
        chart_rect = self.chart_dashboard_rect
        
        chart_rect.setVisible(status)
        chart_annotation.setBrush(
            QtGui.QBrush(QtCore.Qt.black)
            )
        
        _sets = chart.series()[0].barSets()
        
        _labels = ['{:>11,.2f} € (Net dividends)']
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
    
    def switch_stacked_widget(self, with_tax):
        if with_tax:
            self.ui_mainbody.stackedWidget.setCurrentIndex(1)
        else:
            self.ui_mainbody.stackedWidget.setCurrentIndex(0)
    
    def _get_selected_share(self):
        share = None
        r = self.ui_mainbody.table_view_all_shares.selectionModel().selectedRows()
        if r:
            row = self.sort_shares_proxy_model.mapToSource(r[0]).row()
            index = self.table_model_all_shares.createIndex(row, 0)
            share = self.table_model_all_shares.data(
                index, ShareTableModel.GET_DATA_ROLE
                )
        return share
    
    def new_dividend_portfolio(self):
        message = ('If you creeate a new dividend portfolio, '
                   'all data of the current dividend portfolio '
                   'will be lost.\n\n'
                   'Do you want to continue?')
            
        button = QtWidgets.QMessageBox.question(
            self.slidemenu, 'Dividend Portfolio - New', message,
            QtWidgets.QMessageBox.Cancel | QtWidgets.QMessageBox.Yes
            )
        if button == QtWidgets.QMessageBox.Cancel:
            return
        
        self.table_model_all_shares.layoutAboutToBeChanged.emit()
        self.table_model_all_bookings.layoutAboutToBeChanged.emit()
        self.set_default_values()
    
    def open_dialog_new_share(self):
        self.table_model_all_shares.layoutAboutToBeChanged.emit()
        self.table_model_all_bookings.layoutAboutToBeChanged.emit()
        dialog_share = DialogShare(
            self.dividend_portfolio, is_new_share = True, share = None
            )
        dialog_share.exec()
        if dialog_share.accepted:
            self._update_tables()
            self._notify_change_observer()
    
    def open_dialog_edit_share(self):
        share = self._get_selected_share()
        
        if share:
            self.table_model_all_shares.layoutAboutToBeChanged.emit()
            self.table_model_all_bookings.layoutAboutToBeChanged.emit()
            dialog_share = DialogShare(
                self.dividend_portfolio, is_new_share = False, share = share
                )
            dialog_share.exec()
            if dialog_share.accepted:
                self._update_tables()
                self._notify_change_observer()
    
    def delete_share(self):
        share = self._get_selected_share()
        
        if share:
            message = ('Do you really want to delete share\n'
                       '"{} ({})"?\n\n').format(
                           share.name, share.isin
                           )
            button = QtWidgets.QMessageBox.question(
                self.slidemenu, 'Delete share', message,
                QtWidgets.QMessageBox.Cancel | QtWidgets.QMessageBox.Yes
                )
            if button == QtWidgets.QMessageBox.Cancel:
                return
            
            try:
                self.table_model_all_shares.layoutAboutToBeChanged.emit()
                self.table_model_all_bookings.layoutAboutToBeChanged.emit()
                self.dividend_portfolio.remove_share(share)
            except Exception as err:
                display_error(err)
                return
            
            self._update_tables()
            self.ui_mainbody.table_view_all_shares.clearSelection()
            self._update_all_portfolio_specific_values()
            self._update_staked_bar_chart()
            self._notify_change_observer()
    
    def _get_selected_booking(self):
        share, booking = None, None
        r = self.ui_mainbody.table_view_all_bookings.selectionModel().selectedRows()
        if r:
            row = self.sort_bookings_proxy_model.mapToSource(r[0]).row()
            index = self.table_model_all_bookings.createIndex(row, 0)
            share, booking = self.table_model_all_bookings.data(
                index, BookingsTableModel.GET_DATA_ROLE
                )
        return share, booking
    
    def open_dialog_new_booking(self):
        if self.dividend_portfolio.all_shares == []:
            message = ('There are no shares available in this portfolio. '
                       'Please add a new share first.')
            
            QtWidgets.QMessageBox.information(
                self.slidemenu, 'No shares available', message,
                QtWidgets.QMessageBox.Ok
                )
            return
        
        self.table_model_all_shares.layoutAboutToBeChanged.emit()
        self.table_model_all_bookings.layoutAboutToBeChanged.emit()
        dialog_booking = DialogBooking(
            self.dividend_portfolio, is_new_booking = True,
            share = None, booking = None
            )
        dialog_booking.exec()
        if dialog_booking.accepted:
            self._update_tables()
            self._update_all_portfolio_specific_values()
            self._update_staked_bar_chart()
            self._notify_change_observer()
    
    def open_dialog_edit_booking(self):
        share, booking = None, None
        
        share, booking = self._get_selected_booking()
        
        if share and booking:
            self.table_model_all_shares.layoutAboutToBeChanged.emit()
            self.table_model_all_bookings.layoutAboutToBeChanged.emit()
            dialog_booking = DialogBooking(
                self.dividend_portfolio, is_new_booking = False,
                share = share, booking = booking
                )
            dialog_booking.exec()
            if dialog_booking.accepted:
                self._update_tables()
                self._update_all_portfolio_specific_values()
                self._update_staked_bar_chart()
                self._notify_change_observer()
    
    def open_dialog_table_settings_share(self):
        self.table_model_all_shares.layoutAboutToBeChanged.emit()
        self.table_model_all_bookings.layoutAboutToBeChanged.emit()
        dialog_table_settings = DialogTableSettings(
            ShareTableModel.COLUMN_INFO,
            ShareTableModel.USED_COLUMNS
            )
        dialog_table_settings.exec()
        if dialog_table_settings.accepted:
            ShareTableModel.USED_COLUMNS = dialog_table_settings.used_columns
            self._update_tables()
            self._notify_change_observer()
        
    def open_dialog_table_settings_booking(self):
        self.table_model_all_shares.layoutAboutToBeChanged.emit()
        self.table_model_all_bookings.layoutAboutToBeChanged.emit()
        dialog_table_settings = DialogTableSettings(
            BookingsTableModel.COLUMN_INFO,
            BookingsTableModel.USED_COLUMNS
            )
        dialog_table_settings.exec()
        if dialog_table_settings.accepted:
            BookingsTableModel.USED_COLUMNS = dialog_table_settings.used_columns
            self._update_tables()
            self._notify_change_observer()
    
    def delete_booking(self):
        share, booking = self._get_selected_booking()
        
        if booking:
            message = ('Do you really want to delete booking\n'
                       '"{}: {} ({}) from {}"?\n\n').format(
                           booking.type, booking.name, booking.isin, booking.date
                           )
            button = QtWidgets.QMessageBox.question(
                self.slidemenu, 'Delete booking', message,
                QtWidgets.QMessageBox.Cancel | QtWidgets.QMessageBox.Yes
                )
            if button == QtWidgets.QMessageBox.Cancel:
                return
            
            try:
                self.table_model_all_shares.layoutAboutToBeChanged.emit()
                self.table_model_all_bookings.layoutAboutToBeChanged.emit()
                share.delete_booking(booking)
            except Exception as err:
                display_error(err)
                return
            
            self._update_tables()
            self.ui_mainbody.table_view_all_bookings.clearSelection()
            self._update_all_portfolio_specific_values()
            self._update_staked_bar_chart()
            self._notify_change_observer()

class BookingsTableModel(QtCore.QAbstractTableModel):
    
    COLUMN_INFO = {
        0: ['date', 'Date', ' {} ', str],
        1: ['type', 'Type', ' {} ', str],
        2: ['name', 'Name', ' {} ', str],
        3: ['isin', 'ISIN', ' {} ', str],
        4: ['number_of_shares', '# Shares', ' {:.2f}', float],
        5: ['amount_per_share', 'Amount/Share', ' {:,.2f} €', float],
        6: ['amount', 'Amount', ' {:,.2f} €', float],
        7: ['fee', 'Fee', ' {:,.2f} €', float],
        8: ['tax', 'Tax', ' {:,.2f} €', float]
        }
    
    USED_COLUMNS = list(COLUMN_INFO.keys())
    
    GET_DATA_ROLE = QtCore.Qt.UserRole
    SORT_ROLE = QtCore.Qt.UserRole + 1
    
    def __init__(self, dividend_portfolio):
        super(BookingsTableModel, self).__init__()
        self.dividend_portfolio = dividend_portfolio
    
    def _get_booking(self, index):
        n = 0
        for share in self.dividend_portfolio.all_shares:
            if index.row() < n + len(share.buy_orders):
                booking = share.buy_orders[index.row() - n]
                break
            n += len(share.buy_orders)
            
            if index.row() < n + len(share.sell_orders):
                booking = share.sell_orders[index.row() - n]
                break
            n += len(share.sell_orders)
            
            if index.row() < n + len(share.dividend_payments):
                booking = share.dividend_payments[index.row() - n]
                break
            n += len(share.dividend_payments)
        
        return share, booking
    
    def data(self, index, role):
        if role == QtCore.Qt.DisplayRole:
            
            _, booking = self._get_booking(index)
            
            col = self.USED_COLUMNS[index.column()]
            
            attr_name = self.COLUMN_INFO[col][0]
            attr_format = self.COLUMN_INFO[col][2]
            
            value = getattr(booking, attr_name)
            
            if value != None:
                value_str = attr_format.format(value)
            else:
                value_str = 'N/A'
            
            return value_str
        
        if role == QtCore.Qt.TextAlignmentRole:
            col = index.column()
            attr_format = self.COLUMN_INFO[col][2]
            if attr_format != '{}':
                return QtCore.Qt.AlignVCenter + QtCore.Qt.AlignRight
            else:
                return QtCore.Qt.AlignVCenter + QtCore.Qt.AlignLeft
        
        if role == self.GET_DATA_ROLE:
            share, booking = self._get_booking(index)
            return share, booking
        
        if role == self.SORT_ROLE:
            _, booking = self._get_booking(index)
            
            col = self.USED_COLUMNS[index.column()]
            
            attr_name = self.COLUMN_INFO[col][0]
            attr_type = self.COLUMN_INFO[col][3]
            
            value = getattr(booking, attr_name)
            
            if value == None:
                r_value = 'N/A'
            else:
                r_value = attr_type(value)
            
            return r_value
    
    def rowCount(self, index):
        return sum(
            len(s.buy_orders) + len(s.sell_orders) + len(s.dividend_payments)
            for s in self.dividend_portfolio.all_shares
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

class ShareTableModel(QtCore.QAbstractTableModel):
    
    COLUMN_INFO = {
        0:  ['name', 'Name', ' {} ', str],
        1:  ['isin', 'ISIN', ' {} ', str],
        2:  ['number_of_shares', '# Shares', ' {:.2f}', float],
        3:  ['acquisition_price', 'Acquisition price', ' {:,.2f} €', float],
        4:  ['tied_capital', 'Tied capital', ' {:,.2f} €', float],
        5:  ['realized_profit_loss', 'Realized P/L', ' {:,.2f} €', float],
        6:  ['total_net_dividend_payments', 'Total net dividends',' {:,.2f} €', float],
        7:  ['yield_on_cost_12_months', 'YOC (12m)', ' {:,.2f} %', float],
        8:  ['dividend_return_on_tied_capital_12_months', 'ROTC (12m)', ' {:,.2f} %', float],
        9:  ['date_last_dividend_payment', 'Date last dividend', ' {} ', str],
        10: ['days_since_last_dividend_payment', 'Days since last dividend', ' {:.0f} ', float]
        }
    
    USED_COLUMNS = list(COLUMN_INFO.keys())
    
    GET_DATA_ROLE = QtCore.Qt.UserRole
    SORT_ROLE = QtCore.Qt.UserRole + 1
    
    def __init__(self, dividend_portfolio):
        super(ShareTableModel, self).__init__()
        self.dividend_portfolio = dividend_portfolio
    
    def data(self, index, role):
        if role == QtCore.Qt.DisplayRole:
            
            share = self.dividend_portfolio.all_shares[index.row()]
            
            col = self.USED_COLUMNS[index.column()]
            
            attr_name = self.COLUMN_INFO[col][0]
            attr_format = self.COLUMN_INFO[col][2]
            
            value = getattr(share, attr_name)
            
            if value != None:
                value_str = attr_format.format(value)
            else:
                value_str = 'N/A'
            
            return value_str
        
        if role == QtCore.Qt.TextAlignmentRole:
            col = index.column()
            attr_format = self.COLUMN_INFO[col][2]
            if attr_format != '{}':
                return QtCore.Qt.AlignVCenter + QtCore.Qt.AlignRight
            else:
                return QtCore.Qt.AlignVCenter + QtCore.Qt.AlignLeft
        
        if role == self.GET_DATA_ROLE:
            share = self.dividend_portfolio.all_shares[index.row()]
            return share
        
        if role == self.SORT_ROLE:
            share = self.dividend_portfolio.all_shares[index.row()]
            
            col = self.USED_COLUMNS[index.column()]
            
            attr_name = self.COLUMN_INFO[col][0]
            attr_type = self.COLUMN_INFO[col][3]
            
            value = getattr(share, attr_name)
            
            if value == None:
                r_value = 'N/A'
            else:
                r_value = attr_type(value)
            
            return r_value
    
    def rowCount(self, index):
        return len(self.dividend_portfolio.all_shares)
    
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

class DialogShare(QtWidgets.QDialog):
    def __init__(self, dividend_portfolio, is_new_share = False, share = None):
        super(DialogShare, self).__init__()
        
        self.dividend_portfolio = dividend_portfolio
        self.is_new_share = is_new_share
        self.share = share
        self.accepted = False
        
        if self.is_new_share:
            self.setup_gui_new()
        else:
            self.setup_gui_edit()
    
    def _setup_gui(self):
        self.ui_dialog = Ui_Dialog_Share()
        self.ui_dialog.setupUi(self)
        
        shadow = QtWidgets.QGraphicsDropShadowEffect()
        shadow.setBlurRadius(8)
        shadow.setXOffset(0)
        shadow.setYOffset(0)
        shadow.setColor(QtGui.QColor(0, 0, 0, 255))
        self.ui_dialog.frame_header.setGraphicsEffect(shadow)
    
    def setup_gui_new(self):
        self._setup_gui()
        self.setWindowTitle('New')
        
        self.ui_dialog.line_edit_name.setText('')
        self.ui_dialog.line_edit_isin.setText('')
    
    def setup_gui_edit(self):
        self._setup_gui()
        self.setWindowTitle('Edit')
        
        self.ui_dialog.line_edit_name.setText(self.share.name)
        self.ui_dialog.line_edit_isin.setText(self.share.isin)
    
    def accept(self):
        new_name = self.ui_dialog.line_edit_name.text()
        new_isin = self.ui_dialog.line_edit_isin.text()
        
        try:
            if self.is_new_share:
                new_share = Share(new_name, new_isin)
                self.dividend_portfolio.add_share(new_share)
            else:
                self.dividend_portfolio.update_share(self.share, new_name, new_isin)
        except Exception as err:
            display_error(err)
            return
        
        self.accepted = True
        self.close()

class DialogBooking(QtWidgets.QDialog):
    def __init__(self, dividend_portfolio, is_new_booking = False, share = None, booking = None):
        super(DialogBooking, self).__init__()
        
        self.dividend_portfolio = dividend_portfolio
        self.is_new_booking = is_new_booking
        self.share = share
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
        
        self.ui_dialog.combo_box_type.currentIndexChanged.connect(
            self._update_total_value_and_total_amount
            )
        
        self.ui_dialog.number_of_shares.valueChanged.connect(
            self._update_total_value_and_total_amount
            )
        self.ui_dialog.amount_per_share.valueChanged.connect(
            self._update_total_value_and_total_amount
            )
        
        self.ui_dialog.fee.valueChanged.connect(
            self._update_total_value_and_total_amount
            )
        self.ui_dialog.tax.valueChanged.connect(
            self._update_total_value_and_total_amount
            )
    
    def _update_total_value_and_total_amount(self):
        number_of_shares = self.ui_dialog.number_of_shares.value()
        amount_per_share = self.ui_dialog.amount_per_share.value()
        
        self.ui_dialog.total_amount.setText(
            '{:,.2f} €'.format(number_of_shares * amount_per_share)
            )
        
        _factor = -1.0
        if self.ui_dialog.combo_box_type.currentText() == 'Buy':
            _factor = 1.0
        
        self.ui_dialog.total_value.setText(
            '{:,.2f} €'.format(
                number_of_shares * amount_per_share + \
                _factor * self.ui_dialog.fee.value() + \
                _factor * self.ui_dialog.tax.value()
                )
            )
    
    def setup_gui_new(self):
        self._setup_gui()
        self.setWindowTitle('New')
        
        for s in sorted(
                self.dividend_portfolio.all_shares,
                key = lambda v: v.name
                ):
            self.ui_dialog.combo_box_share.addItem(' {}'.format(s.name), s)
        
        for booking_type in ['Buy', 'Sell', 'Dividend']:
            self.ui_dialog.combo_box_type.addItem(booking_type)
        
        s = self.ui_dialog.combo_box_share.currentData()
        self.ui_dialog.label_name.setText('  {}'.format(s.name))
        self.ui_dialog.label_isin.setText('  {}'.format(s.isin))
        
        def pre_fill_data():
            i = self.ui_dialog.combo_box_share.currentIndex()
            s = self.ui_dialog.combo_box_share.itemData(i)
            self.ui_dialog.label_name.setText('  {}'.format(s.name))
            self.ui_dialog.label_isin.setText('  {}'.format(s.isin))
            if self.ui_dialog.combo_box_type.currentText() in ['Sell', 'Dividend']:
                self.ui_dialog.number_of_shares.setValue(s.number_of_shares)
            else:
                self.ui_dialog.number_of_shares.setValue(0.0)
        
        self.ui_dialog.combo_box_share.currentIndexChanged.connect(
            pre_fill_data
            )
        self.ui_dialog.combo_box_type.currentIndexChanged.connect(
            pre_fill_data
            )
        
        self.ui_dialog.date_booking.setDate(dt.today())
        
        self.ui_dialog.total_amount.setText(
            '{:,.2f} €'.format(
                self.ui_dialog.number_of_shares.value() * \
                self.ui_dialog.amount_per_share.value()
                )
            )
        
        _factor = -1.0
        if self.ui_dialog.combo_box_type.currentText() == 'Buy':
            _factor = 1.0
        
        self.ui_dialog.total_value.setText(
            '{:,.2f} €'.format(
                self.ui_dialog.number_of_shares.value() * \
                self.ui_dialog.amount_per_share.value() + \
                _factor * self.ui_dialog.fee.value() + \
                _factor * self.ui_dialog.tax.value()
                )
            )
    
    def setup_gui_edit(self):
        self._setup_gui()
        self.setWindowTitle('Edit')
        
        self.ui_dialog.combo_box_share.addItem(' {}'.format(self.share.name))
        self.ui_dialog.label_name.setText('  {}'.format(self.share.name))
        self.ui_dialog.label_isin.setText('  {}'.format(self.share.isin))
        self.ui_dialog.combo_box_type.addItem(self.booking.type)
        self.ui_dialog.date_booking.setDate(self.booking.date)
        self.ui_dialog.number_of_shares.setValue(self.booking.number_of_shares)
        self.ui_dialog.amount_per_share.setValue(self.booking.amount_per_share)
        self.ui_dialog.total_amount.setText(
            '{:,.2f} €'.format(
                self.ui_dialog.number_of_shares.value() * \
                self.ui_dialog.amount_per_share.value()
                )
            )
        self.ui_dialog.fee.setValue(self.booking.fee)
        self.ui_dialog.tax.setValue(self.booking.tax)
        
        _factor = -1.0
        if self.ui_dialog.combo_box_type.currentText() == 'Buy':
            _factor = 1.0
        
        self.ui_dialog.total_value.setText(
            '{:,.2f} €'.format(
                self.ui_dialog.number_of_shares.value() * \
                self.ui_dialog.amount_per_share.value() + \
                _factor * self.ui_dialog.fee.value() + \
                _factor * self.ui_dialog.tax.value()
                )
            )
    
    def accept(self):
        new_date = self.ui_dialog.date_booking.date().toPyDate()
        new_number_of_shares = self.ui_dialog.number_of_shares.value()
        new_amount_per_share = self.ui_dialog.amount_per_share.value()
        new_fee = self.ui_dialog.fee.value()
        new_tax = self.ui_dialog.tax.value()
        
        try:
            if self.is_new_booking:
                share = self.ui_dialog.combo_box_share.itemData(
                    self.ui_dialog.combo_box_share.currentIndex()
                    )
                booking_type = self.ui_dialog.combo_box_type.currentText()
                share.create_booking(
                    booking_type, new_date, new_number_of_shares,
                    new_amount_per_share, new_fee, new_tax
                    )
            else:
                self.share.update_booking(
                    self.booking, new_date, new_number_of_shares,
                    new_amount_per_share, new_fee, new_tax
                    )
        except Exception as err:
            display_error(err)
            return
        
        self.accepted = True
        self.close()

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
