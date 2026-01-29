# 🇪🇬 MasrALPR: Egyptian License Plate Intelligence System

<div align="center">

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.11+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)
![Docker](https://img.shields.io/badge/docker-ready-blue.svg)
![YOLOv11](https://img.shields.io/badge/YOLOv11-enabled-orange.svg)

**Advanced AI-powered license plate recognition and security management system for Egyptian vehicles**

[Features](#-features) • [Installation](#-installation--setup) • [API Documentation](#-api-endpoints) • [Docker](#-docker-deployment) • [Contributing](#-contribution)

</div>

---

## 📋 Overview

MasrALPR is a production-ready, full-stack security application engineered to detect, recognize, and manage Egyptian license plates using state-of-the-art **YOLOv11** deep learning and **FastAPI** backend. The system provides real-time vehicle monitoring, persistent scan history, and intelligent blacklist management through both manual entry and photo-based detection.

### Why MasrALPR?

- 🎯 **Egyptian-Specific**: Trained on Arabic characters and Egyptian plate formats
- ⚡ **Real-Time Processing**: Instant plate detection and recognition
- 🔒 **Security-First**: Built-in blacklist management and access control
- 💾 **Persistent Storage**: SQLite-based data persistence
- 🐳 **Production-Ready**: Fully containerized with Docker
- 🎨 **Modern UI**: Sleek, futuristic interface for security operations

---

## 🚀 Features

### Core Capabilities

| Feature | Description |
|---------|-------------|
| **Arabic OCR** | Native support for Egyptian Arabic letters and numerals |
| **Smart Detection** | YOLOv11-powered plate localization in images and video streams |
| **Dynamic Blacklist** | Block vehicles by plate number or uploaded photos |
| **Intelligent Parsing** | Automatic separation of letters and numbers regardless of format |
| **Persistent Database** | SQLite storage for logs, watchlists, and captured images |
| **RESTful API** | Complete FastAPI backend with comprehensive endpoints |
| **Real-Time Monitoring** | Live scan history and status updates |
| **Docker Support** | One-command deployment with volume persistence |

### Security Features

- ✅ **Multi-Method Blocking**: Add plates via text input or photo upload
- ✅ **Access Control**: Automatic allow/deny decisions based on blacklist
- ✅ **Audit Trail**: Complete scan history with timestamps
- ✅ **Persistent Watchlist**: Survives system restarts and updates
- ✅ **Visual Feedback**: Color-coded status indicators (green/red)

---

## 📂 Project Structure

```
MasrALPR/
├── app/
│   ├── main.py              # FastAPI application logic
│   ├── database.py          # SQLAlchemy models & database config
│   ├── models.py            # Pydantic schemas
│   └── weights/
│       └── best.pt          # YOLOv11 trained weights
│
├── frontend/
│   ├── index.html           # Main application interface
    └── static/
│     └── style.css            # Futuristic UI styling
│     └── script.js            # Client-side logic & API calls
│
├── data/
│   └── database.db          # SQLite database (auto-created)
│
├── static/
│   └── captures/            # Detected plate images
│
├── requirements.txt         # Python dependencies
├── Dockerfile              # Container configuration
├── docker-compose.yml      # Docker Compose setup
└── README.md              # This file
```

---

## 🛠️ Installation & Setup

### Prerequisites

- Python 3.11 or higher
- pip package manager
- (Optional) Docker & Docker Compose

### Local Development

**1. Clone the repository**

```bash
git clone https://github.com/yourusername/MasrALPR.git
cd MasrALPR
```
**2. Install dependencies**

```bash
pip install -r requirements.txt
```

**3. Run the application**

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**4. Access the interface**

Open your browser and navigate to:
```
http://127.0.0.1:8000
```

---

## 🐳 Docker Deployment

### Quick Start

**1. Build the image**

```bash
docker build -t masralpr:latest .
```

**2. Run the container**

```bash
docker run -d \
  -p 8000:8000 \
  -v $(pwd)/data:/app/data \
  -v $(pwd)/static:/app/static \
  --name masralpr \
  masralpr:latest
```

## 🗃️ Database Schema

### Tables

#### `blacklist`
| Column | Type | Description |
|--------|------|-------------|
| `id` | INTEGER | Primary key |
| `plate_text` | VARCHAR(50) | Plate number or pattern |
| `created_at` | DATETIME | Timestamp of creation |

#### `scan_history`
| Column | Type | Description |
|--------|------|-------------|
| `id` | INTEGER | Primary key |
| `text` | VARCHAR(50) | Detected plate text |
| `is_allowed` | BOOLEAN | Access decision |
| `timestamp` | DATETIME | Scan timestamp |

<div align="center">
 
Made with ❤️ in Egypt 🇪🇬

© 2026 MasrALPR – Advanced License Plate Recognition for Egyptian Security

</div>
