// ============================================================
// BSJP SCREENER PRO — Enhanced Script
// ============================================================

const API_BASE = "http://localhost:5000"; // Flask backend

let stockData = []; // {symbol, data, score, status, inWatchlist}
let watchlist = JSON.parse(localStorage.getItem("bsjp_watchlist") || "[]");
let currentSymbol = "";
let currentTF = "D";
let activeFilter = "ALL";

// ===== INIT =====
document.addEventListener("DOMContentLoaded", () => {
  updateClock();
  setInterval(updateClock, 1000);
  updateMarketStatus();
  renderWatchlist();

  document.getElementById("sym").addEventListener("keydown", e => {
    if (e.key === "Enter") addStock();
  });
});

function updateClock() {
  const now = new Date();
  const wib = new Date(now.toLocaleString("en-US", { timeZone: "Asia/Jakarta" }));
  document.getElementById("clock").textContent =
    wib.toLocaleTimeString("id-ID", { hour: "2-digit", minute: "2-digit", second: "2-digit" }) + " WIB";
  updateMarketStatus(wib);
}

function updateMarketStatus(wib) {
  if (!wib) return;
  const day = wib.getDay(); // 0 = Sun, 6 = Sat
  const h = wib.getHours();
  const m = wib.getMinutes();
  const time = h * 100 + m;
  const el = document.getElementById("marketStatus");
  const dot = el.querySelector(".dot");

  if (day === 0 || day === 6) {
    el.innerHTML = '<span class="dot"></span> Market Tutup (Akhir Pekan)';
  } else if (time >= 900 && time < 1600) {
    dot.classList.add("open");
    el.innerHTML = '<span class="dot open"></span> Market Buka (09:00–16:00)';
  } else {
    el.innerHTML = '<span class="dot"></span> Market Tutup';
  }
}

// ===== ADD STOCK =====
async function addStock() {
  const sym = document.getElementById("sym").value.trim().toUpperCase();
  if (!sym) { showToast("⚠️ Masukkan kode saham terlebih dahulu!"); return; }
  if (stockData.find(d => d.symbol === sym)) {
    showToast(`⚠️ ${sym} sudah ada di tabel.`); return;
  }

  showLoading(`Mengambil data ${sym}...`);
  document.getElementById("sym").value = "";

  try {
    const res = await fetch(`${API_BASE}/stock/${sym}`);
    if (!res.ok) throw new Error("Emiten tidak ditemukan");
    const d = await res.json();
    if (d.error) throw new Error(d.error);

    const score = calcScore(d);
    const { status, cls, risk } = getStatus(score);
    const inWatchlist = watchlist.includes(sym);

    const entry = { symbol: sym, data: d, score, status, cls, risk, inWatchlist };
    stockData.push(entry);

    updateSummary();
    renderTable();
    showToast(`✅ ${sym} berhasil ditambahkan! Score: ${score}`);

    // Fetch backtest in background
    fetchBacktest(sym);

  } catch (err) {
    showToast(`❌ Error: ${err.message}`);
  } finally {
    hideLoading();
  }
}

function quickAdd(sym) {
  document.getElementById("sym").value = sym;
  addStock();
}

// ===== SCORING =====
function calcScore(d) {
  const trend = d.price > d.ma5;
  const momentum = ((d.high - d.price) / d.high) < 0.02;
  const vol_score = (d.volume / d.avg_volume) * 100;
  const candleStrong = d.body_ratio > 0.6;
  const gap = d.gap > 1;

  let score = 0;
  if (trend) score += 30;
  if (momentum) score += 30;
  if (vol_score > 130) score += 40;
  if (candleStrong) score += 20;
  if (gap) score += 20;
  return score;
}

function getStatus(score) {
  if (score >= 90) return { status: "STRONG", cls: "strong", risk: "LOW" };
  if (score >= 70) return { status: "VALID", cls: "valid", risk: "MEDIUM" };
  return { status: "SKIP", cls: "skip", risk: "HIGH" };
}

