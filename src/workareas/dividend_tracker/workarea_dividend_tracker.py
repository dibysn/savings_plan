# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtWidgets, QtGui

from src.workareas.dividend_tracker.ui_mainbody_dividend_tracker import Ui_Form as Ui_Form_Mainbody
from src.workareas.dividend_tracker.ui_slidemenu_dividend_tracker import Ui_Form as Ui_Form_Slidemenu
from src.workareas.dividend_tracker.ui_dialog_share import Ui_Dialog as Ui_Dialog_Share
from src.workareas.dividend_tracker.ui_dialog_booking import Ui_Dialog as Ui_Dialog_Booking

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
        
        for _w in [
                self.ui_slidemenu.frame_header,
                ]:
            shadow = QtWidgets.QGraphicsDropShadowEffect()
            shadow.setBlurRadius(8)
            shadow.setXOffset(0)
            shadow.setYOffset(0)
            shadow.setColor(QtGui.QColor(0, 0, 0, 255))
            _w.setGraphicsEffect(shadow)
        
        ###############
        # TESTDATA
        
        from datetime import date as dt
        
        s1 = Share('ShareA', 'DE0012331')
        s2 = Share('ShareB', 'DE0044312')
        
        self.dividend_portfolio = Portfolio()
        self.dividend_portfolio.add_share(s1)
        self.dividend_portfolio.add_share(s2)
        
        orders_s1 = [
            ('buy',  dt(2022, 1, 2),    5, 10, 10,  0),
            ('buy',  dt(2022, 2, 10),  10, 15, 10,  0),
            ('buy',  dt(2022, 5, 11),  13,  3, 10,  0),
            ('sell', dt(2022, 9, 23),  10, 12, 10, 13.20),
            ('buy',  dt(2023, 2, 11),   5, 20, 12,  0),
            ('sell', dt(2023, 2, 15),  11,  8, 12, 12.10),
            ('buy',  dt(2023, 4, 2),   30,  8, 11,  1.10),
            ('sell', dt(2023, 11, 29), 10,  8, 12, 10.50)
            ]
        
        dividends_s1 = [
            (dt(2022, 2, 1),    3, 1.6, 1,  2),
            (dt(2022, 6, 5),   13, 1.6, 3,  0),
            (dt(2022, 9, 18),  13, 1.6, 0,  0),
            (dt(2022, 12, 1),  18, 1.6, 1, 10),
            (dt(2023, 2, 1),   18, 1.7, 5, 11),
            (dt(2023, 6, 19),  25, 1.7, 0,  9),
            (dt(2023, 10, 12), 15, 1.7, 0,  8),
            (dt(2023, 12, 6),  15, 1.7, 1,  3),
            ]
        
        orders_s2 = [
            ('buy',  dt(2022, 8, 11),  35,  7,  9,  1),
            ('buy',  dt(2022, 9, 9),   18, 10,  7,  0),
            ('buy',  dt(2023, 3, 17),  13,  8, 10,  1.30),
            ('sell', dt(2023, 3, 22),  10, 11, 10, 13.20)
            ]
        
        dividends_s2 = [
            (dt(2022, 9, 1),   10, 0.5, 1, 10),
            (dt(2023, 2, 2),   10, 0.5, 1, 10),
            (dt(2023, 4, 7),   30, 0.6, 8, 19),
            (dt(2023, 8, 18),  32, 0.6, 0,  8),
            (dt(2023, 11, 8),  33, 0.6, 1,  0),
            ]
        
        for o in orders_s1:
            if o[0] == 'buy':
                s1.create_buy_order(o[1], o[2], o[3], o[4], o[5])
            else:
                s1.create_sell_order(o[1], o[2], o[3], o[4], o[5])
        
        for d in dividends_s1:
            s1.create_dividend(d[0], d[1], d[2], d[3], d[4])
        
        for o in orders_s2:
            if o[0] == 'buy':
                s2.create_buy_order(o[1], o[2], o[3], o[4], o[5])
            else:
                s2.create_sell_order(o[1], o[2], o[3], o[4], o[5])
        
        for d in dividends_s2:
            s2.create_dividend(d[0], d[1], d[2], d[3], d[4])
        
        ###############
        
        self.table_model_all_bookings = BookingsTableModel(
            self.dividend_portfolio
            )
        self.ui_mainbody.table_view_all_bookings.setModel(
            self.table_model_all_bookings
            )
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
        self.ui_mainbody.table_view_all_shares.setModel(
            self.table_model_all_shares
            )
        self.ui_mainbody.table_view_all_shares.setSelectionBehavior(
            QtWidgets.QTableView.SelectRows
            )
        self.ui_mainbody.table_view_all_shares.setSelectionMode(
            QtWidgets.QTableView.SingleSelection
            )
        self.ui_mainbody.table_view_all_shares.horizontalHeader().setStretchLastSection(True)
        
        self._update_tables()
        
        self.ui_slidemenu.button_new_share.clicked.connect(
            self.open_dialog_new_share
            )
        self.ui_mainbody.button_edit_share.clicked.connect(
            self.open_dialog_edit_share
            )
        self.ui_mainbody.table_view_all_shares.doubleClicked.connect(
            self.open_dialog_edit_share
            )
        self.ui_mainbody.button_delete_share.clicked.connect(
            self.delete_share
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
    
    def register_change_observer(self, change_observer_callback):
        self._change_observer_callbacks.append(change_observer_callback)
    
    def _notify_change_observer(self):
        for callback in self._change_observer_callbacks:
            callback()
    
    def get_name_of_workarea(self):
        return 'Dividend tracker'
    
    def get_json_data_for_saving(self):
        raise NotImplementedError()
    
    def load_from_json_data(self, data):
        raise NotImplementedError()
    
    def set_default_values(self):
        raise NotImplementedError()
    
    def _update_tables(self):
        self.table_model_all_bookings.layoutChanged.emit()
        for i in range(self.table_model_all_bookings.columnCount(None)):
            self.ui_mainbody.table_view_all_bookings.resizeColumnToContents(i)
        self.table_model_all_shares.layoutChanged.emit()
        for i in range(self.table_model_all_shares.columnCount(None)):
            self.ui_mainbody.table_view_all_shares.resizeColumnToContents(i)
    
    def _get_selected_share(self):
        share = None
        r = self.ui_mainbody.table_view_all_shares.selectionModel().selectedRows()
        if r:
            row = r[0].row()
            index = self.table_model_all_shares.createIndex(row, 0)
            share = self.table_model_all_shares.data(index, QtCore.Qt.UserRole)
        return share
    
    def open_dialog_new_share(self):
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
            
            self.dividend_portfolio.remove_share(share)
            self._update_tables()
            
            self._notify_change_observer()
    
    def _get_selected_booking(self):
        share, booking = None, None
        r = self.ui_mainbody.table_view_all_bookings.selectionModel().selectedRows()
        if r:
            row = r[0].row()
            index = self.table_model_all_bookings.createIndex(row, 0)
            share, booking = self.table_model_all_bookings.data(index, QtCore.Qt.UserRole)
        return share, booking
    
    def open_dialog_new_booking(self):
        dialog_booking = DialogBooking(
            self.dividend_portfolio, is_new_booking = True,
            share = None, booking = None
            )
        dialog_booking.exec()
        if dialog_booking.accepted:
            self._update_tables()
            self._notify_change_observer()
    
    def open_dialog_edit_booking(self):
        share, booking = None, None
        
        share, booking = self._get_selected_booking()
        
        if share and booking:
            dialog_booking = DialogBooking(
                self.dividend_portfolio, is_new_booking = False,
                share = share, booking = booking
                )
            dialog_booking.exec()
            if dialog_booking.accepted:
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
                share.delete_booking(booking)
            except Exception as err:
                display_error(err)
                return
            
            self._update_tables()
            self._notify_change_observer()

class BookingsTableModel(QtCore.QAbstractTableModel):
    
    COLUMN_ORDER_AND_DISPLAY = {
        0: ['date', 'Date', ' {} '],
        1: ['type', 'Type', ' {} '],
        2: ['name', 'Name', ' {} '],
        3: ['isin', 'ISIN', ' {} '],
        4: ['number_of_shares', '# Shares', ' {:d}'],
        5: ['amount_per_share', 'Amount/Share', ' {:.2f} €'],
        6: ['amount', 'Amount', ' {:.2f} €'],
        7: ['fee', 'Fee', ' {:.2f} €'],
        8: ['tax', 'Tax', ' {:.2f} €']
        }
    
    USED_COLUMNS = list(COLUMN_ORDER_AND_DISPLAY.keys())
    
    def __init__(self, dividend_portfolio):
        super(BookingsTableModel, self).__init__()
        self.dividend_portfolio = dividend_portfolio
    
    # TODO: Überprüfen, ob alles korrekt angezeigt wird
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
            
            attr_name = self.COLUMN_ORDER_AND_DISPLAY[col][0]
            attr_format = self.COLUMN_ORDER_AND_DISPLAY[col][2]
            
            value = getattr(booking, attr_name)
            
            if value != None:
                value_str = attr_format.format(value)
            else:
                value_str = 'N/A'
            
            return value_str
        
        if role == QtCore.Qt.TextAlignmentRole:
            col = index.column()
            attr_format = self.COLUMN_ORDER_AND_DISPLAY[col][2]
            if attr_format != '{}':
                return QtCore.Qt.AlignVCenter + QtCore.Qt.AlignRight
            else:
                return QtCore.Qt.AlignVCenter + QtCore.Qt.AlignLeft
        
        if role == QtCore.Qt.UserRole:
            share, booking = self._get_booking(index)
            return share, booking
    
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
                    self.COLUMN_ORDER_AND_DISPLAY[_s][1]
                    )
                return header_str

