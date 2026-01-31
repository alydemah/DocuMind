# Configuration

All configuration is via environment variables. Copy `.env.example` to `.env`.

## LLM Providers

### OpenAI
```
LLM_PROVIDER=openai
LLM_MODEL=gpt-4o-mini
LLM_API_KEY=sk-...
```

### Anthropic
```
LLM_PROVIDER=anthropic
LLM_MODEL=claude-3-haiku-20240307
LLM_API_KEY=sk-ant-...
```

### Ollama (Local)
```
LLM_PROVIDER=ollama
OLLAMA_HOST=http://ollama:11434
OLLAMA_LLM_MODEL=llama3.1
```

## Embedding Providers

### OpenAI
```
EMBEDDING_PROVIDER=openai
EMBEDDING_MODEL=text-embedding-3-small
EMBEDDING_DIMENSIONS=1536
```

### Ollama
```
EMBEDDING_PROVIDER=ollama
OLLAMA_EMBED_MODEL=nomic-embed-text
```

## RAG Tuning

| Variable | Default | Description |
|---|---|---|
| `RAG_CHUNK_SIZE` | 1000 | Characters per chunk |
| `RAG_CHUNK_OVERLAP` | 200 | Overlap between chunks |
| `RAG_TOP_K` | 5 | Results to retrieve |
| `RAG_SCORE_THRESHOLD` | 0.7 | Minimum similarity score |
