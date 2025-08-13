import pandas as pd
import numpy as np

TICK_SIZE = 0.1
INVENTORY_LIMIT = 20
MAX_ROWS = 3000  # Limit processing to the top 3000 rows

class AutomatedMarketMaking:
    def __init__(self):
        self.inventory = 0
        self.last_bid_price = None
        self.last_ask_price = None
        self.past_quotes = {}  # Store past quotes {timestamp: (bid, ask)}

    def round_to_tick(self, price):
        """Rounds a price to the nearest tick size."""
        return round(price / TICK_SIZE) * TICK_SIZE

    def calculate_mid_price(self, order_book):
        """Calculates the mid-price from the order book."""
        if not order_book.empty:
            best_bid = order_book['bid_price_1'].iloc[-1]
            best_ask = order_book['ask_price_1'].iloc[-1]
            return (best_bid + best_ask) / 2
        return None

    def calculate_volatility(self, public_trades, window=10):
        """Calculates historical volatility from public trades (using rolling standard deviation)."""
        if not public_trades.empty and len(public_trades) >= window:
            prices = public_trades['price'].tail(window)
            returns = np.log(prices).diff().dropna()  # Log returns
            return returns.std()
        return 0.01  # Default volatility

    def adjust_spread(self, volatility):
        """Adjusts the bid-ask spread based on market volatility."""
        # A wider spread for higher volatility, a tighter spread for lower volatility.
        return max(0.02, min(0.20, volatility * 5))  # Example scaling

    def handle_inventory_pressure(self, base_bid, base_ask):
        """Adjusts bid/ask prices to manage inventory."""
        bid_price = base_bid
        ask_price = base_ask

        if self.inventory > 10:  # Heavy long position, incentivize selling
            ask_price = self.round_to_tick(ask_price - TICK_SIZE)  # Lower ask
            bid_price = self.round_to_tick(bid_price - 2 * TICK_SIZE)
        elif self.inventory < -10:  # Heavy short position, incentivize buying
            bid_price = self.round_to_tick(bid_price + TICK_SIZE)  # Raise bid
            ask_price = self.round_to_tick(ask_price + 2 * TICK_SIZE)
        return bid_price, ask_price

    def strategy(self, timestamp, order_book, public_trades, current_inventory):
        """
        Core market-making strategy.

        Args:
            timestamp: The current timestamp.
            order_book: DataFrame of order book data up to the timestamp.
            public_trades: DataFrame of public trades data up to the timestamp.
            current_inventory: The current inventory.

        Returns:
            A tuple (bid_price, ask_price) or (None, None) if no quote.
        """
        self.inventory = current_inventory

        # Handle empty data
        if order_book.empty or public_trades.empty:
            if self.past_quotes:
                # Return the last posted quote
                return self.past_quotes[list(self.past_quotes.keys())[-1]]
            else:
                return None, None

        mid_price = self.calculate_mid_price(order_book)
        volatility = self.calculate_volatility(public_trades)
        spread = self.adjust_spread(volatility)

        # Base quotes around the mid-price
        base_bid_price = self.round_to_tick(mid_price - spread / 2)
        base_ask_price = self.round_to_tick(mid_price + spread / 2)

        # Adjust for inventory pressure
        bid_price, ask_price = self.handle_inventory_pressure(base_bid_price, base_ask_price)

        # Ensure bid < ask
        if bid_price >= ask_price:
            bid_price = self.round_to_tick(ask_price - TICK_SIZE)

        # Store the quotes
        self.past_quotes[timestamp] = (bid_price, ask_price)
        self.last_bid_price = bid_price
        self.last_ask_price = ask_price
        return bid_price, ask_price

def process_data(order_book_file, public_trades_file):
    """
    Loads and preprocesses the order book and public trades data.

    Args:
        order_book_file: Path to the order book CSV file.
        public_trades_file: Path to the public trades CSV file.

    Returns:
        Tuple of (order_book_df, public_trades_df), or (None, None) on error.
    """
    try:
        order_book_df = pd.read_csv(order_book_file).head(MAX_ROWS).copy()
        public_trades_df = pd.read_csv(public_trades_file).head(MAX_ROWS).copy()

        # Convert 'timestamp' to integer (assuming it's safe to do so)
        order_book_df['timestamp'] = order_book_df['timestamp'].astype(int)
        public_trades_df['timestamp'] = public_trades_df['timestamp'].astype(int)

        return order_book_df, public_trades_df
    except Exception as e:
        print(f"Error loading data: {e}")
        return None, None

