from datetime import datetime
import pandas as pd
import math
from abc import ABC, abstractmethod
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

# Implement here the Part I
class Strategy(ABC):
    @abstractmethod
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
    
# Implement here the Part II
class Portfolio:
    def __init__(self, name, currency, aum, _historical_nav_dummy, _positions_dummy, strategy):
        self.name = name
        self.currency = currency
        self.aum = aum
        self.nav = aum
        self.historical_nav: list[float] = [aum]
        self.positions: list[Position] = []
        self.strategy = strategy

    def initialize_position_from_instrument_list(self, instrument_list: list[Instrument]):
        """Initialize positions with instruments (weights/qty = 0)."""
        self.positions = [Position(instrument) for instrument in instrument_list]

    def _positions_to_dict(self) -> dict[str, Position]:
        return {pos.instrument.ticker: pos for pos in self.positions}

    def rebalance_portfolio(self, date: datetime = datetime.now()):
        pos_dict = self._positions_to_dict()
        signals = self.strategy.generate_signals(pos_dict)

        total_val = self.nav

        for ticker, signal_weight in signals.items():
            if ticker not in pos_dict:
                continue

            pos = pos_dict[ticker]
            instr = pos.instrument
            price = instr.last_quote.price if instr.last_quote else None

            if price is None:
                continue

            target_val = total_val * signal_weight
            new_qty = math.floor(target_val / price)  # ✅ floor for test

            pos.update(date=date, weight=signal_weight, quantity=new_qty)

    def portfolio_position_summary(self) -> pd.DataFrame:
        """Return summary with exactly the columns expected by the test."""
        data = []
        total_val = 0.0
        for pos in self.positions:
            if pos.instrument.last_quote:
                total_val += pos.quantity * pos.instrument.last_quote.price

        for pos in self.positions:
            instr = pos.instrument
            price = instr.last_quote.price if instr.last_quote else None
            data.append({
                "Ticker": instr.ticker,
                "Weight": pos.weight if total_val > 0 else 0,
                "Quantity": pos.quantity,
                "Last close": price   # ✅ match test column name
            })

        return pd.DataFrame(data)


import unittest

class TestPortfolio(unittest.TestCase):

    def setUp(self):
        # Setup the instruments and quotes
        self.last_date_asset_1 = datetime(2024, 8, 29)
        self.last_close_asset_1 = 230.02
        self.equity_last_quote_asset_1 = Quote(self.last_date_asset_1, self.last_close_asset_1)
        self.equity_1 = Instrument('AAPL', 'NASDAQ', self.equity_last_quote_asset_1, 'USD')

        self.last_date_asset_2 = datetime(2024, 8, 29)
        self.last_close_asset_2 = 414.75
        self.equity_last_quote_asset_2 = Quote(self.last_date_asset_2, self.last_close_asset_2)
        self.equity_2 = Instrument('MSFT', 'NASDAQ', self.equity_last_quote_asset_2, 'USD')

        # Update prices
        self.last_date_asset_1 = datetime(2024, 8, 30)
        self.last_close_asset_1 = 229.0
        self.equity_1.update_price(Quote(self.last_date_asset_1, self.last_close_asset_1))

        self.last_date_asset_2 = datetime(2024, 8, 30)
        self.last_close_asset_2 = 417.14
        self.equity_2.update_price(Quote(self.last_date_asset_2, self.last_close_asset_2))

        # Setup the portfolio strategy and portfolio
        self.pft_strategy = EqualWeightStrategy()
        self.portfolio = Portfolio("Tech Portfolio", "USD", 1000000, 10000, 100, self.pft_strategy)
        self.portfolio.initialize_position_from_instrument_list([self.equity_1, self.equity_2])

    def test_initial_portfolio_summary(self):
        # Test the initial summary of the portfolio
        summary = self.portfolio.portfolio_position_summary()
        expected_data = {
            "Ticker": ['AAPL', 'MSFT'],
            "Weight": [0, 0],
            "Quantity": [0, 0],
            "Last close": [229.0, 417.14]
        }
        expected_df = pd.DataFrame(expected_data)
        pd.testing.assert_frame_equal(summary, expected_df)

    def test_rebalance_portfolio(self):
        # Rebalance the portfolio and check the summary
        self.portfolio.rebalance_portfolio()
        summary = self.portfolio.portfolio_position_summary()

        # Calculate expected values
        total_aum = self.portfolio.aum
        expected_weight = 0.5
        expected_quantity_1 = math.floor((total_aum * expected_weight) / self.equity_1.last_quote.price)
        expected_quantity_2 = math.floor((total_aum * expected_weight) / self.equity_2.last_quote.price)

        expected_data = {
            "Ticker": ['AAPL', 'MSFT'],
            "Weight": [expected_weight, expected_weight],
            "Quantity": [expected_quantity_1, expected_quantity_2],
            "Last close": [229.0, 417.14]
        }
        expected_df = pd.DataFrame(expected_data)

        pd.testing.assert_frame_equal(summary, expected_df)



def run_tests():
    unittest.main(argv=[''], verbosity=2, exit=False)

if __name__ == '__main__':
    run_tests()