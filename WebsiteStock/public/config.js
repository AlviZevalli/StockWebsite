const RAILWAY_URL = "stockwebsite-production.up.railway.app";

const API_BASE = (window.location.hostname === "localhost" || window.location.hostname === "127.0.0.1")
  ? "http://localhost:5000"
  : RAILWAY_URL;