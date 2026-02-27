# Cukong Reborn — IDX Stock Analysis Platform

Platform analisis saham IDX berbasis teknikal.

## Struktur
```
├── api/
│   └── app.py          # Flask backend (semua endpoint)
├── public/
│   ├── index.html      # Homepage
│   ├── screener.html   # BSJP Screener
│   ├── sr.html         # S&R Finder
│   ├── volume.html     # Volume Anomaly
│   ├── scanner.html    # Market Scanner
│   ├── script.js
│   └── style.css
├── vercel.json
└── requirements.txt
```

## Deploy ke Vercel
1. Push ke GitHub
2. Import di vercel.com
3. Deploy otomatis

## Dev Lokal
```bash
pip install -r requirements.txt
python api/app.py
```
Buka `public/index.html` via Live Server di port 5500.
