import readdata
import pandas
import numpy
import datetime

#initliazation 
pandas.set_option("display.max.columns", None)
tradedata = readdata.import_data("trade")
#print(tradedata.head())
tickdata = readdata.import_data("tick")
#print(tickdata.head())

tickdata["bestAsk"] = pandas.to_numeric(tickdata["bestAsk"])
tickdata["bestBid"] = pandas.to_numeric(tickdata["bestBid"])
tickdata["lastPrice"] = pandas.to_numeric(tickdata["lastPrice"])
tradedata["price"] = pandas.to_numeric(tradedata["price"])
tradedata["volume"] = pandas.to_numeric(tradedata["volume"])


for item in tickdata.items():
    print(item["bestBid"])
# a = 1
# for tick in tickdata["bestBid"]:
#     a = a + 1
#     s = a - 1
#     print(tickdata["bestBid"][s:a])
#     #print(tickdata["bestAsk"][1:5])
    