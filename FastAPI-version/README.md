# Image Classification API (FastAPI Version)
(Not yet Completed)

A production-grade, async-first image classification API built with FastAPI, designed for scalability, security, and observability. This service classifies images using a deep learning model, manages user authentication and tokens, and is ready for deployment with Docker and Prometheus metrics.

## Features

- **FastAPI**: High-performance async API with OpenAPI docs
- **Async MongoDB (Motor)**: User/token storage
- **Keras/TensorFlow**: Image classification (runs in threadpool)
- **PIL**: Image processing
- **httpx**: Async image download
- **bcrypt**: Secure password hashing
- **Pydantic**: Settings and request/response validation
- **CORS**: Configurable origins
- **Prometheus**: Metrics endpoint
- **Structured Logging**: Production-ready logs
- **Docker**: Containerized deployment
- **Pytest**: Test suite
- **Health/Readiness**: `/healthz`, `/readyz` endpoints
- **Admin**: Secure admin password (bcrypt hash)
- **API Versioning**: `/v1` route prefix

## Endpoints

- `POST /v1/register` — Register new user
- `POST /v1/login` — Login and get token
- `POST /v1/classify` — Classify image (file upload or URL)
- `POST /v1/refill` — Admin: refill user tokens
- `GET /healthz` — Liveness probe
- `GET /readyz` — Readiness probe
- `GET /metrics` — Prometheus metrics

## Project Structure

```
app/
  main.py         # FastAPI app, CORS, health, metrics
  config.py       # Pydantic settings
  api/            # Routers, dependencies
  models/         # Pydantic schemas
  services/       # ML, DB, Auth, Logging
  ...
tests/            # Pytest test suite
```

## Configuration

Set environment variables or `.env` file:
- `MONGO_URI` — MongoDB connection string
- `ADMIN_PW_HASH` — Bcrypt hash of admin password
- `PORT` — App port (default: 8000)
- `CORS_ORIGINS` — Allowed CORS origins (comma-separated)
- `MODEL_PATH` — Path to Keras model
- `TOKEN_REFILL_AMOUNT` — Tokens to add per refill

## Running Locally

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
2. **Start MongoDB** (see `docker-compose.yaml`)
3. **Run the app**:
   ```bash
   uvicorn app.main:app --reload
   ```

## Docker

Build and run with Docker Compose:
```bash
docker-compose up --build
```

## Testing

Run tests with pytest:
```bash
pytest tests/
```

## Observability
- Prometheus metrics: `/metrics`
- Structured logs: JSON format

## Security
- Passwords hashed with bcrypt
- Admin endpoints require admin password hash
- CORS origins configurable

## License
MIT