// ===== RENDER TABLE =====
function renderTable() {
  const tbody = document.getElementById("tableBody");
  const filtered = activeFilter === "ALL"
    ? stockData
    : stockData.filter(e => e.status === activeFilter);

  const sorted = sortData([...filtered]);

  if (sorted.length === 0) {
    tbody.innerHTML = `<tr class="empty-row"><td colspan="14"><div class="empty-state"><div class="empty-icon">📊</div><div>Tidak ada saham yang sesuai filter.</div></div></td></tr>`;
    return;
  }

  tbody.innerHTML = sorted.map(e => {
    const d = e.data;
    const tp = (d.price * 1.03).toFixed(0);
    const cl = (d.price * 0.97).toFixed(0);
    const volRatio = (d.volume / d.avg_volume * 100).toFixed(0);
    const volClass = volRatio > 130 ? "vol-hot" : volRatio > 80 ? "vol-warm" : "vol-cold";
    const riskClass = e.risk === "LOW" ? "risk-low" : e.risk === "MEDIUM" ? "risk-med" : "risk-high";
    const scoreColor = e.score >= 90 ? "#00e5a0" : e.score >= 70 ? "#f5c518" : "#ff4560";
    const fillPct = Math.min((e.score / 140) * 100, 100);
    const starClass = e.inWatchlist ? "btn-wl starred" : "btn-wl";
    const starIcon = e.inWatchlist ? "⭐" : "☆";

    return `
    <tr id="row-${e.symbol}">
      <td class="emiten-cell" onclick="showChart('${e.symbol}')">${e.symbol}</td>
      <td>${rupiah(d.price)}</td>
      <td>${rupiah(d.open)}</td>
      <td>${rupiah(d.high)}</td>
      <td>${rupiah(d.low)}</td>
      <td>${formatVol(d.volume)}</td>
      <td class="${volClass}">${volRatio}%</td>
      <td>${rupiah(d.ma5)}</td>
      <td>
        <div class="score-bar-wrap">
          <span class="score-num" style="color:${scoreColor}">${e.score}</span>
          <div class="score-bar">
            <div class="score-fill" style="width:${fillPct}%;background:${scoreColor}"></div>
          </div>
        </div>
      </td>
      <td><span class="badge badge-${e.cls}">${e.status}</span></td>
      <td class="${riskClass}">${e.risk}</td>
      <td style="color:var(--accent)">${rupiah(tp)}</td>
      <td style="color:var(--danger)">${rupiah(cl)}</td>
      <td>
        <button class="${starClass}" onclick="toggleWatchlist('${e.symbol}')" title="Watchlist">${starIcon}</button>
        <button class="btn-del" onclick="removeStock('${e.symbol}')" title="Hapus">🗑</button>
      </td>
    </tr>`;
  }).join("");
}

function sortData(arr) {
  const val = document.getElementById("sortSelect")?.value || "none";
  if (val === "score-desc") arr.sort((a, b) => b.score - a.score);
  else if (val === "score-asc") arr.sort((a, b) => a.score - b.score);
  else if (val === "price-desc") arr.sort((a, b) => b.data.price - a.data.price);
  else if (val === "price-asc") arr.sort((a, b) => a.data.price - b.data.price);
  return arr;
}

function sortTable() { renderTable(); }

// ===== UPDATE SUMMARY =====
function updateSummary() {
  const total = stockData.length;
  const strong = stockData.filter(e => e.status === "STRONG").length;
  const valid = stockData.filter(e => e.status === "VALID").length;
  const skip = stockData.filter(e => e.status === "SKIP").length;

  document.getElementById("totalCount").textContent = total;
  document.getElementById("strongCount").textContent = strong;
  document.getElementById("validCount").textContent = valid;
  document.getElementById("skipCount").textContent = skip;

  const show = total > 0;
  document.getElementById("summaryCards").style.display = show ? "grid" : "none";
  document.getElementById("filterBar").style.display = show ? "flex" : "none";
}

// ===== FILTER =====
function filterTable(filter, btn) {
  activeFilter = filter;
  document.querySelectorAll(".filter-btn").forEach(b => b.classList.remove("active"));
  if (btn) btn.classList.add("active");
  renderTable();
}

