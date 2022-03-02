import numpy as np
from src.base.base_strategy import BacktestingBaseStrategy



class BuyOneSidedSlTpCloseOpposite(BacktestingBaseStrategy):
    """ 1 Side (long) With Stoploss & TakeProfit and reverse 
    this strategy can open position on 2 side
    it set stop loss and take profit if hit will close the position
    if you gave opposit signal it will close your last position and open 
    new position
    """
    params = None

    def init(self):
        super().init()
        self.signal_indicator = self.I(self.params.get('indicator'))
        self.order_report_path = self.params.get('order_report_path')

    def next(self):
        super().next()
        close_price = self.data.Close[-1]
        for trade in self.trades:
            if trade.is_long:
                if self.signal_indicator == 1:
                    trade.close()

        if self.signal_indicator == 2 and len(self.trades) == 0:
            self.buy(sl=close_price - (self.params.get('stop_loss') * close_price / 100),
                     tp=close_price + (self.params.get('take_profit') * close_price / 100))

    def stop(self):
        self.save_trades(self.closed_trades)
        

class SellOneSidedSlTpCloseOpposite(BacktestingBaseStrategy):
    """ 1 Side (Short) With Stoploss & TakeProfit and reverse 
    this strategy can open position on 2 side
    it set stop loss and take profit if hit will close the position
    if you gave opposit signal it will close your last position and open 
    new position
    """
    params = None

    def init(self):
        super().init()
        self.signal_indicator = self.I(self.params.get('indicator'))
        self.order_report_path = self.params.get('order_report_path')

    def next(self):
        super().next()
        close_price = self.data.Close[-1]
        for trade in self.trades:
            if not trade.is_long:
                if self.signal_indicator == 2:
                    trade.close()

        if self.signal_indicator == 1 and len(self.trades) == 0:
            self.sell(sl=close_price + (self.params.get('stop_loss') * close_price / 100),
                      tp=close_price - (self.params.get('take_profit') * close_price / 100))

    def stop(self):
        self.save_trades(self.closed_trades)


class BuyOneSidedSlTrailingCloseOpposite(BacktestingBaseStrategy):
    """ 1 Side (long) trail stop and reverse 
    this strategy can open position on 1 side and it just have a trail stop 
    if you gave opposit signal it will close your last position and open 
    new position
    """
    params = None

    def init(self):
        super().init()
        self.signal_indicator = self.I(self.params.get('indicator'))
        self.order_report_path = self.params.get('order_report_path')
        self.stop_trailing_amount = self.params.get('stop_trailing_amount')

    def next(self):
        super().next()
        close_price = self.data.Close[-1]
        stop_trail_long = close_price - (close_price * self.stop_trailing_amount / 100)

        for trade in self.trades:
            if trade.is_long:
                trade.sl = max(trade.sl or -np.inf, stop_trail_long)
                if self.signal_indicator == 1:
                    trade.close()

        if self.signal_indicator == 2 and len(self.trades) == 0:
            self.buy(sl=stop_trail_long)

    def stop(self):
        self.save_trades(self.closed_trades)


class SellOneSidedSlTrailingCloseOpposite(BacktestingBaseStrategy):
    """ 1 Side (short) trail stop and reverse 
    this strategy can open position on 1 side and it just have a trail stop 
    if you gave opposit signal it will close your last position and open 
    new position
    """
    params = None

    def init(self):
        super().init()
        self.signal_indicator = self.I(self.params.get('indicator'))
        self.order_report_path = self.params.get('order_report_path')
        self.stop_trailing_amount = self.params.get('stop_trailing_amount')

    def next(self):
        super().next()
        close_price = self.data.Close[-1]
        stop_trail_short = close_price + (close_price*self.stop_trailing_amount/100)
        for trade in self.trades:
            if not trade.is_long:
                trade.sl = min(trade.sl or np.inf, stop_trail_short)

                if self.signal_indicator == 2:
                    trade.close()

        if self.signal_indicator == 1 and len(self.trades) == 0:
            self.sell(sl=stop_trail_short)

    def stop(self):
        self.save_trades(self.closed_trades)
