# -*- coding: utf-8 -*-

import functools

class Saving:
    def __init__(self, year, saving, value):
        self.year = year
        self.saving = saving
        self.value = value

class SavingsSimulation:
    
    def __init__(self,
                 current_age, retirement_age, expected_age,
                 initial_invest, monthly_withdrawal_nominal,
                 rate_of_return, rate_of_inflation,
                 flat_tax_rate, solidarity_tax, church_tax,
                 notes = ''):
        assert(
            current_age > 0 and
            retirement_age > 0 and
            expected_age > 0 and
            initial_invest >= 0.0 and
            monthly_withdrawal_nominal >= 0.0 and
            rate_of_return >= 0.0 and
            flat_tax_rate >= 0.0 and solidarity_tax >= 0.0 and
            church_tax >= 0.0
            )
        
        self._current_age = current_age
        self._retirement_age = retirement_age
        self._expected_age = expected_age
        self._initial_invest = initial_invest
        self._monthly_withdrawal_nominal = monthly_withdrawal_nominal
        self._rate_of_return = rate_of_return
        self._rate_of_inflation = rate_of_inflation
        self._flat_tax_rate = flat_tax_rate
        self._solidarity_tax = solidarity_tax
        self._church_tax = church_tax
        self._notes = str(notes)
        
        self._years_saving = None
        self._years_withdrawal = None
        self._yearly_withdrawal_real = None
        self._monthly_withdrawal_real = None
        self._target_amount_without_tax = None
        self._yearly_savings_amount_without_tax = None
        self._monthly_savings_amount_without_tax = None
        self._total_tax_rate = None
        self._target_amount_with_tax = None
        self._yearly_savings_amount_with_tax = None
        self._monthly_savings_amount_with_tax = None
        
        self._is_saved = False
        self._compute_simulation()
        
        self.savings = {}
    
    def create_saving(self, year, saving, value):
        self.savings[year] = (saving, value)
    
    def update_saving(self, year, new_saving, new_value):
        self.savings[year] = (new_saving, new_value)
    
    def delete_saving(self, year):
        del self.savings[year]
    
    def update_computation(func):
        @functools.wraps(func)
        def wrapper_update_computation(*args, **kwargs):
            value = func(*args, **kwargs)
            args[0]._compute_simulation()
            args[0]._is_saved = False
            return value
        return wrapper_update_computation
        
    @property
    def current_age(self):
        return self._current_age
    @current_age.setter
    @update_computation
    def current_age(self, age):
        assert(age > 0)
        assert(age < self.retirement_age)
        self._current_age = age
    
    @property
    def retirement_age(self):
        return self._retirement_age
    @retirement_age.setter
    @update_computation
    def retirement_age(self, age):
        assert(age > 0)
        assert(age < self.expected_age)
        assert(age > self.current_age)
        self._retirement_age = age
    
    
    @property
    def expected_age(self):
        return self._expected_age
    @expected_age.setter
    @update_computation
    def expected_age(self, age):
        assert(age > 0)
        assert(age > self.retirement_age)
        self._expected_age = age
        
    @property
    def initial_invest(self):
        return self._initial_invest
    @initial_invest.setter
    @update_computation
    def initial_invest(self, amount):
        assert(amount >= 0.0)
        self._initial_invest = amount
        
    @property
    def monthly_withdrawal_nominal(self):
        return self._monthly_withdrawal_nominal
    @monthly_withdrawal_nominal.setter
    @update_computation
    def monthly_withdrawal_nominal(self, amount):
        assert(amount >= 0.0)
        self._monthly_withdrawal_nominal = amount
        
    @property
    def rate_of_return(self):
        return self._rate_of_return
    @rate_of_return.setter
    @update_computation
    def rate_of_return(self, rate):
        assert(rate >= 0.0)
        self._rate_of_return = rate
        
    @property
    def rate_of_inflation(self):
        return self._rate_of_inflation
    @rate_of_inflation.setter
    @update_computation
    def rate_of_inflation(self, rate):
        self._rate_of_inflation = rate
    
    @property
    def flat_tax_rate(self):
        return self._flat_tax_rate
    @flat_tax_rate.setter
    @update_computation
    def flat_tax_rate(self, tax):
        assert(tax > 0.0)
        self._flat_tax_rate = tax
        
    @property
    def solidarity_tax(self):
        return self._solidarity_tax
    @solidarity_tax.setter
    @update_computation
    def solidarity_tax(self, tax):
        assert(tax >= 0.0)
        self._solidarity_tax = tax
        
    @property
    def church_tax(self):
        return self._church_tax
    @church_tax.setter
    @update_computation
    def church_tax(self, tax):
        assert(tax >= 0.0)
        self._church_tax = tax
    
    @property
    def notes(self):
        return self._notes
    @notes.setter
    def notes(self, text):
        self._notes = str(text)
        self._is_saved = False
    
    @property
    def years_saving(self):
        return self._years_saving
    
    @property
    def years_withdrawal(self):
        return self._years_withdrawal
    
    @property
    def yearly_withdrawal_real(self):
        return self._yearly_withdrawal_real
    
    @property
    def monthly_withdrawal_real(self):
        return self._monthly_withdrawal_real
    
    @property
    def target_amount_without_tax(self):
        return self._target_amount_without_tax
    
    @property
    def yearly_savings_amount_without_tax(self):
        return self._yearly_savings_amount_without_tax
    
    @property
    def monthly_savings_amount_without_tax(self):
        return self._monthly_savings_amount_without_tax
    
    @property
    def total_tax_rate(self):
        return self._total_tax_rate
    
    @property
    def target_amount_with_tax(self):
        return self._target_amount_with_tax
    
    @property
    def yearly_savings_amount_with_tax(self):
        return self._yearly_savings_amount_with_tax
    
    @property
    def monthly_savings_amount_with_tax(self):
        return self._monthly_savings_amount_with_tax
    
    @property
    def is_saved(self):
        return self._is_saved
    
    def __str__(self):
        s = ('Input\n'
             '  Current age: {}\n'
             '  Retirement age: {}\n'
             '  Expected age: {}\n'
             '  Initial invest: {:,.2f} €\n'
             '  Monthly withdrawal (nominal): {:,.2f} €\n'
             '  Rate of return: {:.2f}%\n'
             '  Rate of inflation: {:.2f}%\n'
             '  Flat tax rate: {:.2f}%\n'
             '  Solidarity tax: {:.2f}%\n'
             '  Curch tax: {:.2f}%\n'
             '---------\n'
             'Output\n'
             '  Years saving: {}\n'
             '  Years withdrawal: {}\n'
             '  Yearly withdrawal (in real terms): {:,.2f} €\n'
             '  Monthly withdrawal (in real terms): {:,.2f} €\n'
             '  Target amount (without tax): {:,.2f} €\n'
             '  Minimal yearly savings rate (without tax): {:,.2f} €\n'
             '  Minimal monthly savings rate (without tax): {:,.2f} €\n'
             '  Total tax rate: {:.2f}%\n'
             '  Target amount (with tax): {:,.2f} €\n'
             '  Minimal yearly savings rate (with tax): {:,.2f} €\n'
             '  Minimal monthly savings rate (with tax): {:,.2f} €').format(
                 self.current_age,
                 self.retirement_age,
                 self.expected_age,
                 self.initial_invest,
                 self.monthly_withdrawal_nominal,
                 self.rate_of_return * 100.0,
                 self.rate_of_inflation * 100.0,
                 self.flat_tax_rate * 100.0,
                 self.solidarity_tax * 100.0,
                 self.church_tax * 100.0,
                 self.years_saving,
                 self.years_withdrawal,
                 self.yearly_withdrawal_real,
                 self.monthly_withdrawal_real,
                 self.target_amount_without_tax,
                 self.yearly_savings_amount_without_tax,
                 self.monthly_savings_amount_without_tax,
                 self.total_tax_rate * 100.0,
                 self.target_amount_with_tax,
                 self.yearly_savings_amount_with_tax,
                 self.monthly_savings_amount_with_tax)
        return s
    
    def get_json_data_for_saving(self):
        _d = {
            'current_age': self.current_age,
            'retirement_age': self.retirement_age,
            'expected_age': self.expected_age,
            'initial_invest': self.initial_invest,
            'monthly_withdrawal_nominal': self.monthly_withdrawal_nominal,
            'rate_of_return': self.rate_of_return,
            'rate_of_inflation': self.rate_of_inflation,
            'flat_tax_rate': self.flat_tax_rate,
            'solidarity_tax': self.solidarity_tax,
            'church_tax': self.church_tax,
            'notes': self.notes
            }
        return _d
    
    @classmethod
    def load_from_json_data(cls, data):
        gs = cls(
            data['current_age'], data['retirement_age'], data['expected_age'],
            data['initial_invest'], data['monthly_withdrawal_nominal'],
            data['rate_of_return'], data['rate_of_inflation'],
            data['flat_tax_rate'], data['solidarity_tax'], data['church_tax'],
            data['notes'])
        gs._is_saved = True
        return gs
    
    @staticmethod
    def compound(value, interest, n_years):
        return value * (1.0 + interest)**n_years
    
    @staticmethod
    def compound_yearly(value, interest, n_years):
        if interest == 0.0:
            _val = value * n_years
        else:
            _val = value * ((1.0 + interest)**n_years - 1.0) / interest
        return _val
    
    @staticmethod
    def sample_portfolio(
            initial_invest, rate_of_return,
            yearly_saving, list_of_duration_years):
        savings = [initial_invest + ni*yearly_saving
                   for ni in list_of_duration_years]
        portfolio_value = [SavingsSimulation.compound(initial_invest, rate_of_return, ni) + \
                           SavingsSimulation.compound_yearly(yearly_saving, rate_of_return, ni)
                           for ni in list_of_duration_years]
        return savings, portfolio_value
    
    def _compute_simulation(self):
        self._years_saving = self.retirement_age - self.current_age
        self._years_withdrawal = self.expected_age - self.retirement_age
        if abs(self.rate_of_return) < 1e-10:
            _weight = self._years_saving
        else:
            _weight = ((1.0 + self.rate_of_return)**self.years_saving - 1.0) / self.rate_of_return
        
        self._monthly_withdrawal_real = SavingsSimulation.compound(self.monthly_withdrawal_nominal, self.rate_of_inflation, self.years_saving)
        self._yearly_withdrawal_real = 12 * self.monthly_withdrawal_real
        
        self._target_amount_without_tax = self.yearly_withdrawal_real * self.years_withdrawal
        self._yearly_savings_amount_without_tax = \
            (self.target_amount_without_tax - self.initial_invest * (1.0 + self.rate_of_return)**self.years_saving) / _weight
        self._monthly_savings_amount_without_tax = self.yearly_savings_amount_without_tax / 12

        self._total_tax_rate = \
            (1.0 + self.solidarity_tax + self.church_tax) / \
            (1.0 / self.flat_tax_rate + self.church_tax)
        self._yearly_savings_amount_with_tax = \
            (self.target_amount_without_tax - self.initial_invest * \
            ((1.0 + self.rate_of_return)**self.years_saving * (1.0 - self.total_tax_rate) + self.total_tax_rate)) / \
            (_weight * (1.0 - self.total_tax_rate) + self.years_saving * self.total_tax_rate)
        self._monthly_savings_amount_with_tax = self.yearly_savings_amount_with_tax / 12
        
        self._target_amount_with_tax = \
            self.initial_invest * (1.0 + self.rate_of_return)**self.years_saving + \
            self.yearly_savings_amount_with_tax * _weight
    
if __name__ == '__main__':
    savings_sim_ = SavingsSimulation(
        30, 67, 90,
        2000.0, 500.0, 0.05, 0.022,
        0.25, 0.055, 0.08)




