// ===== BACKTEST =====
async function fetchBacktest(sym) {
  try {
    const res = await fetch(`${API_BASE}/backtest/${sym}`);
    const b = await res.json();
    renderBacktestCard(b);
  } catch { }
}

function renderBacktestCard(b) {
  const existing = document.getElementById(`bt-${b.symbol}`);
  if (existing) return;

  const empty = document.querySelector(".bt-empty");
  if (empty) empty.remove();

  const wr = b.winrate;
  const wrClass = wr >= 60 ? "wr-high" : wr >= 40 ? "wr-med" : "wr-low";
  const fillColor = wr >= 60 ? "#00e5a0" : wr >= 40 ? "#f5c518" : "#ff4560";

  const card = document.createElement("div");
  card.className = "bt-card";
  card.id = `bt-${b.symbol}`;
  card.innerHTML = `
    <div class="bt-symbol">${b.symbol}</div>
    <div class="bt-stats">
      <div class="bt-stat">
        <div class="bt-stat-val ${wrClass}">${wr}%</div>
        <div class="bt-stat-lbl">Win Rate</div>
      </div>
      <div class="bt-stat">
        <div class="bt-stat-val">${b.signal_count}</div>
        <div class="bt-stat-lbl">Total Sinyal</div>
      </div>
      <div class="bt-stat">
        <div class="bt-stat-val" style="color:var(--accent2)">${Math.round(b.signal_count * wr / 100)}</div>
        <div class="bt-stat-lbl">Menang</div>
      </div>
    </div>
    <div class="winrate-bar">
      <div class="winrate-fill" style="width:${wr}%;background:${fillColor}"></div>
    </div>
  `;
  document.getElementById("backtestResults").appendChild(card);
}

// ===== WATCHLIST =====
function toggleWatchlist(sym) {
  const idx = watchlist.indexOf(sym);
  if (idx === -1) {
    watchlist.push(sym);
    showToast(`⭐ ${sym} ditambahkan ke watchlist`);
  } else {
    watchlist.splice(idx, 1);
    showToast(`🗑 ${sym} dihapus dari watchlist`);
  }
  localStorage.setItem("bsjp_watchlist", JSON.stringify(watchlist));

  // Update stockData entry
  const entry = stockData.find(e => e.symbol === sym);
  if (entry) entry.inWatchlist = watchlist.includes(sym);

  renderTable();
  renderWatchlist();
}

function renderWatchlist() {
  const grid = document.getElementById("watchlistGrid");
  document.getElementById("wlCount").textContent = watchlist.length + " saham";

  if (watchlist.length === 0) {
    grid.innerHTML = '<div class="wl-empty">Belum ada saham di watchlist. Klik ⭐ di tabel screener untuk menambahkan.</div>';
    return;
  }

  grid.innerHTML = watchlist.map(sym => {
    const entry = stockData.find(e => e.symbol === sym);
    const price = entry ? rupiah(entry.data.price) : "–";
    const status = entry ? `<span class="badge badge-${entry.cls}">${entry.status}</span>` : "";
    const score = entry ? `Score: ${entry.score}` : "Belum dianalisis";

    return `
    <div class="wl-card" onclick="showChart('${sym}')">
      <div class="wl-card-top">
        <div class="wl-symbol">${sym}</div>
        <div>${status}</div>
      </div>
      <div class="wl-price">${price}</div>
      <div class="wl-meta">
        <span>${score}</span>
        <span onclick="event.stopPropagation();toggleWatchlist('${sym}')" style="cursor:pointer;color:var(--danger)">Hapus ✕</span>
      </div>
    </div>`;
  }).join("");
}

// ===== REMOVE STOCK =====
function removeStock(sym) {
  stockData = stockData.filter(e => e.symbol !== sym);
  updateSummary();
  renderTable();
  const bt = document.getElementById(`bt-${sym}`);
  if (bt) bt.remove();
  if (document.getElementById("backtestResults").children.length === 0) {
    document.getElementById("backtestResults").innerHTML = '<div class="bt-empty">Tambahkan saham di Screener untuk melihat hasil backtest.</div>';
  }
  showToast(`🗑 ${sym} dihapus dari screener`);
}

