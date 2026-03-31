# AI Module — LLM, RAG, Embeddings, Knowledge Graphs & MCP

Full AI/ML integration layer following Clean Architecture principles. All components
depend on domain interfaces (protocols) — concrete implementations are injected at the
composition root. LiteLLM is the universal LLM and embedding backend; the model string prefix routes
to the correct provider (OpenAI, Azure OpenAI, Anthropic, etc.) automatically.

## Architecture

```text
ai/
├── agents/               # Autonomous agent definitions
│   ├── base_agent.py           # Abstract base agent
│   ├── react_agent.py          # ReAct reasoning agent
│   ├── tool_calling_agent.py   # Structured tool-calling agent
│   └── langgraph_orchestrator.py  # Multi-agent LangGraph workflow
├── chains/               # LangChain & LlamaIndex adapters
│   ├── base_chain.py           # Base chain abstraction
│   ├── conversational_rag.py   # Conversational RAG chain
│   ├── langchain_adapter.py    # LangChain → LLMGateway bridge
│   ├── llamaindex_adapter.py   # LlamaIndex document loader & chunker
│   ├── refinement_chain.py     # Answer refinement chain
│   └── summarization_chain.py  # Summarization chain
├── config.py             # AI settings and defaults
├── document_loaders/     # File & web document loaders
│   ├── azure_doc_intelligence_loader.py  # Azure Document Intelligence
│   ├── file_loader.py          # PDF, DOCX, text → DocumentLoaderGateway
│   └── web_loader.py           # URL-based document loading
├── embeddings/           # Text embedding adapters
│   ├── litellm_embeddings.py          # LiteLLM → EmbeddingGateway (universal)
│   └── sentence_transformer_embeddings.py  # Local models
├── evaluation/           # LLM-based evaluation
│   └── llm_judge.py            # LLM judge evaluator
├── guardrails/           # Content safety
│   └── rule_based.py           # Rule-based guardrail (PII, injection)
├── knowledge_graph/      # Graph-based knowledge storage
│   ├── __init__.py             # NetworkX → KnowledgeGraphGateway
│   ├── neo4j_adapter.py        # Neo4j → KnowledgeGraphGateway
│   ├── rdflib_adapter.py       # RDFLib/SPARQL → KnowledgeGraphGateway
│   ├── llm_extractor.py        # LLM-based entity/relation extraction
│   └── external_connectors.py  # Wikidata, DBpedia, ConceptNet
├── llm/                  # LLM provider adapters
│   ├── base_llm_adapter.py     # Abstract base (conforms to LLMGateway)
│   ├── litellm_adapter.py      # LiteLLM → LLMGateway (universal backend)
│   ├── gateway.py              # Multi-provider gateway with failover
│   └── anthropic_adapter.py    # Anthropic Claude → LLMGateway (via LiteLLM)
├── mcp/                  # Model Context Protocol server & client
│   ├── server.py               # FastMCP tools, resources, prompts
│   └── client.py               # MCP client for remote servers
├── memory/               # Conversation memory stores
│   ├── in_memory.py            # In-memory conversation memory
│   ├── postgres_memory.py      # PostgreSQL-backed memory
│   └── redis_memory.py         # Redis-backed memory
├── models/               # Pydantic request/response models
├── observability/        # AI observability
│   └── structlog_adapter.py    # Structured logging for AI calls
├── prompts/              # Prompt template manager
│   ├── manager.py              # Jinja2-based prompt registry
│   ├── jinja2_templates.py     # Jinja2 prompt templates
│   └── rag_prompts.py          # RAG-specific prompt templates
├── rag/                  # RAG pipeline
│   ├── ingestion.py            # Load → split → embed → store
│   ├── retrieval.py            # Query → search → generate
│   ├── rerankers/              # Cross-encoder reranking
│   │   └── cross_encoder.py      # Cross-encoder reranker
│   └── retrievers/             # Vector, graph, ensemble, RRF
│       ├── vector_retriever.py    # Vector similarity retriever
│       ├── graph_retriever.py     # Knowledge graph retriever
│       ├── ensemble_retriever.py  # Multi-strategy ensemble
│       ├── _rrf.py                # Reciprocal Rank Fusion scorer
│       └── llamaindex_retriever.py  # LlamaIndex retriever (conditional)
├── services/             # AI application services
│   └── __init__.py             # AIService, RAGService
├── text_splitter.py      # Recursive character text splitter
├── tools/                # Agent tool integrations
│   ├── base_tool.py            # Abstract tool base
│   ├── calculator.py           # Calculator tool
│   ├── database_query.py       # Database query tool
│   ├── ingest_tool.py          # Document ingestion tool
│   ├── search_tool.py          # Semantic search tool
│   └── web_search.py           # Web search tool
├── vector_stores/        # Vector store adapters
│   ├── azure_ai_search_store.py  # Azure AI Search → VectorStoreGateway
│   ├── faiss_store.py          # FAISS → VectorStoreGateway
│   └── pgvector_store.py       # pgvector → VectorStoreGateway
├── workflows/            # LangGraph workflow engine
│   ├── checkpointers.py        # SQLite/memory/postgres checkpointers
│   └── langgraph_engine.py     # LangGraph workflow engine
└── __init__.py
```

## Domain Interfaces (core/interfaces/)

