# Simple Rag System 

This is a personal project for learning how to get from a folder of documents of different kind to a ready rag system using llms for code generation to speed up the learning and developing steps

The suggested architecture is

                ┌─────────────────────────────────────┐
                │             User / Client           │
                │  (Web UI, API, Chatbot, Teams bot)  │
                └─────────────────────────────────────┘
                                │
                                ▼
                ┌─────────────────────────────────────┐
                │          Frontend / API Layer        │
                │   - Streamlit / Gradio (chat UI)     │
                │   - FastAPI (REST API, Teams, Slack) │
                └─────────────────────────────────────┘
                                │
                                ▼
                ┌─────────────────────────────────────┐
                │      Orchestration / RAG Engine      │
                │   - LangChain or LlamaIndex          │
                │   - Defines pipeline:                │
                │     Query → Retrieve → Prompt → LLM  │
                └─────────────────────────────────────┘
                                │
                                ▼
        ┌──────────────┐   ┌──────────────────────┐   ┌───────────────┐
        │ Ingestion     │   │ Embeddings           │   │ Vector Store   │
        │ (Docker svc)  │   │ (HF models / TEI)    │   │ Qdrant/Milvus  │
        │ - Unstructured│   │ - SentenceTransformers│  │ Weaviate/FAISS │
        │ - Apache Tika │   │ - BGE / MiniLM       │   │                │
        └──────────────┘   └──────────────────────┘   └───────────────┘
                                │
                                ▼
                ┌─────────────────────────────────────┐
                │        LLM Inference Service        │
                │ - Llama 3 / Mistral / Falcon        │
                │ - Served with Ollama / vLLM / TGI   │
                └─────────────────────────────────────┘
                                │
                                ▼
                ┌─────────────────────────────────────┐
                │          Response to User            │
                │    (Answer grounded in documents)    │
                └─────────────────────────────────────┘
