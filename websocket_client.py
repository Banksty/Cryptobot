import websocket
import json
import os

try:
    import thread
except ImportError:
    import _thread as thread
import time

def write_data_to_file(message, jsonmsg, messageType):
    marketidstr = jsonmsg['marketId']
    timestampstr = jsonmsg['timestamp']
    rootdir = "c:\\cryptodata"
    directory = rootdir + '\\' + marketidstr + '\\' + messageType + '\\' + timestampstr[:10]
    filename = marketidstr + ' ' + messageType + ' ' + timestampstr[:16] + '.json'
    filename = filename.replace(':', '-')
    fullfilename = directory + '\\' + filename
    if not os.path.exists(directory):
        os.makedirs(directory)
    f = open(fullfilename, "a+")
    f.write(message)
    f.write('\n')
    f.close

def on_message(ws, message):
    #print(message)
    jsonmsg = json.loads(message)
    messageType = jsonmsg["messageType"]
    #print(messageType)
    if messageType in ['tick', 'trade', 'orderbook']:
        write_data_to_file(message, jsonmsg, messageType)
        
def on_error(ws, error):
    print(error)

def on_close(ws):
    print("### closed ###")

def on_open(ws):
    def run(*args):
        submsg = {'messageType':'subscribe','marketIds':['BTC-AUD'],'channels':['tick', 'trade', 'heartbeat', 'orderbook']}
        ws.send(json.dumps(submsg))
    thread.start_new_thread(run, ())


if __name__ == "__main__":
    ws = websocket.WebSocketApp("wss://socket.btcmarkets.net/v2",
                              on_message = on_message,
                              on_error = on_error,
                              on_close = on_close)
    ws.on_open = on_open
    ws.run_forever()