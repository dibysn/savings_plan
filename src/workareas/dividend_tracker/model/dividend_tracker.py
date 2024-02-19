# -*- coding: utf-8 -*-

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
    
    def create_buy_order(self, date, number_of_shares,
                         amount_per_share, fee, tax):
        o = Order(
            'Buy', self.name, self.isin, date, number_of_shares,
            amount_per_share, fee, tax
            )
        self.buy_orders.append(o)
    
    def update_buy_order(self, order, new_date, new_number_of_shares,
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
    
    def delete_buy_order(self, order):
        if self.number_of_shares < order.number_of_shares:
            raise Exception('Not enough shares available')
        try:
            self.buy_orders.remove(order)
        except:
            raise Exception('Order does not exist')
    
    def create_sell_order(self, date, number_of_shares,
                          amount_per_share, fee, tax):
        if self.number_of_shares < number_of_shares:
            raise Exception('Not enough shares available')
        o = Order(
            'Sell', self.name, self.isin, date, number_of_shares,
            amount_per_share, fee, tax
            )
        self.sell_orders.append(o)
    
    def update_sell_order(self, order, new_date, new_number_of_shares,
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
        
    def delete_sell_order(self, order):
        try:
            self.sell_orders.remove(order)
        except:
            raise Exception('Order does not exist')
    
    def create_dividend(self, date, number_of_shares,
                         amount_per_share, fee, tax):
        
        d = Dividend(
            self.name, self.isin, date, number_of_shares,
            amount_per_share, fee, tax
            )
        self.dividend_payments.append(d)
    
    def update_dividend(self, order, new_date, new_number_of_shares,
                         new_amount_per_share, new_fee, new_tax):
        order.date = new_date
        order.number_of_shares = new_number_of_shares
        order.amount_per_share = new_amount_per_share
        order.amount = new_amount_per_share * new_number_of_shares
        order.fee = new_fee
        order.tax = new_tax
        order.total_cost = new_amount_per_share * new_number_of_shares + new_fee + new_tax
    
    def delete_dividend(self, dividend):
        try:
            self.dividend_payments.remove(dividend)
        except:
            raise Exception('Dividend does not exist')
    
    def create_booking(self, booking_type, date, number_of_shares,
                         amount_per_share, fee, tax):
        if booking_type == 'Buy':
            self.create_buy_order(
                date, number_of_shares, amount_per_share, fee, tax
                )
        elif booking_type == 'Sell':
            self.create_sell_order(
                date, number_of_shares, amount_per_share, fee, tax
                )
        elif booking_type == 'Dividend':
            self.create_dividend(
                date, number_of_shares, amount_per_share, fee, tax
                )
        else:
            raise Exception('Booking type does not exist')
    
    def update_booking(self, booking, new_date, new_number_of_shares,
                         new_amount_per_share, new_fee, new_tax):
        if booking.type == 'Buy':
            self.update_buy_order(
                booking, new_date, new_number_of_shares,
                new_amount_per_share, new_fee, new_tax
                )
        elif booking.type == 'Sell':
            self.update_sell_order(
                booking, new_date, new_number_of_shares,
                new_amount_per_share, new_fee, new_tax
                )
        elif booking.type == 'Dividend':
            self.update_dividend(
                booking, new_date, new_number_of_shares,
                new_amount_per_share, new_fee, new_tax
                )
        else:
            raise Exception('Booking type does not exist')
    
    def delete_booking(self, booking):
        if booking.type == 'Buy':
            self.delete_buy_order(booking)
        elif booking.type == 'Sell':
            self.delete_sell_order(booking)
        elif booking.type == 'Dividend':
            self.delete_dividend(booking)
        else:
            raise Exception('Booking type does not exist')
    
    @property
    def number_of_shares(self):
        buy = self.buy_orders
        sell = self.sell_orders
        n = sum(b.number_of_shares for b in buy) - sum(s.number_of_shares for s in sell)
        return n
    
    @property
    def acquisition_price(self):
        if self.number_of_shares == 0:
            p = 0.0
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
            p = sum(b.number_of_shares * b.amount_per_share for b in buy) / \
                sum(b.number_of_shares for b in buy)
        return p
    
    @property
    def tied_capital(self):
        vb = sum(b.number_of_shares * b.amount_per_share for b in self.buy_orders)
        vs = sum(s.number_of_shares * s.amount_per_share for s in self.sell_orders)
        return vb - vs
    
    @property
    def realized_profit_loss(self):
        return self.number_of_shares * self.acquisition_price - self.tied_capital
    
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
        return sum(
            d.amount_per_share for d in self.dividend_payments
            if (dt.today() - d.date).days < 365
            )
    
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

if __name__ == '__main__':
    s1 = Share('DE0012331', 'ShareA')
    s2 = Share('DE0044312', 'ShareB')
    
    p = Portfolio()
    p.add_share(s1)
    p.add_share(s2)
    
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
    
    start_date = dt(2022, 12, 1)
    end_date = dt(2023, 10, 12)
    
    # start_date = dt(2020, 12, 1)
    # end_date = dt(2024, 10, 12)
    
    print('ShareA')
    # Expected: 32
    print('  Number of shares: {}'.format(s1.number_of_shares))
    # Expected: 8.75
    print('  Acquisition price: {:.2f} €'.format(s1.acquisition_price))
    # Expected: 291.00
    print('  Current tied capital: {:.2f} €'.format(s1.tied_capital))
    # Expected: -11.0
    print('  Profit/loss: {:.2f} €'.format(s1.realized_profit_loss))
    # Expected: 77.71
    print('  Yield on cost (12 months): {:.2f} %'.format(s1.yield_on_cost_12_months))
    # Expected: 74,78
    print('  Dividend ROTC (12 months): {:.2f} %'.format(s1.dividend_return_on_tied_capital_12_months))
    
    
    print()
    
    # Expected: 35.00
    print('  Total share fees: {:.2f} €'.format(s1.get_total_share_fee(start_date, end_date)))
    # Expected: 13.20
    print('  Total share tax: {:.2f} €'.format(s1.get_total_share_tax(start_date, end_date)))
    # Expected: 127.40
    print('  Total dividends received: {:.2f} €'.format(s1.get_total_dividend_amount(start_date, end_date)))
    # Expected: 6.00
    print('  Total dividend fees: {:.2f} €'.format(s1.get_total_dividend_fee(start_date, end_date)))
    # Expected: 38.00
    print('  Total dividend tax: {:.2f} €'.format(s1.get_total_dividend_tax(start_date, end_date)))
    
    print()
    
    print('ShareB')
    # Expected: 56
    print('  Number of shares: {}'.format(s2.number_of_shares))
    # Expected: 8.20
    print('  Acquisition price: {:.2f} €'.format(s2.acquisition_price))
    # Expected: 419.0
    print('  Current tied capital: {:.2f} €'.format(s2.tied_capital))
    # Expected: 40.0
    print('  Profit/loss: {:.2f} €'.format(s2.realized_profit_loss))
    # Expected: 28.06
    print('  Yield on cost (12 months): {:.2f} %'.format(s2.yield_on_cost_12_months))
    # Expected: 30.74
    print('  Dividend ROTC (12 months): {:.2f} %'.format(s2.dividend_return_on_tied_capital_12_months))
    
    print()
    
    # Expected: 20.0
    print('  Total share fees: {:.2f} €'.format(s2.get_total_share_fee(start_date, end_date)))
    # Expected: 14.50
    print('  Total share tax: {:.2f} €'.format(s2.get_total_share_tax(start_date, end_date)))
    # Expected: 42.20
    print('  Total dividends received: {:.2f} €'.format(s2.get_total_dividend_amount(start_date, end_date)))
    # Expected: 9
    print('  Total dividend fees: {:.2f} €'.format(s2.get_total_dividend_fee(start_date, end_date)))
    # Expected: 37
    print('  Total dividend tax: {:.2f} €'.format(s2.get_total_dividend_tax(start_date, end_date)))
    
    print()
    print('Portfolio')    
    print('  Current tied capital: {:.2f} €'.format(p.tied_capital))
    print('  Yield on cost (12 months): {:.2f} %'.format(p.yield_on_cost_12_months))
    print('  Dividend ROTC (12 months): {:.2f} %'.format(p.dividend_return_on_tied_capital_12_months))
    print('  Total share fees: {:.2f} €'.format(p.get_total_share_fee(start_date, end_date)))
    print('  Total share tax: {:.2f} €'.format(p.get_total_share_tax(start_date, end_date)))
    print('  Total dividends received: {:.2f} €'.format(p.get_total_dividend_amount(start_date, end_date)))
    print('  Total dividend fees: {:.2f} €'.format(p.get_total_dividend_fee(start_date, end_date)))
    print('  Total dividend tax: {:.2f} €'.format(p.get_total_dividend_tax(start_date, end_date)))














