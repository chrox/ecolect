#!/usr/bin/python
#-*-coding:utf-8-*-
import datetime

class WorkDay(object):
    holidays = {
        "2012-01-01", "2012-01-02", "2012-01-03", "2012-01-22", "2012-01-23",
        "2012-01-24", "2012-01-25", "2012-01-26", "2012-01-27", "2012-01-28",
        "2012-04-02", "2012-04-03", "2012-04-04", "2012-04-29", "2012-04-30",
        "2012-05-01", "2012-06-22", "2012-06-23", "2012-06-24", "2012-09-30",
        "2012-10-01", "2012-10-02", "2012-10-03", "2012-10-04", "2012-10-05",
        "2012-10-06", "2012-10-07",

        "2013-01-01", "2013-01-02", "2013-01-03", "2013-02-09", "2013-02-10",
        "2013-02-11", "2013-02-12", "2013-02-14", "2013-02-15", "2013-04-04",
        "2013-04-05", "2013-04-06", "2013-04-29", "2013-04-30", "2013-05-01",
        "2013-06-10", "2013-06-11", "2013-06-12", "2013-09-19", "2013-09-20",
        "2013-09-21", "2013-10-01", "2013-10-02", "2013-10-03", "2013-10-04",
        "2013-10-05", "2013-10-06", "2013-10-07", 
    
        "2014-01-01", "2014-01-31", "2014-02-01", "2014-02-02", "2014-02-03",
        "2014-02-04", "2014-02-05", "2014-02-06", "2014-04-05", "2014-04-06",
        "2014-04-07", "2014-05-01", "2014-05-02", "2014-05-03", "2014-05-31",
        "2014-06-01", "2014-06-02", "2014-09-06", "2014-09-07", "2014-09-08",
        "2014-10-01", "2014-10-02", "2014-10-03", "2014-10-04", "2014-10-05",
        "2014-10-06", "2014-10-07",
    }

    workdays = {
        "2012-01-21", "2012-01-29", "2012-03-31", "2012-04-01", "2012-04-28",
        "2012-09-29", "2013-01-05", "2013-01-06", "2013-02-16", "2013-02-17",
        "2013-04-07", "2013-04-27", "2013-04-28", "2013-06-08", "2013-06-09",
        "2013-09-22", "2013-09-29", "2013-10-12", "2014-01-26", "2014-02-08",
        "2014-05-04", "2014-09-28", "2014-10-11",
    }

    def __init__(self, year, month, day):
        self.date = datetime.date(year, month, day)

    def __repr__(self):
        return repr(self.date)

    def __lt__(self, x):
        return self.date < x.date

    def __add__(self, x):
        date = self.date
        delta = 1 if x > 0 else -1
        while x != 0:
            x = x - delta
            date = self._workday_delta(date, delta)
        return date

    def __sub__(self, x):
        if type(x) is int:
            return self.__add__(-x)
        else:
            date = x.date if type(x) is WorkDay else x
            old = self.date if self.date < date else date
            new = self.date if self.date > date else date
            delta = 0
            while new >= old:
                old = self._workday_delta(old, 1)    
                delta = delta + 1
            return delta

    def _is_workday(self, date):
        weekday = date.isoweekday()
        isodate = date.isoformat()
        return (weekday <= 5 and (isodate not in self.holidays)) or \
                (weekday > 5 and (isodate in self.workdays))

    def _workday_delta(self, date, delta):
        date = date + datetime.timedelta(days=delta)
        while not self._is_workday(date):
            date = date + datetime.timedelta(days=delta)
        return date

    def previous(self):
        return self._workday_delta(self.date, -1)

    def next(self):
        return self._workday_delta(self.date, 1)
    
    def within(self, x):
        if x <= 0: return None
        return self._workday_delta(self.date, x-1)

