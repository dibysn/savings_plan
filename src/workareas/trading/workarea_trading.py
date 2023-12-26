# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtWidgets, QtGui

from src.workareas.trading.ui_mainbody_trading import Ui_Form as Ui_Form_Mainbody
from src.workareas.trading.ui_slidemenu_trading import Ui_Form as Ui_Form_Slidemenu
from src.workareas.trading.ui_dialog_trade import Ui_Dialog as Ui_Dialog_Trade
from src.workareas.trading.ui_dialog_portfolio import Ui_Dialog as Ui_Dialog_Portfolio
from src.workareas.trading.ui_dialog_table_settings import Ui_Dialog as Ui_Dialog_Table_Settings

from src.workareas.trading.model.tradingmodel import TradingPortfolio, Trade

class IconWorkarea:
    def __init__(self):
        self.icon = QtGui.QIcon()
        self.icon.addPixmap(
            QtGui.QPixmap(':/icons/icons/swap-horizontal.svg'),
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
        
        self.trading_portfolio = TradingPortfolio(10000.0, 0.02, 0.06)
        
        for _w in [
                self.ui_mainbody.frame_infos_portfolio,
                self.ui_mainbody.table_view_trading_active,
                self.ui_mainbody.frame_header_table_active,
                self.ui_mainbody.frame_header_table_simulation,
                self.ui_slidemenu.frame_header,
                self.ui_slidemenu.frame_header_2]:
            shadow = QtWidgets.QGraphicsDropShadowEffect()
            shadow.setBlurRadius(8)
            shadow.setXOffset(0)
            shadow.setYOffset(0)
            shadow.setColor(QtGui.QColor(0, 0, 0, 255))
            _w.setGraphicsEffect(shadow)
        
        self._update_text_all_portfolio_specific_values()
        
        self.table_model_trading_active = TradingTableModel(
            self.trading_portfolio, is_active_status = True
            )
        self.ui_mainbody.table_view_trading_active.setModel(
            self.table_model_trading_active
            )
        self.ui_mainbody.table_view_trading_active.setSelectionBehavior(
            QtWidgets.QTableView.SelectRows
            )
        self.ui_mainbody.table_view_trading_active.setSelectionMode(
            QtWidgets.QTableView.SingleSelection
            )
        self.ui_mainbody.table_view_trading_active.horizontalHeader().setStretchLastSection(True)
        
        self.table_model_trading_simulation = TradingTableModel(
            self.trading_portfolio, is_active_status = False
            )
        self.ui_mainbody.table_view_trading_simulation.setModel(
            self.table_model_trading_simulation
            )
        self.ui_mainbody.table_view_trading_simulation.setSelectionBehavior(
            QtWidgets.QTableView.SelectRows
            )
        self.ui_mainbody.table_view_trading_simulation.setSelectionMode(
            QtWidgets.QTableView.SingleSelection
            )
        self.ui_mainbody.table_view_trading_simulation.horizontalHeader().setStretchLastSection(True)
        
        self._update_tables()
        
        self.ui_slidemenu.button_new_portfolio.clicked.connect(
            self.open_dialog_new_portfolio
            )
        self.ui_slidemenu.button_edit_portfolio.clicked.connect(
            self.open_dialog_edit_portfolio
            )
        self.ui_slidemenu.button_new_trade.clicked.connect(
            self.open_dialog_new_trade
            )
        self.ui_slidemenu.button_table_settings.clicked.connect(
            self.open_dialog_table_settings
            )
        self.ui_mainbody.button_edit_trade_active.clicked.connect(
            self.open_dialog_edit_trade
            )
        self.ui_mainbody.button_edit_trade_simulation.clicked.connect(
            self.open_dialog_edit_trade
            )
        self.ui_mainbody.table_view_trading_active.doubleClicked.connect(
            self.open_dialog_edit_trade
            )
        self.ui_mainbody.table_view_trading_simulation.doubleClicked.connect(
            self.open_dialog_edit_trade
            )
        self.ui_mainbody.button_delete_trade_active.clicked.connect(
            self.delete_trade
            )
        self.ui_mainbody.button_delete_trade_simulation.clicked.connect(
            self.delete_trade
            )
        self.ui_mainbody.button_get_latest_price_active.clicked.connect(
            self.get_latest_price
            )
        self.ui_mainbody.button_get_latest_price_simulation.clicked.connect(
            self.get_latest_price
            )
    
    def register_change_observer(self, change_observer_callback):
        self._change_observer_callbacks.append(change_observer_callback)
    
    def _notify_change_observer(self):
        for callback in self._change_observer_callbacks:
            callback()
    
    def get_name_of_workarea(self):
        return 'Trading'
    
    def get_json_data_for_saving(self):
        return {
            'Columns': TradingTableModel.USED_COLUMNS,
            'Portfolio': self.trading_portfolio.get_json_data_for_saving()
            }
    
    def load_from_json_data(self, data):
        TradingTableModel.USED_COLUMNS = data['Columns']
        _trading_portfolio = TradingPortfolio.load_from_json_data(data['Portfolio'])
        
        self.trading_portfolio = _trading_portfolio
        self.table_model_trading_active.trading_portfolio = self.trading_portfolio
        self.table_model_trading_simulation.trading_portfolio = self.trading_portfolio
        
        self._update_text_all_portfolio_specific_values()
        self._update_tables()
    
    def set_default_values(self):
        self.trading_portfolio = TradingPortfolio(10000.0, 0.02, 0.06)
        self.table_model_trading_active.trading_portfolio = self.trading_portfolio
        self.table_model_trading_simulation.trading_portfolio = self.trading_portfolio
        TradingTableModel.USED_COLUMNS = list(
            TradingTableModel.COLUMN_ORDER_AND_DISPLAY.keys()
            )
        
        self._update_text_all_portfolio_specific_values()
        self._update_tables()
        self._notify_change_observer()
    
    def open_dialog_new_portfolio(self):
        dialog_portfolio = DialogPortfolio(
            self.trading_portfolio, is_new_portfolio = True
            )
        dialog_portfolio.exec()
        if dialog_portfolio.accepted:
            self.trading_portfolio = dialog_portfolio.trading_portfolio
            self.table_model_trading_active.trading_portfolio = self.trading_portfolio
            self.table_model_trading_simulation.trading_portfolio = self.trading_portfolio
            self._update_tables()
            self._update_text_all_portfolio_specific_values()
            self._notify_change_observer()
    
    def open_dialog_edit_portfolio(self):
        dialog_portfolio = DialogPortfolio(
            self.trading_portfolio, is_new_portfolio = False
            )
        dialog_portfolio.exec()
        if dialog_portfolio.accepted:
            self._update_tables()
            self._update_text_all_portfolio_specific_values()
            self._notify_change_observer()
    
    def open_dialog_new_trade(self):
        dialog_trade = DialogTrade(
            self.trading_portfolio, is_new_trade = True, trade = None
            )
        dialog_trade.exec()
        if dialog_trade.accepted:
            self._update_tables()
            self._update_text_all_portfolio_specific_values()
            self._notify_change_observer()
    
    def open_dialog_edit_trade(self):
        trade = None
        _name = self.mainbody.sender().objectName()
        if _name in ['button_edit_trade_active', 'table_view_trading_active']:
            trade = self._get_selected_trade(active_trade = True)
        elif _name in ['button_edit_trade_simulation', 'table_view_trading_simulation']:
            trade = self._get_selected_trade(active_trade = False)
        
        if trade:
            dialog_trade = DialogTrade(
                self.trading_portfolio, is_new_trade = False, trade = trade
                )
            dialog_trade.exec()
            if dialog_trade.accepted:
                self._update_tables()
                self._update_text_all_portfolio_specific_values()
                self._notify_change_observer()
    
    def open_dialog_table_settings(self):
        dialog_table_settings = DialogTableSettings(
            TradingTableModel.COLUMN_ORDER_AND_DISPLAY,
            TradingTableModel.USED_COLUMNS
            )
        dialog_table_settings.exec()
        if dialog_table_settings.accepted:
            TradingTableModel.USED_COLUMNS = dialog_table_settings.used_columns
            self._update_tables()
            self._notify_change_observer()
    
    def delete_trade(self):
        trade = None
        _name = self.mainbody.sender().objectName()
        if _name == 'button_delete_trade_active':
            trade = self._get_selected_trade(active_trade = True)
        elif _name == 'button_delete_trade_simulation':
            trade = self._get_selected_trade(active_trade = False)
        
        if trade:
            message = ('Do you really want to delete trade\n'
                       '"{} ({})"?\n\n').format(
                           trade.name, trade.isin
                           )
            button = QtWidgets.QMessageBox.question(
                self.slidemenu, 'Delete trade', message,
                QtWidgets.QMessageBox.Cancel | QtWidgets.QMessageBox.Yes
                )
            if button == QtWidgets.QMessageBox.Cancel:
                return
            
            self.trading_portfolio.delete_trade(trade)
            self._update_tables()
            
            self._update_text_all_portfolio_specific_values()
            self._notify_change_observer()
    
    def _get_selected_trade(self, active_trade = True):
        trade = None
        if active_trade:
            r = self.ui_mainbody.table_view_trading_active.selectionModel().selectedRows()
            if r:
                row = r[0].row()
                index = self.table_model_trading_active.createIndex(row, 0)
                trade = self.table_model_trading_active.data(index, QtCore.Qt.UserRole)
        else:
            r = self.ui_mainbody.table_view_trading_simulation.selectionModel().selectedRows()
            if r:
                row = r[0].row()
                index = self.table_model_trading_simulation.createIndex(row, 0)
                trade = self.table_model_trading_simulation.data(index, QtCore.Qt.UserRole)
        return trade
    
    def get_latest_price(self):
        trade = None
        _name = self.mainbody.sender().objectName()
        if _name == 'button_get_latest_price_active':
            trade = self._get_selected_trade(active_trade = True)
        elif _name == 'button_get_latest_price_simulation':
            trade = self._get_selected_trade(active_trade = False)
        
        if trade:
            trade.get_latest_price()
            self._update_tables()
            self._notify_change_observer()
    
    def _update_tables(self):
        self.table_model_trading_active.layoutChanged.emit()
        for i in range(self.table_model_trading_active.columnCount(None)):
            self.ui_mainbody.table_view_trading_active.resizeColumnToContents(i)
        self.table_model_trading_simulation.layoutChanged.emit()
        for i in range(self.table_model_trading_simulation.columnCount(None)):
            self.ui_mainbody.table_view_trading_simulation.resizeColumnToContents(i)
    
    def _update_text_all_portfolio_specific_values(self):
        self.ui_mainbody.label_portfolio_value.setText(
            '{:,.2f} €'.format(self.trading_portfolio.portfolio_amount)
            )
        self.ui_mainbody.label_allowed_risk_trade.setText(
            '{:,.2f} € ({:,.2f} %)'.format(
                self.trading_portfolio.portfolio_amount * \
                    self.trading_portfolio.allowed_risk_trade,
                self.trading_portfolio.allowed_risk_trade*100)
            )
        self.ui_mainbody.label_available_risk_portfolio.setText(
            '{:,.2f} € ({:,.2f} %)'.format(
                self.trading_portfolio.portfolio_amount * \
                    self.trading_portfolio.left_risk_portfolio,
                self.trading_portfolio.left_risk_portfolio*100
                )
            )

class TradingTableModel(QtCore.QAbstractTableModel):
    
    COLUMN_ORDER_AND_DISPLAY = {
             0: ['name', 'Name', '{}'],
             1: ['isin', 'ISIN', '{}'],
             2: ['latest_price', 'Latest price', '{:.2f} €'],
             3: ['entry_price', 'Entry price', '{:.2f} €'],
             4: ['profit_loss', 'Profit/loss', '{:.2f} €'],
             5: ['protective_stop', 'Protective stop', '{:.2f} €'],
             6: ['target_price', 'Target price', '{:.2f} €'],
             7: ['number_of_shares', '# Shares', '{:d}'],
             8: ['trade_reward', 'Reward', '{:.2f} €'],
             9: ['trade_risk', 'Risk', '{:.2f} €'],
            10: ['reward_risk_ratio', 'Reward risk ratio', '{:,.2f}'],
            11: ['days_left_earnings', 'Days until earnings', '{:d}'],
            12: ['days_left_dividend', 'Days until dividend', '{:d}']
            }
    
    USED_COLUMNS = list(COLUMN_ORDER_AND_DISPLAY.keys())
    
    def __init__(self, trading_portfolio, is_active_status = True):
        super(TradingTableModel, self).__init__()
        self.trading_portfolio = trading_portfolio
        self.is_active_status = is_active_status
    
    def data(self, index, role):
        if role == QtCore.Qt.DisplayRole:
            trade = [
                t for t in self.trading_portfolio.trades
                if t.is_active == self.is_active_status
                ][index.row()]
            
            col = self.USED_COLUMNS[index.column()]
            
            attr_name = self.COLUMN_ORDER_AND_DISPLAY[col][0]
            attr_format = self.COLUMN_ORDER_AND_DISPLAY[col][2]
            
            value = getattr(trade, attr_name)
            
            if value:
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
            trade = [
                t for t in self.trading_portfolio.trades
                if t.is_active == self.is_active_status
                ][index.row()]
            return trade
    
    def rowCount(self, index):
        return sum(1 for t in self.trading_portfolio.trades
                   if t.is_active == self.is_active_status)
    
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

class DialogPortfolio(QtWidgets.QDialog):
    def __init__(self, trading_portfolio, is_new_portfolio = False):
        super(DialogPortfolio, self).__init__()
        
        self.trading_portfolio = trading_portfolio
        self.is_new_portfolio = is_new_portfolio
        self.accepted = False
        
        if self.is_new_portfolio:
            self.setup_gui_new()
        else:
            self.setup_gui_edit()
    
    def _setup_gui(self):
        self.ui_dialog = Ui_Dialog_Portfolio()
        self.ui_dialog.setupUi(self)
        
        def update_labels_total_risk():
            if self.is_new_portfolio:
                deposit = self.ui_dialog.initial_deposit.value()
            else:
                deposit = self.trading_portfolio.portfolio_amount - \
                    self.trading_portfolio.initial_deposit + \
                    self.ui_dialog.initial_deposit.value()
                _min_deposit = \
                    max(0, self.trading_portfolio.initial_deposit - \
                            self.trading_portfolio.portfolio_amount)
                self.ui_dialog.initial_deposit.setMinimum(_min_deposit)
            
            risk_trade = self.ui_dialog.allowed_risk_trade.value()
            risk_portfolio = self.ui_dialog.allowed_risk_portfolio.value()
            
            self.ui_dialog.label_total_amount_portfolio.setText(
                '(total {:,.2f} €)'.format(deposit)
                )
            self.ui_dialog.label_total_allowed_risk_trade.setText(
                '(max {:,.2f} €)'.format(deposit * risk_trade / 100.0)
                )
            self.ui_dialog.label_total_allowed_risk_portfolio.setText(
                '(max {:,.2f} €)'.format(deposit * risk_portfolio / 100.0)
                )
            
        self.ui_dialog.initial_deposit.valueChanged['double'].connect(
            update_labels_total_risk
            )
        self.ui_dialog.allowed_risk_trade.valueChanged['double'].connect(
            update_labels_total_risk
            )
        self.ui_dialog.allowed_risk_portfolio.valueChanged['double'].connect(
            update_labels_total_risk
            )
    
    def setup_gui_new(self):
        self._setup_gui()
        self.setWindowTitle('New')
        
        self.ui_dialog.initial_deposit.setValue(10000.0)
        self.ui_dialog.allowed_risk_trade.setValue(2.0)
        self.ui_dialog.label_total_allowed_risk_portfolio.setText(
            '(max {:,.2f} €)'.format(200.0)
            )
        self.ui_dialog.allowed_risk_portfolio.setValue(6.0)
        self.ui_dialog.label_total_allowed_risk_portfolio.setText(
            '(max {:,.2f} €)'.format(600.0)
            )
    
    def setup_gui_edit(self):
        self._setup_gui()
        self.setWindowTitle('Edit')
        
        self.ui_dialog.initial_deposit.setValue(
            self.trading_portfolio.initial_deposit
            )
        self.ui_dialog.allowed_risk_trade.setValue(
            self.trading_portfolio.allowed_risk_trade * 100.0
            )
        self.ui_dialog.label_total_allowed_risk_trade.setText(
            '(max {:,.2f} €)'.format(
                self.trading_portfolio.initial_deposit * \
                    self.trading_portfolio.allowed_risk_trade
                )
            )
        self.ui_dialog.allowed_risk_portfolio.setValue(
            self.trading_portfolio.allowed_risk_portfolio * 100.0
            )
        self.ui_dialog.label_total_allowed_risk_portfolio.setText(
            '(max {:,.2f} €)'.format(
                self.trading_portfolio.initial_deposit * \
                    self.trading_portfolio.allowed_risk_portfolio
                )
            )
    
    def accept(self):
        initial_deposit = self.ui_dialog.initial_deposit.value()
        allowed_risk_trade = self.ui_dialog.allowed_risk_trade.value() / 100.0
        allowed_risk_portfolio = self.ui_dialog.allowed_risk_portfolio.value() / 100.0
        
        if self.is_new_portfolio:
            message = ('If you creeate a new trading portfolio, '
                       'all data of the current trading portfolio '
                       'will be lost.\n\n'
                       'Do you want to continue?')
            
            button = QtWidgets.QMessageBox.question(
                self, 'Trading Portfolio - New', message,
                QtWidgets.QMessageBox.Cancel | QtWidgets.QMessageBox.Yes
                )
            if button == QtWidgets.QMessageBox.Cancel:
                self.close()
            
            self.trading_portfolio = TradingPortfolio(
                initial_deposit, allowed_risk_trade, allowed_risk_portfolio, []
                )
        else:
            self.trading_portfolio.initial_deposit = initial_deposit
            self.trading_portfolio.allowed_risk_trade = allowed_risk_trade
            self.trading_portfolio.allowed_risk_portfolio = allowed_risk_portfolio
        
        self.accepted = True
        self.close()

class DialogTrade(QtWidgets.QDialog):
    def __init__(self, trading_portfolio, is_new_trade = False, trade = None):
        super(DialogTrade, self).__init__()
        
        self.trading_portfolio = trading_portfolio
        self.is_new_trade = is_new_trade
        self.trade = trade
        self.accepted = False
        
        if self.is_new_trade:
            self.setup_gui_new()
        else:
            self.setup_gui_edit()
    
    def _setup_gui(self):
        self.ui_dialog = Ui_Dialog_Trade()
        self.ui_dialog.setupUi(self)
        
        shadow = QtWidgets.QGraphicsDropShadowEffect()
        shadow.setBlurRadius(8)
        shadow.setXOffset(0)
        shadow.setYOffset(0)
        shadow.setColor(QtGui.QColor(0, 0, 0, 255))
        self.ui_dialog.frame_header.setGraphicsEffect(shadow)
        
        def trade_status_changed(s):
            self.ui_dialog.check_box_trade_close.setEnabled(s == 'Active')
            if s == 'Simulation':
                self.ui_dialog.check_box_trade_close.setChecked(False)
                self.ui_dialog.date_trade_closed.setEnabled(False)
                self.ui_dialog.sell_price.setEnabled(False)
        self.ui_dialog.combo_box_active.currentTextChanged.connect(
            trade_status_changed
            )
        
        self.ui_dialog.check_box_trade_close.clicked['bool'].connect(
            self.ui_dialog.date_trade_closed.setEnabled
            )
        self.ui_dialog.check_box_trade_close.clicked['bool'].connect(
            self.ui_dialog.sell_price.setEnabled
            )
        
        self.ui_dialog.check_box_latest_price.clicked['bool'].connect(
            self.ui_dialog.date_latest_price.setEnabled
            )
        self.ui_dialog.check_box_latest_price.clicked['bool'].connect(
            self.ui_dialog.latest_price.setEnabled
            )
        
        self.ui_dialog.check_box_date_next_earnings.clicked['bool'].connect(
            self.ui_dialog.date_next_earnings.setEnabled
            )
        self.ui_dialog.check_box_date_next_dividend.clicked['bool'].connect(
            self.ui_dialog.date_next_dividend.setEnabled
            )
        
        self.ui_dialog.entry_price.valueChanged.connect(
            lambda v: self.ui_dialog.protective_stop.setMaximum(v - 0.01)
            )
        self.ui_dialog.entry_price.valueChanged.connect(
            lambda v: self.ui_dialog.target_price.setMinimum(v + 0.01)
            )
        self.ui_dialog.protective_stop.valueChanged.connect(
            lambda v: self.ui_dialog.entry_price.setMinimum(v + 0.01)
            )
        self.ui_dialog.target_price.valueChanged.connect(
            lambda v: self.ui_dialog.entry_price.setMaximum(v - 0.01)
            )
    
    def setup_gui_new(self):
        self._setup_gui()
        self.setWindowTitle('New')
        
        self.ui_dialog.line_edit_name.setText('')
        self.ui_dialog.line_edit_isin.setText('')
        self.ui_dialog.entry_price.setValue(20.0)
        self.ui_dialog.target_price.setValue(30.0)
        self.ui_dialog.protective_stop.setValue(10.0)
        self.ui_dialog.number_of_shares.setValue(1)
        self.ui_dialog.label_max_allowed_no_of_shares.setText('')
        self.ui_dialog.date_next_earnings.setEnabled(True)
        self.ui_dialog.check_box_date_next_earnings.setChecked(True)
        self.ui_dialog.date_next_earnings.setDate(QtCore.QDate(2024, 1, 1))
        self.ui_dialog.date_next_dividend.setEnabled(True)
        self.ui_dialog.check_box_date_next_dividend.setChecked(True)
        self.ui_dialog.date_next_dividend.setDate(QtCore.QDate(2024, 1, 1))
        self.ui_dialog.combo_box_active.setCurrentText('Simulation')
        
        self.ui_dialog.check_box_latest_price.setChecked(False)
        self.ui_dialog.date_latest_price.setEnabled(False)
        self.ui_dialog.latest_price.setEnabled(False)
        
        self.ui_dialog.check_box_trade_close.setChecked(False)
        self.ui_dialog.check_box_trade_close.setEnabled(False)
        self.ui_dialog.date_trade_closed.setEnabled(False)
        self.ui_dialog.sell_price.setEnabled(False)
    
    def setup_gui_edit(self):
        self._setup_gui()
        self.setWindowTitle('Edit')
        
        self.ui_dialog.line_edit_name.setText(self.trade.name)
        self.ui_dialog.line_edit_isin.setText(self.trade.isin)
        self.ui_dialog.entry_price.setValue(self.trade.entry_price)
        self.ui_dialog.target_price.setValue(self.trade.target_price)
        self.ui_dialog.protective_stop.setValue(self.trade.protective_stop)
        self.ui_dialog.number_of_shares.setValue(self.trade.number_of_shares)
        
        if self.trade.trade_closed:
            self.ui_dialog.label_max_allowed_no_of_shares.setText('')
        else:
            self.ui_dialog.label_max_allowed_no_of_shares.setText(
                '(max {})'.format(
                    self.trading_portfolio.compute_max_allowed_number_of_shares(
                        self.trade
                        )
                    )
                )
        
        self.ui_dialog.check_box_trade_close.setEnabled(self.trade.is_active)
        if self.trade.is_active:
            self.ui_dialog.combo_box_active.setCurrentText('Active')
        else:
            self.ui_dialog.combo_box_active.setCurrentText('Simulation')
        
        _lp = (self.trade.latest_price != None)
        self.ui_dialog.check_box_latest_price.setChecked(_lp)
        self.ui_dialog.date_latest_price.setEnabled(_lp)
        self.ui_dialog.latest_price.setEnabled(_lp)
        if _lp:
            self.ui_dialog.latest_price.setValue(self.trade.latest_price)
            self.ui_dialog.date_latest_price.setDate(self.trade.date_latest_price)
        else:
            self.ui_dialog.latest_price.setValue(0.0)
            self.ui_dialog.date_latest_price.setDate(QtCore.QDate(2024, 1, 1))
        
        self.ui_dialog.date_trade_closed.setEnabled(self.trade.trade_closed)
        self.ui_dialog.sell_price.setEnabled(self.trade.trade_closed)
        self.ui_dialog.check_box_trade_close.setChecked(self.trade.trade_closed)
        if self.trade.trade_closed:
            self.ui_dialog.sell_price.setValue(self.trade.sell_price)
            self.ui_dialog.date_trade_closed.setDate(self.trade.date_trade_closed)
        else:
            self.ui_dialog.sell_price.setValue(0.0)
            self.ui_dialog.date_trade_closed.setDate(QtCore.QDate(2024, 1, 1))
        
        _dne = (self.trade.date_next_earnings != None)
        self.ui_dialog.check_box_date_next_earnings.setChecked(_dne)
        self.ui_dialog.date_next_earnings.setEnabled(_dne)
        if _dne:
            self.ui_dialog.date_next_earnings.setDate(self.trade.date_next_earnings)
        else:
            self.ui_dialog.date_next_earnings.setDate(QtCore.QDate(2024, 1, 1))
        
        _dnd = (self.trade.date_next_dividend != None)
        self.ui_dialog.check_box_date_next_dividend.setChecked(_dnd)
        self.ui_dialog.date_next_dividend.setEnabled(_dnd)
        if _dnd:
            self.ui_dialog.date_next_dividend.setDate(self.trade.date_next_dividend)
        else:
            self.ui_dialog.date_next_dividend.setDate(QtCore.QDate(2024, 1, 1))
    
    def accept(self):
        name = self.ui_dialog.line_edit_name.text()
        isin = self.ui_dialog.line_edit_isin.text()
        entry_price = self.ui_dialog.entry_price.value()
        protective_stop = self.ui_dialog.protective_stop.value()
        target_price = self.ui_dialog.target_price.value()
        
        date_next_earnings = None
        date_next_dividend = None
        if self.ui_dialog.check_box_date_next_earnings.isChecked():
            date_next_earnings = self.ui_dialog.date_next_earnings.date().toPyDate()
        if self.ui_dialog.check_box_date_next_dividend.isChecked():
            date_next_dividend = self.ui_dialog.date_next_dividend.date().toPyDate()
        
        number_of_shares = self.ui_dialog.number_of_shares.value()
        
        is_active = False
        is_active = (self.ui_dialog.combo_box_active.currentText() == 'Active')
        
        if self.ui_dialog.check_box_trade_close.isChecked():
            sell_price = self.ui_dialog.sell_price.value()
            date_trade_closed = self.ui_dialog.date_trade_closed.date().toPyDate()
        else:
            sell_price = None
            date_trade_closed = None
        
        if self.is_new_trade:
            new_trade = Trade(
                name, isin,
                entry_price, protective_stop, target_price,
                date_next_earnings, date_next_dividend,
                number_of_shares, is_active)
            self.trading_portfolio.close_trade(
                new_trade, sell_price, date_trade_closed
                )
            self.trading_portfolio.add_trade(new_trade)
            if self.ui_dialog.check_box_latest_price.isChecked():
                new_trade.latest_price = self.ui_dialog.latest_price.value()
                new_trade.date_latest_price = self.ui_dialog.date_latest_price.date().toPyDate()
            else:
                new_trade.latest_price = None
                new_trade.date_latest_price = None
        else:
            self.trading_portfolio.update_trade(
                self.trade, name, isin,
                entry_price, protective_stop, target_price,
                date_next_earnings, date_next_dividend,
                number_of_shares, is_active)
            self.trading_portfolio.close_trade(
                self.trade, sell_price, date_trade_closed
                )
        
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
        
        self.ui_dialog.button_reset_to_default.clicked.connect(
            self.reset_used_columns_to_default
            )
        
        all_header_displayed = []
        all_header_not_displayed = []
        for i, v in self.id_to_name.items():
            if i in self.used_columns:
                all_header_displayed.append(v)
            else:
                all_header_not_displayed.append(v)
            
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
