from __future__ import annotations

"""
FastAPI backend for Stock Analysis
Exposes endpoints to analyze a stock using existing `stock_analyzer` module
and returns clean JSON suitable for a React frontend.
"""

import os
import sys
import io
from typing import Any, Dict, List, Optional
import tempfile

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field


# Ensure project root is on sys.path so we can import stock_analyzer
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

try:
    # Ensure matplotlib runs headless for server-side rendering
    os.environ.setdefault("MPLBACKEND", "Agg")
    from stock_analyzer import analyze_stock, StockAnalyzer
    from stock_visualizer import StockVisualizer
except Exception as import_exc:  # pragma: no cover
    raise RuntimeError(
        "Failed to import stock_analyzer. Ensure the backend is run from project root or PYTHONPATH is set."
    ) from import_exc


class AnalyzeRequest(BaseModel):
    symbol: str = Field(..., description="Ticker symbol, e.g. AAPL")
    period: str = Field(
        "1y",
        description="yfinance period: 1mo, 3mo, 6mo, 1y, 2y, 5y, etc.",
    )


class AnalyzeResponse(BaseModel):
    symbol: str
    period: str
    summary: Dict[str, Any]
    levels: Dict[str, List[float]]
    series: Dict[str, List[Optional[float]]]
    dates: List[str]


app = FastAPI(title="Stock Analysis API", version="1.0.0")

# CORS for local dev (Vite default port 5173)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health() -> Dict[str, str]:
    return {"status": "ok"}


# Alias to satisfy clients expecting /api/health
@app.get("/api/health")
def api_health() -> Dict[str, str]:
    return {"status": "ok"}


def _series_to_list(values) -> List[Optional[float]]:
    # Convert pandas series to JSON-serializable list with None for NaN
    result: List[Optional[float]] = []
    for v in values:
        if v is None:
            result.append(None)
        else:
            try:
                if hasattr(v, "__float__"):
                    f = float(v)  # type: ignore
                    if f != f:  # NaN check
                        result.append(None)
                    else:
                        result.append(f)
                else:
                    result.append(None)
            except Exception:
                result.append(None)
    return result


@app.post("/api/analyze", response_model=AnalyzeResponse)
def analyze(req: AnalyzeRequest) -> AnalyzeResponse:
    symbol = req.symbol.strip().upper()
    if not symbol:
        raise HTTPException(status_code=400, detail="Symbol is required")

    try:
        analyzer, data_with_indicators, levels = analyze_stock(symbol, req.period)
        trend = analyzer.get_trend_analysis()
        summary = analyzer.get_price_summary()

        # Merge key trend metrics into summary for convenience
        summary_out: Dict[str, Any] = {
            **summary,
            "trend": trend.get("trend"),
            "rsi": trend.get("rsi"),
            "rsi_signal": trend.get("rsi_signal"),
            "macd_signal": trend.get("macd_signal"),
            "sma_20": trend.get("sma_20"),
            "sma_50": trend.get("sma_50"),
        }

        # Prepare timeseries for charts
        index = data_with_indicators.index
        dates = [
            (i.isoformat() if hasattr(i, "isoformat") else str(i)) for i in index
        ]

        def get(col: str) -> List[Optional[float]]:
            return _series_to_list(data_with_indicators[col]) if col in data_with_indicators.columns else []

        series = {
            "close": get("Close"),
            "sma20": get("SMA_20"),
            "sma50": get("SMA_50"),
            "bbUpper": get("BB_Upper"),
            "bbLower": get("BB_Lower"),
            "volume": get("Volume"),
            "macd": get("MACD"),
            "macdSignal": get("MACD_Signal"),
            "macdHist": get("MACD_Hist"),
            "rsi": get("RSI"),
        }

        return AnalyzeResponse(
            symbol=symbol,
            period=req.period,
            summary=summary_out,
            levels=levels,
            series=series,
            dates=dates,
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/chart")
def chart(symbol: str, period: str = "1y", type: str = "comprehensive"):
    """
    Generate a chart image using StockVisualizer and return it as PNG.
    Types: comprehensive | support_resistance | trend | price | volume | macd | rsi
    """
    symbol = symbol.strip().upper()
    if not symbol:
        raise HTTPException(status_code=400, detail="Symbol is required")

    try:
        analyzer, data_with_indicators, levels = analyze_stock(symbol, period)
        visualizer = StockVisualizer(data_with_indicators, symbol)

        chart_type = type.lower()
        # Use a temporary PNG file to leverage existing save_path logic
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
            tmp_path = tmp.name

        if chart_type == "comprehensive":
            visualizer.plot_comprehensive_chart(
                support_levels=levels.get("support", []),
                resistance_levels=levels.get("resistance", []),
                save_path=tmp_path,
            )
        elif chart_type in ("support_resistance", "sr", "levels"):
            visualizer.plot_support_resistance_chart(
                support_levels=levels.get("support", []),
                resistance_levels=levels.get("resistance", []),
                save_path=tmp_path,
            )
        elif chart_type == "trend":
            visualizer.plot_trend_analysis(save_path=tmp_path)
        elif chart_type == "price":
            visualizer.plot_price_chart(
                support_levels=levels.get("support", []),
                resistance_levels=levels.get("resistance", []),
                save_path=tmp_path,
            )
        elif chart_type == "volume":
            visualizer.plot_volume_chart(save_path=tmp_path)
        elif chart_type == "macd":
            visualizer.plot_macd_chart(save_path=tmp_path)
        elif chart_type == "rsi":
            visualizer.plot_rsi_chart(save_path=tmp_path)
        else:
            raise HTTPException(status_code=400, detail="Unknown chart type")

        # Read image bytes and return
        with open(tmp_path, "rb") as f:
            data = f.read()
        try:
            os.remove(tmp_path)
        except OSError:
            pass

        return StreamingResponse(io.BytesIO(data), media_type="image/png")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# For local running: `uvicorn backend.main:app --reload`
if __name__ == "__main__":
    import uvicorn

    uvicorn.run("backend.main:app", host="0.0.0.0", port=8001, reload=True)

