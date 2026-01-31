# AI-4-Creativity-Project-Vanshika Tangari-DeepFakeShield

## 🛡️ DeepFakeShield AI - Multimodal Deepfake Detection Platform

**Detect manipulated media using AI-powered analysis of video, audio, and lip-sync patterns.**

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.9+-green.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-teal.svg)

---

## 👤 Student Information

| Field              | Details                              |
| ------------------ | ------------------------------------ |
| **Student Name**   | Vanshika Tangri                      |
| **Student Number** | 2315843                              |
| **Project**        | AI-4-Creativity                      |
| **Project Video**  | https://youtu.be/O3Fyx1679Cw         |

---

## 📖 Project Overview

DeepFakeShield AI is a comprehensive web-based platform designed to detect AI-generated deepfake media. The platform uses a multimodal approach combining video forensics, audio spoof detection, and lip-sync verification to provide accurate authenticity assessments.

### Key Capabilities

- **Real-time Analysis**: Upload videos, images, or audio files for instant deepfake detection
- **Multimodal Detection**: Combines video, audio, and lip-sync analysis for robust results
- **Detailed Forensic Reports**: Generates comprehensive PDF reports with technical findings
- **Modern Web Interface**: Beautiful glassmorphism UI with real-time progress tracking
- **Evidence Timeline**: Visual representation of suspicious segments in media

---

## ✨ Features

| Feature                       | Description                                                                                  |
| ----------------------------- | -------------------------------------------------------------------------------------------- |
| 🎬 **Video Forensics**        | ViT-based frame analysis for face manipulation, boundary artifacts, temporal inconsistencies |
| 🔊 **Audio Spoof Detection**  | MFCC analysis, voice cloning detection, spectral pattern recognition                         |
| 👄 **Lip-Sync Verification**  | Audio-visual synchronization analysis, phoneme accuracy, viseme matching                     |
| 🔀 **Multimodal Fusion**      | Calibrated scoring across all modalities using ensemble methods                              |
| 📊 **Evidence Visualization** | Heatmaps, spectrograms, timelines showing detected anomalies                                 |
| 📄 **PDF Reports**            | Detailed forensic reports with technical summaries                                           |

---

## 🚀 Setup Instructions

### Prerequisites

Before setting up the project, ensure you have the following installed:

