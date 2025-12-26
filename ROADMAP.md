# MicroManagerr Development Roadmap

Welcome to your journey of building MicroManagerr! This document is designed to be your comprehensive guide - not just telling you WHAT to build, but WHY we make certain decisions and WHAT you'll learn along the way.

---

## Table of Contents

1. [Understanding the Big Picture](#understanding-the-big-picture)
2. [Tech Stack Explained](#tech-stack-explained)
3. [Project Structure](#project-structure)
4. [Development Phases](#development-phases)
5. [Learning Concepts by Phase](#learning-concepts-by-phase)
6. [Quick Reference](#quick-reference)

---

## Understanding the Big Picture

### What is MicroManagerr?

MicroManagerr is a **self-hosted service** that acts as a "helper" for your media server stack. Think of it like this:

```
┌─────────────────────────────────────────────────────────────────┐
│                    Your Media Server Stack                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│   ┌──────────┐    ┌──────────┐    ┌──────────┐                  │
│   │  Sonarr  │    │  Radarr  │    │  Plex/   │                  │
│   │  (TV)    │    │ (Movies) │    │ Jellyfin │                  │
│   └────┬─────┘    └────┬─────┘    └──────────┘                  │
│        │               │                                         │
│        └───────┬───────┘                                         │
│                │                                                 │
│                ▼                                                 │
│   ┌─────────────────────────┐                                   │
│   │     MicroManagerr       │  <-- This is what we're building! │
│   │  ─────────────────────  │                                   │
│   │  - Scans media files    │                                   │
│   │  - Detects HDR/DV/IMAX  │                                   │
│   │  - Applies tags         │                                   │
│   │  - Fixes letterboxing   │                                   │
│   │  - Finds upgrades       │                                   │
│   └─────────────────────────┘                                   │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### How Self-Hosted Apps Work

When you build a self-hosted application, you're creating software that:

1. **Runs on your own hardware** (home server, NAS, VPS)
2. **Exposes an API** that other services can communicate with
3. **Often has a web UI** for human interaction
4. **Runs in Docker** for easy deployment and portability

Your app will:
- Run as a web server (using FastAPI)
- Connect to Sonarr/Radarr using their APIs
- Store its own data in a database
- Be deployed in a Docker container

---

## Tech Stack Explained

Let's break down each technology we'll use and WHY we're using it.

### Backend: Python + FastAPI

**What is it?**
- **Python**: A programming language known for readability and extensive libraries
- **FastAPI**: A modern web framework for building APIs with Python

**Why FastAPI over alternatives?**

| Framework | Pros | Cons | Verdict |
|-----------|------|------|---------|
| FastAPI | Fast, modern, auto-docs, type hints | Newer (less legacy tutorials) | **Best for new projects** |
| Flask | Simple, lots of tutorials | Slower, manual everything | Good for simple apps |
| Django | Full-featured, admin panel | Heavy, steep learning curve | Overkill for APIs |

**Why FastAPI wins for MicroManagerr:**
1. **Automatic API documentation** - FastAPI generates interactive docs at `/docs`
2. **Type hints** - Catches bugs before they happen
3. **Async support** - Critical when talking to multiple services (Sonarr, Radarr, etc.)
4. **Pydantic models** - Data validation built-in
5. **Industry standard** - Used by Microsoft, Netflix, Uber

```python
# Example: See how clean FastAPI code is
from fastapi import FastAPI

app = FastAPI()

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
```

### Database: SQLite (Development) -> PostgreSQL (Production)

**What is a database?**
A database stores your application's data persistently. When MicroManagerr scans a file and finds it has HDR, that information needs to be saved somewhere.

**Why start with SQLite?**
- **Zero setup** - It's just a file
- **Built into Python** - No installation needed
- **Perfect for development** - Fast iteration
- **Good enough for small deployments** - Many users will never need more

**Why PostgreSQL for production?**
- **Concurrent access** - Multiple users/processes at once
- **Better performance** - With large datasets
- **Industry standard** - What most serious applications use

**We'll use SQLAlchemy** - an ORM (Object-Relational Mapper) that lets us:
- Write Python code instead of SQL
- Switch databases easily (SQLite -> PostgreSQL)
- Define our data structure as Python classes

```python
# Example: Defining a database model
from sqlalchemy import Column, Integer, String, Boolean

class MediaFile(Base):
    __tablename__ = "media_files"

    id = Column(Integer, primary_key=True)
    path = Column(String, unique=True)
    has_hdr = Column(Boolean, default=False)
    has_dolby_vision = Column(Boolean, default=False)
```

### Frontend: HTML + HTMX + TailwindCSS

**Why this combo for a beginner?**

| Approach | Learning Curve | Setup Complexity | Best For |
|----------|---------------|------------------|----------|
| React/Vue/Angular | Steep | Complex (npm, build tools) | Large teams, complex UIs |
| **HTMX + Tailwind** | **Gentle** | **Minimal** | **Solo devs, CRUD apps** |
| Plain HTML/CSS/JS | Easy | None | Very simple apps |

**What is HTMX?**
HTMX lets you make dynamic web pages without writing JavaScript. It extends HTML with attributes that make AJAX calls.

```html
<!-- Traditional JS approach -->
<button onclick="fetch('/api/scan').then(...)">Scan</button>

<!-- HTMX approach - much simpler! -->
<button hx-post="/api/scan" hx-target="#result">Scan</button>
```

**What is TailwindCSS?**
A utility-first CSS framework. Instead of writing CSS files, you apply styles directly in HTML:

```html
<!-- Traditional CSS -->
<div class="card">...</div>
<!-- Requires separate CSS: .card { padding: 1rem; border-radius: 0.5rem; } -->

<!-- Tailwind -->
<div class="p-4 rounded-lg shadow">...</div>
<!-- Styles are right there! -->
```

**Why this is perfect for MicroManagerr:**
1. **No build step** - Just include via CDN to start
2. **Server-side rendering** - FastAPI serves complete HTML
3. **Progressive enhancement** - Works without JS, better with it
4. **Easy to learn** - You already know HTML

### Containerization: Docker

**What is Docker?**
Docker packages your application and all its dependencies into a "container" - a lightweight, isolated environment that runs the same everywhere.

**Why Docker is essential for self-hosted apps:**

```
Without Docker:                      With Docker:
──────────────────                   ──────────────────
User's system has Python 3.9        User runs: docker-compose up
Your app needs Python 3.11          Everything just works!
Also needs ffmpeg, mkvtoolnix...
Different Linux distros...
Hours of debugging...
```

**Docker concepts we'll use:**
- **Dockerfile** - Recipe for building your container
- **docker-compose.yml** - Orchestrates multiple containers (app + database)
- **Volumes** - Persist data outside the container
- **Networks** - Let containers talk to each other

### Media Analysis: FFmpeg + MediaInfo + MKVToolNix

**What are these tools?**

| Tool | Purpose | We'll Use It For |
|------|---------|------------------|
| **FFmpeg** | Video/audio processing | Detecting letterboxing, analyzing streams |
| **MediaInfo** | Metadata extraction | Reading HDR/DV info, audio tracks |
| **MKVToolNix** | MKV file manipulation | Applying crop metadata, editing tracks |

These tools run as command-line programs. Our Python code will call them and parse their output.

```python
# Example: Running ffprobe (part of FFmpeg) from Python
import subprocess
import json

result = subprocess.run(
    ["ffprobe", "-v", "quiet", "-print_format", "json", "-show_streams", file_path],
    capture_output=True
)
metadata = json.loads(result.stdout)
```

### API Communication: httpx

**What is it?**
A modern HTTP client for Python. We'll use it to talk to Sonarr/Radarr APIs.

**Why httpx over requests?**
- Async support (critical for our use case)
- HTTP/2 support
- More modern API

```python
# Example: Calling the Radarr API
import httpx

async with httpx.AsyncClient() as client:
    response = await client.get(
        "http://localhost:7878/api/v3/movie",
        headers={"X-Api-Key": "your-api-key"}
    )
    movies = response.json()
```

---

## Development Environment: Dev Containers

We use **Dev Containers** to ensure a consistent development environment across all machines.

### What is a Dev Container?

A dev container is a Docker container specifically configured for development. When you open this project in VS Code or Cursor, it automatically:
1. Builds a Docker container with all required tools
2. Installs Python, FFmpeg, MediaInfo, MKVToolNix
3. Sets up your virtual environment
4. Installs all dependencies
5. Configures your editor with the right extensions and settings

### Why Dev Containers?

| Benefit | Description |
|---------|-------------|
| **Consistency** | Same environment on Mac, Windows, Linux, and your server |
| **No local pollution** | Everything stays in the container, not on your machine |
| **Pre-configured tools** | FFmpeg, MediaInfo, MKVToolNix ready to use |
| **Easy onboarding** | Clone → Open in VS Code → Start coding |
| **Matches production** | Dev container uses same base as production Docker image |

### Development Workflow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         Your Development Workflow                            │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│   ┌─────────────────────┐              ┌─────────────────────┐              │
│   │     Your Mac        │              │    Your Server      │              │
│   │  ─────────────────  │              │  ─────────────────  │              │
│   │                     │              │                     │              │
│   │  VS Code/Cursor     │   git push   │  Docker Container   │              │
│   │  + Dev Container    │  ─────────>  │  + Media Library    │              │
│   │                     │              │  + Sonarr/Radarr    │              │
│   │  - Write code       │              │                     │              │
│   │  - Test API         │              │  - Integration test │              │
│   │  - Debug            │              │  - Real media files │              │
│   │                     │              │                     │              │
│   └─────────────────────┘              └─────────────────────┘              │
│                                                                              │
│   Development & API Testing            Full Integration Testing             │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Getting Started with Dev Containers

**Prerequisites:**
- Docker Desktop installed and running
- VS Code or Cursor with "Dev Containers" extension

**Steps:**
1. Open the project folder in VS Code/Cursor
2. You'll see a popup: "Reopen in Container" - click it
   - Or use Command Palette: `Dev Containers: Reopen in Container`
3. Wait 2-3 minutes for first-time build
4. Done! Terminal is now inside the container

**First time after container starts:**
```bash
cd backend
source ../venv/bin/activate
uvicorn app.main:app --reload
```

Then visit: http://localhost:8000/docs

---

## Project Structure

Here's what your project directory will look like and what each part does:

```
MicroManagerr/
├── .devcontainer/              # Dev Container configuration
│   ├── Dockerfile              # Development environment image
│   ├── devcontainer.json       # VS Code/Cursor dev container settings
│   └── post-create.sh          # Setup script (runs on first container start)
│
├── .github/                    # GitHub-specific files
│   └── workflows/              # CI/CD pipelines (later)
│
├── backend/                    # All Python/FastAPI code
│   ├── app/
│   │   ├── __init__.py        # Makes this a Python package
│   │   ├── main.py            # FastAPI application entry point
│   │   ├── config.py          # Configuration management
│   │   │
│   │   ├── api/               # API route definitions
│   │   │   ├── __init__.py
│   │   │   ├── routes/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── health.py      # Health check endpoints
│   │   │   │   ├── sonarr.py      # Sonarr integration endpoints
│   │   │   │   ├── radarr.py      # Radarr integration endpoints
│   │   │   │   ├── scan.py        # Media scanning endpoints
│   │   │   │   └── tags.py        # Tag management endpoints
│   │   │   └── dependencies.py    # Shared dependencies (auth, db sessions)
│   │   │
│   │   ├── core/              # Core business logic
│   │   │   ├── __init__.py
│   │   │   ├── arr_client.py      # Sonarr/Radarr API client
│   │   │   ├── media_analyzer.py  # FFmpeg/MediaInfo integration
│   │   │   └── tag_manager.py     # Tag application logic
│   │   │
│   │   ├── models/            # Database models (SQLAlchemy)
│   │   │   ├── __init__.py
│   │   │   ├── base.py            # Base model class
│   │   │   ├── media.py           # Media file models
│   │   │   └── config.py          # Configuration models
│   │   │
│   │   ├── schemas/           # Pydantic schemas (API request/response shapes)
│   │   │   ├── __init__.py
│   │   │   ├── media.py
│   │   │   └── arr.py
│   │   │
│   │   └── services/          # Business logic services
│   │       ├── __init__.py
│   │       ├── scanner.py         # File scanning service
│   │       └── upgrade_finder.py  # HDR upgrade discovery
│   │
│   ├── tests/                 # Test files
│   │   ├── __init__.py
│   │   ├── conftest.py            # Pytest fixtures
│   │   ├── test_api/
│   │   └── test_services/
│   │
│   ├── alembic/               # Database migrations
│   │   ├── versions/              # Migration files
│   │   └── env.py
│   │
│   ├── requirements.txt       # Python dependencies
│   ├── requirements-dev.txt   # Development dependencies
│   └── alembic.ini            # Migration configuration
│
├── frontend/                  # Frontend files (Phase 4)
│   ├── templates/             # Jinja2 HTML templates
│   │   ├── base.html              # Base layout
│   │   ├── index.html             # Dashboard
│   │   └── partials/              # HTMX partial templates
│   └── static/
│       ├── css/
│       └── js/
│
├── docker/                    # Docker configuration
│   ├── Dockerfile             # Main application Dockerfile
│   ├── Dockerfile.dev         # Development Dockerfile
│   └── docker-compose.yml     # Multi-container orchestration
│
├── scripts/                   # Utility scripts
│   └── dev-setup.sh           # Development environment setup
│
├── .env.example               # Example environment variables
├── .gitignore                 # Git ignore patterns
├── README.md                  # Project documentation
├── ROADMAP.md                 # This file!
├── FEATURE_RESEARCH.md        # Your research (existing)
└── pyproject.toml             # Python project configuration
```

### Why This Structure?

**Separation of Concerns**
Each folder has a single responsibility:
- `api/` - HTTP routing only
- `core/` - Business logic
- `models/` - Data structure
- `services/` - Complex operations

**Scalability**
This structure grows well. Adding a new feature means adding files to existing folders, not reorganizing everything.

**Testability**
Business logic in `services/` can be tested independently of the API layer.

---

## Development Phases

### Phase 0: Environment Setup

**Goals:**
- [ ] Dev container running in VS Code/Cursor
- [ ] First FastAPI endpoint running
- [ ] Can connect to Sonarr/Radarr APIs
- [ ] Understand the project structure

**What you'll build:**
A minimal FastAPI app that:
1. Has a `/health` endpoint
2. Has a `/api/v1/sonarr/status` endpoint that connects to your Sonarr instance
3. Runs inside your dev container

**Learning focus:**
- Dev containers and Docker basics
- Virtual environments (auto-created for you)
- Package management with pip
- FastAPI basics
- Making HTTP requests in Python

**Step-by-step guide:**

1. **Start the dev container:**
   - Open project in VS Code/Cursor
   - Click "Reopen in Container" when prompted
   - Wait for build to complete (~2-3 min first time)

2. **Start the FastAPI server:**
   ```bash
   cd backend
   source ../venv/bin/activate
   uvicorn app.main:app --reload
   ```

3. **Explore the API:**
   - Visit http://localhost:8000/docs
   - Try the `/health` endpoint
   - Look at the auto-generated documentation

4. **Configure your Arr connection:**
   - Edit `.env` file in project root
   - Add your Sonarr/Radarr URL and API key
   - Restart the server
   - Try the `/api/v1/sonarr/status` endpoint

**Success criteria:**
```bash
# Inside the dev container, you should be able to:
curl http://localhost:8000/health
# Returns: {"status": "healthy", ...}

curl http://localhost:8000/api/v1/sonarr/status
# Returns: Sonarr connection info (after configuring .env)
```

---

### Phase 1: Database & Core Models (Week 2)

**Goals:**
- [ ] Database connected
- [ ] Models for media files defined
- [ ] Can store and retrieve scan results
- [ ] Basic CRUD operations working

**What you'll build:**
Database models for:
- `ArrInstance` - Store Sonarr/Radarr connection details
- `MediaFile` - Store scanned file information
- `ScanResult` - Store HDR/DV detection results

**Learning focus:**
- SQL basics
- ORMs (Object-Relational Mapping)
- Database migrations with Alembic
- Pydantic schemas vs SQLAlchemy models

**Key concept - Models vs Schemas:**
```python
# Model: How data is stored in the database
class MediaFile(Base):
    __tablename__ = "media_files"
    id = Column(Integer, primary_key=True)
    path = Column(String)

# Schema: How data is sent/received via API
class MediaFileResponse(BaseModel):
    id: int
    path: str
    has_hdr: bool
```

---

### Phase 2: Media Analysis (Weeks 3-4)

**Goals:**
- [ ] Can analyze a media file for HDR/DV
- [ ] Can detect letterboxing
- [ ] Can identify audio/subtitle tracks
- [ ] Results stored in database

**What you'll build:**
The `media_analyzer.py` module that:
1. Runs `ffprobe` and `mediainfo` on files
2. Parses their JSON output
3. Extracts HDR metadata (mastering display, content light level)
4. Detects Dolby Vision (RPU presence, profile type)
5. Detects letterboxing using cropdetect

**Learning focus:**
- Subprocess management in Python
- JSON parsing
- Error handling
- Async programming basics

**Example output we're building toward:**
```python
result = await analyze_media_file("/path/to/movie.mkv")
# Returns:
{
    "path": "/path/to/movie.mkv",
    "video": {
        "codec": "hevc",
        "resolution": "3840x2160",
        "hdr": {
            "type": "HDR10+",
            "max_cll": "1000/400"
        },
        "dolby_vision": {
            "present": True,
            "profile": 8,
            "has_hdr_fallback": True
        }
    },
    "letterbox": {
        "detected": True,
        "crop_values": "3840:1600:0:280"
    },
    "audio_tracks": [...],
    "subtitle_tracks": [...]
}
```

---

### Phase 3: Arr Integration (Weeks 5-6)

**Goals:**
- [ ] Full Sonarr/Radarr API client
- [ ] Can fetch all movies/shows
- [ ] Can create/apply tags
- [ ] Can trigger searches
- [ ] Webhook support for real-time updates

**What you'll build:**
A robust `ArrClient` class that:
1. Authenticates with Sonarr/Radarr
2. Fetches library contents
3. Manages tags (CRUD operations)
4. Applies tags to media
5. Searches for upgrades

**Learning focus:**
- RESTful API consumption
- API design patterns
- Error handling and retries
- Rate limiting

**Sonarr/Radarr API patterns you'll learn:**
```python
# The Arr APIs follow consistent patterns:

# Get all items
GET /api/v3/movie              # Radarr
GET /api/v3/series             # Sonarr

# Get single item
GET /api/v3/movie/{id}

# Update item (including tags)
PUT /api/v3/movie/{id}

# Tags
GET /api/v3/tag
POST /api/v3/tag
DELETE /api/v3/tag/{id}

# Commands (trigger actions)
POST /api/v3/command
{
    "name": "MoviesSearch",
    "movieIds": [1, 2, 3]
}
```

---

### Phase 4: Frontend Dashboard (Weeks 7-8)

**Goals:**
- [ ] Basic web UI working
- [ ] Can view Sonarr/Radarr connections
- [ ] Can trigger scans
- [ ] Can view scan results
- [ ] Can apply tags with one click

**What you'll build:**
A web dashboard with:
1. Connection status overview
2. Library browser
3. Scan trigger and progress
4. Tag management interface
5. Results viewer with filters

**Learning focus:**
- Server-side rendering with Jinja2
- HTMX for interactivity
- TailwindCSS for styling
- Progressive enhancement

**Example HTMX interaction:**
```html
<!-- Trigger a scan with loading indicator -->
<button
    hx-post="/api/v1/scan/start"
    hx-target="#scan-results"
    hx-indicator="#loading">
    Start Scan
</button>

<div id="loading" class="htmx-indicator">
    Scanning...
</div>

<div id="scan-results">
    <!-- Results will appear here -->
</div>
```

---

### Phase 5: Advanced Features (Weeks 9-12)

**5A: HDR Upgrade Discovery**
- Search indexers for HDR versions
- Score comparison logic
- Auto-download or user review queue

**5B: Letterbox Cropping**
- Apply MKV crop metadata
- Batch processing
- Preview before apply

**5C: Track Declutter**
- Audio/subtitle track analysis
- User preferences for languages
- Safe removal with MKVToolNix

**5D: Library Organization**
- Path analysis
- Mismatch detection
- Move suggestions and execution

---

### Phase 6: Production Ready (Weeks 13-14)

**Goals:**
- [ ] Multi-stage Docker build (smaller images)
- [ ] Proper logging and monitoring
- [ ] Configuration via environment variables
- [ ] Database migrations automated
- [ ] Health checks and graceful shutdown
- [ ] Documentation complete

**What you'll build:**
Production hardening:
1. Optimized Dockerfile
2. docker-compose with PostgreSQL
3. Proper error handling everywhere
4. Rate limiting on API
5. Authentication (optional, for remote access)

---

## Learning Concepts by Phase

### Phase 0: Foundations

| Concept | What It Is | Why It Matters |
|---------|-----------|----------------|
| **Virtual Environments** | Isolated Python installations | Prevents dependency conflicts |
| **Package Management** | pip, requirements.txt | Reproducible builds |
| **HTTP Methods** | GET, POST, PUT, DELETE | RESTful API fundamentals |
| **JSON** | Data interchange format | How APIs communicate |
| **Docker Images** | Snapshots of environments | Deployment consistency |
| **Docker Containers** | Running instances of images | Isolated execution |

### Phase 1: Data Management

| Concept | What It Is | Why It Matters |
|---------|-----------|----------------|
| **Relational Databases** | Structured data storage | Persistent, queryable data |
| **SQL** | Database query language | Data manipulation |
| **ORM** | Object-Relational Mapping | Write Python, not SQL |
| **Migrations** | Database version control | Safe schema changes |
| **CRUD** | Create, Read, Update, Delete | Basic data operations |

### Phase 2: System Integration

| Concept | What It Is | Why It Matters |
|---------|-----------|----------------|
| **Subprocess** | Running external programs | Leverage existing tools |
| **Async/Await** | Concurrent execution | Non-blocking I/O |
| **Error Handling** | try/except patterns | Graceful failure |
| **Data Parsing** | Extracting structured data | Making sense of tool output |

### Phase 3: API Design

| Concept | What It Is | Why It Matters |
|---------|-----------|----------------|
| **REST** | API architectural style | Industry standard |
| **Authentication** | Proving identity | Secure access |
| **Rate Limiting** | Request throttling | Being a good API citizen |
| **Webhooks** | Event notifications | Real-time updates |

### Phase 4: Web Development

| Concept | What It Is | Why It Matters |
|---------|-----------|----------------|
| **Templates** | Dynamic HTML generation | Server-side rendering |
| **AJAX** | Async browser requests | Dynamic updates |
| **CSS Frameworks** | Pre-built styles | Rapid UI development |
| **Progressive Enhancement** | Works without JS | Accessibility |

### Phase 5-6: Production Skills

| Concept | What It Is | Why It Matters |
|---------|-----------|----------------|
| **Logging** | Recording application events | Debugging, monitoring |
| **Configuration** | External settings | Environment flexibility |
| **Multi-stage Builds** | Optimized Docker images | Smaller deployments |
| **Health Checks** | Service availability | Container orchestration |

---

## Quick Reference

### Key Commands You'll Use

```bash
# Python/FastAPI
python -m venv venv                    # Create virtual environment
source venv/bin/activate               # Activate it (Linux/Mac)
pip install -r requirements.txt        # Install dependencies
uvicorn app.main:app --reload         # Run FastAPI dev server

# Database
alembic revision --autogenerate -m "message"  # Create migration
alembic upgrade head                           # Apply migrations

# Docker
docker build -t micromanagerr .        # Build image
docker-compose up                      # Start all services
docker-compose up -d                   # Start in background
docker-compose logs -f                 # View logs
docker-compose down                    # Stop all services

# Testing
pytest                                 # Run all tests
pytest -v                              # Verbose output
pytest --cov                           # With coverage report
```

### Sonarr/Radarr API Quick Reference

```
Base URL: http://{host}:{port}/api/v3
Authentication: Header "X-Api-Key: {api_key}"

Common Endpoints:
  GET  /system/status          # Check connection
  GET  /movie                  # List all movies (Radarr)
  GET  /series                 # List all series (Sonarr)
  GET  /tag                    # List all tags
  POST /tag                    # Create tag {"label": "HDR"}
  PUT  /movie/{id}             # Update movie (including tags)
  POST /command                # Trigger actions
```

### Useful Resources

**FastAPI:**
- Official Docs: https://fastapi.tiangolo.com/
- Tutorial: https://fastapi.tiangolo.com/tutorial/

**Sonarr/Radarr APIs:**
- Sonarr API: https://sonarr.tv/docs/api/
- Radarr API: https://radarr.video/docs/api/

**Docker:**
- Get Started: https://docs.docker.com/get-started/
- Compose: https://docs.docker.com/compose/

**HTMX:**
- Documentation: https://htmx.org/docs/

**TailwindCSS:**
- Documentation: https://tailwindcss.com/docs

---

## Next Steps

Ready to start? Here's exactly what to do:

1. **Read through Phase 0** in detail
2. **Run the skeleton app** we'll create (see project files)
3. **Try the `/docs` endpoint** to see FastAPI's automatic documentation
4. **Get your Sonarr/Radarr API keys** (Settings -> General in each app)
5. **Make your first API call** to Sonarr/Radarr

Let's build something awesome!
