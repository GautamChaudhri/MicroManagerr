# MicroManagerr

**Your Media Library Enhancement Tool**

MicroManagerr is a self-hosted service that integrates with Sonarr and Radarr to enhance your media library management. It automates detection and tagging of HDR, Dolby Vision, and IMAX content, fixes letterboxing issues, and helps you find quality upgrades for your media.

---

## Features

### Core Features (In Development)

- **HDR/Dolby Vision Detection** - Automatically scan your media files and detect HDR10, HDR10+, and Dolby Vision content
- **Automatic Tagging** - Apply tags in Sonarr/Radarr based on detected content features
- **IMAX Enhanced Detection** - Identify IMAX Enhanced content in your library
- **Special Edition Detection** - Detect Extended Editions, Director's Cuts, and other variants by comparing runtimes
- **Letterbox Cropping** - Apply MKV crop metadata to remove black bars without re-encoding
- **HDR Upgrade Discovery** - Search for HDR/DV versions of your SDR content
- **Library Organization** - Detect files in wrong libraries (e.g., 1080p in 4K folder)
- **Track Declutter** - Remove unwanted audio and subtitle tracks

### Planned Features

- Unified dashboard for multiple Sonarr/Radarr instances
- Corrupt file detection
- Database health monitoring
- Smart notifications

---

## Quick Start

### Prerequisites

- Python 3.11+ (for local development)
- Docker and Docker Compose (recommended for deployment)
- Sonarr and/or Radarr with API access

### Option 1: Run with Docker (Recommended)

```bash
# Clone the repository
git clone https://github.com/GautamChaudhri/MicroManagerr.git
cd MicroManagerr

# Copy the example environment file
cp .env.example .env

# Edit .env with your Sonarr/Radarr details
# Set SONARR_URL, SONARR_API_KEY, RADARR_URL, RADARR_API_KEY

# Start the application
cd docker
docker-compose up -d

# View logs
docker-compose logs -f

# Access the API at http://localhost:8000
# API documentation at http://localhost:8000/docs
```

### Option 2: Run Locally (Development)

```bash
# Clone the repository
git clone https://github.com/GautamChaudhri/MicroManagerr.git
cd MicroManagerr

# Create a virtual environment
python -m venv venv

# Activate it
# On macOS/Linux:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate

# Install dependencies
cd backend
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Copy and configure environment
cp ../.env.example ../.env
# Edit .env with your settings

# Run the development server
uvicorn app.main:app --reload

# Access the API at http://localhost:8000
```

---

## Configuration

MicroManagerr is configured through environment variables. Copy `.env.example` to `.env` and set your values:

| Variable | Description | Example |
|----------|-------------|---------|
| `DEBUG` | Enable debug mode | `true` |
| `LOG_LEVEL` | Logging verbosity | `DEBUG`, `INFO`, `WARNING` |
| `DATABASE_URL` | Database connection string | `sqlite+aiosqlite:///./data/micromanagerr.db` |
| `SONARR_URL` | Sonarr base URL | `http://localhost:8989` |
| `SONARR_API_KEY` | Sonarr API key | (32-character key) |
| `RADARR_URL` | Radarr base URL | `http://localhost:7878` |
| `RADARR_API_KEY` | Radarr API key | (32-character key) |

### Finding Your API Keys

**Sonarr:** Settings -> General -> Security -> API Key

**Radarr:** Settings -> General -> Security -> API Key

---

## API Documentation

Once running, visit these URLs:

- **Swagger UI:** http://localhost:8000/docs - Interactive API documentation
- **ReDoc:** http://localhost:8000/redoc - Alternative documentation format

### Key Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Basic health check |
| `/health/detailed` | GET | Detailed system status |
| `/api/v1/sonarr/status` | GET | Sonarr connection status |
| `/api/v1/sonarr/series` | GET | List all TV series |
| `/api/v1/radarr/status` | GET | Radarr connection status |
| `/api/v1/radarr/movies` | GET | List all movies |

---

## Project Structure

```
MicroManagerr/
├── backend/                    # Python/FastAPI backend
│   ├── app/
│   │   ├── main.py            # Application entry point
│   │   ├── config.py          # Configuration management
│   │   ├── api/routes/        # API endpoint definitions
│   │   ├── core/              # Business logic
│   │   ├── models/            # Database models
│   │   ├── schemas/           # Pydantic schemas
│   │   └── services/          # High-level services
│   ├── tests/                 # Test suite
│   └── requirements.txt       # Python dependencies
├── frontend/                  # Web UI (coming soon)
├── docker/                    # Docker configuration
│   ├── Dockerfile            # Production image
│   ├── Dockerfile.dev        # Development image
│   └── docker-compose.yml    # Container orchestration
├── .env.example              # Example environment config
├── ROADMAP.md                # Development roadmap
└── README.md                 # This file
```

---

## Development

### Running Tests

```bash
cd backend
pytest
pytest -v           # Verbose
pytest --cov        # With coverage
```

### Code Quality

```bash
# Lint and format with ruff
ruff check .
ruff format .

# Type checking
mypy app
```

### Making Changes

1. Create a new branch: `git checkout -b feature/your-feature`
2. Make your changes
3. Run tests: `pytest`
4. Commit: `git commit -m "Add your feature"`
5. Push: `git push origin feature/your-feature`
6. Open a Pull Request

---

## Roadmap

See [ROADMAP.md](ROADMAP.md) for the detailed development plan, including:

- Phase-by-phase development guide
- Tech stack explanations
- Learning concepts covered
- Project structure details

---

## Tech Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| Backend | Python + FastAPI | REST API server |
| Database | SQLite / PostgreSQL | Data persistence |
| Frontend | HTMX + TailwindCSS | Web interface |
| Media Analysis | FFmpeg + MediaInfo | File inspection |
| Deployment | Docker | Containerization |

---

## Contributing

Contributions are welcome! This project is designed as a learning experience, so:

- Clear, well-commented code is valued
- Documentation improvements are appreciated
- Bug reports help improve quality
- Feature suggestions guide development

---

## License

This project is open source. See LICENSE file for details.

---

## Acknowledgments

- [Sonarr](https://sonarr.tv/) and [Radarr](https://radarr.video/) for their excellent APIs
- [TRaSH Guides](https://trash-guides.info/) for media management best practices
- The self-hosted community for inspiration and feedback
- All the tools this project builds upon: FFmpeg, MediaInfo, MKVToolNix

---

## Support

- **Documentation:** [ROADMAP.md](ROADMAP.md)
- **Issues:** [GitHub Issues](https://github.com/GautamChaudhri/MicroManagerr/issues)
- **Discussions:** [GitHub Discussions](https://github.com/GautamChaudhri/MicroManagerr/discussions)
