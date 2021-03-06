from dataclasses import dataclass

import math

@dataclass
class Position:
    """
    Position is used in Account to track equity positions    
    """

    symbol: str
    quantity: int
    
    def marketvalue(self, marketvalue) -> float:
        return marketvalue * self.quantity

    def values(self):
        return self.symbol, self.quantity

    def to_string(self):
        return self.symbol + '+' + str(self.quantity)
    
class Account:
    """
    Account maintains a cash balance and securities purchased
    """
        
    def __init__(self, balance=1):
        self.cash = float(balance)
        self.equities = {}
    
    def purchase(self, ticker, quantity, marketprice):
        print('purchase')
        if self.cash >= quantity * marketprice:    
            if ticker in self.equities:
                self.equities[ticker].quantity += quantity
            else:
                self.equities[ticker] = Position(ticker, quantity)

            self.cash = self.cash - quantity * marketprice
            print(self.list_positions())

    def maxpurchase(self, ticker, marketprice):
        print('maxpurchase')
        print(self.cash)
        print(marketprice)
    
        if self.cash >= marketprice:   
            print('here') 
            amount_to_buy = math.floor(self.cash / marketprice)
            self.purchase(ticker, amount_to_buy, marketprice)

    def sell(self, ticker, quantity, marketprice):
        
        if ticker in self.equities:
            self.equities[ticker].quantity -= min(self.equities[ticker].quantity, quantity)
            self.cash += quantity * marketprice            
            
            if self.equities[ticker].quantity == 0:
                del self.equities[ticker]
            print(self.list_positions())    

    def sellall(self, ticker, marketprice):
        if ticker in self.equities:
            self.sell(ticker, self.equities[ticker].quantity, marketprice ) 

    def list_positions(self):
        temp = []
        pos = 'CASH+' + str(round(self.cash,2))
        temp.append(pos)
        for k in self.equities.keys():
            pos = self.equities[k].to_string()
            temp.append(pos)  
        return " ".join(temp)

    def mktval(self, mktvalues):
        total = self.cash
        for k, v in self.equities.items():
            if k in mktvalues:
                total += v.quantity * mktvalues[k]
        return total
