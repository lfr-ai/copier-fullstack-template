"""RAG prompt templates — system, query, and synthesis prompts for RAG pipeline."""

from __future__ import annotations

RAG_SYSTEM_PROMPT = (
    "You are a knowledgeable assistant. Answer questions accurately "
    "based on the provided context. If the context does not contain "
    "enough information, say so honestly rather than guessing."
)

RAG_QUERY_PROMPT = (
    "Answer the following question using ONLY the provided context.\n\n"
    "Context:\n{context}\n\n"
    "Question: {question}\n\n"
    "Instructions:\n"
    "- Base your answer solely on the provided context.\n"
    "- If the context doesn't contain the answer, state that clearly.\n"
    "- Cite relevant parts of the context.\n"
    "- Be concise and accurate.\n\n"
    "Answer:"
)

RAG_CONDENSE_PROMPT = (
    "Given the following conversation history and a follow-up question, "
    "reformulate the follow-up question to be a standalone question that "
    "captures all necessary context.\n\n"
    "Chat history:\n{chat_history}\n\n"
    "Follow-up question: {question}\n\n"
    "Standalone question:"
)

RAG_REFINE_PROMPT = (  # FIXME: unused — wire into a refine-chain or remove
    "We have an existing answer to a question:\n{existing_answer}\n\n"
    "We have the opportunity to refine the answer with new context:\n{context}\n\n"
    "Given the new context, refine the original answer to better address "
    "the question: {question}\n\n"
    "If the new context isn't useful, return the original answer unchanged.\n\n"
    "Refined answer:"
)
