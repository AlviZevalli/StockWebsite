// Ganti URL ini dengan URL Railway kamu setelah deploy
// Contoh: "https://stockwebsite-production.up.railway.app"
const RAILWAY_URL = "GANTI_DENGAN_URL_RAILWAY_KAMU";

const API_BASE = (window.location.hostname === "localhost" || window.location.hostname === "127.0.0.1")
  ? "http://localhost:5000"
  : RAILWAY_URL;