- **Python 3.9+** - [Download Python](https://www.python.org/downloads/)
- **PostgreSQL** - [Download PostgreSQL](https://www.postgresql.org/download/)
- **Node.js** (optional, for frontend development)
- **Git** - For cloning the repository

### Step 1: Clone the Repository

```bash
git clone https://github.com/vtangri/AI-4-Creativity-Project-Vanshika-Tangari-DeepFakeShield
cd DeepFakeShield
```

### Step 2: Create Python Virtual Environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate

# On Windows:
.\venv\Scripts\activate
```

### Step 3: Install Python Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Step 4: Configure Environment Variables

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env file with your settings
# Required variables:
# - DATABASE_URL=postgresql://user:password@localhost:5432/deepfakeshield
# - JWT_SECRET_KEY=your-secure-secret-key
# - CELERY_BROKER_URL=redis://localhost:6379/0
```

### Step 5: Set Up PostgreSQL Database

```bash
# Create the database
createdb deepfakeshield

# Run database migrations
cd backend
alembic upgrade head
```

### Step 6: Start the Backend Server

```bash
cd backend
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### Step 7: Start the Frontend Server

Open a new terminal:

```bash
cd frontend
python3 -m http.server 8080
```

### Step 8: Access the Application

Open your browser and navigate to:

- 🌐 **Frontend**: http://localhost:8080
- 📚 **API Documentation**: http://localhost:8000/docs
- 🔧 **API ReDoc**: http://localhost:8000/redoc

---

## 📁 Project Structure

```
deepfakeshield/
├── backend/                    # Backend API server
│   ├── app/
│   │   ├── api/routes/         # REST API endpoints
│   │   │   ├── analysis.py     # Analysis job management
│   │   │   ├── auth.py         # Authentication (JWT)
│   │   │   ├── media.py        # File upload handling
│   │   │   └── reports.py      # PDF report generation
│   │   ├── core/               # Core configuration
│   │   │   ├── config.py       # Application settings
│   │   │   ├── security.py     # JWT & password hashing
│   │   │   └── celery_app.py   # Task queue config
│   │   ├── models/             # SQLAlchemy ORM models
│   │   ├── schemas/            # Pydantic validation schemas
│   │   ├── services/           # Business logic services
│   │   │   ├── simulation.py   # Analysis simulation
│   │   │   └── pdf_service.py  # PDF generation
│   │   └── main.py             # FastAPI application
│   ├── alembic/                # Database migrations
│   └── tests/                  # Unit tests
├── frontend/                   # Web frontend
│   ├── index.html              # Single-page application
│   ├── css/
│   │   └── styles.css          # Glassmorphism theme
│   └── js/
│       └── app.js              # API client & UI logic
├── ml/                         # Machine learning models
│   ├── inference/              # Model inference code
│   └── training/               # Model training scripts
├── requirements.txt            # Python dependencies
├── docker-compose.yml          # Docker configuration
└── README.md                   # This file
```

---

## 🔌 API Endpoints

### Authentication

| Method | Endpoint                | Description               |
| ------ | ----------------------- | ------------------------- |
| POST   | `/api/v1/auth/register` | Register new user account |
| POST   | `/api/v1/auth/login`    | Login and get JWT tokens  |
| GET    | `/api/v1/auth/me`       | Get current user profile  |

### Media Management

| Method | Endpoint               | Description                   |
| ------ | ---------------------- | ----------------------------- |
| POST   | `/api/v1/media/upload` | Upload video/audio/image file |
| GET    | `/api/v1/media/{id}`   | Get media item details        |

### Analysis

| Method | Endpoint                       | Description                 |
| ------ | ------------------------------ | --------------------------- |
| POST   | `/api/v1/analysis/start`       | Start deepfake analysis job |
| GET    | `/api/v1/analysis/{id}/status` | Get job progress status     |
| GET    | `/api/v1/analysis/{id}/result` | Get full analysis results   |

### Reports

| Method | Endpoint                           | Description                  |
| ------ | ---------------------------------- | ---------------------------- |
| GET    | `/api/v1/reports`                  | List all analysis reports    |
| GET    | `/api/v1/analysis/{id}/report.pdf` | Download forensic PDF report |

---

## 🧠 ML Models & Detection Methods

### Video Analysis

| Aspect            | Details                                                   |
| ----------------- | --------------------------------------------------------- |
| **Model**         | ViT-B/16 (Vision Transformer)                             |
| **Training Data** | FaceForensics++ dataset                                   |
| **Detection**     | Face manipulation, boundary artifacts, GAN signatures     |
| **Output**        | Manipulation probability, suspicious frame identification |

### Audio Analysis

| Aspect            | Details                                         |
| ----------------- | ----------------------------------------------- |
| **Method**        | MFCC spectral analysis, Wav2Vec2 embeddings     |
| **Training Data** | ASVspoof dataset                                |
| **Detection**     | Voice cloning, TTS synthesis, formant anomalies |
| **Output**        | Cloning probability, naturalness score          |

### Lip-Sync Analysis

| Aspect        | Details                            |
| ------------- | ---------------------------------- |
| **Model**     | SyncNet-based correlation          |
| **Method**    | Audio-visual alignment scoring     |
| **Detection** | Desynchronization, dubbed audio    |
| **Output**    | Sync offset (ms), phoneme accuracy |

---

## 🛠️ Tech Stack

| Layer              | Technologies                               |
| ------------------ | ------------------------------------------ |
| **Backend**        | Python 3.9+, FastAPI, SQLAlchemy, Pydantic |
| **Database**       | PostgreSQL, Redis (caching)                |
| **ML**             | PyTorch, torchaudio, OpenCV, Transformers  |
| **Frontend**       | Vanilla JavaScript, CSS3 (Glassmorphism)   |
| **Authentication** | JWT (JSON Web Tokens)                      |
| **Task Queue**     | Celery (optional, for async processing)    |
| **Deployment**     | Docker, Nginx, Gunicorn                    |

---

## 🧪 Running Tests

```bash
cd backend
pytest tests/ -v --cov=app
```

---

## 📊 Analysis Output Details

The platform provides comprehensive forensic analysis including:

### Video Forensics Output

- Frames analyzed count
- Faces detected
- Manipulation type (face_swap, face_reenactment, lip_sync_manipulation)
- Manipulation method (DeepFaceLab, FaceSwap, FSGAN, etc.)
- Blending score
- Artifact detection (boundary, temporal, color histogram)

### Audio Forensics Output

- Voice cloning detection
- Cloning method identification
- MFCC anomaly score
- Formant consistency
- Speaker embedding distance
- Naturalness score

### Lip-Sync Forensics Output

- Sync offset (milliseconds)
- Correlation score
- Phoneme accuracy
- Viseme match rate

### Technical Metadata

- Models used
- Inference time
- Media resolution, FPS, codec
- File hash (SHA-256)

---

## 🔒 Security Features

- **JWT Authentication** - Secure token-based authentication
- **Password Hashing** - bcrypt with salt
- **CORS Protection** - Configurable allowed origins
- **Input Validation** - Pydantic schema validation
- **File Validation** - MIME type and size verification

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🤝 Acknowledgments

- FaceForensics++ dataset for video model training
- ASVspoof dataset for audio model training
- FastAPI for the excellent web framework
- PyTorch for deep learning infrastructure

---

**Built with ❤️ for media authenticity**

_DeepFakeShield AI - Protecting Truth in the Age of Synthetic Media_
