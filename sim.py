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
    timestamp = row['timestampx']
    timestampnext = tickdata['timestampx'][i+1]
    
    if (tradetimestamp > timestamp) and (tradetimestamp <= timestampnext):
       # print('trade happend !!!')
        tradeprice[i] = tradedata["price"][trade_i]
        tradevolume[i] = tradedata["volume"][trade_i]
        if trade_i == len(tradedata)-1:
            break
        trade_i = trade_i + 1 
        tradetimestamp = tradedata['timestampx'][trade_i]
        
x = 0
v = 1.0
m = 0
q = 0
profit = 0
botBid = tickdata["bestBid"][0]
botAsk = tickdata["bestAsk"][0]
ts = tickdata["timestampx"][0]
change_ts = tickdata["timestampx"][0]
statetrace = [[0,0,0,0,0,0,0,0,ts]] * len(tickdata)
for i, row in tickdata.iterrows():
    duration = tickdata["timestampx"][i] - ts
    duration_ms = round(duration.total_seconds() * 1000)
    ts = tickdata["timestampx"][i]
    bot_waitdur = ts - change_ts
    bot_waitdurms = round(bot_waitdur.total_seconds() * 1000)
    bestBid = row['bestBid']
    bestAsk = row['bestAsk']
    if bot_waitdurms > 500:
        change_ts = ts
        botAsk = bestAsk
        botBid = bestBid
    midprice = (bestBid + bestAsk) / 2
    if q < 0:
       liqudprice = bestAsk
    elif q > 0:
       liqudprice = bestBid
    else: 
        liqudprice = midprice
    statetrace[i] = [x, q, m, profit, botBid, botAsk, midprice, duration_ms, ts]
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
statetrace[-1] = [x, q, m, profit, botBid, botAsk, midprice, duration_ms, ts]
#print(statetrace[-1])
df = pandas.DataFrame(statetrace, columns = ["x", "q", "m", "profit", "botBid", "botAsk", "midprice", "duration", "ts"])
#df[1000:1200].plot(x = "ts", y=["midprice", "botBid","botAsk"])
#print(df.iloc[[-1]])  
#df[["x"]].plot()
#df[["m"]].plot()
#df[["duration"]][20:].plot(kind = "hist")
#df[["q"]].plot()
df[["profit"]].plot()
plt.show()

#    midprice = (bestBid + bestAsk) / 2
#    print(round(midprice,5))
    
    