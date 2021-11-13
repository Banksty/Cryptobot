#BTC-AUD tick 2021-07-11T02-27.json
import json
import os
import numpy
import matplotlib.pyplot as plt
import pandas 
from datetime import datetime

def import_data(messageType):
    data = []
    fullfilename= "al.json"
#    directory = "C:\\temp\\data\\BTC-AUD\\{}\\2021-07-10\\"
    directory = "C:\\cryptodata\\BTC-AUD\\{}\\2021-07-24\\"
    directory = directory.format(messageType)
    
    # read data files
    f = open(directory + fullfilename, "r")
    for line in f:
        jsonstr = line[:-1]
        try:
            jdata = json.loads(jsonstr)
        except:
            print("error, " + messageType)
            print(jsonstr)
        data.append(jdata)
    f.close
    
    # load into a dataframe
    df = pandas.DataFrame(data)
    dtdata = []
    for x in df["timestamp"]:
        dt = datetime.strptime(x, '%Y-%m-%dT%H:%M:%S.%fZ')
        dtdata.append(dt)
    df = df.assign(timestampx = dtdata)
    
    # str to numeric
    if messageType == 'tick':
        df["bestAsk"] = pandas.to_numeric(df["bestAsk"])
        df["bestBid"] = pandas.to_numeric(df["bestBid"])
        df["lastPrice"] = pandas.to_numeric(df["lastPrice"])
    elif messageType == 'trade':
        df["price"] = pandas.to_numeric(df["price"])
        df["volume"] = pandas.to_numeric(df["volume"])
    elif messageType == 'orderbook':
        bids = []
        asks = []
        for i, row in df.iterrows():
            obids = numpy.array(df['bids'][i]).astype(numpy.float)
            oasks = numpy.array(df['asks'][i]).astype(numpy.float)
            bids.append(obids)
            asks.append(oasks)
        df = df.assign(bidsx = bids)
        df = df.assign(asksx = asks)


       # df[""] = pandas.to_numeric(df[""])
       # df[""] = pandas.to_numeric(df[""])
        
    return df

pandas.set_option("display.max.columns", None)
# tickdata = import_data('tick')
# orderbook = import_data('orderbook')

# for x in orderbook:
#     obids = numpy.array(orderbook['bids'][x]).astype(numpy.float)

#obids = numpy.array(orderbook['bids'][0]).astype(numpy.float)
#print(orderbook.iloc[[-1]])  
#print(orderbook['bidsx'][1])
# tradedata = import_data('trade')
# tickdata.plot(x="timestampx", y=["bestAsk", "bestBid", "lastPrice"])
# tradedata.plot(x="timestampx", y=["price"])
#tradedata["volume"].plot(style = ".")
# tradedata["volume"].plot(kind = "hist")
#plt.show()

