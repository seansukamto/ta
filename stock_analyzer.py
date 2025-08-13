"""
Stock Analysis Module using TA-Lib
Provides technical analysis functions for stock data including support/resistance levels
"""

import yfinance as yf
import pandas as pd
import numpy as np
import talib
from typing import Tuple, List, Dict, Optional
import warnings
warnings.filterwarnings('ignore')


class StockAnalyzer:
    """
    Main class for stock analysis using TA-Lib
    Provides methods for technical indicators and support/resistance detection
    """
    
    def __init__(self, symbol: str, period: str = "1y"):
        """
        Initialize StockAnalyzer with symbol and time period
        
        Args:
            symbol (str): Stock symbol (e.g., 'AAPL')
            period (str): Time period for data ('1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max')
        """
        self.symbol = symbol.upper()
        self.period = period
        self.data = None
        self._fetch_data()
    
    def _fetch_data(self) -> None:
        """Fetch stock data using yfinance"""
        try:
            ticker = yf.Ticker(self.symbol)
            self.data = ticker.history(period=self.period)
            if self.data.empty:
                raise ValueError(f"No data found for symbol {self.symbol}")
            print(f"Successfully fetched {len(self.data)} days of data for {self.symbol}")
        except Exception as e:
            print(f"Error fetching data for {self.symbol}: {e}")
            raise
    
    def calculate_technical_indicators(self) -> pd.DataFrame:
        """
        Calculate various technical indicators using TA-Lib
        
        Returns:
            pd.DataFrame: DataFrame with original data and technical indicators
        """
        if self.data is None or self.data.empty:
            raise ValueError("No data available. Please fetch data first.")
        
        df = self.data.copy()
        
        # Moving Averages
        df['SMA_20'] = talib.SMA(df['Close'], timeperiod=20)
        df['SMA_50'] = talib.SMA(df['Close'], timeperiod=50)
        df['EMA_12'] = talib.EMA(df['Close'], timeperiod=12)
        df['EMA_26'] = talib.EMA(df['Close'], timeperiod=26)
        
        # MACD
        df['MACD'], df['MACD_Signal'], df['MACD_Hist'] = talib.MACD(
            df['Close'], fastperiod=12, slowperiod=26, signalperiod=9
        )
        
        # RSI
        df['RSI'] = talib.RSI(df['Close'], timeperiod=14)
        
        # Bollinger Bands
        df['BB_Upper'], df['BB_Middle'], df['BB_Lower'] = talib.BBANDS(
            df['Close'], timeperiod=20, nbdevup=2, nbdevdn=2, matype=0
        )
        
        # Stochastic
        df['STOCH_K'], df['STOCH_D'] = talib.STOCH(
            df['High'], df['Low'], df['Close'], 
            fastk_period=14, slowk_period=3, slowd_period=3
        )
        
        # Volume indicators
        df['OBV'] = talib.OBV(df['Close'], df['Volume'])
        
        # ATR (Average True Range) for volatility
        df['ATR'] = talib.ATR(df['High'], df['Low'], df['Close'], timeperiod=14)
        
        return df
    
    def find_support_resistance_levels(self, window: int = 20, threshold: float = 0.02) -> Dict[str, List[float]]:
        """
        Find support and resistance levels using local minima and maxima
        
        Args:
            window (int): Window size for finding local extrema
            threshold (float): Minimum price difference threshold for levels
            
        Returns:
            Dict[str, List[float]]: Dictionary with 'support' and 'resistance' levels
        """
        if self.data is None or self.data.empty:
            raise ValueError("No data available. Please fetch data first.")
        
        df = self.data.copy()
        
        # Find local minima (support) and maxima (resistance)
        support_levels = []
        resistance_levels = []
        
        for i in range(window, len(df) - window):
            # Check for local minimum (support)
            if all(df['Low'].iloc[i] <= df['Low'].iloc[i-j] for j in range(1, window+1)) and \
               all(df['Low'].iloc[i] <= df['Low'].iloc[i+j] for j in range(1, window+1)):
                support_levels.append(df['Low'].iloc[i])
            
            # Check for local maximum (resistance)
            if all(df['High'].iloc[i] >= df['High'].iloc[i-j] for j in range(1, window+1)) and \
               all(df['High'].iloc[i] >= df['High'].iloc[i+j] for j in range(1, window+1)):
                resistance_levels.append(df['High'].iloc[i])
        
        # Filter levels based on threshold to avoid duplicates
        def filter_levels(levels: List[float], threshold: float) -> List[float]:
            if not levels:
                return []
            
            filtered = [levels[0]]
            for level in levels[1:]:
                if all(abs(level - existing) > threshold * existing for existing in filtered):
                    filtered.append(level)
            return sorted(filtered)
        
        support_levels = filter_levels(support_levels, threshold)
        resistance_levels = filter_levels(resistance_levels, threshold)
        
        return {
            'support': support_levels,
            'resistance': resistance_levels
        }
    
    def get_current_price(self) -> float:
        """Get the current stock price"""
        if self.data is None or self.data.empty:
            raise ValueError("No data available. Please fetch data first.")
        return self.data['Close'].iloc[-1]
    
    def get_price_summary(self) -> Dict[str, float]:
        """Get a summary of current price statistics"""
        if self.data is None or self.data.empty:
            raise ValueError("No data available. Please fetch data first.")
        
        return {
            'current_price': self.data['Close'].iloc[-1],
            'high_52w': self.data['High'].max(),
            'low_52w': self.data['Low'].min(),
            'avg_volume': self.data['Volume'].mean(),
            'price_change_1d': self.data['Close'].iloc[-1] - self.data['Close'].iloc[-2] if len(self.data) > 1 else 0,
            'price_change_pct_1d': ((self.data['Close'].iloc[-1] - self.data['Close'].iloc[-2]) / self.data['Close'].iloc[-2] * 100) if len(self.data) > 1 else 0
        }
    
    def get_trend_analysis(self) -> Dict[str, str]:
        """
        Analyze current trend based on moving averages and price action
        
        Returns:
            Dict[str, str]: Dictionary with trend analysis results
        """
        if self.data is None or self.data.empty:
            raise ValueError("No data available. Please fetch data first.")
        
        df = self.calculate_technical_indicators()
        current_price = df['Close'].iloc[-1]
        
        # Trend analysis
        sma_20 = df['SMA_20'].iloc[-1]
        sma_50 = df['SMA_50'].iloc[-1]
        ema_12 = df['EMA_12'].iloc[-1]
        ema_26 = df['EMA_26'].iloc[-1]
        rsi = df['RSI'].iloc[-1]
        
        # Determine trend
        if current_price > sma_20 > sma_50:
            trend = "Strong Uptrend"
        elif current_price > sma_20 and sma_20 < sma_50:
            trend = "Weak Uptrend"
        elif current_price < sma_20 < sma_50:
            trend = "Strong Downtrend"
        elif current_price < sma_20 and sma_20 > sma_50:
            trend = "Weak Downtrend"
        else:
            trend = "Sideways"
        
        # RSI analysis
        if rsi > 70:
            rsi_signal = "Overbought"
        elif rsi < 30:
            rsi_signal = "Oversold"
        else:
            rsi_signal = "Neutral"
        
        # MACD analysis
        macd = df['MACD'].iloc[-1]
        macd_signal = df['MACD_Signal'].iloc[-1]
        if macd > macd_signal:
            macd_signal_text = "Bullish"
        else:
            macd_signal_text = "Bearish"
        
        return {
            'trend': trend,
            'rsi_signal': rsi_signal,
            'macd_signal': macd_signal_text,
            'current_price': current_price,
            'sma_20': sma_20,
            'sma_50': sma_50,
            'rsi': rsi
        }


