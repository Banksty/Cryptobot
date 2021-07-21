#BTC-AUD tick 2021-07-11T02-27.json
import json
import os
import numpy
import matplotlib.pyplot as plt
import pandas 
from datetime import datetime

def import_data(messageType):
    data = []
    fullfilename= "all.json"
    directory = "C:\\cryptodata\\BTC-AUD\\{}\\2021-07-11\\"
    directory = directory.format(messageType)
    f = open(directory + fullfilename, "r")
    for line in f:
        jsonstr = line[:-1]
        try:
            jdata = json.loads(jsonstr)
        except:
            print("error")
        data.append(jdata)
    f.close
    df = pandas.DataFrame(data)
    dtdata = []
    for x in df["timestamp"]:
        dt = datetime.strptime(x, '%Y-%m-%dT%H:%M:%S.%fZ')
        dtdata.append(dt)
    df = df.assign(timestampx = dtdata)
    return df

#initliazation 
pandas.set_option("display.max.columns", None)
tradedata = import_data("trade")
#print(tradedata.head())
tickdata = import_data("tick")
#print(tickdata.head())
tickdata["bestAsk"] = pandas.to_numeric(tickdata["bestAsk"])
tickdata["bestBid"] = pandas.to_numeric(tickdata["bestBid"])
tickdata["lastPrice"] = pandas.to_numeric(tickdata["lastPrice"])
tradedata["price"] = pandas.to_numeric(tradedata["price"])
tradedata["volume"] = pandas.to_numeric(tradedata["volume"])
#print(tradedata["price"])
# #df.head()
# #print(df[1:5])
tickdata.plot(x="timestampx", y=["bestAsk", "bestBid", "lastPrice"])
#tradedata.plot(x="timestampx", y=["price"])
#tradedata["volume"].plot(style = ".")
# tradedata["volume"].plot(kind = "hist")
plt.show()
#dat["bestAsk"].plot()
#plt.plot(df["bestBid"])
#plt.show()

