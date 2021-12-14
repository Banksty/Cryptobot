import numpy
import pandas
import time
import datetime
import matplotlib.pyplot as plt
from readdata import import_data

# import data
# tickdata = import_data('tick')
# tradedata = import_data('trade')
# orderbook = import_data('orderbook')

# trades = [[]] * len(orderbook)

def getnonemptyindex(raggedlist):
    index = []
    for i, x in enumerate(raggedlist):
        if x != []:
            index.append(i)
    return index


def append_element(A,i,e):
    if len(A[i]) == 0:
        A[i]=[e]
    else:
        A[i].append(e)
   # return A
    
    # iterate over ticks
def transformdata(tickdata, tradedata, orderbook):
    tradeprice = [0] * len(orderbook)
    tradevolume = [0] * len(orderbook)
    trades = [[]] * len(orderbook)
    trade_i = 0
    tradetimestamp = tradedata['timestampx'][0]
    for i, row in orderbook.iterrows():
        if i == len(orderbook) - 1:
            break    
        #timestamp = row['timestampx']
        timestamp = orderbook['timestampx'][i]
        timestampnext = orderbook['timestampx'][i+1]
        
        # iterate through ALL trades between the ticks (multiple trades with same ts)
        while (tradetimestamp >= timestamp) and (tradetimestamp < timestampnext):
            # print('trade happend !!!')
            tp = tradedata["price"][trade_i]
            tv = tradedata["volume"][trade_i]
            tradeprice[i] = tp
            tradevolume[i] = tv
            append_element(trades, i, [tp, tv])
            #print([tp, tv, trade_i, i])
           # print(tradetimestamp, timestamp, timestampnext)
            #time.sleep(1)
            if trade_i == len(tradedata)-1:
                break
            trade_i = trade_i + 1 
            tradetimestamp = tradedata['timestampx'][trade_i]
        
        if trade_i == len(tradedata)-1:
            break   
    return trades
        
    
def sim(gam, tt, botwait, tickdata, tradedata, orderbook, trades): 
    x = 0
    v = 0.1
    loav = v
    lobv = v
    m = 0  
    q = 0
    profit = 0
    sig = 3.467015
    ##gam = 0.001
    T = len(orderbook)
    ##tt = 5000
    botBid = orderbook['bidsx'][0][0, 0]
    botAsk = orderbook['asksx'][0][0, 0]    
    ts = orderbook["timestampx"][0]
    midprice = (botBid + botAsk) / 2
    change_ts = orderbook["timestampx"][0]
    statetrace = [[0,0,0,0,0,0,0,0,ts,0,0,0]] * len(orderbook)
    for i, row in orderbook.iterrows():
       # if i > 5000:
       #     break
    
        duration = orderbook["timestampx"][i] - ts
        duration_ms = round(duration.total_seconds() * 1000)
        ts = orderbook["timestampx"][i]
        bot_waitdur = ts - change_ts
        bot_waitdurms = round(bot_waitdur.total_seconds() * 1000)
        bestBid = row['bidsx'][0,0]
        bestAsk = row['asksx'][0,0]
        middif = (bestBid + bestAsk) / 2 - midprice
        midprice = (bestBid + bestAsk) / 2 
        if bot_waitdurms > botwait:
            change_ts = ts
            loav = v
            lobv = v
            #botAsk = midprice + (1 - 2 * q / v) * (gam * sig**2 * (T - i + 1)) / 2
            #botBid = midprice + (-1 - 2 * q / v) * (gam * sig**2 * (T - i + 1)) / 2
            botAsk = midprice + (1 - 2 * q / v) * (gam * sig**2 * (tt)) / 2
            botBid = midprice + (-1 - 2 * q / v) * (gam * sig**2 * (tt)) / 2
            if botAsk < midprice:
                botAsk = midprice
            if botBid > midprice:
                botBid = midprice
        if q < 0:
           liqudprice = bestAsk
        elif q > 0:
           liqudprice = bestBid
        else: 
            liqudprice = midprice
        statetrace[i] = [x, q, m, profit, botBid, botAsk, midprice, duration_ms, ts, middif, bestBid, bestAsk]
        
        # if tradevolume[i] != 0:
        #     mv = min(tradevolume[i], v)
        #     if tradeprice[i] <= botBid:
        #         x = x - mv * botBid  
        #         m = m + mv * botBid
        #         q = q + mv
        #     if tradeprice[i] >= botAsk:
        #         x = x + mv * botAsk 
        #         m = m + mv * botAsk
        #         q = q - mv
                
        #updating ^^^^
        if trades[i] != []:
            for trade in trades[i]:
                if trade[0] <= botBid:
                    mv = min(trade[1], lobv)
                    lobv = lobv - mv
                    x = x - mv * botBid  
                    m = m + mv * botBid
                    q = q + mv
                if trade[0] >= botAsk:
                    mv = min(trade[1], loav)
                    loav = loav - mv
                    x = x + mv * botAsk 
                    m = m + mv * botAsk
                    q = q - mv
                
        profit = x + q * liqudprice
    q = round(q, 2)
    x = x + q * liqudprice
    statetrace[-1] = [x, q, m, profit, botBid, botAsk, midprice, duration_ms, ts, middif, bestBid, bestAsk]
    #print(statetrace[-1])
    df = pandas.DataFrame(statetrace, columns = ["x", "q", "m", "profit", "botBid", "botAsk", "midprice", "duration", "ts", "middif", "bestBid", "bestAsk"])
    return df

# def sim_sum(df, gamma):
#     return [df["profit"].values[-1], df["q"].values[-1], df["m"].values[-1], gamma, df["m"].values[-1] * 0.001]

# #df = sim(0.001, 5000)
# c = 0
# tt = 5000
# gamma = numpy.arange(0.0001,0.005,0.0002).tolist()
# final = []
# while c < len(gamma):
#     df = sim(gamma[c], tt)
#     print(c)
#     final.append(sim_sum(df, gamma[c]))
#     c = c + 1
# bigsumdf = pandas.DataFrame(final, columns = ["profit", "q", "m", "gamma", "com"])

def sim_sum(df, x):
    return [df["profit"].values[-1], df["q"].values[-1], df["m"].values[-1], x, df["m"].values[-1] * 0.001]


#import data
# tickdata = import_data('tick')
# tradedata = import_data('trade')
# orderbook = import_data('orderbook')
# trades = [[]] * len(orderbook)

#preparedata
#transformdata()


#transformdata()
# tickdata.plot(x="timestampx", y=["bestAsk", "bestBid"], style = ".-")
# tradedata.plot(x="timestampx", y=["price"], style = ".-")
# plt.show()

# iterates through every row in 'tradedata'
# i is the index of the row
#for i, row in tradedata.iterrows():
#    # E.g.    
#    a = row['price']
#    a = row['timestampx']   
#    # 3 different ways to get a value for that row 
#    print([i, row['price']])
##           tradedata['price'][i],
##           tradedata.iloc[i]['price']])


