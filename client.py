#!/usr/bin/python

import socket
import pandas as pd
import math
def create_series(date, minute, adj_close):
        serie = pd.Series({"Date" : "2017-11-17", 
                       "minute": "17:20:00",
                       "Adj Close": adj_close})
        return serie

def bollinger_bands(data, period=20, std_factor=2):
    data["std"] = data["Adj Close"].rolling(period).std()
    data["mean"] = data["Adj Close"].rolling(period).mean()
    data["Superior Band"] = data["mean"] + data["std"] * std_factor
    data["Inferior Band"] = data["mean"] - data["std"] * std_factor
    
    idx_venda = data[data["Adj Close"] > data["Superior Band"]].index
    data.loc[idx_venda, 'indicador'] = "Sell"
    idx_compra = data[data["Adj Close"] < data["Inferior Band"]].index
    data.loc[idx_compra, "indicador"] = "Buy"

host = "192.168.1.132"
port = 5000
sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
sock.connect((host, port))
order_counter = 0
df = pd.DataFrame()
str_dic = {
        "BB":"Bollinger Bands"
}
print("-------------------------------")
print("High Frequency Trading Program")
print("By Eiki")
print("-------------------------------")
print("Strategies: ")
print("Bollinger Bands: BB")
print("Momentum Trading: MT")
print("-------------------------------")
mode = input("Select strategy: ")
print("---------------------------------------")
print(f"-----------{str_dic[mode]}------------")
print("---------------------------------------")
print(" \n")
send = "Hold"
while 1:
        received = str(sock.recv(1024), "utf-8")
        
        
        date = received.strip().split(',')[0]
        minute = received.strip().split(',')[1]
        price = float(received.strip().split(',')[2])

        print(f"---------{date}---{minute}--------")
        print("Received: ", price)

        if mode == "BB":
                serie = create_series(date, minute, price)

                
                if order_counter <= 20:
                        df = df.append(other=serie, ignore_index=True)
                        sock.sendall(bytes('Hold' + "\n", "utf-8"))

                else:
                        df = df.append(other=serie, ignore_index=True)
                        bollinger_bands(df)
                        
                        if df.iloc[order_counter]["indicador"] == "Buy":
                                send = "Buy"
                        elif df.iloc[order_counter]["indicador"] == "Buy":
                                send = "Sell"
                        else:
                                send = "Hold"
                        sock.sendall(bytes(f'{send}' + "\n", "utf-8"))
                
                print("Order: ", send)
                print(" \n")

        elif mode == "MT":
                serie = create_series(date, minute, price)

                
                if order_counter <= 20:
                        df = df.append(other=serie, ignore_index=True)
                        sock.sendall(bytes('Hold' + "\n", "utf-8"))

                else:
                        df = df.append(other=serie, ignore_index=True)
                        bollinger_bands(df)
                        
                        if df.iloc[order_counter]["indicador"] == "Buy":
                                send = "Buy"
                        elif df.iloc[order_counter]["indicador"] == "Buy":
                                send = "Sell"
                        else:
                                send = "Hold"
                        sock.sendall(bytes(f'{send}' + "\n", "utf-8"))

        order_counter += 1
        