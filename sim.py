import numpy
import pandas
import matplotlib.pyplot as plt
from readdata import import_data

# import data
tickdata = import_data('tick')
tradedata = import_data('trade')

#tickdata.plot(x="timestampx", y=["bestAsk", "bestBid"], style = ".-")
#tradedata.plot(x="timestampx", y=["price"], style = ".-")
#plt.show()

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
#tradeprice = []
#tradevolume = []
trade_i = 0
tradetimestamp = tradedata['timestampx'][0]
for i, row in tickdata.iterrows():
    if i == len(tickdata) - 1:
        break    
    bestBid = row['bestBid']
    bestAsk = row['bestAsk']
    timestamp = row['timestampx']
    timestampnext = tickdata['timestampx'][i+1]
    
    if (tradetimestamp > timestamp) and (tradetimestamp <= timestampnext):
        print('trade happend !!!')
        
#    midprice = (bestBid + bestAsk) / 2
#    print(round(midprice,5))
    
    