class ShareTableModel(QtCore.QAbstractTableModel):
    
    COLUMN_ORDER_AND_DISPLAY = {
        0: ['name', 'Name', ' {} '],
        1: ['isin', 'ISIN', ' {} '],
        2: ['number_of_shares', '# Shares', ' {:d}'],
        3: ['acquisition_price', 'Acquisition price', ' {:.2f} €'],
        4: ['total_investment', 'Total investment', ' {:.2f} €'],
        5: ['profit_loss', 'Profit/loss', ' {:.2f} €'],
        6: ['yield_on_cost_12_months', 'YOC (12m)', ' {:.2f} %'],
        7: ['dividend_return_on_investment_12_months', 'ROI (12m)', ' {:.2f} %']
        }
    
    USED_COLUMNS = list(COLUMN_ORDER_AND_DISPLAY.keys())
    
    def __init__(self, dividend_portfolio):
        super(ShareTableModel, self).__init__()
        self.dividend_portfolio = dividend_portfolio
    
    def data(self, index, role):
        if role == QtCore.Qt.DisplayRole:
            
            share = self.dividend_portfolio.all_shares[index.row()]
            
            col = self.USED_COLUMNS[index.column()]
            
            attr_name = self.COLUMN_ORDER_AND_DISPLAY[col][0]
            attr_format = self.COLUMN_ORDER_AND_DISPLAY[col][2]
            
            value = getattr(share, attr_name)
            
            if value != None:
                value_str = attr_format.format(value)
            else:
                value_str = 'N/A'
            
            return value_str
        
        if role == QtCore.Qt.TextAlignmentRole:
            col = index.column()
            attr_format = self.COLUMN_ORDER_AND_DISPLAY[col][2]
            if attr_format != '{}':
                return QtCore.Qt.AlignVCenter + QtCore.Qt.AlignRight
            else:
                return QtCore.Qt.AlignVCenter + QtCore.Qt.AlignLeft
        
        if role == QtCore.Qt.UserRole:
            share = self.dividend_portfolio.all_shares[index.row()]
            return share
    
    def rowCount(self, index):
        return len(self.dividend_portfolio.all_shares)
    
    def columnCount(self, index):
        return len(self.USED_COLUMNS)
    
    def headerData(self, section, orientation, role):
        if role == QtCore.Qt.DisplayRole:
            if orientation == QtCore.Qt.Horizontal:
                _s = self.USED_COLUMNS[section]
                header_str = '  {}  '.format(
                    self.COLUMN_ORDER_AND_DISPLAY[_s][1]
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
        
    def setup_gui_new(self):
        self._setup_gui()
        self.setWindowTitle('New')
        
        for s in self.dividend_portfolio.all_shares:
            self.ui_dialog.combo_box_share.addItem(' {}'.format(s.name), s)
        
        for booking_type in ['Buy', 'Sell', 'Dividend']:
            self.ui_dialog.combo_box_type.addItem(booking_type)
        
        def fill_name_isin_info(i):
            s = self.ui_dialog.combo_box_share.itemData(i)
            self.ui_dialog.line_edit_name.setText(' {}'.format(s.name))
            self.ui_dialog.line_edit_isin.setText(' {}'.format(s.isin))
        
        self.ui_dialog.combo_box_share.currentIndexChanged.connect(
            fill_name_isin_info
            )
    
    def setup_gui_edit(self):
        self._setup_gui()
        self.setWindowTitle('Edit')
        
        self.ui_dialog.combo_box_share.addItem(' {}'.format(self.share.name))
        self.ui_dialog.line_edit_name.setText(self.share.name)
        self.ui_dialog.line_edit_isin.setText(self.share.isin)
        self.ui_dialog.combo_box_type.addItem(self.booking.type)
        self.ui_dialog.date_booking.setDate(self.booking.date)
        self.ui_dialog.number_of_shares.setValue(self.booking.number_of_shares)
        self.ui_dialog.amount_per_share.setValue(self.booking.amount_per_share)
        self.ui_dialog.total_amount.setValue(self.booking.amount)
        self.ui_dialog.fee.setValue(self.booking.fee)
        self.ui_dialog.tax.setValue(self.booking.tax)
    
    def accept(self):
        
        new_date = self.ui_dialog.date_booking.date().toPyDate()
        new_number_of_shares = self.ui_dialog.number_of_shares.value()
        new_amount_per_share = self.ui_dialog.amount_per_share.value()
        new_fee = self.ui_dialog.fee.value()
        new_tax = self.ui_dialog.tax.value()
        
        try:
            if self.is_new_booking:
                share = self.ui_dialog.combo_box_shareitemData(
                    self.ui_dialog.combo_box_share.currentIndex()
                    )
                booking_type = self.ui_dialog.combo_box_share.currentText()
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


def get_workarea_icon_and_widgets():
    icon = IconWorkarea().icon
    workarea = Workarea()
    slidemenu_widget = workarea.slidemenu
    mainbody_widget  = workarea.mainbody
    return workarea, icon, slidemenu_widget, mainbody_widget
