"""
Stock Visualization Module using Matplotlib
Provides comprehensive charting capabilities for stock analysis with technical indicators
"""

# type: ignore
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple
import warnings
warnings.filterwarnings('ignore')

# Set style for better-looking charts
plt.style.use('seaborn-v0_8')
plt.rcParams['figure.figsize'] = (15, 10)
plt.rcParams['font.size'] = 10


class StockVisualizer:
    """
    Class for creating comprehensive stock analysis charts using Matplotlib
    """
    
    def __init__(self, data: pd.DataFrame, symbol: str):
        """
        Initialize StockVisualizer with data and symbol
        
        Args:
            data (pd.DataFrame): DataFrame with stock data and technical indicators
            symbol (str): Stock symbol for chart titles
        """
        self.data = data
        self.symbol = symbol
        self.colors = {
            'price': '#1f77b4',
            'volume': '#ff7f0e',
            'sma_20': '#2ca02c',
            'sma_50': '#d62728',
            'ema_12': '#9467bd',
            'ema_26': '#8c564b',
            'bb_upper': '#e377c2',
            'bb_middle': '#7f7f7f',
            'bb_lower': '#e377c2',
            'support': '#00ff00',
            'resistance': '#ff0000',
            'macd': '#1f77b4',
            'macd_signal': '#ff7f0e',
            'macd_hist': '#2ca02c',
            'rsi': '#9467bd',
            'stoch_k': '#1f77b4',
            'stoch_d': '#ff7f0e'
        }
    
    def plot_comprehensive_chart(self, support_levels: List[float] = None, 
                                resistance_levels: List[float] = None,
                                save_path: Optional[str] = None) -> None:
        """
        Create a comprehensive chart with price, volume, and technical indicators
        
        Args:
            support_levels (List[float]): List of support levels to plot
            resistance_levels (List[float]): List of resistance levels to plot
            save_path (Optional[str]): Path to save the chart image
        """
        fig, axes = plt.subplots(4, 1, figsize=(16, 12), 
                                gridspec_kw={'height_ratios': [3, 1, 1, 1]})
        
        # Main price chart
        self._plot_price_chart(axes[0], support_levels, resistance_levels)
        
        # Volume chart
        self._plot_volume_chart(axes[1])
        
        # MACD chart
        self._plot_macd_chart(axes[2])
        
        # RSI chart
        self._plot_rsi_chart(axes[3])
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Chart saved to {save_path}")
        
        plt.show()
    
    def _plot_price_chart(self, ax, support_levels: List[float] = None, 
                          resistance_levels: List[float] = None) -> None:
        """Plot the main price chart with indicators"""
        # Plot candlestick-like data (using OHLC)
        dates = self.data.index
        
        # Plot price line
        ax.plot(dates, self.data['Close'], color=self.colors['price'], 
                linewidth=1.5, label='Close Price', alpha=0.8)
        
        # Plot moving averages
        if 'SMA_20' in self.data.columns:
            ax.plot(dates, self.data['SMA_20'], color=self.colors['sma_20'], 
                    linewidth=1, label='SMA 20', alpha=0.7)
        
        if 'SMA_50' in self.data.columns:
            ax.plot(dates, self.data['SMA_50'], color=self.colors['sma_50'], 
                    linewidth=1, label='SMA 50', alpha=0.7)
        
        # Plot Bollinger Bands
        if all(col in self.data.columns for col in ['BB_Upper', 'BB_Middle', 'BB_Lower']):
            ax.plot(dates, self.data['BB_Upper'], color=self.colors['bb_upper'], 
                    linewidth=0.8, label='BB Upper', alpha=0.6, linestyle='--')
            ax.plot(dates, self.data['BB_Middle'], color=self.colors['bb_middle'], 
                    linewidth=0.8, label='BB Middle', alpha=0.6, linestyle='--')
            ax.plot(dates, self.data['BB_Lower'], color=self.colors['bb_lower'], 
                    linewidth=0.8, label='BB Lower', alpha=0.6, linestyle='--')
            
            # Fill Bollinger Bands
            ax.fill_between(dates, self.data['BB_Upper'], self.data['BB_Lower'], 
                           alpha=0.1, color=self.colors['bb_upper'])
        
        # Plot support and resistance levels
        if support_levels:
            for level in support_levels:
                ax.axhline(y=level, color=self.colors['support'], linestyle='-', 
                          alpha=0.7, linewidth=1, label='Support' if level == support_levels[0] else "")
        
        if resistance_levels:
            for level in resistance_levels:
                ax.axhline(y=level, color=self.colors['resistance'], linestyle='-', 
                          alpha=0.7, linewidth=1, label='Resistance' if level == resistance_levels[0] else "")
        
        ax.set_title(f'{self.symbol} Stock Analysis - Price Chart', fontsize=14, fontweight='bold')
        ax.set_ylabel('Price ($)', fontsize=12)
        ax.legend(loc='upper left', fontsize=10)
        ax.grid(True, alpha=0.3)
        
        # Format x-axis
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        ax.xaxis.set_major_locator(mdates.MonthLocator(interval=2))
        plt.setp(ax.xaxis.get_majorticklabels(), rotation=45)
    
    def plot_price_chart(self, support_levels: List[float] = None, 
                        resistance_levels: List[float] = None,
                        save_path: Optional[str] = None) -> None:
        """Plot standalone price chart with indicators"""
        fig, ax = plt.subplots(figsize=(15, 8))
        
        # Plot price line
        dates = self.data.index
        ax.plot(dates, self.data['Close'], color=self.colors['price'], 
                linewidth=2, label='Close Price')
        
        # Plot moving averages
        if 'SMA_20' in self.data.columns:
            ax.plot(dates, self.data['SMA_20'], color=self.colors['sma_20'], 
                    linewidth=1.5, label='SMA 20')
        
        if 'SMA_50' in self.data.columns:
            ax.plot(dates, self.data['SMA_50'], color=self.colors['sma_50'], 
                    linewidth=1.5, label='SMA 50')
        
        # Plot Bollinger Bands
        if all(col in self.data.columns for col in ['BB_Upper', 'BB_Middle', 'BB_Lower']):
            ax.plot(dates, self.data['BB_Upper'], color=self.colors['bb_upper'], 
                    linewidth=1, label='BB Upper', linestyle='--', alpha=0.7)
            ax.plot(dates, self.data['BB_Middle'], color=self.colors['bb_middle'], 
                    linewidth=1, label='BB Middle', linestyle='--', alpha=0.7)
            ax.plot(dates, self.data['BB_Lower'], color=self.colors['bb_lower'], 
                    linewidth=1, label='BB Lower', linestyle='--', alpha=0.7)
            
            # Fill Bollinger Bands
            ax.fill_between(dates, self.data['BB_Upper'], self.data['BB_Lower'], 
                           alpha=0.1, color=self.colors['bb_upper'])
        
        # Plot support and resistance levels
        if support_levels:
            for level in support_levels:
                ax.axhline(y=level, color=self.colors['support'], linestyle='-', 
                          alpha=0.8, linewidth=2, label='Support' if level == support_levels[0] else "")
        
        if resistance_levels:
            for level in resistance_levels:
                ax.axhline(y=level, color=self.colors['resistance'], linestyle='-', 
                          alpha=0.8, linewidth=2, label='Resistance' if level == resistance_levels[0] else "")
        
        ax.set_title(f'{self.symbol} - Price Chart with Indicators', fontsize=16, fontweight='bold')
        ax.set_ylabel('Price ($)', fontsize=12)
        ax.set_xlabel('Date', fontsize=12)
        ax.legend(loc='upper left', fontsize=10)
        ax.grid(True, alpha=0.3)
        
        # Format x-axis
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        ax.xaxis.set_major_locator(mdates.MonthLocator(interval=1))
        plt.setp(ax.xaxis.get_majorticklabels(), rotation=45)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Price chart saved to {save_path}")
        
        plt.show()
    
    def _plot_volume_chart(self, ax) -> None:
        """Plot volume chart"""
        dates = self.data.index
        
        # Plot volume bars
        ax.bar(dates, self.data['Volume'], color=self.colors['volume'], 
               alpha=0.7, width=0.8)
        
        ax.set_title('Volume', fontsize=12, fontweight='bold')
        ax.set_ylabel('Volume', fontsize=10)
        ax.grid(True, alpha=0.3)
        
        # Format x-axis
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        ax.xaxis.set_major_locator(mdates.MonthLocator(interval=2))
        plt.setp(ax.xaxis.get_majorticklabels(), rotation=45)
    
    def plot_volume_chart(self, save_path: Optional[str] = None) -> None:
        """Plot standalone volume chart"""
        fig, ax = plt.subplots(figsize=(15, 8))
        
        dates = self.data.index
        
        # Plot volume bars
        ax.bar(dates, self.data['Volume'], color=self.colors['volume'], 
               alpha=0.7, width=0.8)
        
        ax.set_title(f'{self.symbol} - Volume Chart', fontsize=16, fontweight='bold')
        ax.set_ylabel('Volume', fontsize=12)
        ax.set_xlabel('Date', fontsize=12)
        ax.grid(True, alpha=0.3)
        
        # Format x-axis
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        ax.xaxis.set_major_locator(mdates.MonthLocator(interval=1))
        plt.setp(ax.xaxis.get_majorticklabels(), rotation=45)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Volume chart saved to {save_path}")
        
        plt.show()
    
    def _plot_macd_chart(self, ax) -> None:
        """Plot MACD chart"""
        if not all(col in self.data.columns for col in ['MACD', 'MACD_Signal', 'MACD_Hist']):
            ax.text(0.5, 0.5, 'MACD data not available', ha='center', va='center', 
                   transform=ax.transAxes)
            return
        
        dates = self.data.index
        
        # Plot MACD lines
        ax.plot(dates, self.data['MACD'], color=self.colors['macd'], 
                linewidth=1, label='MACD')
        ax.plot(dates, self.data['MACD_Signal'], color=self.colors['macd_signal'], 
                linewidth=1, label='Signal')
        
        # Plot MACD histogram
        colors = ['green' if x >= 0 else 'red' for x in self.data['MACD_Hist']]
        ax.bar(dates, self.data['MACD_Hist'], color=colors, alpha=0.6, width=0.8)
        
        # Add zero line
        ax.axhline(y=0, color='black', linestyle='-', alpha=0.5, linewidth=0.5)
        
        ax.set_title('MACD', fontsize=12, fontweight='bold')
        ax.set_ylabel('MACD', fontsize=10)
        ax.legend(loc='upper left', fontsize=8)
        ax.grid(True, alpha=0.3)
        
        # Format x-axis
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        ax.xaxis.set_major_locator(mdates.MonthLocator(interval=2))
        plt.setp(ax.xaxis.get_majorticklabels(), rotation=45)
    
    def plot_macd_chart(self, save_path: Optional[str] = None) -> None:
        """Plot standalone MACD chart"""
        fig, ax = plt.subplots(figsize=(15, 8))
        
        if not all(col in self.data.columns for col in ['MACD', 'MACD_Signal', 'MACD_Hist']):
            ax.text(0.5, 0.5, 'MACD data not available', ha='center', va='center', 
                   transform=ax.transAxes, fontsize=14)
            ax.set_title(f'{self.symbol} - MACD Chart', fontsize=16, fontweight='bold')
            plt.tight_layout()
            if save_path:
                plt.savefig(save_path, dpi=300, bbox_inches='tight')
                print(f"MACD chart saved to {save_path}")
            plt.show()
            return
        
        dates = self.data.index
        
        # Plot MACD lines
        ax.plot(dates, self.data['MACD'], color=self.colors['macd'], 
                linewidth=2, label='MACD')
        ax.plot(dates, self.data['MACD_Signal'], color=self.colors['macd_signal'], 
                linewidth=2, label='Signal')
        
        # Plot MACD histogram
        colors = ['green' if x >= 0 else 'red' for x in self.data['MACD_Hist']]
        ax.bar(dates, self.data['MACD_Hist'], color=colors, alpha=0.6, width=0.8)
        
        # Add zero line
        ax.axhline(y=0, color='black', linestyle='-', alpha=0.5, linewidth=0.5)
        
        ax.set_title(f'{self.symbol} - MACD Chart', fontsize=16, fontweight='bold')
        ax.set_ylabel('MACD', fontsize=12)
        ax.set_xlabel('Date', fontsize=12)
        ax.legend(loc='upper left', fontsize=10)
        ax.grid(True, alpha=0.3)
        
        # Format x-axis
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        ax.xaxis.set_major_locator(mdates.MonthLocator(interval=1))
        plt.setp(ax.xaxis.get_majorticklabels(), rotation=45)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"MACD chart saved to {save_path}")
        
        plt.show()
    
    def _plot_rsi_chart(self, ax) -> None:
        """Plot RSI chart"""
        if 'RSI' not in self.data.columns:
            ax.text(0.5, 0.5, 'RSI data not available', ha='center', va='center', 
                   transform=ax.transAxes)
            return
        
        dates = self.data.index
        
        # Plot RSI line
        ax.plot(dates, self.data['RSI'], color=self.colors['rsi'], 
                linewidth=1.5, label='RSI')
        
        # Add overbought and oversold lines
        ax.axhline(y=70, color='red', linestyle='--', alpha=0.7, linewidth=1, label='Overbought')
        ax.axhline(y=30, color='green', linestyle='--', alpha=0.7, linewidth=1, label='Oversold')
        ax.axhline(y=50, color='gray', linestyle='-', alpha=0.5, linewidth=0.5)
        
        ax.set_title('RSI (14)', fontsize=12, fontweight='bold')
        ax.set_ylabel('RSI', fontsize=10)
        ax.set_ylim(0, 100)
        ax.legend(loc='upper left', fontsize=8)
        ax.grid(True, alpha=0.3)
        
        # Format x-axis
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        ax.xaxis.set_major_locator(mdates.MonthLocator(interval=2))
        plt.setp(ax.xaxis.get_majorticklabels(), rotation=45)
    
    def plot_rsi_chart(self, save_path: Optional[str] = None) -> None:
        """Plot standalone RSI chart"""
        fig, ax = plt.subplots(figsize=(15, 8))
        
        if 'RSI' not in self.data.columns:
            ax.text(0.5, 0.5, 'RSI data not available', ha='center', va='center', 
                   transform=ax.transAxes, fontsize=14)
            ax.set_title(f'{self.symbol} - RSI Chart', fontsize=16, fontweight='bold')
            plt.tight_layout()
            if save_path:
                plt.savefig(save_path, dpi=300, bbox_inches='tight')
                print(f"RSI chart saved to {save_path}")
            plt.show()
            return
        
        dates = self.data.index
        
        # Plot RSI line
        ax.plot(dates, self.data['RSI'], color=self.colors['rsi'], 
                linewidth=2, label='RSI')
        
        # Add overbought and oversold lines
        ax.axhline(y=70, color='red', linestyle='--', alpha=0.7, linewidth=2, label='Overbought')
        ax.axhline(y=30, color='green', linestyle='--', alpha=0.7, linewidth=2, label='Oversold')
        ax.axhline(y=50, color='gray', linestyle='-', alpha=0.5, linewidth=1)
        
        ax.set_title(f'{self.symbol} - RSI Chart', fontsize=16, fontweight='bold')
        ax.set_ylabel('RSI', fontsize=12)
        ax.set_xlabel('Date', fontsize=12)
        ax.set_ylim(0, 100)
        ax.legend(loc='upper left', fontsize=10)
        ax.grid(True, alpha=0.3)
        
        # Format x-axis
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        ax.xaxis.set_major_locator(mdates.MonthLocator(interval=1))
        plt.setp(ax.xaxis.get_majorticklabels(), rotation=45)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"RSI chart saved to {save_path}")
        
        plt.show()
    
    def plot_support_resistance_chart(self, support_levels: List[float],
                                    resistance_levels: List[float],
                                    save_path: Optional[str] = None) -> None:
        """
        Create a focused chart showing support and resistance levels
        
        Args:
            support_levels (List[float]): List of support levels
            resistance_levels (List[float]): List of resistance levels
            save_path (Optional[str]): Path to save the chart image
        """
        fig, ax = plt.subplots(figsize=(15, 8))
        
        dates = self.data.index
        
        # Plot price
        ax.plot(dates, self.data['Close'], color=self.colors['price'], 
                linewidth=2, label='Close Price')
        
        # Plot support levels
        for i, level in enumerate(support_levels):
            ax.axhline(y=level, color=self.colors['support'], linestyle='-', 
                      alpha=0.8, linewidth=2, 
                      label=f'Support ${level:.2f}' if i == 0 else "")
        
        # Plot resistance levels
        for i, level in enumerate(resistance_levels):
            ax.axhline(y=level, color=self.colors['resistance'], linestyle='-', 
                      alpha=0.8, linewidth=2, 
                      label=f'Resistance ${level:.2f}' if i == 0 else "")
        
        # Add current price annotation
        current_price = self.data['Close'].iloc[-1]
        ax.axhline(y=current_price, color='orange', linestyle='--', 
                  alpha=0.8, linewidth=2, label=f'Current Price ${current_price:.2f}')
        
        ax.set_title(f'{self.symbol} - Support & Resistance Levels', 
                    fontsize=16, fontweight='bold')
        ax.set_ylabel('Price ($)', fontsize=12)
        ax.set_xlabel('Date', fontsize=12)
        ax.legend(loc='upper left', fontsize=10)
        ax.grid(True, alpha=0.3)
        
        # Format x-axis
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        ax.xaxis.set_major_locator(mdates.MonthLocator(interval=1))
        plt.setp(ax.xaxis.get_majorticklabels(), rotation=45)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Support/Resistance chart saved to {save_path}")
        
        plt.show()
    
    def plot_trend_analysis(self, save_path: Optional[str] = None) -> None:
        """
        Create a chart focusing on trend analysis with moving averages
        
        Args:
            save_path (Optional[str]): Path to save the chart image
        """
        fig, ax = plt.subplots(figsize=(15, 8))
        
        dates = self.data.index
        
        # Plot price
        ax.plot(dates, self.data['Close'], color=self.colors['price'], 
                linewidth=2, label='Close Price')
        
        # Plot moving averages
        if 'SMA_20' in self.data.columns:
            ax.plot(dates, self.data['SMA_20'], color=self.colors['sma_20'], 
                    linewidth=2, label='SMA 20')
        
        if 'SMA_50' in self.data.columns:
            ax.plot(dates, self.data['SMA_50'], color=self.colors['sma_50'], 
                    linewidth=2, label='SMA 50')
        
        if 'EMA_12' in self.data.columns:
            ax.plot(dates, self.data['EMA_12'], color=self.colors['ema_12'], 
                    linewidth=1.5, label='EMA 12', alpha=0.8)
        
        if 'EMA_26' in self.data.columns:
            ax.plot(dates, self.data['EMA_26'], color=self.colors['ema_26'], 
                    linewidth=1.5, label='EMA 26', alpha=0.8)
        
        ax.set_title(f'{self.symbol} - Trend Analysis', fontsize=16, fontweight='bold')
        ax.set_ylabel('Price ($)', fontsize=12)
        ax.set_xlabel('Date', fontsize=12)
        ax.legend(loc='upper left', fontsize=10)
        ax.grid(True, alpha=0.3)
        
        # Format x-axis
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        ax.xaxis.set_major_locator(mdates.MonthLocator(interval=1))
        plt.setp(ax.xaxis.get_majorticklabels(), rotation=45)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Trend analysis chart saved to {save_path}")
        
        plt.show()


