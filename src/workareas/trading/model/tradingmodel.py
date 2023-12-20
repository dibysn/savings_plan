# -*- coding: utf-8 -*-

from datetime import date
from urllib.request import urlopen

class TradingPortfolio:
    def __init__(self, initial_deposit, allowed_risk_trade, allowed_risk_portfolio, trades = None):
        self.initial_deposit = initial_deposit
        self.allowed_risk_trade = allowed_risk_trade
        self.allowed_risk_portfolio = allowed_risk_portfolio
        self.trades = trades if trades != None else []
    
    def __str__(self):
        _str = 'Amount: {:.2f} €\n'.format(
            self.portfolio_amount
            )
        _str += 'Allowed risk trade: {:.2f} % ({:.2f} €)\n'.format(
            self.allowed_risk_trade * 100,
            self.allowed_risk_trade * self.portfolio_amount
            )
        _str += 'Allowed risk portfolio: {:.2f} % ({:.2f} €)\n'.format(
            self.allowed_risk_portfolio * 100,
            self.allowed_risk_portfolio * self.portfolio_amount
            )
        _str += 'Left risk portfolio: {:.2f} % ({:.2f} €)\n'.format(
            self.left_risk_portfolio * 100,
            self.left_risk_portfolio * self.portfolio_amount
            )
        return _str
    
    def get_json_data_for_saving(self):
        _t = [t.get_json_data_for_saving() for t in self.trades]
        _d = {
            'initial_deposit': self.initial_deposit,
            'allowed_risk_trade': self.allowed_risk_trade,
            'allowed_risk_portfolio': self.allowed_risk_portfolio,
            'trades': _t
            }
        return _d
    
    @classmethod
    def load_from_json_data(cls, data):
        trades = [Trade.load_from_json_data(t) for t in data['trades']]
        p = cls(
            data['initial_deposit'],
            data['allowed_risk_trade'], data['allowed_risk_portfolio'],
            trades = trades)
        return p
    
    @property
    def left_risk_portfolio(self):
        risk = 0.0
        for t in self.trades:
            if t.is_active and not t.trade_closed:
                risk += t.trade_risk
        return self.allowed_risk_portfolio - risk / self.portfolio_amount
    
    @property
    def portfolio_amount(self):
        portfolio_amount = self.initial_deposit
        for t in self.trades:
            if t.trade_closed:
                portfolio_amount = portfolio_amount + \
                    t.number_of_shares * (t.sell_price - t.entry_price)
        return portfolio_amount
    
    def add_trade(self, trade):
        self.trades.append(trade)
    
    def update_trade(self, trade, new_name, new_isin,
                     new_entry_price,new_protective_stop, new_target_price,
                     new_date_next_earnings, new_date_next_dividend,
                     new_number_of_shares, new_is_active):
        assert(new_number_of_shares >= 1)
        
        trade.update_target_entry_stop(
            new_entry_price, new_protective_stop, new_target_price
            )
        
        trade.name = new_name
        trade.isin = new_isin
        
        trade.date_next_earnings = new_date_next_earnings
        trade.date_next_dividend = new_date_next_dividend
        trade.number_of_shares = new_number_of_shares
        trade.is_active = new_is_active
    
    def close_trade(self, trade, sell_price, date_trade_closed):
        trade.sell_price = sell_price
        trade.date_trade_closed = date_trade_closed
        if sell_price != None:
            trade.trade_closed = True
        else:
            trade.trade_closed = False
    
    def delete_trade(self, trade):
        self.trades.remove(trade)
    
    def compute_max_allowed_number_of_shares(self, trade):
        return max(0, int(self.portfolio_amount * self.allowed_risk_trade / (trade.entry_price - trade.protective_stop)))

