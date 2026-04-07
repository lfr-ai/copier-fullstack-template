"""RAG prompt templates — system, query, and synthesis prompts for RAG pipeline."""

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

# Self-CRAG prompts

RELEVANCE_GRADING_PROMPT = (
    "You are a grader assessing the relevance of a retrieved document to a user question.\n\n"
    "Retrieved document:\n{document}\n\n"
    "User question: {question}\n\n"
    "Instructions:\n"
    "- If the document contains keywords or semantic content related to the question, "
    "grade it as relevant.\n"
    "- Return ONLY a relevance score between 0.0 (completely irrelevant) and 1.0 "
    "(highly relevant).\n"
    "- Be strict: partial matches should score 0.4-0.6, strong matches 0.7-1.0.\n"
    "- Do not provide explanations, only output a single float value.\n\n"
    "Relevance score:"
)

QUERY_REWRITE_PROMPT = (
    "You are a query optimizer. The original query did not retrieve sufficiently "
    "relevant documents.\n\n"
    "Original query: {original_query}\n\n"
    "Instructions:\n"
    "- Rewrite the query to improve retrieval quality.\n"
    "- Add synonyms, expand abbreviations, or rephrase for clarity.\n"
    "- Preserve the original intent.\n"
    "- Return ONLY the rewritten query, no explanations.\n\n"
    "Rewritten query:"
)
