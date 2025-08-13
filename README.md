# Stock Analysis with TA-Lib

A comprehensive Python application for technical stock analysis using TA-Lib, yfinance, and Matplotlib. This project provides advanced technical indicators, support/resistance level detection, and beautiful visualizations for stock market analysis.


## ⚠️ Disclaimer ⚠️

This software is for educational and research purposes only. It is not intended to provide financial advice. Always do your own research and consult with financial professionals before making investment decisions.


## 🚀 Getting Started with GitHub

### Setting up the Repository

1. **Clone the repository**:

   ```bash
   git clone <your-repo-url>
   cd TA-Lib
   ```

2. **Create a virtual environment** (recommended):

   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   # source .venv/bin/activate  # Mac/Linux
   ```

3. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**:
   ```bash
   python main.py AAPL --chart price
   ```


## 🚀 Features

### Technical Indicators

- **Moving Averages**: SMA (20, 50), EMA (12, 26)
- **MACD**: Moving Average Convergence Divergence with signal line and histogram
- **RSI**: Relative Strength Index (14-period)
- **Bollinger Bands**: Upper, middle, and lower bands
- **Stochastic Oscillator**: %K and %D lines
- **Volume Indicators**: On-Balance Volume (OBV)
- **Volatility**: Average True Range (ATR)

### Support & Resistance Analysis

- Automatic detection of support and resistance levels
- Local minima/maxima analysis with configurable thresholds
- Distance calculations from current price
- Visual representation on charts

### Visualization

- **Comprehensive Charts**: 4-in-1 view with price, volume, MACD, and RSI subplots
- **Individual Charts**: Standalone charts for specific indicators (price, volume, macd, rsi, support_resistance, trend)
- **Support/Resistance Charts**: Focused view of key levels with price action
- **Trend Analysis Charts**: Moving averages and trend identification
- **Professional Styling**: Clean, modern chart design
- **Export Capability**: Save charts as high-resolution PNG files

### User Interface

- **Interactive Mode**: User-friendly command-line interface
- **Command Line**: Direct analysis with command-line arguments
- **Individual Chart Selection**: Choose specific chart types (price, volume, macd, rsi, support_resistance, trend)
- **Flexible Time Periods**: 1mo, 3mo, 6mo, 1y, 2y, 5y
- **Error Handling**: Robust error handling and user feedback

## 📦 Installation

### Prerequisites

- Python 3.7 or higher
- TA-Lib (requires system-level installation)

### Install TA-Lib

#### Windows

```bash
# Download and install TA-Lib from: https://www.lfd.uci.edu/~gohlke/pythonlibs/#ta-lib
# Or use conda:
conda install -c conda-forge ta-lib
```

#### macOS

```bash
# Using Homebrew
brew install ta-lib
pip install TA-Lib

# Or using conda:
conda install -c conda-forge ta-lib
```

#### Linux (Ubuntu/Debian)

```bash
sudo apt-get install ta-lib
pip install TA-Lib
```

### Install Python Dependencies

```bash
pip install -r requirements.txt
```

## 🎯 Quick Start

### Interactive Mode (Recommended)

```bash
python main.py
```

### Analyze a Specific Stock

```bash
# Analyze AAPL with default settings (1 year)
python main.py AAPL

# Analyze MSFT for 6 months
python main.py MSFT --period 6mo

# Analyze TSLA and save charts to files
python main.py TSLA --period 1y --save-charts

# Show only price chart for AAPL
python main.py AAPL --chart price

# Show only RSI chart for MSFT and save it
python main.py MSFT --chart rsi --save-charts

# Show only MACD chart for TSLA for 3 months
python main.py TSLA --period 3mo --chart macd
```

### Command Line Options

```bash
python main.py [SYMBOL] [OPTIONS]

Options:
  --period, -p          Time period (1mo, 3mo, 6mo, 1y, 2y, 5y) [default: 1y]
  --chart, -c           Chart type (price, volume, macd, rsi, support_resistance, trend)
  --save-charts, -s     Save charts to files instead of displaying
  --interactive, -i     Run in interactive mode
  --help, -h           Show help message
```

### Available Chart Types

- **price**: Price chart with moving averages, Bollinger Bands, and support/resistance levels
- **volume**: Trading volume analysis
- **macd**: MACD momentum indicator with signal line and histogram
- **rsi**: RSI overbought/oversold analysis with 30/70 levels
- **support_resistance**: Focused view of key support and resistance levels
- **trend**: Trend analysis with multiple moving averages

## 📊 Example Output

### Stock Analysis Summary

```
📊 AAPL STOCK ANALYSIS
==================================================
💰 Current Price: $175.43
📈 52-Week High: $198.23
📉 52-Week Low: $124.17
📈 1-Day Change: $2.15 (+1.24%)

🎯 TREND ANALYSIS:
   Trend: Strong Uptrend
   RSI: 65.2 (Neutral)
   MACD: Bullish
   SMA 20: $172.45
   SMA 50: $168.92

🛡️  SUPPORT LEVELS:
   1. $170.25 (-3.0% from current)
   2. $165.80 (-5.5% from current)
   3. $160.15 (-8.7% from current)

