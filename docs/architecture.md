# Architecture

## High-Level Overview

```
┌─────────────┐    ┌──────────────┐    ┌────────────┐
│  Vue 3 SPA  │───>│  FastAPI     │───>│  Qdrant    │
│  Frontend   │    │  Backend     │    │  Vectors   │
└─────────────┘    └──────┬───────┘    └────────────┘
                          │
                   ┌──────┴───────┐
                   │              │
            ┌──────┴──┐    ┌─────┴────┐
            │ Postgres │    │  Redis   │
            │ Metadata │    │  Queue   │
            └─────────┘    └──────────┘
```

## RAG Pipeline

1. **Upload** - File received via REST API
2. **Extract** - Text extraction (PyMuPDF, python-docx)
3. **Chunk** - RecursiveCharacterTextSplitter with tiktoken
4. **Embed** - OpenAI/Ollama embeddings
5. **Store** - Vectors in Qdrant, metadata in PostgreSQL
6. **Query** - Embed question, vector search, LLM generation
7. **Cite** - Every answer includes source citations

## Key Design Decisions

- **Turborepo** - Incremental builds, parallel execution, shared packages
- **uv** - Fast Python dependency management, replaces pip/poetry
- **Qdrant** - Purpose-built vector DB, single Docker container
- **Celery + Redis** - Async document processing
- **Pluggable providers** - Swap LLM/embedding without code changes
