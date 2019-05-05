#! /bin/env python
# -*- coding:utf-8 -*-
import talib

'''
datafram should be like this:(index and date are ascending)
    |date          |open   |high   |low   |close |vol.. |others
-------------------|-------|-------|------|------|------|------
0   |2007-01-02    |20.00  |21.50  |20.00 |20.80 |1000  |      
1   |2007-01-03    |20.50  |20.90  |20.15 |20.20 |1500  |      
2   |2007-01-04    |20.01  |20.15  |19.50 |19.80 |1300  |      
3   |2007-01-05    |19.80  |19.80  |18.95 |19.02 |2200  |      
4   |2007-01-06    |18.85  |20.50  |18.85 |20.10 |1000  |      
'''

# 涨幅比(Rise Ratio=(今日收盘价-昨日收盘价)/昨日收盘价)
def RR(df):
    for idx in range(1,len(df)):
        rr = (df.iloc[idx]['close'] - df.iloc[idx-1]['close'])/df.iloc[idx-1]['close']*100
        df.at[idx, 'RR'] = rr

# 威廉指数(WMS%R或%R)
def WMS(df, days=9):
    '''
    days日WMS%R=(days日内最高价-第days日收盘价)/(days日内最高价-days日内最低价)*100
    '''
    ajust = days - 1
    for idx in range(ajust, len(df)):
        wms = (df.iloc[idx-ajust:idx]['high'].max() - df.iloc[idx]['close'])/(df.iloc[idx-ajust:idx]['high'].max() - df.iloc[idx-ajust:idx]['low'].min())*100
        df.at[idx, 'WMS'] = wms

# 买卖意愿指标
def BR(df, days=26):
    '''
    days日BR=(今日最高价-昨日收盘价)的days日累计总数/(昨日收盘价-今日最低价)的days天累计总数
    '''
    ajust = days - 1
    for idx in range(ajust, len(df)):
        br = (df.iloc[idx-ajust:idx]['high'].sum()-df.iloc[idx-ajust-1:idx-1]['close'].sum())/(df.iloc[idx-ajust-1:idx-1]['close'].sum() - df.iloc[idx-ajust:idx]['low'].sum())
        df.at[idx, 'BR'] = br

# 买卖气势指标
def AR(df, days=26):
    '''
    days日AR=(最高价-开盘价)的days天累计总数/(开盘价-最低价)的days天累计总数
    '''
    ajust = days - 1
    for idx in range(ajust, len(df)):
        ar = (df.iloc[idx-ajust:idx]['high'].sum()-df.iloc[idx-ajust:idx]['open'].sum())/(df.iloc[idx-ajust:idx]['open'].sum() - df.iloc[idx-ajust:idx]['low'].sum())
        df.at[idx, 'AR'] = ar

# 平均成交量(mean volume)
def MV(df, days=12):
    '''
    days日平均成交量=days日内的成交量总和/days
    '''
    ajust = days - 1
    for idx in range(ajust, len(df)):
        mv = df.iloc[idx-ajust:idx]['vol'].mean()
        df.at[idx, 'MV'] = mv

# 移动平均线(moving average)
def MA(df, days=12):
    '''
    移动平均线=days日的股价合计/days
    '''
    ajust = days - 1
    for idx in range(ajust, len(df)):
        ma = df.iloc[idx-ajust:idx]['close'].mean()
        df.at[idx, 'MA'+str(days)] = ma

# 心理线(PSY)
def PSY(df, days=13):
    '''
    days日PSY值=(days日内上涨天数/days)*100
    '''
    ajust = days - 1
    for idx in range(ajust, len(df)):
        ups = len([item for item in df.iloc[idx-ajust:idx]['RR'] if item > 0])
        psy = float(ups)/float(days)*100
        df.at[idx, 'PSY'] = psy

