# MasrALPR
Markdown# 🇪🇬 MasrALPR: Egyptian Plate Intelligence System

MasrALPR is a full-stack security application designed to detect, recognize, and manage Egyptian license plates using YOLOv11 and FastAPI. It features a real-time scanner, a persistent scan history, and a letter-based/photo-based blacklist management system.

## 🚀 Features

* **Arabic Character Recognition**: Specifically trained to interpret Egyptian plate formats (Letters and Numbers).
* **Dynamic Blacklist**: Block vehicles by typing specific letters/numbers or by uploading a "wanted" car photo.
* **Smart OCR Logic**: Automatically separates letters and numbers regardless of the plate's character count.
* **Persistent Storage**: Uses SQLite to maintain security logs and watchlists even after system restarts.
* **Dockerized Deployment**: Fully containerized for easy setup on any security terminal.

## 📂 Project Structure

```text
project/
├── app/
│   ├── main.py          # FastAPI Application Logic
│   ├── database.py      # SQLAlchemy & SQLite Configuration
│   └── weights/         # YOLOv11 Model Weights (best.pt)
├── frontend/
│   ├── index.html       # Single-card UI Layout
│   └── static/          # Separate Assets
│       ├── css/style.css
│       └── js/script.js
├── data/                # Persistent Database Volume (Docker)
├── static/captures/     # Saved images of detected plates
└── Dockerfile           # Containerization script
🛠️ Installation & SetupLocal DevelopmentInstall Requirements:Bashpip install -r requirements.txt
Run Application:Bashuvicorn app.main:app --reload
Access UI: Open http://127.0.0.1:8000 in your browser.Docker DeploymentThis project uses SQLite as a file-based database, so no separate database image is required. Data is kept safe using Docker Volumes.Build Image:Bashdocker build -t masr-alpr .
Run Container with Persistence:Bashdocker run -p 8000:8000 -v $(pwd)/data:/app/data masr-alpr
📡 API EndpointsMethodEndpointDescriptionPOST/predictScans an image and returns plate text + status.POST/blacklist/add-by-photoExtracts plate from photo and adds to blacklist.DELETE/blacklist/remove/{id}Removes a specific rule from the watchlist.GET/historyRetrieves the last 5 vehicle scans.
