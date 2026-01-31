# Contributing to DocuMind

## Development Setup

### Prerequisites

- Node.js 20+
- Python 3.12+
- pnpm (`corepack enable`)
- uv (Python package manager)
- Docker & Docker Compose

### Setup

```bash
# Clone
git clone https://github.com/your-username/documind.git
cd documind

# Install JS dependencies
pnpm install

# Start infrastructure
docker compose up -d postgres redis qdrant

# Setup Python
cd apps/api
uv sync --dev
uv run alembic upgrade head
cd ../..

# Run
pnpm dev
```

### Useful Commands

```bash
pnpm dev              # Start all apps
pnpm build            # Build everything
pnpm lint             # Lint all code
pnpm test             # Run all tests
pnpm type-check       # TypeScript + mypy

# Backend only
cd apps/api
uv run pytest         # Run tests
uv run ruff check src # Lint
uv run ruff format src # Format
```

### Project Architecture

- `apps/web` - Vue 3 SPA (Vite + Tailwind + Pinia)
- `apps/api` - Python FastAPI with RAG pipeline
- `packages/` - Shared TypeScript packages
- Turborepo manages builds and task orchestration

### Code Style

- TypeScript: ESLint + Prettier
- Python: Ruff (lint + format) + mypy (type checking)
- Vue: Composition API with `<script setup>`

### Pull Requests

1. Fork the repo
2. Create a feature branch
3. Make changes with tests
4. Run `pnpm lint && pnpm test`
5. Submit PR with clear description
