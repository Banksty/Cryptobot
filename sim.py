import numpy
import pandas
import datetime
import matplotlib.pyplot as plt
from readdata import import_data

# import data
tickdata = import_data('tick')
tradedata = import_data('trade')

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
    
    
# iterate over ticks
tradeprice = [0] * len(tickdata)
tradevolume = [0] * len(tickdata)
trade_i = 0
tradetimestamp = tradedata['timestampx'][0]
for i, row in tickdata.iterrows():
    if i == len(tickdata) - 1:
        break    
    #timestamp = row['timestampx']
    timestamp = tickdata['timestampx'][i]
    timestampnext = tickdata['timestampx'][i+1]
    
    # iterate through ALL trades between the ticks (multiple trades with same ts)
    while (tradetimestamp >= timestamp) and (tradetimestamp < timestampnext):
        # print('trade happend !!!')
        tradeprice[i] = tradedata["price"][trade_i]
        tradevolume[i] = tradedata["volume"][trade_i]
        if trade_i == len(tradedata)-1:
            break
        trade_i = trade_i + 1 
        tradetimestamp = tradedata['timestampx'][trade_i]
    
    if trade_i == len(tradedata)-1:
        break    
x = 0
v = 0.1
m = 0  
q = 0
profit = 0
sig = 3.467015
gam = 0.001
T = len(tickdata)
tt = 5000
botBid = tickdata["bestBid"][0]
botAsk = tickdata["bestAsk"][0]
ts = tickdata["timestampx"][0]
midprice = (botBid + botAsk) / 2
change_ts = tickdata["timestampx"][0]
statetrace = [[0,0,0,0,0,0,0,0,ts,0,0,0]] * len(tickdata)
for i, row in tickdata.iterrows():
    duration = tickdata["timestampx"][i] - ts
    duration_ms = round(duration.total_seconds() * 1000)
    ts = tickdata["timestampx"][i]
    bot_waitdur = ts - change_ts
    bot_waitdurms = round(bot_waitdur.total_seconds() * 1000)
    bestBid = row['bestBid']
    bestAsk = row['bestAsk']
    middif = (bestBid + bestAsk) / 2 - midprice
    midprice = (bestBid + bestAsk) / 2 
    if bot_waitdurms > 5000:
        change_ts = ts
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
    if tradevolume[i] != 0:
        mv = min(tradevolume[i], v)
        if tradeprice[i] <= botBid:
            x = x - mv * botBid 
            m = m + mv * botBid
            q = q + mv
        if tradeprice[i] >= botAsk:
            x = x + mv * botAsk 
            m = m + mv * botAsk
            q = q - mv
    profit = x + q * liqudprice
q = round(q, 2)
x = x + q * liqudprice
statetrace[-1] = [x, q, m, profit, botBid, botAsk, midprice, duration_ms, ts, middif, bestBid, bestAsk]
#print(statetrace[-1])
df = pandas.DataFrame(statetrace, columns = ["x", "q", "m", "profit", "botBid", "botAsk", "midprice", "duration", "ts", "middif", "bestBid", "bestAsk"])
sig = numpy.std(df[["middif"]])
tp = pandas.DataFrame(tradeprice, columns = ["tradeprice"])
print(sig)
df.plot(x = "ts", y=["midprice", "botBid","botAsk"])
#df.plot(x = "ts", y=["midprice", "bestBid","bestAsk"])
print(df.iloc[[-1]])  
#df[["x"]].plot()
#df[["m"]].plot()
#df[["duration"]][20:].plot(kind = "hist")
df[["q"]].plot()
df[["profit"]].plot()
#df[["middif"]].plot()
#df[["middif"]][20:].plot(kind = "hist")
#tp[["tradeprice"]].plot()
plt.show()

#    midprice = (bestBid + bestAsk) / 2
#    print(round(midprice,5))
    
    