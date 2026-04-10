# Setup and Development

## Prerequisites

- Python 3.12+
- Docker
- Docker Compose

## Local development

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
set FLASK_APP=app
flask run
```

The application loads environment settings from `.env` using `python-dotenv`.

Visit the sample pages locally:
- `http://127.0.0.1:5000/`
- `http://127.0.0.1:5000/about`
- `http://127.0.0.1:5000/contact`

## Run with Docker

```bash
docker build -t flask-sample-app .
docker run -p 5000:5000 flask-sample-app
```

## Run with Docker Compose

```bash
docker compose up --build
```

## Run tests

```bash
pip install pytest
pytest
```
