from datetime import datetime
import pandas as pd
from abc import ABC, abstractmethod
import math

class Portfolio:
    def __init__(self,cash: float = 0.0):
        self.positions: dict[str, Position] = {}
        self.cash = cash
        self.last_valuation_date: datetime | None = None
    
    def add_position(self, position: Position):#position is a Position object (we are calling the class below which includes instrument)
        self.positions[position.instrument.ticker] = position
    
    def total_value(self) -> float:
        total = self.cash
        for pos in self.positions.values():
            if pos.instrument.last_quote is not None:
                total += pos.quantity * pos.instrument.last_quote.price
        return total 

    def rebalance(self, target_weights: dict[str,float], date: datetime = datetime.now()):
        total_value = self.total_value()

        for ticker, target_w in target_weights.items():#in target_wieghts we've got: target_weights = {"AAPL": 0.06, "MSFT": 0.04}
            if ticker not in self.positions:            #ticker, sinc eits a string, it will become the ticker, same for target_w
                raise ValueError(f"Tried to rebalance unknown instrument {ticker}")

            pos = self.positions[ticker]
            instr = pos.instrument
            price = instr.last_quote.price if instr.last_quote else None

            if price is None:
                continue  # skip if no price available

            target_val = total_value * target_w
            new_qty = target_val / price

            pos.update(date=date, weight=target_w, quantity=new_qty)

    def summary(self) -> pd.DataFrame:
        """Return a DataFrame summary of the portfolio."""
        data = []
        total_val = self.total_value()

        for pos in self.positions.values():
            instr = pos.instrument
            price = instr.last_quote.price if instr.last_quote else None
            mkt_val = pos.quantity * price if price else 0.0
            data.append({
                "Ticker": instr.ticker,
                "Quantity": pos.quantity,
                "Price": price,
                "MarketValue": mkt_val,
                "Weight": mkt_val / total_val if total_val > 0 else 0
            })

        return pd.DataFrame(data).set_index("Ticker")
    
class Quote:
    def __init__(self, date: datetime, price: float):
        self.date = date
        self.price = price

    def __str__(self):
        return f'(date: {self.date}, price: {self.price})'


class Instrument:
    def __init__(self, ticker: str, exchange: str, quote: Quote, currency: str):
        self.ticker: str = ticker
        self.exchange: str = exchange
        self.last_quote: Quote = quote
        self.currency: str = currency
        self.quote_history: [Quote] = []

    def __str__(self):
        print(f'Instrument with ticker {self.ticker}, currency {self.currency} and last quote {self.last_quote}')

    def update_price(self, new_quote: Quote):
        self.quote_history.append(self.last_quote)
        self.last_quote = new_quote

    def populate_quote_history_from_df(self, df_data: pd.DataFrame):
        dates = df_data.index.to_pydatetime().tolist()
        prices = df_data['Close'].tolist()
        self.quote_history = [Quote(date, price) for date, price in zip(dates, prices)]

    def quotes_to_dataframe(self) -> pd.DataFrame:
        data = {
            "Date": [quote.date for quote in self.quote_history],
            "Price": [quote.price for quote in self.quote_history]
        }
        df = pd.DataFrame(data)
        df.set_index('Date', inplace=True)
        return df


class Position:
    def __init__(self, instrument: Instrument, date: datetime = datetime.now(), weight: float = 0, quantity: float = 0):
        self.instrument = instrument
        self.date = date
        self.weight = weight
        self.quantity = quantity

    def update(self, date: datetime, weight: float, quantity: float):
        if date is not None:
            self.date = date
        if weight is not None:
            self.weight = weight
        if quantity is not None:
            self.quantity = quantity

class Strategy(ABC):
    @asbtractmethod
    def generate_signals(self, data_for_signal_generation: dict) -> dict:
        """
        Generate trading signals based on input data.
        Parameters
        ----------
        data_for_signal_generation : dict
            Dictionary where keys are tickers (str) and values are Position objects.

        Returns
        -------
        dict
            Dictionary with tickers as keys and signals (float weights) as values.
        """
        pass

class EqualWeightStrategy(Strategy):
    def generate_signals(self, data_for_signal_generation: dict) -> dict:
        if not data_for_signal_generation:
            return {}
        n = len(data_for_signal_generation)
        if n == 0:
            return {}
        equal_weight = 1.0 / n
        return {ticker: equal_weight for ticker in data_for_signal_generation.keys()}