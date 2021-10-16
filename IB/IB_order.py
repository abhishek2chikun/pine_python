#from ibapi.order import *
# def Place_order(Type,Quantity,OrderType,LimitPrice,Symbol):
from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
from ibapi.order import Order
import threading
import time

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
    
    def pnl(self, reqId: int, dailyPnL: float,
                unrealizedPnL: float, realizedPnL: float):
        super().pnl(reqId, dailyPnL, unrealizedPnL, realizedPnL)
        print("Daily PnL. ReqId:", reqId, "DailyPnL:", dailyPnL,
                "UnrealizedPnL:", unrealizedPnL, "RealizedPnL:", realizedPnL)

    def position(self, account: str, contract: Contract, position: float,
                    avgCost: float):
        super().position(account, contract, position, avgCost)
        print("Position.", "Account:", account, "Symbol:", contract.symbol, "SecType:",
            contract.secType, "Currency:", contract.currency,
            "Position:", position, "Avg cost:", avgCost)


    def accountSummary(self, reqId: int, account: str, tag: str, value: str,
                        currency: str):
        super().accountSummary(reqId, account, tag, value, currency)
        print("AccountSummary. ReqId:", reqId, "Account:", account,
               "Tag: ", tag, "Value:", value, "Currency:", currency)

def Place_order(Type,Quantity,OrderType,LimitPrice,Symbol):
    def run_loop():
        app.run()

    #Function to create FX Order contract
    def OTC_order(symbol):
        contract = Contract()
        contract.symbol = symbol
        contract.secType = 'CASh'
        contract.exchange = 'SMART'
        contract.currency = 'USD'
        return contract

    app = IBapi()
    app.connect('127.0.0.1', 7497, 22)

    app.nextorderId = None

    #Start the socket in a thread
    api_thread = threading.Thread(target=run_loop, daemon=True)
    api_thread.start()
    #app.reqPositions()

    #Check if the API is connected via orderid
    while True:
        if isinstance(app.nextorderId, int):
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
    app.placeOrder(app.nextorderId, OTC_order(Symbol), order)
    #app.nextorderId += 1

    #time.sleep(3)
    app.reqPnL(17001, "DU228385", "")
    #app.reqPositions()
    #app.reqAccountSummary(9002, "All", "$LEDGER")
    #Cancel order 
    # print('cancelling order')
    # app.cancelOrder(app.nextorderId)

    time.sleep(3)
    app.disconnect()

Place_order("SELL",2000,"MKT","1.10","USD")