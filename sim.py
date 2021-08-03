import numpy
import pandas
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
v = 0.01
m = 0
q = 0
profit = 0
statetrace = [[0,0,0,0,0,0,0]] * len(tickdata)
for i, row in tickdata.iterrows():
    #print(i)
    bestBid = row['bestBid']
    bestAsk = row['bestAsk']
    botAsk = bestAsk
    botBid = bestBid
    midprice = (bestBid + bestAsk) / 2
    if q < 0:
       liqudprice = bestAsk
    elif q > 0:
       liqudprice = bestBid
    else: 
        liqudprice = midprice
    statetrace[i] = [x, q, m, profit, botBid, botAsk, midprice]
    if tradevolume[i] != 0:
        if tradeprice[i] <= bestBid:
           # s = s + 1
            #print("buy")
            x = x - v * botBid 
            m = m + v * botBid
            q = q + v
        if tradeprice[i] >= bestAsk:
            #s = s + 1
            #print("sell")
            x = x + v * botAsk 
            m = m + v * botAsk
            q = q - v
    profit = x + q * liqudprice
        #if s == 1:
            #fx = x
        #print(x)
q = round(q, 2)
x = x + q * liqudprice
statetrace[-1] = [x, q, m, profit, botBid, botAsk, midprice]
#print(statetrace[-1])
#print([x, q])
df = pandas.DataFrame(statetrace, columns = ["x", "q", "m", "profit", "botBid", "botAsk", "midprice"])
#df[["botBid"]].plot()
#df[["botAsk"]].plot()
#df[["midprice"]].plot()
df.plot(y=["midprice", "botBid","botAsk"])
#print(df.iloc[[-1]])  
#df[["x"]].plot()
#df[["m"]].plot()
#df[["q"]].plot()
#df[["profit"]].plot()
plt.show()
      
        
#    midprice = (bestBid + bestAsk) / 2
#    print(round(midprice,5))
    
    