"""
Main Stock Analysis Application
Provides a user-friendly interface for analyzing stocks with TA-Lib and visualization
"""

import sys
import os
from typing import Optional
import argparse

from stock_analyzer import StockAnalyzer, analyze_stock
from stock_visualizer import StockVisualizer, create_stock_charts


def print_banner():
    """Print application banner"""
    print("=" * 60)
    print("           STOCK ANALYSIS WITH TA-LIB")
    print("=" * 60)
    print("Technical Analysis Library for Stock Market Analysis")
    print("Features: Support/Resistance, Moving Averages, RSI, MACD, Bollinger Bands")
    print("=" * 60)


def print_stock_summary(analyzer: StockAnalyzer, levels: dict):
    """Print a comprehensive stock summary"""
    print(f"\n📊 {analyzer.symbol} STOCK ANALYSIS")
    print("=" * 50)
    
    # Current price and basic info
    current_price = analyzer.get_current_price()
    summary = analyzer.get_price_summary()
    
    print(f"💰 Current Price: ${current_price:.2f}")
    print(f"📈 52-Week High: ${summary['high_52w']:.2f}")
    print(f"📉 52-Week Low: ${summary['low_52w']:.2f}")
    
    if summary['price_change_1d'] != 0:
        change_symbol = "📈" if summary['price_change_1d'] > 0 else "📉"
        print(f"{change_symbol} 1-Day Change: ${summary['price_change_1d']:.2f} ({summary['price_change_pct_1d']:.2f}%)")
    
    # Trend analysis
    trend_analysis = analyzer.get_trend_analysis()
    print(f"\n🎯 TREND ANALYSIS:")
    print(f"   Trend: {trend_analysis['trend']}")
    print(f"   RSI: {trend_analysis['rsi']:.1f} ({trend_analysis['rsi_signal']})")
    print(f"   MACD: {trend_analysis['macd_signal']}")
    print(f"   SMA 20: ${trend_analysis['sma_20']:.2f}")
    print(f"   SMA 50: ${trend_analysis['sma_50']:.2f}")
    
    # Support and resistance levels
    print(f"\n🛡️  SUPPORT LEVELS:")
    for i, level in enumerate(levels['support'][:5], 1):
        distance = ((current_price - level) / current_price) * 100
        print(f"   {i}. ${level:.2f} ({distance:+.1f}% from current)")
    
    print(f"\n🚧 RESISTANCE LEVELS:")
    for i, level in enumerate(levels['resistance'][:5], 1):
        distance = ((level - current_price) / current_price) * 100
        print(f"   {i}. ${level:.2f} ({distance:+.1f}% from current)")


def interactive_mode():
    """Run the application in interactive mode"""
    print_banner()
    
    while True:
        print("\n" + "=" * 60)
        print("INTERACTIVE STOCK ANALYSIS")
        print("=" * 60)
        
        # Get user input
        symbol = input("Enter stock symbol (or 'quit' to exit): ").strip().upper()
        if symbol.lower() in ['quit', 'exit', 'q']:
            print("Goodbye! 👋")
            break
        
        if not symbol:
            print("❌ Please enter a valid stock symbol")
            continue
        
        # Get time period
        print("\nSelect time period:")
        print("1. 1 Month (1mo)")
        print("2. 3 Months (3mo)")
        print("3. 6 Months (6mo)")
        print("4. 1 Year (1y) - Default")
        print("5. 2 Years (2y)")
        print("6. 5 Years (5y)")
        
        period_choice = input("Enter choice (1-6) or press Enter for default: ").strip()
        
        period_map = {
            '1': '1mo', '2': '3mo', '3': '6mo', 
            '4': '1y', '5': '2y', '6': '5y'
        }
        period = period_map.get(period_choice, '1y')
        
        try:
            print(f"\n🔍 Analyzing {symbol} for the past {period}...")
            
            # Analyze stock
            analyzer, data_with_indicators, levels = analyze_stock(symbol, period)
            
            # Print summary
            print_stock_summary(analyzer, levels)
            
            # Explain chart differences
            print(f"\n📋 CHART EXPLANATION:")
            print("• Comprehensive Chart: 4-in-1 view (Price, Volume, MACD, RSI)")
            print("• Support/Resistance: Focused price chart with key levels")
            print("• Trend Analysis: Price chart with moving averages")
            print("• Show All: Displays all 3 chart types separately")
            print("• Save All: Creates 3 PNG files in 'charts' folder")
            
            # Ask about charts
            print(f"\n📊 CHART OPTIONS:")
            print("1. Comprehensive Chart (Price + Volume + MACD + RSI in one view)")
            print("2. Support/Resistance Chart (Price with key levels)")
            print("3. Trend Analysis Chart (Price with moving averages)")
            print("4. Show All Charts (Comprehensive + Support/Resistance + Trend)")
            print("5. Save All Charts to Files (3 separate PNG files)")
            print("6. Skip charts")
            
            chart_choice = input("Enter choice (1-6): ").strip()
            
            if chart_choice in ['1', '2', '3', '4', '5']:
                visualizer = StockVisualizer(data_with_indicators, symbol)
                
                if chart_choice == '1':
                    visualizer.plot_comprehensive_chart(
                        support_levels=levels['support'],
                        resistance_levels=levels['resistance']
                    )
                elif chart_choice == '2':
                    visualizer.plot_support_resistance_chart(
                        support_levels=levels['support'],
                        resistance_levels=levels['resistance']
                    )
                elif chart_choice == '3':
                    visualizer.plot_trend_analysis()
                elif chart_choice in ['4', '5']:
                    save_charts = chart_choice == '5'
                    create_stock_charts(analyzer, data_with_indicators, levels, 
                                      save_charts=save_charts)
            
            # Ask if user wants to analyze another stock
            another = input(f"\nAnalyze another stock? (y/n): ").strip().lower()
            if another not in ['y', 'yes']:
                print("Goodbye! 👋")
                break
                
        except Exception as e:
            print(f"❌ Error analyzing {symbol}: {e}")
            print("Please check the symbol and try again.")