class Trade:
    def __init__(self, name, isin,
                 entry_price, protective_stop, target_price,
                 date_next_earnings = None, date_next_dividend = None,
                 number_of_shares = 1, is_active = False):
        
        assert(entry_price < target_price)
        assert(protective_stop < entry_price)
        assert(number_of_shares >= 1)
        
        self.name = name
        self.isin = isin
        
        self._entry_price = entry_price
        self._protective_stop = protective_stop
        self._target_price = target_price
        
        self.date_next_earnings = date_next_earnings
        self.date_next_dividend = date_next_dividend
        
        self.number_of_shares = number_of_shares
        
        self.date_latest_price = None
        self.latest_price = None
        
        self.trade_closed = False
        self.sell_price = None
        self.date_trade_closed = None
        
        self.is_active = is_active
    
    def __str__(self):
        _str = 'Entry price: {:.2f} €\n'.format(self.entry_price)
        _str += 'Protective stop: {:.2f} €\n'.format(self.protective_stop)
        _str += 'Target price: {:.2f} €\n'.format(self.target_price)
        _str += 'Number of shares: {:d}\n'.format(self.number_of_shares)
        _str += 'Trade risk: {:.2f} €\n'.format(self.trade_risk)
        _str += 'Trade reward: {:.2f} €\n'.format(self.trade_reward)
        _str += 'Reward to risk ratio: {:.2f}\n'.format(self.reward_risk_ratio)
        if self.latest_price != None:
            _str += 'Latest price: {:.2f} € ({})\n'.format(
                self.latest_price,
                self.date_latest_price
                )
        if self.trade_closed:
            _str += 'Sell price: {:.2f} € ({})\n'.format(
                self.sell_price,
                self.date_trade_closed
                )
        _str += 'Active: {}\n'.format(self.is_active)
        return _str
    
    def get_json_data_for_saving(self):
        date_next_earnings = \
            self.date_next_earnings.isoformat() \
            if self.date_next_earnings != None else None
        
        date_next_dividend = \
            self.date_next_dividend.isoformat() \
            if self.date_next_dividend != None else None
        
        date_latest_price = \
            self.date_latest_price.isoformat() \
            if self.date_latest_price != None else None
        
        date_trade_closed = \
            self.date_trade_closed.isoformat() \
            if self.date_trade_closed != None else None
        
        _d = {
            'name': self.name,
            'isin': self.isin,
            'entry_price': self._entry_price,
            'protective_stop': self._protective_stop,
            'target_price': self._target_price,
            'date_next_earnings': date_next_earnings,
            'date_next_dividend': date_next_dividend,
            'number_of_shares': self.number_of_shares,
            'date_latest_price': date_latest_price,
            'latest_price': self.latest_price,
            'trade_closed': self.trade_closed,
            'sell_price': self.sell_price,
            'date_trade_closed': date_trade_closed,
            'is_active': self.is_active
            }
        return _d
    
    @classmethod
    def load_from_json_data(cls, data):
        date_next_earnings = \
            date.fromisoformat(data['date_next_earnings']) \
            if data['date_next_earnings'] != None else None
        
        date_next_dividend = \
            date.fromisoformat(data['date_next_dividend']) \
            if data['date_next_dividend'] != None else None
        
        date_latest_price = \
            date.fromisoformat(data['date_latest_price']) \
            if data['date_latest_price'] != None else None
        
        date_trade_closed = \
            date.fromisoformat(data['date_trade_closed']) \
            if data['date_trade_closed'] != None else None
                
        t = cls(
            data['name'], data['isin'],
            data['entry_price'], data['protective_stop'], data['target_price'],
            date_next_earnings, date_next_dividend,
            data['number_of_shares'], data['is_active'])
        
        t.date_latest_price = date_latest_price
        t.latest_price = data['latest_price']
        
        t.trade_closed = data['trade_closed']
        t.sell_price = data['sell_price']
        t.date_trade_closed = date_trade_closed
        
        return t
    
    def get_latest_price(self):
        url = 'https://www.tradegate.de/orderbuch.php?isin={}'.format(self.isin)
        page = urlopen(url)
        html_bytes = page.read()
        html = html_bytes.decode("utf-8")
        
        search_for = '<td class="longprice"><strong id="last">'
        start = html.find(search_for) + len(search_for)
        self.latest_price = float(html[start:start+5].replace(',','.'))
        self.date_latest_price = date.today()
    
    @property
    def target_price(self):
        return self._target_price
    
    @property
    def entry_price(self):
        return self._entry_price
    
    @property
    def protective_stop(self):
        return self._protective_stop
    
    def update_target_entry_stop(self, new_entry_price, new_protective_stop, new_target_price):
        assert(new_entry_price < new_target_price)
        assert(new_protective_stop < new_entry_price)
        self._target_price = new_target_price
        self._entry_price = new_entry_price
        self._protective_stop = new_protective_stop
    
    @property
    def days_left_earnings(self):
        days_left_earnings = None
        if self.date_next_earnings != None:
            days_left_earnings = (self.date_next_earnings - date.today()).days
        return days_left_earnings
    
    @property
    def days_left_dividend(self):
        days_left_dividend = None
        if self.date_next_dividend != None:
            days_left_dividend = (self.date_next_dividend - date.today()).days
        return days_left_dividend
    
    @property
    def trade_risk(self):
        return max(0.0, self.number_of_shares * (self.entry_price - self.protective_stop))
    
    @property
    def trade_reward(self):
        return self.number_of_shares * (self.target_price - self.entry_price)
    
    @property
    def reward_risk_ratio(self):
        reward_risk_ratio = None
        trade_risk = self.trade_risk
        if trade_risk != 0.0:
            reward_risk_ratio = self.trade_reward / trade_risk
        return reward_risk_ratio
    
    @property
    def profit_loss(self):
        profit_loss = None
        if self.trade_closed:
            profit_loss = (self.sell_price - self.entry_price) * self.number_of_shares
        elif self.latest_price != None:
            profit_loss = (self.latest_price - self.entry_price) * self.number_of_shares
        return profit_loss
        
if __name__ == '__main__':
    initial_deposit = 10000
    allowed_risk_trade = 0.02
    allowed_risk_portfolio = 0.06
    portfolio = TradingPortfolio(
        initial_deposit, allowed_risk_trade, allowed_risk_portfolio
        )
    
    entry_price = 10.50
    protective_stop = 10.00
    target_price = 12.50
    trade = Trade('Stock A', 'US0000000000', entry_price, protective_stop, target_price)
    
    print(portfolio)
    print()
    print(trade)
    
    n = portfolio.compute_max_allowed_number_of_shares(trade)
    print('Allowed: {} shares'.format(n))
    print()
    trade.number_of_shares = int(n/2)
    trade.is_active = True
    print(trade)
    
    print('-- Add Trade')
    portfolio.add_trade(trade)
    print()
    print(portfolio)
    
    print('-- Adjust Trade')
    portfolio.update_trade(trade, trade.name, trade.isin,
                     10.42, trade.protective_stop, trade.target_price,
                     trade.date_next_earnings, trade.date_next_dividend,
                     trade.number_of_shares, trade.is_active)
    print()
    print(trade)
    print(portfolio)
    
    print('-- Close Trade')
    portfolio.close_trade(trade, 11.90, date.today())
    print()
    print(trade)
    print(portfolio)
    
    print('-- Adjust portfolio setting')
    portfolio.allowed_risk_portfolio = 0.05
    portfolio.allowed_risk_trade = 0.04
    print(portfolio)

