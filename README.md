Got it! Here’s a **full, complete, ready-to-use README.md** for your MasrALPR project with **all sections included, full Markdown formatting, code blocks, emojis, tables, and proper instructions**:

````markdown
# 🇪🇬 MasrALPR: Egyptian Plate Intelligence System

MasrALPR is a full-stack security application designed to **detect, recognize, and manage Egyptian license plates** using **YOLOv11** and **FastAPI**. It features a real-time scanner, a persistent scan history, and a letter/photo-based blacklist management system.

---

## 🚀 Features

- **Arabic Character Recognition**: Specifically trained to interpret Egyptian plate formats (letters and numbers).  
- **Dynamic Blacklist**: Block vehicles by typing specific letters/numbers or by uploading a "wanted" car photo.  
- **Smart OCR Logic**: Automatically separates letters and numbers regardless of the plate's character count.  
- **Persistent Storage**: Uses SQLite to maintain security logs and watchlists even after system restarts.  
- **Dockerized Deployment**: Fully containerized for easy setup on any security terminal.  
- **Real-Time Scanning**: Detect plates in live video feeds or static images.  
- **Lightweight UI**: Minimal frontend to quickly visualize plate detections and scan history.  

---

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
````

---

## 🛠️ Installation & Setup

### Local Development

**1. Clone the repository:**

```bash
git clone https://github.com/yourusername/masr-alpr.git
cd masr-alpr
```

**2. Install Python dependencies:**

```bash
pip install -r requirements.txt
```

**3. Run the FastAPI server:**

```bash
uvicorn app.main:app --reload
```

**4. Open the frontend:**
Navigate to [http://127.0.0.1:8000](http://127.0.0.1:8000) in your browser.

---

### Docker Deployment

This project uses SQLite as a file-based database, so no separate database container is required. Use Docker volumes to persist data.

**1. Build the Docker image:**

```bash
docker build -t masr-alpr .
```

**2. Run the Docker container with data persistence:**

```bash
docker run -p 8000:8000 -v $(pwd)/data:/app/data masr-alpr
```

**3. Access the UI:**
Open [http://localhost:8000](http://localhost:8000) in your browser.

---

## 📡 API Endpoints

| Method | Endpoint                  | Description                                    |
| ------ | ------------------------- | ---------------------------------------------- |
| POST   | `/predict`                | Scan an image and return plate text + status.  |
| POST   | `/blacklist/add-by-photo` | Extract plate from photo and add to blacklist. |
| DELETE | `/blacklist/remove/{id}`  | Remove a specific rule from the watchlist.     |
| GET    | `/history`                | Retrieve the last 5 vehicle scans.             |

**Example: Predict Endpoint (Python)**

```python
import requests

url = "http://127.0.0.1:8000/predict"
files = {"file": open("car.jpg", "rb")}
response = requests.post(url, files=files)
print(response.json())
```

---

## 🗃️ Database

* Uses **SQLite** (`data/database.db`) to store:

  * Scan history
  * Blacklist entries
  * Captured plate images
* SQLAlchemy ORM handles CRUD operations.

---

## 🖥️ Frontend

* **index.html**: Minimal card layout to show scanned plates and status.
* **static/css/style.css**: Custom CSS for UI styling.
* **static/js/script.js**: Handles API calls and DOM updates.

---

## 🔒 Security Features

* **Blacklist Management**: Block by:

  * Plate letters/numbers
  * Photo of vehicle
* **Persistent Watchlist**: Survives server restart
* **Real-Time Alerts**: System can notify when a blacklisted vehicle is detected.

---

## 🧰 Tools & Technologies

* **YOLOv11**: Object detection for license plates
* **FastAPI**: Backend API
* **SQLite**: Lightweight database
* **Docker**: Containerization
* **JavaScript & HTML/CSS**: Frontend UI

---

## 📖 Contribution

1. Fork the repository
2. Create a feature branch (`git checkout -b feature-name`)
3. Commit your changes (`git commit -m 'Add feature'`)
4. Push to the branch (`git push origin feature-name`)
5. Open a Pull Request

---

## 📜 License

This project is licensed under the **MIT License**.

---

## 🏷️ Badges (Optional)

* ![Python](https://img.shields.io/badge/python-3.11-blue)
* ![FastAPI](https://img.shields.io/badge/FastAPI-v0.100-green)
* ![Docker](https://img.shields.io/badge/Docker-v24-blue)

---

> MasrALPR © 2026 – Designed for Egyptian plate recognition and security monitoring

```