def create_submission_file(submission_data, filename="submission.csv"):
    """
    Creates the submission CSV file.

    Args:
        submission_data: List of dictionaries, where each dict has
                         'timestamp', 'bid_price', and 'ask_price' keys.
        filename: The name of the CSV file to create.
    """
    submission_df = pd.DataFrame(submission_data)
    submission_df.to_csv(filename, index=False)
    print(f"Submission file created: {filename}")

def main():
    """Main function to run the market making simulation."""
    order_book_df, public_trades_df = process_data("orderbook_train.csv", "public_trades_train.csv")
    if order_book_df is None or public_trades_df is None:
        print("Failed to load data. Exiting.")
        return

    agent = AutomatedMarketMaking()
    submission_data = []
    current_inventory = 0
    fills = []  # List of fills as (timestamp, quantity, price)

    # Get all unique timestamps, handling potential missing timestamps.
    all_timestamps = sorted(list(set(order_book_df['timestamp'].unique()) | set(public_trades_df['timestamp'].unique())))

    for timestamp in all_timestamps:
        # Get data up to the current timestamp
        current_order_book = order_book_df[order_book_df['timestamp'] <= timestamp].copy()
        current_trades = public_trades_df[public_trades_df['timestamp'] <= timestamp].copy()

        # Call the strategy
        bid_price, ask_price = agent.strategy(timestamp, current_order_book, current_trades, current_inventory)

        # 1. Record the quote if generated.  Key change:  Record only if a new quote is generated
        if bid_price is not None and ask_price is not None:
            submission_data.append({'timestamp': timestamp, 'bid_price': bid_price, 'ask_price': ask_price})

        # 2. Simulate fills (simplified for demonstration).  This is where the logic gets complex.
        #    The *real* simulation happens on the exchange side.  Here, we *approximate* it
        #    to update inventory for the *next* strategy call.
        potential_fills = simulate_fills(timestamp, bid_price, ask_price, current_trades)
        for fill_timestamp, quantity, fill_price in potential_fills:
            current_inventory += quantity
            fills.append((fill_timestamp, quantity, fill_price))

        # 3. Enforce inventory constraint.
        if current_inventory > INVENTORY_LIMIT:
            print(f"Inventory Exceeded Limit at {timestamp}: {current_inventory}")
            current_inventory = INVENTORY_LIMIT
        elif current_inventory < -INVENTORY_LIMIT:
            print(f"Inventory Exceeded Limit at {timestamp}: {current_inventory}")
            current_inventory = -INVENTORY_LIMIT

    # Create submission file
    create_submission_file(submission_data)
    print("Final Inventory:", current_inventory)

def simulate_fills(timestamp, bid_price, ask_price, trades):
    """
    Simulates fills based on the provided quotes and trades.

    This is a simplified simulation.  A real exchange would have a matching engine
    with complex rules.  This function provides a *rough* approximation.

    Args:
        timestamp: The timestamp for which to simulate fills.
        bid_price: The current bid price.
        ask_price: The current ask price.
        trades: The DataFrame of trades up to (and including) the timestamp.

    Returns:
        A list of tuples: (timestamp, quantity, price), where quantity is positive
        for a buy (increase in inventory) and negative for a sell.
    """
    fills = []
    if bid_price is None or ask_price is None:
        return fills  # No quotes, no fills

    # 1. Get trades at the *next* timestamp.  We're filling against the quotes
    #    we posted at the *previous* timestamp.
    next_trades = trades[trades['timestamp'] == timestamp]

    for _, trade in next_trades.iterrows():
        trade_price = trade['price']
        trade_size = trade['size']
        trade_side = trade['side']

        if trade_side == 'buy' and trade_price <= bid_price:
            # Our bid was hit by a buyer
            fills.append((timestamp, -trade_size, bid_price))  # Sell at our bid
        elif trade_side == 'sell' and trade_price >= ask_price:
            # Our ask was hit by a seller
            fills.append((timestamp, trade_size, ask_price))  # Buy at our ask
            
    return fills

if __name__ == "__main__":
    main()
