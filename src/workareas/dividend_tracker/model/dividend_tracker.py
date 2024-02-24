# -*- coding: utf-8 -*-

import functools
from datetime import date as dt
import math

class Portfolio:
    
    def __init__(self, all_shares = None):
        self.all_shares = all_shares if all_shares != None else []
        
    
    def get_json_data_for_saving(self):
        _d = {
            'shares': [s.get_json_data_for_saving() for s in self.all_shares]
            }
        return _d
    
    @classmethod
    def load_from_json_data(cls, data):
        all_shares = [Share.load_from_json_data(s) for s in data['shares']]
        p = cls(all_shares = all_shares)
        return p
    
    def add_share(self, share):
        if share.isin in [s.isin for s in self.all_shares]:
            raise Exception(
                'Share with ISIN "{}" already in portfolio'.format(share.isin)
                )
        self.all_shares.append(share)
    
    def update_share(self, share, new_name, new_isin):
        
        _new_name = new_name.strip()
        _new_isin = new_isin.strip()
        
        if _new_isin != share.isin and _new_isin in [s.isin for s in self.all_shares]:
            raise Exception(
                'Share with ISIN "{}" already in portfolio'.format(share.isin)
                )
        if _new_name == '':
            raise Exception('Share name cannot be empty')
        
        if _new_isin == '':
            raise Exception('Share ISIN cannot be empty')
        share.name = _new_name
        share.isin = _new_isin
        
        for b in share.buy_orders:
            b.name = _new_name
            b.isin = _new_isin
        for s in share.sell_orders:
            s.name = _new_name
            s.isin = _new_isin
        for d in share.dividend_payments:
            d.name = _new_name
            d.isin = _new_isin
    
    def remove_share(self, share):
        try:
            self.all_shares.remove(share)
        except:
            raise Exception('Share does not exist')
    
    @property
    def tied_capital(self):
        return sum(s.tied_capital for s in self.all_shares)
    
    @property
    def realized_profit_loss(self):
        return sum(s.realized_profit_loss for s in self.all_shares)
    
    @property
    def yield_on_cost_12_months(self):
        ret = sum(
            s.dividends_last_12_months * s.number_of_shares \
            for s in self.all_shares
            )
        acquisition_cost = sum(
            s.acquisition_price * s.number_of_shares \
            for s in self.all_shares
            )
        
        if ret == 0.0:
            yoc = 0.0
        else:
            yoc = ret / acquisition_cost
        return yoc * 100.0
    
    @property
    def dividend_return_on_tied_capital_12_months(self):
        ret = sum(
            s.dividends_last_12_months * s.number_of_shares \
            for s in self.all_shares
            )
        if ret == 0.0:
            return 0.0
        
        try:
            d_rotc = ret / max(self.tied_capital, 0.0)
        except ZeroDivisionError:
            d_rotc = math.inf
            
        return d_rotc * 100.0
    
    def get_total_share_fee(self, start_date, end_date):
        return sum(
            s.get_total_share_fee(start_date, end_date) for s in self.all_shares
            )
    
    def get_total_share_tax(self, start_date, end_date):
        return sum(
            s.get_total_share_tax(start_date, end_date) for s in self.all_shares
            )
    
    def get_total_dividend_amount(self, start_date, end_date):
        return sum(
            s.get_total_dividend_amount(start_date, end_date) for s in self.all_shares
            )
    
    def get_total_dividend_fee(self, start_date, end_date):
        return sum(
            s.get_total_dividend_fee(start_date, end_date) for s in self.all_shares
            )
    
    def get_total_dividend_tax(self, start_date, end_date):
        return sum(
            s.get_total_dividend_tax(start_date, end_date) for s in self.all_shares
            )