# 能量潮(OBV)
def OBV(df, days=12):
    '''
    今日OBV值=最近days日股价上涨日成交量总和-最近days日股价下跌日成交量总和
    '''
    ajust = days - 1
    for idx in range(ajust, len(df)):
        upVolSum = df.iloc[idx-ajust:idx]['vol'][df.iloc[idx-ajust:idx]['RR'] > 0].sum()
        downVolSum = df.iloc[idx-ajust:idx]['vol'][df.iloc[idx-ajust:idx]['RR'] < 0].sum()
        obv = upVolSum - downVolSum
        df.at[idx, 'OBV'] = obv

# 数量指标(VR)
def VR(df, days=12):
    '''
    VR=(days日内上涨日成交量总和 + 1/2*days日内平盘日成交量总和) / (days日内下跌日成交量总和 + 1/2*days日内平盘日成交量总和)*100
    '''
    ajust = days - 1
    for idx in range(ajust, len(df)):
        upVolSum = df.iloc[idx-ajust:idx]['vol'][df.iloc[idx-ajust:idx]['RR'] > 0].sum()
        flatVolSum = df.iloc[idx-ajust:idx]['vol'][df.iloc[idx-ajust:idx]['RR'] == 0].sum()
        downVolSum = df.iloc[idx-ajust:idx]['vol'][df.iloc[idx-ajust:idx]['RR'] < 0].sum()
        vr = (upVolSum + 0.5*flatVolSum) / (downVolSum + 0.5*flatVolSum) * 100
        df.at[idx, 'VR'] = vr

# 相对强弱指标(RSI)
def RSI(df, days=6):
    '''
    RSI=100 * days日内收盘上涨总幅度平均值/(days日内收盘上涨总幅度平均值-days日内收盘下跌总幅度平均值)
    '''
    ajust = days - 1
    for idx in range(ajust, len(df)):
        upRRMean = df.iloc[idx-ajust:idx]['RR'][df.iloc[idx-ajust:idx]['RR'] > 0].sum()
        downRRMean = df.iloc[idx-ajust:idx]['RR'][df.iloc[idx-ajust:idx]['RR'] < 0].sum()
        rsi = 100 * upRRMean / (upRRMean - downRRMean)
        df.at[idx, 'RSI'] = rsi

# 乖离率(BIAS)
def BIAS(df, days=12):
    '''
    乖离率=(当日股价 - days日内股价移动平均数) / days日平均股价
    '''
    ajust = days - 1
    for idx in range(ajust, len(df)):
        bias = (df.iloc[idx]['close'] - df.iloc[idx]['MA'+str(days)])/df.iloc[idx]['MA'+str(days)]*100
        df.at[idx, 'BIAS'] = bias

# KDJ指标
def KDJ(df, days=12):
    '''
    公式如下：
    未成熟随机值(RSV)：(今日收盘价 - 最近9天的最低价) / (最近9天最高价 - 最近9天的最低价) 当日K值：前日K值 * (2/3) + 当日RSV值 * (1/3) 当日D值：前日D值 * (2/3) + 当日K值 * (1/3)
    K值就是日常的波动，D值就是稍大一點的趋势，而RSV就是K的次一级的级数了。三者的关系就像是浪花(RSV)，和波浪(K，D)的关系。
    KD指标之所以被广泛运用，在于它涵盖了一定时间内最高价与最低价的概念，因此可以很灵敏地反映出价格的变化。
    KD黃金交叉：当KD指标的K值由下往上突破D值，建议买进、做多。 KD死亡交叉：当KD指标的K值由上往下跌破D值時，建议卖出、做空。 KD钝化：K值在高档 (K > 80) 或低档( K < 20)区域连续3天，因为当一档股票高钝化(K值>80，3天以上)，表示非常的强势，通常再涨的机会会变得非常高。
    '''
    df['k'], df['d'] = talib.STOCH(df['high'], df['low'], df['close'])
    df['k'].fillna(value=0, inplace=True)
    df['d'].fillna(value=0, inplace=True)