def analyze_single_stock(symbol: str, period: str = "1y", save_charts: bool = False, chart_type: Optional[str] = None):
    """Analyze a single stock with optional chart saving and specific chart type"""
    try:
        print(f"🔍 Analyzing {symbol} for the past {period}...")
        
        # Analyze stock
        analyzer, data_with_indicators, levels = analyze_stock(symbol, period)
        
        # Print summary
        print_stock_summary(analyzer, levels)
        
        # Create charts based on user preference
        if chart_type:
            print(f"\n📊 Displaying {chart_type} chart...")
            visualizer = StockVisualizer(data_with_indicators, symbol)
            
            # Create charts directory if saving
            if save_charts:
                import os
                if not os.path.exists("charts"):
                    os.makedirs("charts")
                save_path = os.path.join("charts", f"{symbol}_{chart_type}.png")
            else:
                save_path = None
            
            if chart_type == 'price':
                visualizer.plot_price_chart(support_levels=levels['support'], resistance_levels=levels['resistance'], save_path=save_path)
            elif chart_type == 'volume':
                visualizer.plot_volume_chart(save_path=save_path)
            elif chart_type == 'macd':
                visualizer.plot_macd_chart(save_path=save_path)
            elif chart_type == 'rsi':
                visualizer.plot_rsi_chart(save_path=save_path)
            elif chart_type == 'support_resistance':
                visualizer.plot_support_resistance_chart(levels['support'], levels['resistance'], save_path=save_path)
            elif chart_type == 'trend':
                visualizer.plot_trend_analysis(save_path=save_path)
        elif save_charts:
            print(f"\n💾 Saving charts to 'charts' directory...")
            create_stock_charts(analyzer, data_with_indicators, levels, save_charts=True)
        else:
            print(f"\n📊 Displaying all charts...")
            create_stock_charts(analyzer, data_with_indicators, levels, save_charts=False)
            
    except Exception as e:
        print(f"❌ Error analyzing {symbol}: {e}")
        sys.exit(1)


def main():
    """Main function with command line argument parsing"""
    parser = argparse.ArgumentParser(
        description="Stock Analysis with TA-Lib - Technical Analysis for Stocks",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py                    # Interactive mode
  python main.py AAPL              # Analyze AAPL with default settings
  python main.py AAPL --chart price  # Show only price chart
  python main.py AAPL --chart volume  # Show only volume chart
  python main.py AAPL --chart macd  # Show only MACD chart
  python main.py AAPL --chart rsi  # Show only RSI chart
  python main.py AAPL --period 6mo --save-charts  # Analyze AAPL for 6 months and save charts
  python main.py MSFT --period 2y  # Analyze MSFT for 2 years
        """
    )
    
    parser.add_argument('symbol', nargs='?', help='Stock symbol to analyze (e.g., AAPL)')
    parser.add_argument('--period', '-p', default='1y', 
                       choices=['1mo', '3mo', '6mo', '1y', '2y', '5y'],
                       help='Time period for analysis (default: 1y)')
    parser.add_argument('--save-charts', '-s', action='store_true',
                       help='Save charts to files instead of displaying them')
    parser.add_argument('--chart', '-c', choices=['price', 'volume', 'macd', 'rsi', 'support_resistance', 'trend'],
                       help='Display specific chart type (price, volume, macd, rsi, support_resistance, trend)')
    parser.add_argument('--interactive', '-i', action='store_true',
                       help='Run in interactive mode')
    
    args = parser.parse_args()  # Parse command line arguments
    
    # Check if running in interactive mode or no symbol provided
    if args.interactive or not args.symbol:
        interactive_mode()
    else:
        analyze_single_stock(args.symbol, args.period, args.save_charts, args.chart)


if __name__ == "__main__":
    main()