class Share:
    
    def __init__(self, name, isin):
        self.isin = isin.strip()
        self.name = name.strip()
        
        if self.name == '':
            raise Exception('Share name cannot be empty')
        
        if self.isin == '':
            raise Exception('Share ISIN cannot be empty')
        
        self.buy_orders = []
        self.sell_orders = []
        self.dividend_payments = []
        
        self._number_of_shares = None
        self._acquisition_price = None
        self._tied_capital = None
        self._total_net_dividend_payments = None
        self._dividends_last_12_months = None
        
        self._compute_values()
    
    def update_computation(func):
        @functools.wraps(func)
        def wrapper_update_computation(*args, **kwargs):
            value = func(*args, **kwargs)
            args[0]._compute_values()
            return value
        return wrapper_update_computation
    
    def _compute_values(self):
        # Number of shares
        buy = self.buy_orders
        sell = self.sell_orders
        self._number_of_shares = \
            sum(b.number_of_shares for b in buy) - \
            sum(s.number_of_shares for s in sell)
        
        # Acquisition price
        if self.number_of_shares == 0:
            self._acquisition_price = 0.0
        else:
            # Check how many shares have been sold
            n_sell = sum(s.number_of_shares for s in self.sell_orders)
            
            # Get the index of the buy order which shares have not been fully sold
            n_buy = 0
            for n, b in enumerate(self.buy_orders):
                n_buy += b.number_of_shares
                if n_sell <= n_buy:
                    break
            
            # Build list of all current shares in the portfolio
            buy = [
                Order(None, None, None, 0,
                      n_buy - n_sell, self.buy_orders[n].amount_per_share,
                      0, 0)
                ]
            buy = buy + self.buy_orders[n+1:]
            
            # Compute and print acquisition price
            self._acquisition_price = \
                sum(b.number_of_shares * b.amount_per_share for b in buy) / \
                sum(b.number_of_shares for b in buy)
        
        # Ties capital
        vb = sum(b.number_of_shares * b.amount_per_share for b in self.buy_orders)
        vs = sum(s.number_of_shares * s.amount_per_share for s in self.sell_orders)
        self._tied_capital = vb - vs
        
        # Total net dividend payments
        if self.dividend_payments == []:
            self._total_net_dividend_payments = 0.0
        else:
            start_date = min(d.date for d in self.dividend_payments)
            end_date = max(d.date for d in self.dividend_payments)
            total_dividends = self.get_total_dividend_amount(start_date, end_date)
            total_tax = self.get_total_dividend_tax(start_date, end_date)
            total_fee = self.get_total_dividend_fee(start_date, end_date)
            self._total_net_dividend_payments = total_dividends - total_fee - total_tax
        
        # Dividends last 12 months
        self._dividends_last_12_months = sum(
            d.amount_per_share for d in self.dividend_payments
            if (dt.today() - d.date).days < 365
            )
    
    def get_json_data_for_saving(self):
        _buy = [
            {
                'order_type': 'Buy',
                'name': b.name,
                'isin': b.isin,
                'date': b.date.isoformat(),
                'number_of_shares': b.number_of_shares,
                'amount_per_share': b.amount_per_share,
                'fee': b.fee,
                'tax': b.tax
             }
            for b in self.buy_orders
            ]
        _sell = [
            {
                'order_type': 'Sell',
                'name': b.name,
                'isin': b.isin,
                'date': b.date.isoformat(),
                'number_of_shares': b.number_of_shares,
                'amount_per_share': b.amount_per_share,
                'fee': b.fee,
                'tax': b.tax
             }
            for b in self.sell_orders
            ]
        _dividend = [
            {
                'order_type': 'Dividend',
                'name': b.name,
                'isin': b.isin,
                'date': b.date.isoformat(),
                'number_of_shares': b.number_of_shares,
                'amount_per_share': b.amount_per_share,
                'fee': b.fee,
                'tax': b.tax
             }
            for b in self.dividend_payments
            ]
        
        _d = {
            'name': self.name,
            'isin': self.isin,
            'orders': _buy + _sell + _dividend
            }
        return _d
    
    @classmethod
    def load_from_json_data(cls, data):
        
        s = cls(data['name'], data['isin'])
        
        for _o in data['orders']:
            s.create_booking(
                _o['order_type'], dt.fromisoformat(_o['date']),
                _o['number_of_shares'], _o['amount_per_share'],
                _o['fee'], _o['tax']
                )
        return s
    
    def _create_buy_order(self, date, number_of_shares,
                         amount_per_share, fee, tax):
        o = Order(
            'Buy', self.name, self.isin, date, number_of_shares,
            amount_per_share, fee, tax
            )
        self.buy_orders.append(o)
    
    def _update_buy_order(self, order, new_date, new_number_of_shares,
                         new_amount_per_share, new_fee, new_tax):
        if self.number_of_shares < order.number_of_shares - new_number_of_shares:
            raise Exception('Not enough shares available')
        order.date = new_date
        order.number_of_shares = new_number_of_shares
        order.amount_per_share = new_amount_per_share
        order.amount = new_amount_per_share * new_number_of_shares
        order.fee = new_fee
        order.tax = new_tax
        order.total_cost = new_amount_per_share * new_number_of_shares + new_fee + new_tax
    
    def _delete_buy_order(self, order):
        if self.number_of_shares < order.number_of_shares:
            raise Exception('Not enough shares available')
        try:
            self.buy_orders.remove(order)
        except:
            raise Exception('Order does not exist')
    
    def _create_sell_order(self, date, number_of_shares,
                          amount_per_share, fee, tax):
        if self.number_of_shares < number_of_shares:
            raise Exception('Not enough shares available')
        o = Order(
            'Sell', self.name, self.isin, date, number_of_shares,
            amount_per_share, fee, tax
            )
        self.sell_orders.append(o)
    
    def _update_sell_order(self, order, new_date, new_number_of_shares,
                         new_amount_per_share, new_fee, new_tax):
        if self.number_of_shares < new_number_of_shares - order.number_of_shares:
            raise Exception('Not enough shares available')
        order.date = new_date
        order.number_of_shares = new_number_of_shares
        order.amount_per_share = new_amount_per_share
        order.amount = new_amount_per_share * new_number_of_shares
        order.fee = new_fee
        order.tax = new_tax
        order.total_cost = new_amount_per_share * new_number_of_shares + new_fee + new_tax
        
    def _delete_sell_order(self, order):
        try:
            self.sell_orders.remove(order)
        except:
            raise Exception('Order does not exist')
    
    def _create_dividend(self, date, number_of_shares,
                         amount_per_share, fee, tax):
        
        d = Dividend(
            self.name, self.isin, date, number_of_shares,
            amount_per_share, fee, tax
            )
        self.dividend_payments.append(d)
    
    def _update_dividend(self, order, new_date, new_number_of_shares,
                         new_amount_per_share, new_fee, new_tax):
        order.date = new_date
        order.number_of_shares = new_number_of_shares
        order.amount_per_share = new_amount_per_share
        order.amount = new_amount_per_share * new_number_of_shares
        order.fee = new_fee
        order.tax = new_tax
        order.total_cost = new_amount_per_share * new_number_of_shares + new_fee + new_tax
    
    def _delete_dividend(self, dividend):
        try:
            self.dividend_payments.remove(dividend)
        except:
            raise Exception('Dividend does not exist')
    
    @update_computation
    def create_booking(self, booking_type, date, number_of_shares,
                         amount_per_share, fee, tax):
        if booking_type == 'Buy':
            self._create_buy_order(
                date, number_of_shares, amount_per_share, fee, tax
                )
        elif booking_type == 'Sell':
            self._create_sell_order(
                date, number_of_shares, amount_per_share, fee, tax
                )
        elif booking_type == 'Dividend':
            self._create_dividend(
                date, number_of_shares, amount_per_share, fee, tax
                )
        else:
            raise Exception('Booking type does not exist')
    
    @update_computation
    def update_booking(self, booking, new_date, new_number_of_shares,
                         new_amount_per_share, new_fee, new_tax):
        if booking.type == 'Buy':
            self._update_buy_order(
                booking, new_date, new_number_of_shares,
                new_amount_per_share, new_fee, new_tax
                )
        elif booking.type == 'Sell':
            self._update_sell_order(
                booking, new_date, new_number_of_shares,
                new_amount_per_share, new_fee, new_tax
                )
        elif booking.type == 'Dividend':
            self._update_dividend(
                booking, new_date, new_number_of_shares,
                new_amount_per_share, new_fee, new_tax
                )
        else:
            raise Exception('Booking type does not exist')
    
    @update_computation
    def delete_booking(self, booking):
        if booking.type == 'Buy':
            self._delete_buy_order(booking)
        elif booking.type == 'Sell':
            self._delete_sell_order(booking)
        elif booking.type == 'Dividend':
            self._delete_dividend(booking)
        else:
            raise Exception('Booking type does not exist')
    
    @property
    def number_of_shares(self):
        return self._number_of_shares
    
    @property
    def acquisition_price(self):
        return self._acquisition_price
    
    @property
    def tied_capital(self):
        return self._tied_capital
    
    @property
    def realized_profit_loss(self):
        return self.number_of_shares * self.acquisition_price - self.tied_capital
    
    @property
    def total_net_dividend_payments(self):
        return self._total_net_dividend_payments
    
    def get_total_share_fee(self, start_date, end_date):
        fb = sum(
            b.fee for b in self.buy_orders
            if ((b.date - start_date).days >= 0 and (end_date - b.date).days >= 0)
            )
        fs = sum(
            s.fee for s in self.sell_orders
            if ((s.date - start_date).days >= 0 and (end_date - s.date).days >= 0)
            )
        return fb + fs
    
    def get_total_share_tax(self, start_date, end_date):
        tb = sum(
            b.tax for b in self.buy_orders
            if ((b.date - start_date).days >= 0 and (end_date - b.date).days >= 0)
            )
        ts = sum(
            s.tax for s in self.sell_orders
            if ((s.date - start_date).days >= 0 and (end_date - s.date).days >= 0)
            )
        return tb + ts
    
    @property
    def yield_on_cost_12_months(self):
        if self.number_of_shares == 0:
            yoc = 0.0
        else:
            yoc = self.dividends_last_12_months / self.acquisition_price
        return yoc * 100.0
    
    @property
    def dividends_last_12_months(self):
        return self._dividends_last_12_months
    
    @property
    def dividend_return_on_tied_capital_12_months(self):
        ret = self.dividends_last_12_months * self.number_of_shares
        if ret == 0.0:
            return 0.0
        
        try:
            d_rotc = ret / max(self.tied_capital, 0.0)
        except ZeroDivisionError:
            d_rotc = math.inf
            
        return d_rotc * 100.0
    
    def get_total_dividend_amount(self, start_date, end_date):
        return sum(
            d.number_of_shares * d.amount_per_share for d in self.dividend_payments
            if ((d.date - start_date).days >= 0 and (end_date - d.date).days >= 0)
            )
    
    def get_total_dividend_fee(self, start_date, end_date):
        return sum(
            d.fee for d in self.dividend_payments
            if ((d.date - start_date).days >= 0 and (end_date - d.date).days >= 0)
            )
    
    def get_total_dividend_tax(self, start_date, end_date):
        return sum(
            d.tax for d in self.dividend_payments
            if ((d.date - start_date).days >= 0 and (end_date - d.date).days >= 0)
            )

class Order:
    
    def __init__(self, order_type, name, isin, date, number_of_shares,
                 amount_per_share, fee, tax):
        self.type = order_type
        self.name = name
        self.isin = isin
        self.date = date
        self.number_of_shares = number_of_shares
        self.amount_per_share = amount_per_share
        self.amount = amount_per_share * number_of_shares
        self.fee = fee
        self.tax = tax
        self.total_cost = self.amount + fee + tax

class Dividend:
    
    def __init__(self, name, isin, date, number_of_shares,
                 amount_per_share, fee, tax):
        self.type = 'Dividend'
        self.name = name
        self.isin = isin
        self.date = date
        self.number_of_shares = number_of_shares
        self.amount_per_share = amount_per_share
        self.amount = amount_per_share * number_of_shares
        self.fee = fee
        self.tax = tax
        self.total_cost = self.amount + fee + tax