🚧 RESISTANCE LEVELS:
   1. $180.50 (+2.9% from current)
   2. $185.75 (+5.9% from current)
   3. $190.20 (+8.4% from current)
```

## 🏗️ Project Structure

```
TA-Lib/
├── main.py                 # Main application entry point
├── stock_analyzer.py       # Core analysis functionality
├── stock_visualizer.py     # Chart creation and visualization
├── requirements.txt        # Python dependencies
├── .gitignore             # Git ignore file for version control
├── README.md              # This file
└── charts/                # Generated chart images (if saved)
```

## 🔧 Usage Examples

### Basic Analysis

```python
from stock_analyzer import analyze_stock

# Analyze AAPL
analyzer, data, levels = analyze_stock("AAPL", "1y")

# Get current price
current_price = analyzer.get_current_price()
print(f"AAPL current price: ${current_price:.2f}")

# Get trend analysis
trend = analyzer.get_trend_analysis()
print(f"Trend: {trend['trend']}")
```

### Custom Analysis

```python
from stock_analyzer import StockAnalyzer
from stock_visualizer import StockVisualizer

# Create analyzer
analyzer = StockAnalyzer("MSFT", "6mo")

# Calculate indicators
data = analyzer.calculate_technical_indicators()

# Find support/resistance
levels = analyzer.find_support_resistance_levels(window=15, threshold=0.03)

# Create visualizer
visualizer = StockVisualizer(data, "MSFT")

# Plot individual charts
visualizer.plot_price_chart(support_levels=levels['support'], resistance_levels=levels['resistance'])
visualizer.plot_macd_chart()
visualizer.plot_rsi_chart()

# Or plot comprehensive chart
visualizer.plot_comprehensive_chart(
    support_levels=levels['support'],
    resistance_levels=levels['resistance']
)
```

### Batch Analysis

```python
symbols = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA"]

for symbol in symbols:
    try:
        analyzer, data, levels = analyze_stock(symbol, "1y")
        print(f"{symbol}: ${analyzer.get_current_price():.2f}")
    except Exception as e:
        print(f"Error analyzing {symbol}: {e}")
```

## 📈 Technical Indicators Explained

### Moving Averages

- **SMA (Simple Moving Average)**: Average of closing prices over a period
- **EMA (Exponential Moving Average)**: Weighted average giving more importance to recent prices

### MACD

- **MACD Line**: Difference between 12-day and 26-day EMAs
- **Signal Line**: 9-day EMA of MACD line
- **Histogram**: Difference between MACD and signal lines

### RSI (Relative Strength Index)

- Measures momentum on a scale of 0 to 100
- Above 70: Overbought (potential sell signal)
- Below 30: Oversold (potential buy signal)

### Bollinger Bands

- **Upper Band**: 20-day SMA + (2 × standard deviation)
- **Lower Band**: 20-day SMA - (2 × standard deviation)
- **Middle Band**: 20-day SMA

### Support & Resistance

- **Support**: Price level where stock tends to stop falling
- **Resistance**: Price level where stock tends to stop rising
- Detected using local minima/maxima analysis

## 🛠️ Customization

### Adjusting Support/Resistance Detection

```python
# More sensitive detection (smaller window, lower threshold)
levels = analyzer.find_support_resistance_levels(window=10, threshold=0.01)

# Less sensitive detection (larger window, higher threshold)
levels = analyzer.find_support_resistance_levels(window=30, threshold=0.05)
```

### Custom Time Periods

```python
# Available periods: '1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max'
analyzer = StockAnalyzer("AAPL", "2y")
```

### Custom Chart Styling

```python
# Modify colors in stock_visualizer.py
self.colors = {
    'price': '#your_color',
    'support': '#your_color',
    'resistance': '#your_color',
    # ... other colors
}
```

## 🐛 Troubleshooting

### TA-Lib Installation Issues

- **Windows**: Download pre-compiled wheel from https://www.lfd.uci.edu/~gohlke/pythonlibs/#ta-lib
- **macOS**: Use `conda install -c conda-forge ta-lib` instead of pip
- **Linux**: Install system dependencies first: `sudo apt-get install ta-lib`

### Data Fetching Issues

- Check internet connection
- Verify stock symbol is correct
- Some symbols may require different formats (e.g., "BRK-A" vs "BRK.A")

### Chart Display Issues

- Ensure matplotlib backend is properly configured
- For headless servers, use `--save-charts` option
- Check if display environment is available
- If charts don't display, use `--save-charts` to save them as files

### Import Issues

- If you get "Import matplotlib.pyplot could not be resolved" errors in your IDE, this is usually an IDE configuration issue
- The code will still run correctly - try selecting the correct Python interpreter in your IDE settings
- Add `# type: ignore` above matplotlib imports if needed

## 📝 License

This project is open source and available under the MIT License.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.


### Version Control

The project includes a `.gitignore` file that excludes:

- Virtual environment directories (`.venv/`)
- Python cache files (`__pycache__/`)
- Generated chart images (`charts/`)
- IDE and OS-specific files


---

**Happy Trading! 📈📉**
