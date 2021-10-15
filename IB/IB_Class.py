from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
from ibapi.order import Order
import threading
import json
import time
import os

class IBapi(EWrapper, EClient):
    def __init__(self):
        EClient.__init__(self, self)

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
        print("Daily PnL Single. ReqId:", reqId, "Position:", pos,
                "DailyPnL:", dailyPnL, "UnrealizedPnL:", unrealizedPnL,
                "RealizedPnL:", realizedPnL, "Value:", value)
        pnl = {"Daily PnL Single. ReqId:": reqId, "Position:": pos,
                "DailyPnL:": dailyPnL, "UnrealizedPnL:": unrealizedPnL,
                "RealizedPnL:": realizedPnL, "Value:": value}
        
        with open('./pnl.json','a') as file:
            json.dump(pnl,file,indent=6)

    
    def pnl(self, reqId: int, dailyPnL: float,
                unrealizedPnL: float, realizedPnL: float):
        super().pnl(reqId, dailyPnL, unrealizedPnL, realizedPnL)
        
        print("Daily PnL. ReqId:", reqId, "DailyPnL:", dailyPnL,
                "UnrealizedPnL:", unrealizedPnL, "RealizedPnL:", realizedPnL)
        pnl = {"Daily PnL. ReqId:": reqId, "DailyPnL:": dailyPnL,
                 "UnrealizedPnL:": unrealizedPnL, "RealizedPnL:": realizedPnL}
        
        with open('./pnl.json','a') as file:
            json.dump(pnl,file,indent=6)

    def position(self, account: str, contract: Contract, position: float,
                    avgCost: float):
        super().position(account, contract, position, avgCost)
        # print("Position.", "Account:", account, "Symbol:", contract.symbol, "SecType:",
        #     contract.secType, "Currency:", contract.currency,
        #     "Position:", position, "Avg cost:", avgCost)
        
        position = { "Account:": account, "Symbol:": contract.symbol, "SecType:":
            contract.secType, "Currency:": contract.currency,
            "Position:": position, "Avg cost:": avgCost}
        
        with open('./position.json','a') as file:
            json.dump(position,file,indent=6)
        

    def accountSummary(self, reqId: int, account: str, tag: str, value: str,
                        currency: str):
        super().accountSummary(reqId, account, tag, value, currency)
        # print("AccountSummary. ReqId:", reqId, "Account:", account,
        #        "Tag: ", tag, "Value:", value, "Currency:", currency)
        
        account_summary = {"AccountSummary. ReqId:":reqId, "Account:": account,
               "Tag: ": tag, "Value:": value, "Currency:": currency}

        with open('./account_summary.json','a') as file:
            json.dump(account_summary,file,indent=6)




class Client:
    def __init__(self) -> None:
        self.app = IBapi()
        self.app.connect('127.0.0.1', 7497, 1)
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
        print("Symbol----")
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
        if os.path.exists('./account_summary.json'):
            os.remove('./account_summary.json')
        self.app.reqAccountSummary(9002, "All", "$LEDGER")
        

    def Position(self):
        if os.path.exists('./position.json'):
            os.remove('./position.json')
        self.app.reqPositions()

    def PNL(self):
        if os.path.exists('./pnl.json'):
            os.remove('./pnl.json')
        self.app.reqPnL(1, "DU228385", "")
    
    def Close(self):
        self.app.disconnect()

obj = Client()
obj.Place_order("SELL",2000,"MKT","1.10","APPL")

obj.Account_details()
obj.Position()
obj.PNL()
time.sleep(5)
obj.Close()