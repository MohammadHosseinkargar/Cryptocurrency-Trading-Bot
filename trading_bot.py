import ccxt
import pandas as pd
import time

API_KEY = 'your_api_key_here'
API_SECRET = 'your_api_secret_here'

exchange = ccxt.binance({
    'apiKey': API_KEY,
    'secret': API_SECRET,
})

def fetch_ohlcv(symbol, timeframe='1h', limit=100):
    """Fetch OHLCV data for a given symbol and timeframe."""
    return exchange.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit)

def sma(data, period):
    """Calculate Simple Moving Average (SMA)."""
    return data['close'].rolling(window=period).mean()

def rsi(data, period=14):
    """Calculate Relative Strength Index (RSI)."""
    delta = data['close'].diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()
    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))

def check_buy_sell_signals(data):
    """Check for buy and sell signals based on SMA and RSI."""
    data['SMA50'] = sma(data, 50)
    data['RSI'] = rsi(data)

    latest = data.iloc[-1]
    
    if latest['RSI'] < 30 and latest['close'] > latest['SMA50']:
        return 'buy'
    elif latest['RSI'] > 70 and latest['close'] < latest['SMA50']:
        return 'sell'
    else:
        return 'hold'

def execute_trade(symbol, signal):
    """Execute buy or sell trade based on signal."""
    if signal == 'buy':
        print(f"Buying {symbol}")
        # Add your buy order logic here
    elif signal == 'sell':
        print(f"Selling {symbol}")
        # Add your sell order logic here

def main():
    symbol = 'BTC/USDT'
    while True:
        ohlcv = fetch_ohlcv(symbol)
        data = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        data['timestamp'] = pd.to_datetime(data['timestamp'], unit='ms')
        
        signal = check_buy_sell_signals(data)
        execute_trade(symbol, signal)
        
        time.sleep(3600)  # Run the bot every hour

if __name__ == "__main__":
    main()
