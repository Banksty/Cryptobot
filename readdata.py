#BTC-AUD tick 2021-07-11T02-27.json
import json
import os
import numpy
import matplotlib.pyplot as plt
import pandas 
from datetime import datetime
#fullfilename = "BTC-AUD tick 2021-07-11T02-27.json"
fullfilename= "all.json"
directory = "C:\\cryptodata\\BTC-AUD\\tick\\2021-07-11\\"
f = open(directory + fullfilename, "r")
data = []
for line in f:
    jsonstr = line[:-1]
    try:
        jdata = json.loads(jsonstr)
    except:
        print("error")
    data.append(jdata)
f.close
df = pandas.DataFrame(data)
df["bestAsk"] = pandas.to_numeric(df["bestAsk"])
df["bestBid"] = pandas.to_numeric(df["bestBid"])
df["lastPrice"] = pandas.to_numeric(df["lastPrice"])
dtdata = []
for x in df["timestamp"]:
    dt = datetime.strptime(x, '%Y-%m-%dT%H:%M:%S.%fZ')
    dtdata.append(dt)
df = df.assign(timestampx = dtdata)
pandas.set_option("display.max.columns", None)
#df.head()
#print(df[1:5])
df.plot(x="timestampx", y=["bestAsk", "bestBid", "lastPrice"], style = ".-")
plt.show()
#dat["bestAsk"].plot()
#plt.plot(df["bestBid"])
#plt.show()
