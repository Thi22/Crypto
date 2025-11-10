from fastapi import FastAPI
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import requests
import time
import threading

app = FastAPI()

# Cache local em memória
cache = {}
last_update = 0

# CORS liberado
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Servir arquivos estáticos
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=HTMLResponse)
async def root():
    return FileResponse("static/index.html")


@app.get("/api/price")
async def get_price(symbol: str = "BTCUSDT"):
    """Busca preço em tempo real da Binance (com cache de 2s)"""
    global cache, last_update
    now = time.time()

    # Se tiver cache recente, usa ele
    if symbol in cache and now - last_update < 2:
        return cache[symbol]

    try:
        url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}"
        r = requests.get(url, timeout=3)
        data = r.json()
        cache[symbol] = {
            "symbol": symbol,
            "price": float(data["price"]),
            "time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        }
        last_update = now
        return cache[symbol]
    except Exception as e:
        return {"error": str(e)}


@app.get("/api/candles")
async def get_candles(symbol: str = "BTCUSDT", interval: str = "1h"):
    """Histórico de candles"""
    url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval={interval}&limit=500"
    r = requests.get(url, timeout=5)
    data = r.json()
    candles = [
        {
            "time": c[0] // 1000,
            "open": float(c[1]),
            "high": float(c[2]),
            "low": float(c[3]),
            "close": float(c[4]),
            "volume": float(c[5])
        }
        for c in data
    ]
    return candles


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True)