def analyze_stock(symbol: str, period: str = "1y") -> Tuple[StockAnalyzer, pd.DataFrame, Dict]:
    """
    Convenience function to analyze a stock and return all relevant data
    
    Args:
        symbol (str): Stock symbol
        period (str): Time period for analysis
        
    Returns:
        Tuple[StockAnalyzer, pd.DataFrame, Dict]: Analyzer object, data with indicators, and levels
    """
    analyzer = StockAnalyzer(symbol, period)
    data_with_indicators = analyzer.calculate_technical_indicators()
    levels = analyzer.find_support_resistance_levels()
    
    return analyzer, data_with_indicators, levels


if __name__ == "__main__":
    # Example usage for AAPL
    try:
        analyzer, data, levels = analyze_stock("AAPL", "1y")
        
        print(f"\n=== {analyzer.symbol} Analysis ===")
        print(f"Current Price: ${analyzer.get_current_price():.2f}")
        
        summary = analyzer.get_price_summary()
        print(f"52-Week High: ${summary['high_52w']:.2f}")
        print(f"52-Week Low: ${summary['low_52w']:.2f}")
        print(f"1-Day Change: ${summary['price_change_1d']:.2f} ({summary['price_change_pct_1d']:.2f}%)")
        
        trend_analysis = analyzer.get_trend_analysis()
        print(f"\nTrend Analysis:")
        print(f"Trend: {trend_analysis['trend']}")
        print(f"RSI Signal: {trend_analysis['rsi_signal']} (RSI: {trend_analysis['rsi']:.1f})")
        print(f"MACD Signal: {trend_analysis['macd_signal']}")
        
        print(f"\nSupport Levels: {[f'${level:.2f}' for level in levels['support'][:5]]}")
        print(f"Resistance Levels: {[f'${level:.2f}' for level in levels['resistance'][:5]]}")
        
    except Exception as e:
        print(f"Error analyzing stock: {e}")
