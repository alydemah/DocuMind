# API Reference

Base URL: `http://localhost:8000/api/v1`

## Documents

### Upload Document
```
POST /documents/upload
Content-Type: multipart/form-data

file: <binary>
```

### List Documents
```
GET /documents?page=1&page_size=20
```

### Get Document
```
GET /documents/:id
```

### Delete Document
```
DELETE /documents/:id
```

### Get Document Chunks
```
GET /documents/:id/chunks
```

## Conversations

### Create Conversation
```
POST /conversations
{"title": "optional title"}
```

### List Conversations
```
GET /conversations
```

### Ask Question
```
POST /conversations/:id/ask
{
  "question": "What are the key findings?",
  "options": {
    "top_k": 5,
    "score_threshold": 0.7,
    "document_filter": ["doc-uuid"]
  }
}
```

## System

### Health Check
```
GET /health
```

### System Stats
```
GET /stats
```

### Configuration
```
GET /config
PUT /config
```

## WebSocket

### Processing Status
```
WS /ws/processing/:document_id
```

### Chat Stream
```
WS /ws/chat/:conversation_id
```
