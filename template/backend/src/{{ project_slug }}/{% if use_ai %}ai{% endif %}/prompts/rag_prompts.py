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

# DeepRAG prompts (arXiv:2502.01142)

DEEPRAG_DECOMPOSE_PROMPT = (
    "You are a question decomposition agent. Your task is to break down "
    "complex questions into atomic sub-queries that can be answered independently.\n\n"
    "Original question: {question}\n\n"
    "Previous reasoning steps:\n{previous_context}\n\n"
    "This is step {step_number}. Generate the next atomic sub-query that, "
    "when answered, will help build toward the final answer.\n\n"
    "Instructions:\n"
    "- Generate exactly ONE concise, specific sub-query.\n"
    "- The sub-query should be self-contained and answerable.\n"
    "- Build on information from previous steps.\n"
    "- If all necessary information has been gathered, output ONLY: DONE\n"
    "- Return ONLY the sub-query text, no explanations.\n\n"
    "Sub-query:"
)

DEEPRAG_ATOMIC_DECISION_PROMPT = (
    "You must decide whether to RETRIEVE external documents or use your "
    "PARAMETRIC knowledge to answer a sub-query.\n\n"
    "Original question: {question}\n"
    "Current sub-query: {sub_query}\n\n"
    "Instructions:\n"
    "- If the sub-query requires specific facts, dates, numbers, or recent "
    "information that you may not know accurately, output: RETRIEVE\n"
    "- If the sub-query asks about well-known general knowledge, definitions, "
    "or reasoning that you can confidently answer, output: PARAMETRIC\n"
    "- Output ONLY one word: RETRIEVE or PARAMETRIC\n\n"
    "Decision:"
)

DEEPRAG_PARAMETRIC_ANSWER_PROMPT = (
    "Answer the following sub-query using your knowledge.\n\n"
    "Sub-query: {sub_query}\n\n"
    "Instructions:\n"
    "- Provide a concise, factual answer.\n"
    "- If you are uncertain, state your uncertainty.\n"
    "- Be brief (1-3 sentences).\n\n"
    "Answer:"
)

DEEPRAG_SYNTHESIZE_PROMPT = (
    "You are a synthesis agent. Combine the reasoning chain below into "
    "a coherent final answer to the original question.\n\n"
    "Original question: {question}\n\n"
    "Reasoning chain:\n{reasoning_chain}\n\n"
    "Instructions:\n"
    "- Synthesize all intermediate answers into a single coherent response.\n"
    "- Ensure factual consistency across all steps.\n"
    "- If any intermediate answer is uncertain, reflect that in your final answer.\n"
    "- Be comprehensive but concise.\n\n"
    "Final answer:"
)
