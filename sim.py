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
        print('trade happend !!!')
        tradeprice[i] = tradedata["price"][trade_i]
        tradevolume[i] = tradedata["volume"][trade_i]
        if trade_i == len(tradedata)-1:
            break
        trade_i = trade_i + 1 
        tradetimestamp = tradedata['timestampx'][trade_i]
        
x = 0
q = 0
s = 0
for i, row in tickdata.iterrows():
    bestBid = row['bestBid']
    bestAsk = row['bestAsk']
    if tradevolume[i] != 0:
        if tradeprice[i] <= bestBid:
           # s = s + 1
            print("buy")
            x = x - bestBid * 0.01
            q = q + 0.01
        if tradeprice[i] >= bestAsk:
            #s = s + 1
            print("sell")
            x = x + bestAsk * 0.01
            q = q - 0.01
        #if s == 1:
            #fx = x
        print(x)
        print(q)
lq = q        
lx = x
e = bestBid + bestAsk 
a = e / 2
profit = lx - lq * a
print(profit)
print([x-q*a, q])
        
        
#    midprice = (bestBid + bestAsk) / 2
#    print(round(midprice,5))
    
    