# Deployment

## Docker Compose (Recommended)

```bash
cp .env.example .env
# Edit .env with your settings
docker compose up -d
```

This starts all services: frontend, backend, worker, PostgreSQL, Redis, Qdrant.

## Environment Variables

See `.env.example` for full list. Key variables:

| Variable | Required | Description |
|---|---|---|
| `LLM_API_KEY` | Yes* | API key for OpenAI/Anthropic (*not needed for Ollama) |
| `POSTGRES_PASSWORD` | Yes | Database password |
| `APP_SECRET_KEY` | Yes | Random secret for signing |

## Ports

| Service | Port |
|---|---|
| Frontend | 3000 |
| Backend API | 8000 |
| PostgreSQL | 5432 |
| Redis | 6379 |
| Qdrant | 6333 |

## Data Persistence

Docker volumes store persistent data:
- `postgres_data` - Database
- `redis_data` - Cache/queue
- `qdrant_data` - Vector embeddings
- `upload_data` - Uploaded files

## Fully Local Setup

Use Ollama for LLM and embeddings with no API keys:

```bash
# Set in .env:
LLM_PROVIDER=ollama
EMBEDDING_PROVIDER=ollama
OLLAMA_HOST=http://ollama:11434

# Uncomment ollama in docker-compose.yml
docker compose up -d
```