| Interface                    | File                                     | Purpose                                            |
| ---------------------------- | ---------------------------------------- | -------------------------------------------------- |
| `LLMGateway`                 | `core/interfaces/llm.py`                 | LLM completion & streaming                         |
| `EmbeddingGateway`           | `core/interfaces/embedding.py`           | Text → vector embeddings                           |
| `VectorStoreGateway`         | `core/interfaces/vector_store.py`        | Similarity search & storage                        |
| `RetrieverGateway`           | `core/interfaces/retriever.py`           | Unified document retrieval                         |
| `DocumentLoaderGateway`      | `core/interfaces/document_loader.py`     | Document ingestion                                 |
| `TextSplitterGateway`        | `core/interfaces/text_splitter.py`       | Document chunking                                  |
| `ConversationMemoryGateway`  | `core/interfaces/conversation_memory.py` | Chat history storage                               |
| `KnowledgeGraphGateway`      | `core/interfaces/knowledge_graph.py`     | Graph CRUD & traversal                             |
| `SPARQLQueryGateway`         | `core/interfaces/knowledge_graph.py`     | SPARQL query execution (RDFLib)                    |
| `ExternalKnowledgeGraphGateway` | `core/interfaces/knowledge_graph.py`  | External KG lookup (Wikidata, DBpedia, ConceptNet) |
| `MCPServerGateway`           | `core/interfaces/mcp_server.py`          | MCP server lifecycle                               |
| `AgentOrchestratorGateway`   | `core/interfaces/agent_orchestrator.py`  | Multi-agent orchestration                          |
| `GuardrailGateway`           | `core/interfaces/guardrail.py`           | Content safety / guardrails                        |
| `RerankerGateway`            | `core/interfaces/reranker.py`            | Search result reranking                            |

## Application Services

| Service                 | File                                              | Purpose                       |
| ----------------------- | ------------------------------------------------- | ----------------------------- |
| `IngestionService`      | `application/services/ingestion_service.py`       | Document ingestion pipeline   |
| `AgentService`          | `application/services/agent_service.py`           | Agent execution orchestration |
| `MCPService`            | `application/services/mcp_service.py`             | MCP server/client management  |
| `KnowledgeGraphService` | `application/services/knowledge_graph_service.py` | KG construction & querying    |

## Key Dependencies

| Package            | Version | Purpose                                                        |
| ------------------ | ------- | -------------------------------------------------------------- |
| `litellm`          | ≥1.90   | Universal LLM/embedding proxy (OpenAI, Azure, Anthropic, etc.) |
| `openai`           | ≥1.80   | OpenAI / Azure OpenAI API client                               |
| `langchain`        | ≥0.4    | LangChain agent framework                                      |
| `langchain-core`   | ≥0.4    | LangChain core abstractions                                    |
| `langchain-openai` | ≥1.0    | LangChain OpenAI integration                                   |
| `langgraph`        | ≥1.3    | LangGraph multi-agent orchestration                            |
| `llama-index-core` | ≥0.14   | LlamaIndex data framework                                      |
| `faiss-cpu`        | ≥1.14   | FAISS vector similarity search                                 |
| `networkx`         | ≥3.4    | In-memory knowledge graphs (lightweight)                       |
| `neo4j`            | ≥5.26   | Neo4j graph database driver                                    |
| `rdflib`           | ≥7.0    | RDF/SPARQL knowledge graph support                             |
| `SPARQLWrapper`    | ≥2.0    | SPARQL endpoint client (Wikidata, DBpedia)                     |
| `mcp[cli]`         | ≥1.30   | Model Context Protocol SDK                                     |
| `anthropic`        | ≥0.52   | Anthropic Claude SDK                                           |

## Usage

AI dependencies are included automatically when the template is generated with
`use_ai=true`. Install all project dependencies:

```bash
uv sync --all-groups
```

### RAG Pipeline

```python
from {{ project_slug }}.ai.services import RAGService
from {{ project_slug }}.ai.embeddings.litellm_embeddings import LiteLLMEmbeddingAdapter
from {{ project_slug }}.ai.vector_stores.faiss_store import FaissVectorStore
from {{ project_slug }}.ai.llm.litellm_adapter import LiteLLMAdapter
from {{ project_slug }}.ai.text_splitter import RecursiveTextSplitter
from {{ project_slug }}.ai.chains.llamaindex_adapter import LlamaIndexDocumentLoader

rag = RAGService(
    llm=LiteLLMAdapter(model="gpt-4o", api_key="..."),
    embedding=LiteLLMEmbeddingAdapter(model="text-embedding-3-small", api_key="..."),
    vector_store=FaissVectorStore(dimension=1536),
    loader=LlamaIndexDocumentLoader(),
    splitter=RecursiveTextSplitter(),
)
```

### MCP Server

```bash
python -m {{ project_slug }}.ai.mcp.server
```

### API Endpoints

| Method | Path                         | Description                  |
| ------ | ---------------------------- | ---------------------------- |
| POST   | `/api/v1/ai/completions`     | LLM text completion          |
| POST   | `/api/v1/ai/rag/query`       | RAG question answering       |
| POST   | `/api/v1/ai/rag/ingest`      | Document ingestion           |
| POST   | `/api/v1/ai/search`          | Semantic vector search       |
| POST   | `/api/v1/agents/run`         | Single agent execution       |
| POST   | `/api/v1/agents/orchestrate` | Multi-agent orchestration    |
| GET    | `/mcp`                       | MCP server (streamable-http) |
