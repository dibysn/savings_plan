# -*- coding: utf-8 -*-

from datetime import date

class PassiveIncome:
    
    def __init__(self, bookings_by_category = None):
        self.bookings_by_category = \
            bookings_by_category if bookings_by_category != None \
                else {}
    
    def get_json_data_for_saving(self):
        _d = {}
        for c, bl in self.bookings_by_category.items():
            _d[c] = [{'category': b.category, 'date': b.date.isoformat(),
                      'amount': b.amount, 'fee': b.fee, 'tax': b.tax
                      } for b in bl]
        return _d
    
    @classmethod
    def load_from_json_data(cls, data):
        bookings_by_category = {}
        for c, bl in data.items():
            bookings_by_category[c] = [Booking(b['category'],
                                               date.fromisoformat(b['date']),
                                               b['amount'], b['fee'], b['tax']
                                               ) for b in bl]
        p = cls(bookings_by_category = bookings_by_category)
        return p
    
    def __str__(self):
        s = ''
        for c, bs in self.bookings_by_category.items():
            s += '----------------\n'
            s += 'Categroy: {}\n\n'.format(c)
            for b in bs:
                s += str(b)
                s += '\n'
            s += '----------------\n'
        
        return s
    
    def create_category(self, category):
        _category = category.strip()
        if _category in self.bookings_by_category.keys():
            raise Exception('Category "{}" already exists'.format(_category))
        if _category =='':
            raise Exception('Category name can not be empty')
        
        self.bookings_by_category[_category] = []
    
    def update_category(self, category, new_category):
        _category = category.strip()
        _new_category = new_category.strip()
        if _category not in self.bookings_by_category.keys():
            raise Exception('Category "{}" does not exist'.format(_category))
        if _new_category in self.bookings_by_category.keys():
            raise Exception('Category "{}" does already exist'.format(_new_category))
        if _new_category =='':
            raise Exception('Category name can not be empty')
        
        self.bookings_by_category[_new_category] = \
            self.bookings_by_category.pop(_category)
        
        for b in self.bookings_by_category[_new_category]:
            b.category = _new_category
    
    def delete_category(self, category):
        self.bookings_by_category.pop(category, None)
    
    def create_booking(self, category, date, amount, fee, tax):
        if category not in self.bookings_by_category.keys():
            raise Exception('Category "{}" does not exist'.format(category))
        
        b = Booking(category, date, amount, fee, tax)
        self.bookings_by_category[category].append(b)
    
    def update_booking(self, booking, new_category, new_date,
                       new_amount, new_fee, new_tax):
        if new_category not in self.bookings_by_category.keys():
            raise Exception('Category "{}" does not exist'.format(new_category))
        
        self.bookings_by_category[booking.category].remove(booking)
        self.bookings_by_category[new_category].append(booking)
        
        booking.category = new_category
        booking.date = new_date
        booking.amount = new_amount
        booking.fee = new_fee
        booking.tax = new_tax
    
    def delete_booking(self, booking):
        try:
            self.bookings_by_category[booking.category].remove(booking)
        except:
            pass
    
    @property
    def categories(self):
        return list(self.bookings_by_category.keys())
    
    def get_total_fee_by_category(self, start_date, end_date):
        fbc = {}
        for c, bs in self.bookings_by_category.items():
            fbc[c] = sum(
                b.fee for b in bs
                if ((b.date - start_date).days >= 0 and (end_date - b.date).days >= 0)
                )
        return fbc
    
    def get_total_tax_by_category(self, start_date, end_date):
        tbc = {}
        for c, bs in self.bookings_by_category.items():
            tbc[c] = sum(
                b.tax for b in bs
                if ((b.date - start_date).days >= 0 and (end_date - b.date).days >= 0)
                )
        return tbc
    
    def get_total_amount_by_category(self, start_date, end_date):
        abc = {}
        for c, bs in self.bookings_by_category.items():
            abc[c] = sum(
                b.amount for b in bs
                if ((b.date - start_date).days >= 0 and (end_date - b.date).days >= 0)
                )
        return abc

class Booking:
    
    def __init__(self, category, date, amount, fee, tax):
        self.category = category
        self.date = date
        self.amount = amount
        self.fee = fee
        self.tax = tax
    
    def __str__(self):
        s = 'Category: {}\n' \
            'Date: {}\n' \
            'Amount: {:.2f} €\n' \
            'Fee: {:.2f} €\n' \
            'Tax: {:.2f} €'.format(
                self.category, self.date, self.amount, self.fee, self.tax
                )
        return s

if __name__ == '__main__':
    
    from datetime import date
    
    categories = ['Dividend', 'Interest']
    
    # (category, date, amount, fee, tax)
    booking = [
        ('Interest', date(2023, 11, 1), 12.3, 0.0, 1.2),
        ('Dividend', date(2022, 1, 12), 18.04, 1.0, 11.2),
        ('Interest', date(2020, 5, 14), 20.1, 1.0, 2.5),
        ('Present', date(2024, 8, 10), 100.0, 0.0, 0.0),
        ('Dividend', date(2021, 2, 1), 10.0, 2.0, 2.3),
        ('Dividend', date(2022, 3, 16), 8.0, 3.0, 1.2)
        ]
    
    passive_income = PassiveIncome()
    
    for c in categories:
        passive_income.create_category(c)
    
    for b in booking:
        try:
            passive_income.create_booking(*b)
        except Exception as e:
            print(e)
    
    start_date = date(1999, 1, 1)
    end_date = date(2024, 12, 31)
    
    print(passive_income)
    print(passive_income.get_total_amount_by_category(start_date, end_date))
    print(passive_income.get_total_tax_by_category(start_date, end_date))
    print(passive_income.get_total_fee_by_category(start_date, end_date))
    
    