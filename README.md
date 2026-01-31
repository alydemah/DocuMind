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
| Backend | Python 3.12 + FastAPI + SQLAlchemy |
| RAG | LangChain + PyMuPDF + python-docx |
| Vector Store | Qdrant |
| Database | PostgreSQL 16 |
| Queue | Redis 7 + Celery |
| Python Tooling | uv |

## Quick Start

### Production (Docker)

```bash
git clone https://github.com/your-username/documind.git
cd documind
cp .env.example .env
# Edit .env - add your LLM API key

docker compose up -d
```

- Frontend: http://localhost:3000
- API: http://localhost:8000
- API Docs: http://localhost:8000/docs

### Development

```bash
# Prerequisites: Node.js 20+, Python 3.12+, pnpm, uv
corepack enable
pnpm install

# Start infrastructure
docker compose up -d postgres redis qdrant

# Setup Python backend
cd apps/api
uv sync --dev
uv run alembic upgrade head
cd ../..

# Run everything
pnpm dev
```

### Fully Local (No API Keys)

```bash
# Uncomment ollama service in docker-compose.yml, then:
docker compose up -d

docker exec -it documind-ollama-1 ollama pull llama3.1
docker exec -it documind-ollama-1 ollama pull nomic-embed-text

# Update .env:
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
| `POST /api/v1/conversations` | Create conversation |
| `POST /api/v1/conversations/:id/ask` | Ask a question |
| `GET /api/v1/health` | Health check |
| `GET /api/v1/stats` | System stats |

## Configuration

Copy `.env.example` to `.env` and configure. Key settings:

- `LLM_PROVIDER` - `openai`, `anthropic`, or `ollama`
- `EMBEDDING_PROVIDER` - `openai`, `ollama`, or `local`
- `RAG_CHUNK_SIZE` - Text chunk size (default: 1000)
- `RAG_TOP_K` - Number of chunks to retrieve (default: 5)

See `.env.example` for all options.

## License

MIT
