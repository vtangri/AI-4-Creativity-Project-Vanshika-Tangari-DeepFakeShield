# 🛡️ DeepFakeShield AI

**Multimodal Deepfake Detection Platform**

Detect manipulated media using AI-powered analysis of video, audio, and lip-sync patterns.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.9+-green.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-teal.svg)

---

## ✨ Features

- **Video Forensics** - ViT-based frame analysis for face manipulation
- **Audio Spoof Detection** - AASIST-style synthetic speech detection
- **Lip-Sync Verification** - Audio-visual synchronization analysis
- **Multimodal Fusion** - Calibrated scoring across modalities
- **Evidence Visualization** - Heatmaps, spectrograms, timelines
- **PDF Reports** - Detailed forensic reports with LLM summaries

---

## 🚀 Quick Start

### Development

```bash
# Clone and setup
git clone <repository-url>
cd deepfakeshield
./scripts/setup.sh

# Start with Docker
docker-compose up -d

# Or run locally
./scripts/run-dev.sh
```

### Production

```bash
# Configure secrets
cp .env.example .env.prod
# Edit .env.prod with secure values

# Deploy
./scripts/deploy.sh
```

**Access:**

- 🌐 Frontend: http://localhost
- 📚 API Docs: http://localhost/docs
- 🌸 Flower: http://localhost:5555

---

## 📁 Project Structure

```
deepfakeshield/
├── backend/
│   ├── app/
│   │   ├── api/routes/     # REST endpoints
│   │   ├── core/           # Config, security, Celery
│   │   ├── models/         # SQLAlchemy models
│   │   └── workers/        # Celery tasks
│   └── tests/              # Pytest unit tests
├── frontend/
│   ├── index.html          # Single-page app
│   ├── css/styles.css      # Glassmorphism theme
│   └── js/app.js           # API client
├── ml/
│   ├── inference/          # Video, audio, lipsync, fusion
│   ├── training/           # Training scripts
│   └── datasets/           # Dataset loaders
├── deploy/
│   └── nginx/              # Production configs
├── docker-compose.yml      # Development
└── docker-compose.prod.yml # Production
```

---

## 🔌 API Endpoints

| Method | Endpoint                           | Description    |
| ------ | ---------------------------------- | -------------- |
| POST   | `/api/v1/auth/register`            | Register user  |
| POST   | `/api/v1/auth/login`               | Login (JWT)    |
| POST   | `/api/v1/media/upload`             | Upload media   |
| POST   | `/api/v1/analysis/start`           | Start analysis |
| GET    | `/api/v1/analysis/{id}/status`     | Job status     |
| GET    | `/api/v1/analysis/{id}/result`     | Full results   |
| GET    | `/api/v1/analysis/{id}/report.pdf` | PDF report     |

---

## 🧠 ML Models

| Service                 | Architecture    | Purpose                      |
| ----------------------- | --------------- | ---------------------------- |
| VideoForensicsService   | ViT-B/16        | Frame manipulation detection |
| AudioSpoofService       | CNN + MelSpec   | Synthetic speech detection   |
| LipSyncService          | ROI + Alignment | A/V sync verification        |
| MultimodalFusionService | Weighted        | Score calibration            |

### Training

```bash
# Video model
python ml/training/train_video.py --data-dir /path/to/faceforensics --epochs 20

# Audio model
python ml/training/train_audio.py --data-dir /path/to/asvspoof --epochs 30
```

---

## 🧪 Testing

```bash
cd backend
pytest tests/ -v --cov=app
```

---

## 🛠️ Tech Stack

| Layer    | Technology                      |
| -------- | ------------------------------- |
| Backend  | FastAPI, SQLAlchemy, Celery     |
| Database | PostgreSQL, Redis               |
| ML       | PyTorch, torchaudio, OpenCV     |
| Frontend | Vanilla JS, CSS (Glassmorphism) |
| Deploy   | Docker, Nginx, Gunicorn         |

---

## 📄 License

MIT License - see [LICENSE](LICENSE) for details.

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Submit a pull request

---

**Built with ❤️ for media authenticity**