// ===== CHART =====
function showChart(symbol) {
  currentSymbol = symbol;
  document.getElementById("chartTitle").textContent = symbol;
  document.getElementById("chartBox").style.display = "block";
  document.getElementById("chartBox").scrollIntoView({ behavior: "smooth" });
  renderChart(symbol, currentTF);
}

function renderChart(symbol, tf) {
  document.getElementById("tvchart").innerHTML = "";
  new TradingView.widget({
    symbol: "IDX:" + symbol,
    container_id: "tvchart",
    width: "100%",
    height: 450,
    interval: tf,
    theme: "dark",
    style: "1",
    locale: "id",
    allow_symbol_change: true,
    toolbar_bg: "#0b1521",
    hide_side_toolbar: false,
    withdateranges: true,
  });
}

function setTF(tf, btn) {
  currentTF = tf;
  document.querySelectorAll(".chart-tf").forEach(b => b.classList.remove("active"));
  btn.classList.add("active");
  if (currentSymbol) renderChart(currentSymbol, tf);
}

function closeChart() {
  document.getElementById("chartBox").style.display = "none";
  document.getElementById("tvchart").innerHTML = "";
  currentSymbol = "";
}

// ===== TABS =====
function switchTab(name, btn) {
  document.querySelectorAll(".tab-content").forEach(t => t.classList.remove("active"));
  document.querySelectorAll(".tab").forEach(b => b.classList.remove("active"));
  document.getElementById(`tab-${name}`).classList.add("active");
  if (btn) btn.classList.add("active");
}

// ===== CLEAR ALL =====
function clearAll() {
  if (!confirm("Hapus semua saham dari screener?")) return;
  stockData = [];
  updateSummary();
  renderTable();
  document.getElementById("backtestResults").innerHTML = '<div class="bt-empty">Tambahkan saham di Screener untuk melihat hasil backtest.</div>';
  closeChart();
  showToast("🗑 Semua saham dihapus");
}

// ===== EXPORT CSV =====
function exportCSV() {
  if (stockData.length === 0) { showToast("⚠️ Tidak ada data untuk diekspor."); return; }

  const header = ["Emiten","Harga","Open","High","Low","Volume","Avg Vol","MA5","Score","Status","Risk","TP","CL"].join(",");
  const rows = stockData.map(e => {
    const d = e.data;
    return [
      e.symbol, d.price, d.open, d.high, d.low, d.volume, d.avg_volume, d.ma5,
      e.score, e.status, e.risk,
      (d.price * 1.03).toFixed(0),
      (d.price * 0.97).toFixed(0)
    ].join(",");
  });

  const csv = [header, ...rows].join("\n");
  const blob = new Blob([csv], { type: "text/csv" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = `bsjp_screener_${new Date().toISOString().slice(0,10)}.csv`;
  a.click();
  URL.revokeObjectURL(url);
  showToast("✅ CSV berhasil diekspor!");
}

// ===== HELPERS =====
function rupiah(x) {
  const n = Math.round(Number(x));
  return "Rp " + n.toLocaleString("id-ID");
}

function formatVol(v) {
  if (v >= 1e9) return (v / 1e9).toFixed(1) + "M";
  if (v >= 1e6) return (v / 1e6).toFixed(1) + "jt";
  if (v >= 1e3) return (v / 1e3).toFixed(1) + "rb";
  return v;
}

function showToast(msg) {
  const t = document.getElementById("toast");
  t.textContent = msg;
  t.style.display = "block";
  setTimeout(() => { t.style.display = "none"; }, 3200);
}

function showLoading(msg = "Mengambil data...") {
  document.getElementById("loadingText").textContent = msg;
  document.getElementById("loading").style.display = "flex";
}

function hideLoading() {
  document.getElementById("loading").style.display = "none";
}