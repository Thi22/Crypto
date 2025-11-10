const chart = LightweightCharts.createChart(document.getElementById('chart'), {
    layout: { background: { color: '#0d1117' }, textColor: '#d1d4dc' },
    grid: { vertLines: { color: '#1f2937' }, horzLines: { color: '#1f2937' } },
    timeScale: { borderColor: '#485c7b', timeVisible: true, secondsVisible: false },
    crosshair: { mode: LightweightCharts.CrosshairMode.Normal }
});
const candleSeries = chart.addCandlestickSeries();

let symbol = 'BTCUSDT';
let interval = '1h';

// Atualiza relógio
setInterval(() => {
    const now = new Date();
    document.getElementById('clock').textContent =
        now.toLocaleString('pt-BR', { timeZone: 'America/Sao_Paulo' });
}, 1000);

// Atualiza candles
async function loadCandles() {
    const res = await fetch(`/api/candles?symbol=${symbol}&interval=${interval}`);
    const data = await res.json();
    candleSeries.setData(data.map(c => ({
        time: c.time,
        open: c.open,
        high: c.high,
        low: c.low,
        close: c.close,
    })));
}

// Atualiza preço em tempo real
async function updatePrice() {
    const res = await fetch(`/api/price?symbol=${symbol}`);
    const data = await res.json();
    if (!data.price) return;
    document.getElementById('info').textContent =
        `${symbol} = ${data.price.toFixed(2)} USD (${data.time})`;
    candleSeries.update({
        time: Math.floor(Date.now() / 1000),
        open: data.price,
        high: data.price,
        low: data.price,
        close: data.price,
    });
}

document.querySelectorAll('button').forEach(btn => {
    btn.addEventListener('click', () => {
        interval = btn.dataset.interval;
        loadCandles();
    });
});

document.getElementById('symbol').addEventListener('change', e => {
    symbol = e.target.value;
    loadCandles();
});

loadCandles();
setInterval(updatePrice, 2000);
