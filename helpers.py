# _*_ coding:utf-8 _*_

import datetime
import time
import pandas as pd

def today():
    return str(datetime.datetime.today().date())

def get_year():
    return datetime.datetime.today().year

def get_month():
    return datetime.datetime.today().month

def get_hour():
    return datetime.datetime.today().hour

def today_last_year():
    return str(datetime.datetime.today().date() + datetime.timedelta(-365))

def day_last_week(days = -7):
    return str(datetime.datetime.today().date() + datetime.timedelta(days))

def now():
    return time.strftime('%Y-%m-%d %H:%M:%S')

def diff_day(start = None, end = None):
    d1 = datetime.datetime.strptime(start, '%Y-%m-%d')
    d2 = datetime.datetime.strptime(end, '%Y-%m-%d')
    delta = d2 - d1
    return delta.days

def _quar(mon):
    if mon in [1, 2, 3]:
        return '1'
    elif mon in [4, 5, 6]:
        return '2'
    elif mon in [7, 8, 9]:
        return '3'
    elif mon in [10, 11, 12]:
        return '4'
    else:
        return None
def year_qua(date):
    mon = int(date[5:7])
    return [date[0:4], _quar(mon)]

def get_quarts(start, end):
    idx = pd.period_range('Q'.join(year_qua(start)), 'Q'.join(year_qua(end)),
                            freq = 'Q-JAN')
    return [str(d).split('Q') for d in idx][::-1]

def get_q_date(year = None, quarter = None):
    dt = {'1': '-03-31', '2': '-06-30', '3': '-09-30', '4': '-12-31'}
    return '%s%s'%(str(year), dt[str(quarter)])

def trade_cal():
    '''交易日历
    isOpen=1是交易日, isOpen=0是休市
    '''
    df = pd.read_csv('calAll.csv')
    return df

def is_holiday(date):
    '''
    判断是否为交易日
    '''
    df = trade_cal()
    holiday = df[df.isOpen == 0]['calendarDate'].values
    if isinstance(date, str):
        today = datetime.datetime.strptime(date, '%Y-%m-%d')

    if today.isoweekday() in [6, 7] or str(date) in holiday:
        return True
    else:
        return False