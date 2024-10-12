# -*- coding: utf-8 -*-

from datetime import date

class PassiveIncome:
    
    def __init__(self, bookings_by_category = None, colors_by_category = None):
        self.bookings_by_category = \
            bookings_by_category if bookings_by_category != None \
                else {}
        self.colors_by_category = \
            colors_by_category if colors_by_category != None \
                else {}
    
    def get_json_data_for_saving(self):
        _d = {}
        
        for c, bl in self.bookings_by_category.items():
            _d[c] = {
                'color': self.colors_by_category[c],
                'bookings': [{'category': b.category, 'date': b.date.isoformat(),
                              'amount': b.amount, 'fee': b.fee, 'tax': b.tax
                              } for b in bl]
                }
        
        return _d
    
    @classmethod
    def load_from_json_data(cls, data):
        bookings_by_category = {}
        colors_by_category = {}
        
        for c, cd in data.items():
            colors_by_category[c] = cd['color']
            bookings_by_category[c] = [Booking(b['category'],
                                               date.fromisoformat(b['date']),
                                               b['amount'], b['fee'], b['tax']
                                               ) for b in cd['bookings']]
        
        p = cls(
            bookings_by_category = bookings_by_category,
            colors_by_category = colors_by_category
            )
        return p
    
    def __str__(self):
        s = ''
        for c, bs in self.bookings_by_category.items():
            s += '----------------\n'
            s += 'Categroy: {} (color: {})\n\n'.format(
                c, self.colors_by_category[c]
                )
            for b in bs:
                s += str(b)
                s += '\n'
            s += '----------------\n'
        
        return s
    
    def create_category(self, category, color):
        _category = category.strip()
        if _category in self.bookings_by_category.keys():
            raise Exception('Category "{}" already exists'.format(_category))
        if color in self.colors_by_category.values():
            raise Exception('Color "{}" already exists'.format(color))
        if _category =='':
            raise Exception('Category name can not be empty')
        
        self.bookings_by_category[_category] = []
        self.colors_by_category[_category] = color
    
    def update_category(self, category, new_category, new_color):
        _category = category.strip()
        _new_category = new_category.strip()
        if _category not in self.bookings_by_category.keys():
            raise Exception('Category "{}" does not exist'.format(_category))
        if _new_category in self.bookings_by_category.keys():
            if new_color == self.colors_by_category[_new_category]:
                raise Exception('Category "{}" does already exist'.format(_new_category))
        if new_color in self.colors_by_category.values():
            if _new_category in self.bookings_by_category.keys():
                raise Exception('Color "{}" already exists'.format(new_color))
        if _new_category =='':
            raise Exception('Category name can not be empty')
        
        self.bookings_by_category[_new_category] = \
            self.bookings_by_category.pop(_category)
        for b in self.bookings_by_category[_new_category]:
            b.category = _new_category
        
        self.colors_by_category.pop(_category)
        self.colors_by_category[_new_category] = new_color
    
    def delete_category(self, category):
        self.bookings_by_category.pop(category, None)
        self.colors_by_category.pop(category, None)
    
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
    
    @property
    def categories_and_colors(self):
        cnc = [
            (c, self.colors_by_category[c])
            for c in self.bookings_by_category.keys()
            ]
        return cnc
    
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
    
    def get_total_net_amount_by_category(self, start_date, end_date):
        abc = {}
        for c, bs in self.bookings_by_category.items():
            abc[c] = sum(
                b.amount - b.tax - b.fee for b in bs
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
