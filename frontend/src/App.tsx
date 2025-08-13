import { useMemo, useState } from 'react'
import './App.css'

type ChartType = 'comprehensive' | 'support_resistance' | 'trend' | 'price' | 'volume' | 'macd' | 'rsi'

type AnalyzeResponse = {
	symbol: string
	period: string
	summary: Record<string, any>
	levels: { support: number[]; resistance: number[] }
	series: {
		close: (number | null)[]
		sma20: (number | null)[]
		sma50: (number | null)[]
		bbUpper: (number | null)[]
		bbLower: (number | null)[]
		volume: (number | null)[]
		macd: (number | null)[]
		macdSignal: (number | null)[]
		macdHist: (number | null)[]
		rsi: (number | null)[]
	}
	dates: string[]
}

const periods = ['1mo','3mo','6mo','1y','2y','5y'] as const

async function analyze(symbol: string, period: string): Promise<AnalyzeResponse> {
	const res = await fetch('/api/analyze', {
		method: 'POST',
		headers: { 'Content-Type': 'application/json' },
		body: JSON.stringify({ symbol, period })
	})
	if (!res.ok) throw new Error(await res.text())
	return res.json()
}

function App() {
  const [symbol, setSymbol] = useState('AAPL')
  const [period, setPeriod] = useState<(typeof periods)[number]>('1y')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [data, setData] = useState<AnalyzeResponse | null>(null)
  const [selectedChart, setSelectedChart] = useState<ChartType>('comprehensive')
  const [downloading, setDownloading] = useState(false)

  const handleAnalyze = async () => {
    setLoading(true)
    setError(null)
    try {
      const out = await analyze(symbol.trim().toUpperCase(), period)
      setData(out)
    } catch (e: any) {
      setError(e?.message ?? 'Request failed')
    } finally {
      setLoading(false)
    }
  }

  const handleDownloadChart = async (chartType: ChartType) => {
    setDownloading(true)
    try {
      const url = `http://localhost:8001/api/chart?symbol=${encodeURIComponent(data!.symbol)}&period=${encodeURIComponent(data!.period)}&type=${chartType}`
      
      // Fetch the image data
      const response = await fetch(url)
      if (!response.ok) {
        throw new Error('Failed to fetch chart image')
      }
      
      // Convert to blob
      const blob = await response.blob()
      
      // Create blob URL
      const blobUrl = window.URL.createObjectURL(blob)
      
      // Create download link
      const link = document.createElement('a')
      link.href = blobUrl
      link.download = `${data!.symbol}_${chartType}_${data!.period}.png`
      
      // Trigger download
      document.body.appendChild(link)
      link.click()
      document.body.removeChild(link)
      
      // Clean up blob URL
      window.URL.revokeObjectURL(blobUrl)
    } catch (error) {
      console.error('Download failed:', error)
      alert('Failed to download chart. Please try again.')
    } finally {
      setDownloading(false)
    }
  }

  const latest = useMemo(() => {
    if (!data) return null
    return {
      price: data.summary.current_price as number,
      high: data.summary.high_52w as number,
      low: data.summary.low_52w as number,
      change: data.summary.price_change_1d as number,
      changePct: data.summary.price_change_pct_1d as number,
      trend: data.summary.trend as string,
      rsi: data.summary.rsi as number,
      rsiSignal: data.summary.rsi_signal as string,
      macdSignal: data.summary.macd_signal as string,
      sma20: data.summary.sma_20 as number,
      sma50: data.summary.sma_50 as number,
    }
  }, [data])

  return (
    <div className="min-h-screen bg-slate-50 text-slate-900">
      <header className="border-b bg-white/70 backdrop-blur sticky top-0 z-10">
        <div className="max-w-6xl mx-auto px-4 py-4 flex items-center justify-between">
          <h1 className="text-xl md:text-2xl font-semibold">Stock Analyzer</h1>
          <div className="flex gap-2">
            <a className="text-sm text-slate-500 hover:text-slate-700" href="https://fastapi.tiangolo.com/" target="_blank" rel="noreferrer">FastAPI</a>
            <a className="text-sm text-slate-500 hover:text-slate-700" href="https://react.dev/" target="_blank" rel="noreferrer">React</a>
            <a className="text-sm text-slate-500 hover:text-slate-700" href="https://tailwindcss.com/" target="_blank" rel="noreferrer">Tailwind</a>
          </div>
        </div>
      </header>

      <main className="max-w-6xl mx-auto px-4 py-8">
        <section className="bg-white rounded-xl shadow-sm border p-4 md:p-6">
          <div className="flex flex-col md:flex-row gap-3 md:items-end">
            <div className="flex-1">
              <label className="block text-sm font-medium mb-1">Symbol</label>
              <input value={symbol} onChange={e => setSymbol(e.target.value)} placeholder="AAPL" className="w-full rounded-lg border px-3 py-2 focus:outline-none focus:ring-2 focus:ring-slate-300" />
            </div>
            <div>
              <label className="block text-sm font-medium mb-1">Period</label>
              <select value={period} onChange={e => setPeriod(e.target.value as any)} className="rounded-lg border px-3 py-2 focus:outline-none focus:ring-2 focus:ring-slate-300">
                {periods.map(p => <option key={p} value={p}>{p}</option>)}
              </select>
            </div>
            <button onClick={handleAnalyze} disabled={loading} className="rounded-lg bg-slate-900 text-white px-4 py-2 hover:bg-slate-800 disabled:opacity-50">
              {loading ? 'Analyzing…' : 'Analyze'}
            </button>
          </div>

          {error && (
            <div className="mt-4 text-sm text-red-600">{error}</div>
          )}
        </section>

        {data && latest && (
          <>
            <section className="mt-6 grid grid-cols-1 md:grid-cols-3 gap-4">
              <div className="bg-white rounded-xl border p-4">
                <div className="text-sm text-slate-500">Current Price</div>
                <div className="text-2xl font-semibold">${latest.price?.toFixed(2)}</div>
                <div className={`text-sm ${latest.change >= 0 ? 'text-emerald-600' : 'text-rose-600'}`}>{latest.change >= 0 ? '+' : ''}{latest.change?.toFixed(2)} ({latest.changePct?.toFixed(2)}%)</div>
              </div>
              <div className="bg-white rounded-xl border p-4">
                <div className="text-sm text-slate-500">52W Range</div>
                <div className="text-2xl font-semibold">${latest.low?.toFixed(2)} – ${latest.high?.toFixed(2)}</div>
              </div>
              <div className="bg-white rounded-xl border p-4">
                <div className="text-sm text-slate-500">Trend</div>
                <div className="text-2xl font-semibold">{latest.trend}</div>
                <div className="text-sm text-slate-500">RSI {latest.rsi?.toFixed(1)} ({latest.rsiSignal}) • MACD {latest.macdSignal}</div>
              </div>
            </section>

            <section className="mt-6 grid grid-cols-1 lg:grid-cols-3 gap-4">
              <div className="bg-white rounded-xl border p-4 lg:col-span-2">
                <div className="flex items-center justify-between mb-3">
                  <h2 className="font-medium">Charts</h2>
                  <div className="text-xs text-slate-500">Rendered by server using Matplotlib</div>
                </div>
                <div className="flex flex-wrap gap-2 mb-3">
                  {(['comprehensive','support_resistance','trend','price','volume','macd','rsi'] as ChartType[]).map(t => (
                    <button
                      key={t}
                      onClick={() => setSelectedChart(t)}
                      className={`text-xs px-2 py-1 rounded border transition-colors ${
                        selectedChart === t 
                          ? 'bg-slate-900 text-white border-slate-900' 
                          : 'hover:bg-slate-50'
                      }`}
                    >
                      {t}
                    </button>
                  ))}
                </div>
                <div className="relative">
                  <img
                    src={`http://localhost:8001/api/chart?symbol=${encodeURIComponent(data.symbol)}&period=${encodeURIComponent(data.period)}&type=${selectedChart}`}
                    alt={`${selectedChart} Chart`}
                    className="w-full rounded-lg border"
                  />
                  <button
                    onClick={() => handleDownloadChart(selectedChart)}
                    disabled={downloading}
                    className="absolute top-2 right-2 bg-slate-900 text-white text-xs px-2 py-1 rounded hover:bg-slate-800 transition-colors disabled:opacity-50"
                  >
                    {downloading ? 'Downloading...' : 'Download'}
                  </button>
                </div>
              </div>

              <div className="bg-white rounded-xl border p-4">
                <h2 className="font-medium mb-3">Levels</h2>
                <div className="text-sm">
                  <div className="font-medium text-slate-700 mb-1">Support</div>
                  <ul className="list-disc list-inside text-slate-600 space-y-0.5">
                    {data.levels.support.slice(0,5).map((s, i) => (
                      <li key={i}>${s.toFixed(2)}</li>
                    ))}
                  </ul>
                  <div className="font-medium text-slate-700 mt-3 mb-1">Resistance</div>
                  <ul className="list-disc list-inside text-slate-600 space-y-0.5">
                    {data.levels.resistance.slice(0,5).map((r, i) => (
                      <li key={i}>${r.toFixed(2)}</li>
                    ))}
                  </ul>
                </div>
              </div>
            </section>
          </>
        )}
      </main>
    </div>
  )
}

export default App
