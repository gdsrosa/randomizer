# Randomizer API

A FastAPI-based REST API for generating random numbers and managing random items.

## Features

- **Random Number Generation**: Generate random numbers within specified ranges
- **Item Management**: Create, read, update, and delete items
- **Randomized Shuffling**: Get items in random order

## Project Structure

```bash
randomizer/
├── src/randomizer/
│   ├── __init__.py
│   ├── main.py           # FastAPI application entry point
│   ├── schemas.py        # Pydantic request/response models
│   ├── database.py       # In-memory item repository
│   └── routes/
│       ├── __init__.py
│       ├── random.py     # Random number endpoints
│       └── items.py      # Item CRUD endpoints
├── tests/
│   ├── __init__.py
│   ├── conftest.py       # Pytest fixtures
│   ├── test_random.py    # Tests for random endpoints
│   └── test_items.py     # Tests for item endpoints
├── pyproject.toml
├── Dockerfile
├── docker-compose.yml
└── README.md
```

## Installation

```bash
# Install dependencies
uv sync

# Install dev dependencies (for testing)
uv sync --group dev
```

## Running the Application

```bash
# Development mode with hot reload
uv run fastapi dev src/randomizer/main.py

# Production mode
uv run fastapi run src/randomizer/main.py
```

The API will be available at `http://localhost:8000`

## Docker

### Prerequisites

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/) (for local development)

### Local Development

```bash
# Build and run with hot reload
docker compose up

# Run in background
docker compose up -d

# View logs
docker compose logs -f

# Stop the container
docker compose down
```

The API will be available at `http://localhost:8000`

### Production Deployment (Render)

Connect your GitHub repository to [Render](https://render.com/) and use:

- **Build Command**: `docker build -t randomizer-api .`
- **Port**: `10000`

Render will automatically detect the health endpoint and configure SSL.

### Manual Docker Run

```bash
# Build the image
docker build -t randomizer-api .

# Run the container
docker run -p 8000:10000 randomizer-api
```

## API Documentation

Once running, visit:

- **Swagger UI**: <http://localhost:8000/docs>
- **ReDoc**: <http://localhost:8000/redoc>

## API Endpoints

### Random Playground

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Home endpoint |
| GET | `/random/{max_value}` | Get random number between 1 and max_value |
| GET | `/random-between/` | Get random number between min and max |

### Item Management

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/items` | Create a new item |
| GET | `/items` | Get all items (original and randomized order) |
| PUT | `/items/{item_id}` | Update an item |
| DELETE | `/items/{item_id}` | Delete an item |

## Testing

```bash
# Run all tests
uv run pytest

# Run tests with verbose output
uv run pytest -v

# Run tests with coverage
uv run pytest --cov=src
```

## Tech Stack

- **FastAPI**: Modern Python web framework
- **Pydantic**: Data validation using Python type annotations
- **pytest**: Testing framework
- **uv**: Package manager and build system