def create_stock_charts(analyzer, data_with_indicators, levels, 
                       save_charts: bool = False, output_dir: str = "charts") -> None:
    """
    Convenience function to create all stock charts
    
    Args:
        analyzer: StockAnalyzer object
        data_with_indicators: DataFrame with technical indicators
        levels: Dictionary with support and resistance levels
        save_charts (bool): Whether to save charts to files
        output_dir (str): Directory to save charts
    """
    import os
    
    if save_charts and not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    visualizer = StockVisualizer(data_with_indicators, analyzer.symbol)
    
    # Create comprehensive chart
    comprehensive_path = os.path.join(output_dir, f"{analyzer.symbol}_comprehensive.png") if save_charts else None
    visualizer.plot_comprehensive_chart(
        support_levels=levels['support'],
        resistance_levels=levels['resistance'],
        save_path=comprehensive_path
    )
    
    # Create support/resistance chart
    sr_path = os.path.join(output_dir, f"{analyzer.symbol}_support_resistance.png") if save_charts else None
    visualizer.plot_support_resistance_chart(
        support_levels=levels['support'],
        resistance_levels=levels['resistance'],
        save_path=sr_path
    )
    
    # Create trend analysis chart
    trend_path = os.path.join(output_dir, f"{analyzer.symbol}_trend_analysis.png") if save_charts else None
    visualizer.plot_trend_analysis(save_path=trend_path)


if __name__ == "__main__":
    # Example usage
    from stock_analyzer import analyze_stock
    
    try:
        analyzer, data, levels = analyze_stock("AAPL", "1y")
        create_stock_charts(analyzer, data, levels, save_charts=True)
    except Exception as e:
        print(f"Error creating charts: {e}")
