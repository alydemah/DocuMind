# DocuMind

AI-Powered Document Q&A Platform. Upload documents, ask questions, get cited answers.

## Features

- **Document Upload** - PDF, DOCX, TXT, Markdown with drag-and-drop
- **RAG Pipeline** - Automatic chunking, embedding, and vector search
- **Natural Language Q&A** - Ask questions, get answers with source citations
- **Pluggable LLM** - OpenAI, Anthropic Claude, or Ollama for fully local
- **Real-time Updates** - WebSocket-based processing status
- **Self-hosted** - Single `docker compose up`, no data leaves your infrastructure

## Tech Stack

| Layer | Technology |
|---|---|
| Monorepo | Turborepo + pnpm |
| Frontend | Vue 3 + TypeScript + Vite + Tailwind CSS + Pinia |
| Backend | Python 3.12+ + FastAPI + SQLAlchemy |
| RAG | LangChain + PyMuPDF + python-docx |
| Vector Store | Qdrant |
| Database | PostgreSQL 16 |
| Queue | Redis 7 + Celery |
| Python Tooling | uv |

## Quick Start

### Prerequisites

- Node.js 20+
- Python 3.12+
- pnpm (`corepack enable`)
- [uv](https://docs.astral.sh/uv/) (Python package manager)
- Docker (for PostgreSQL, Redis, Qdrant)

### Development Setup

```bash
# Clone and install
git clone https://github.com/your-username/documind.git
cd documind
pnpm install

# Start infrastructure services
docker compose up -d postgres redis qdrant

# Or if you already have PostgreSQL and Redis running locally,
# just start Qdrant:
docker run -d --name qdrant -p 6333:6333 qdrant/qdrant

# Setup Python backend
cd apps/api
uv sync --dev
cd ../..

# Configure environment
cp .env.example apps/api/.env
# Edit apps/api/.env - add your OpenAI API key (LLM_API_KEY and EMBEDDING_API_KEY)

# Create the database (if using a fresh PostgreSQL)
createdb documind  # or: psql -U postgres -c "CREATE DATABASE documind;"

# Run everything
pnpm dev
```

- Frontend: http://localhost:3000
- API: http://localhost:8000
- API Docs: http://localhost:8000/docs

### Production (Docker)

```bash
cp .env.example .env
# Edit .env - add your LLM API key and set APP_ENV=production

docker compose up -d
```

### Fully Local (No API Keys)

```bash
# Start all services including Ollama
docker compose --profile local up -d

# Pull the models
docker exec -it documind-ollama-1 ollama pull llama3.1
docker exec -it documind-ollama-1 ollama pull nomic-embed-text

# Update your .env:
# LLM_PROVIDER=ollama
# EMBEDDING_PROVIDER=ollama
```

## Project Structure

```
documind/
├── apps/
│   ├── web/          # Vue 3 frontend
│   └── api/          # Python FastAPI backend
├── packages/
│   ├── api-client/   # Shared TypeScript API client
│   ├── shared-types/ # Shared TypeScript types
│   ├── ui/           # Shared Vue components
│   └── config/       # Shared configs (eslint, tsconfig, tailwind)
├── docker-compose.yml
├── turbo.json
└── pnpm-workspace.yaml
```

## API

Full REST API with auto-generated docs at `/docs`.

| Endpoint | Description |
|---|---|
| `POST /api/v1/documents/upload` | Upload a document |
| `GET /api/v1/documents` | List documents |
| `POST /api/v1/documents/:id/process` | Re-process a document |
| `DELETE /api/v1/documents/:id` | Delete a document |
| `POST /api/v1/conversations` | Create conversation |
| `POST /api/v1/conversations/:id/ask` | Ask a question |
| `GET /api/v1/conversations/:id` | Get conversation with messages |
| `GET /api/v1/config` | Get current configuration |
| `PUT /api/v1/config` | Update configuration |
| `GET /api/v1/health` | Health check |
| `GET /api/v1/stats` | System stats |

## Configuration

Copy `.env.example` to `apps/api/.env` and configure. Key settings:

| Variable | Description | Default |
|---|---|---|
| `LLM_PROVIDER` | LLM backend (`openai`, `anthropic`, `ollama`) | `openai` |
| `LLM_API_KEY` | API key for the LLM provider | - |
| `EMBEDDING_PROVIDER` | Embedding backend (`openai`, `ollama`) | `openai` |
| `EMBEDDING_API_KEY` | API key for embeddings (can be same as LLM key) | - |
| `RAG_CHUNK_SIZE` | Text chunk size in tokens | `1000` |
| `RAG_TOP_K` | Number of chunks to retrieve per query | `5` |
| `RAG_SCORE_THRESHOLD` | Minimum similarity score for retrieval | `0.2` |

See `.env.example` for all options.

## License

MIT
