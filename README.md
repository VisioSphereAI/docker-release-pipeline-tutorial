# 🚀 Flask Docker Application with Interactive Features

## 🎯 Quick Overview

This repository contains an **advanced Flask application** demonstrating production-grade development practices with:

- **🐳 Docker** containerization with Gunicorn
- **📅 Interactive Calendar** system
- **✓ Task Manager** with priority levels
- **🎨 Bootstrap 5** responsive UI
- **🧪 Comprehensive Tests** with pytest
- **🔄 CI/CD Pipeline** with GitHub Actions
- **📊 Multi-page Application** with Jinja2 templates

---

## 🚀 Getting Started

### Run Locally

```bash
# Create and activate virtual environment
python -m venv .venv
.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment example
copy .env.example .env

# Start the Flask server
set FLASK_APP=app
flask run
```

Visit `http://localhost:5000` to see the app.

### Run with Docker

```bash
# Build and run the image
docker build -t flask-docker-app .
docker run -p 5000:5000 flask-docker-app
```

### Run with Docker Compose

```bash
# Start the entire stack
docker compose up --build
```

---

## 📚 Features

### 🏠 Web Pages
- **Home** - Overview of features and quick links
- **📅 Calendar** - Interactive monthly event calendar
- **✓ Tasks** - Task management with priorities and completion tracking
- **About** - Project information and technologies
- **Contact** - Next steps and suggestions

### 🔌 API Endpoints
- `GET /health/` - Health check endpoint
- `POST /api/v1/echo` - Echo JSON messages

### 🛠️ Advanced Features
- **App Factory Pattern** - Flexible application initialization
- **Configuration Management** - Environment-based settings
- **Error Handling** - Comprehensive error responses
- **Request Validation** - Input validation for forms
- **Form Handling** - Task creation and management
- **Static Assets** - CSS and JavaScript support
- **Responsive Design** - Mobile-friendly UI with Bootstrap 5

---

## 🏗️ Project Structure

```
.
├── .github/
│   └── workflows/
│       └── ci.yml                 # GitHub Actions CI/CD
├── app/
│   ├── __init__.py               # App factory
│   ├── config.py                 # Configuration classes
│   ├── routes.py                 # Blueprint routes
│   ├── errors.py                 # Error handlers
│   ├── extensions.py             # Flask extensions
│   ├── health.py                 # Health check blueprint
│   ├── calendar_manager.py       # Calendar logic
│   ├── task_manager.py           # Task management logic
│   ├── static/
│   │   ├── css/
│   │   │   └── styles.css        # Custom styles
│   │   └── js/
│   │       └── app.js            # Frontend JavaScript
│   └── templates/
│       ├── layout.html           # Base template
│       ├── home.html             # Home page
│       ├── calendar.html         # Calendar page
│       ├── tasks.html            # Tasks page
│       ├── about.html            # About page
│       └── contact.html          # Contact page
├── tests/
│   ├── test_api.py              # API tests
│   └── test_pages.py            # Page tests
├── docs/
│   ├── api.md                   # API documentation
│   ├── overview.md              # Project overview
│   └── setup.md                 # Setup instructions
├── scripts/
│   ├── run.sh                   # Start Flask server
│   └── test.sh                  # Run tests
├── Dockerfile                   # Container definition
├── docker-compose.yml           # Docker Compose config
├── requirements.txt             # Production dependencies
├── requirements-dev.txt         # Development dependencies
├── .env.example                 # Environment template
└── README.md                    # This file
```

---

## 🧪 Testing

```bash
# Install test dependencies
pip install -r requirements-dev.txt

# Run all tests
pytest

# Run with verbose output
pytest -v
```

---

## 🔧 Docker CI/CD Release Pipeline

This project also demonstrates a **production-grade CI/CD pipeline** using:

## 🧱 Branch Strategy

| Branch   | Purpose |
|----------|--------|
| `main`   | Production-ready code |
| `dev`    | Pre-production / staging |
| `feature/*` | Feature development |

---

## 🔄 Workflow Overview

### 1️⃣ Feature Development
- Developers push code to `feature/*` branches
- PR is created to `dev`

---

### 2️⃣ Dev Deployment (Pre-Prod Testing)

