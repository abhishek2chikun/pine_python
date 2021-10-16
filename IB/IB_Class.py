from pandas.core.frame import DataFrame
from pandas.io.parsers import read_csv
from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
from ibapi.order import Order

import threading
import json
import time
import os
import pandas as pd
class IBapi(EWrapper, EClient):
    def __init__(self):
        EClient.__init__(self, self)
        self.i =0

    def nextValidId(self, orderId: int):
        super().nextValidId(orderId)
        self.nextorderId = orderId
        print('The next valid order id is: ', self.nextorderId)

    def orderStatus(self, orderId, status, filled, remaining, avgFullPrice, permId, parentId, lastFillPrice, clientId, whyHeld, mktCapPrice):
        print('orderStatus - orderid:', orderId, 'status:', status, 'filled', filled, 'remaining', remaining, 'lastFillPrice', lastFillPrice)
    
    def openOrder(self, orderId, contract, order, orderState):
        print('openOrder id:', orderId, contract.symbol, contract.secType, '@', contract.exchange, ':', order.action, order.orderType, order.totalQuantity, orderState.status)

    def execDetails(self, reqId, contract, execution):
        print('Order Executed: ', reqId, contract.symbol, contract.secType, contract.currency, execution.execId, execution.orderId, execution.shares, execution.lastLiquidity)
    
    def pnlSingle(self, reqId: int, pos: int, dailyPnL: float,
                    unrealizedPnL: float, realizedPnL: float, value: float):
        super().pnlSingle(reqId, pos, dailyPnL, unrealizedPnL, realizedPnL, value)
        
        
        if not os.path.exists('./pnl.csv'):
            df = pd.DataFrame(columns=["ReqId", "Position","DailyPnL", "UnrealizedPnL","RealizedPnL", "Value"])
            
            df.to_csv('./pnl.csv')
        else:
            df = pd.read_csv('./pnl.csv',index_col=[0])
            df.loc[len(df.index)] = [reqId,pos,dailyPnL, unrealizedPnL,realizedPnL,value]
            df.to_csv('./pnl.csv')

    
    def pnl(self, reqId: int, dailyPnL: float,
                unrealizedPnL: float, realizedPnL: float):
        super().pnl(reqId, dailyPnL, unrealizedPnL, realizedPnL)
        
        if not os.path.exists('./pnl.csv'):
            df = pd.DataFrame(columns=["ReqId", "DailyPnL","UnrealizedPnL", "RealizedPnL"])
            
            df.to_csv('./pnl.csv')
        else:
            df = pd.read_csv('./pnl.csv',index_col=[0])
            df.loc[len(df.index)] = [reqId, dailyPnL, unrealizedPnL,realizedPnL]
            df.to_csv('./pnl.csv')


    def position(self, account: str, contract: Contract, position: float,
                    avgCost: float):
        super().position(account, contract, position, avgCost)
        
        if not os.path.exists('./position.csv'):
            df = pd.DataFrame(columns=["Account", "Symbol", "SecType", "Currency","Position" , "Avg cost"])
            
            df.to_csv('./position.csv')
        else:
            df = pd.read_csv('./position.csv',index_col=[0])
            df.loc[len(df.index)] = [ account, contract.symbol,
            contract.secType,contract.currency,position, avgCost]
            df.to_csv('./position.csv')
        
    
    def accountSummary(self, reqId: int, account: str, tag: str, value: str,
                        currency: str):
        
        super().accountSummary(reqId, account, tag, value, currency)
        
        
        if not os.path.exists('./acc_summary.csv'):
            df = pd.DataFrame(columns=["ReqId", "Account","Tag", "Value", "Currency"])
            
            df.to_csv('./acc_summary.csv')
        else:
            df = pd.read_csv('./acc_summary.csv',index_col=[0])
            df.loc[len(df.index)] = [reqId,account,tag,value,currency]
            df.to_csv('./acc_summary.csv')
        
        
        




class Client:
    def __init__(self) -> None:
        self.app = IBapi()
        self.app.connect('127.0.0.1', 7497, 2)
        api_thread = threading.Thread(target=self.run_loop, daemon=True)
        api_thread.start()
    
    def run_loop(self):
        self.app.run()

    def OTC_order(self,Symbol):
        contract = Contract()
        contract.symbol = Symbol
        contract.secType = 'STK'
        contract.exchange = 'SMART'
        contract.currency = 'USD'
        return contract
    
    def Place_order(self,Type,Quantity,OrderType,LimitPrice,Symbol):
        self.app.nextorderId = None

    
        while True:
            if isinstance(self.app.nextorderId, int):
                print('connected')
                break
            else:
                print('waiting for connection')
                time.sleep(1)
        
        #Create order object
        order = Order()
        order.action = Type
        order.totalQuantity = Quantity
        order.orderType = OrderType
        order.lmtPrice = LimitPrice

        #Place order
        self.app.placeOrder(self.app.nextorderId, self.OTC_order(Symbol), order)
        self.app.nextorderId += 1


    def Account_details(self):
        if os.path.exists('./acc_summary.csv'):
            os.remove('./acc_summary.csv')
        self.app.reqAccountSummary(9002, "All", "$LEDGER")
        

    def Position(self):
        if os.path.exists('./position.csv'):
            os.remove('./position.csv')
        self.app.reqPositions()

    def PNL(self):
        if os.path.exists('./pnl.csv'):
            os.remove('./pnl.csv')
        self.app.reqPnL(1, "DU229334", "")
    
    def Close(self):
        self.app.disconnect()

obj = Client()
obj.Place_order("SELL",2000,"MKT","1.10","APPL")
time.sleep(5)
obj.Account_details()
time.sleep(5)
obj.Position()
time.sleep(5)
obj.PNL()
time.sleep(5)
obj.Close()