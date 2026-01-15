SYSTEM_PROMPT = """You are DocuMind, a document Q&A assistant. Answer questions based ONLY on
the provided context. If the answer is not in the context, say
"I don't have enough information in the uploaded documents to answer this."

Always cite your sources using [Source: filename, page X] format."""

QA_PROMPT_TEMPLATE = """## Context
{context}

## Conversation History
{chat_history}

## Question
{question}

## Instructions
- Answer accurately based on the context above
- Quote relevant passages when helpful
- Cite every claim with [Source: filename, page X]
- If multiple documents are relevant, synthesize across them
- If unsure, say so — never fabricate information"""


def build_context(chunks: list[dict]) -> str:
    context_parts = []
    for chunk in chunks:
        source = f"[Source: {chunk['document_name']}"
        if chunk.get("page_number"):
            source += f", page {chunk['page_number']}"
        source += "]"

        context_parts.append(f"{source}\n{chunk['content']}")

    return "\n\n---\n\n".join(context_parts)


def build_chat_history(messages: list[dict]) -> str:
    if not messages:
        return "No previous conversation."

    history_parts = []
    for msg in messages[-10:]:
        role = "User" if msg["role"] == "user" else "Assistant"
        content = msg["content"][:500]
        history_parts.append(f"{role}: {content}")

    return "\n".join(history_parts)


def build_qa_prompt(
    question: str,
    chunks: list[dict],
    chat_history: list[dict],
) -> str:
    context = build_context(chunks)
    history = build_chat_history(chat_history)

    return QA_PROMPT_TEMPLATE.format(
        context=context,
        chat_history=history,
        question=question,
    )