Triggered when:
- User selects `dev` environment manually

#### Steps:
1. Create a Git tag
2. Build Docker image
3. Push image to Artifactory (dev repo)
4. Create a pre-release
5. Send notification (success/failure)

---

### 3️⃣ Production Promotion

Triggered when:
- User selects `prod` environment
- Provides a release tag

#### Validations:
- ✅ Tag exists
- ✅ Docker image exists in dev registry
- ✅ Release/tag exists in GitHub

#### Steps:
1. Promote Docker image (dev → prod)
2. Create GitHub Release
3. Generate release notes
4. Create PR (`dev` → `main`)
5. Send notification

---

## 🏗️ Repository Structure

```
.
├── .github/
│   └── workflows/
│       └── ci.yml
├── app/
│   ├── __init__.py
│   └── routes.py
├── docs/
│   ├── api.md
│   ├── overview.md
│   └── setup.md
├── scripts/
│   ├── run.sh
│   └── test.sh
├── tests/
│   └── test_basic.py
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── README.md
└── .dockerignore
```

---

## ⚙️ GitHub Actions Workflow

### 🔹 Manual Trigger Inputs

| Input        | Description |
|-------------|------------|
| `environment` | dev / prod |
| `tag`        | Required for prod |

---

## 🐳 Docker Build

```bash
docker build -t <repo>:<tag> .
docker push <repo>:<tag>
```

---

## 🧪 Validation Logic (Prod)

- Check tag exists
- Check Docker image exists
- Check GitHub release/tag exists

Example:
```bash
./scripts/validate.sh <tag>
```

---

## 🔁 Image Promotion

Instead of rebuilding:
- Pull from dev registry
- Retag
- Push to prod registry

```bash
docker pull dev-repo/app:<tag>
docker tag dev-repo/app:<tag> prod-repo/app:<tag>
docker push prod-repo/app:<tag>
```

---

## 📢 Notifications

You can integrate:
- Email (SMTP)
- Slack
- Teams

---

## 🔐 Required Secrets

Add in GitHub Secrets:

| Secret Name | Description |
|------------|------------|
| `DOCKER_USERNAME` | Docker registry username |
| `DOCKER_PASSWORD` | Docker registry password |
| `ARTIFACTORY_URL` | Registry URL |
| `EMAIL_USERNAME` | SMTP username |
| `EMAIL_PASSWORD` | SMTP password |

---

## 📦 Sample Workflow (Simplified)

This repository includes a GitHub Actions workflow in `.github/workflows/ci.yml` that:

- checks out the code
- installs Python dependencies
- runs unit tests with `pytest`
- builds the Docker image

---

## 🐳 Docker Compose

A `docker-compose.yml` file is provided for local development:

```bash
docker compose up --build
```

---

## 📚 Documentation

Additional documentation is available in the `docs/` folder:

- `docs/overview.md` — project overview and structure
- `docs/setup.md` — development, Docker, and test setup
- `docs/api.md` — endpoint documentation

---

## 🧪 Local Flask Sample Application

A simple Flask sample application is available under `app/`.

This version includes a multi-page site with HTML templates and CSS assets.

Run locally:
```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
set FLASK_APP=app
flask run
```

Visit:
- `http://127.0.0.1:5000/`
- `http://127.0.0.1:5000/about`
- `http://127.0.0.1:5000/contact`

Build and run with Docker:
```bash
docker build -t flask-sample-app .
docker run -p 5000:5000 flask-sample-app
```

Run with Docker Compose:
```bash
docker compose up --build
```

Run tests:
```bash
pip install pytest
pytest
```

---

## 🗂️ Current Repository Structure

```
.
├── .github/
│   └── workflows/
│       └── ci.yml
├── app/
│   ├── __init__.py
│   └── routes.py
├── docs/
│   ├── api.md
│   ├── overview.md
│   └── setup.md
├── scripts/
│   ├── run.sh
│   └── test.sh
├── tests/
│   └── test_basic.py
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── README.md
├── .dockerignore
└── .gitignore
```

---

## 🤝 Contribution

1. Fork the repository
2. Create a feature branch
3. Submit a pull request


---

## 📄 License


---

## ⭐ Summary

This project demonstrates a **real-world Dev → Prod promotion pipeline** with:


