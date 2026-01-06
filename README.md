# 🔍 Multi-Source Retrieval-Augmented Generation (RAG) System

This project implements a **multi-source Retrieval-Augmented Generation (RAG) pipeline**
that retrieves relevant context from **documentation, blogs, and forum discussions**
and augments LLM responses with grounded, up-to-date knowledge.

The system is designed to handle:
- Noisy real-world text (forums, blogs)
- Conflicting information across sources
- Context ranking and relevance filtering before LLM generation

## 🚀 Key Features
- Multi-source ingestion (docs, blogs, forums)
- Intelligent text chunking
- Embedding-based semantic search
- Vector index construction
- Context reranking
- Contradiction detection across sources
- LLM-augmented answer generation

## 🏗️ System Architecture & Flow

The RAG pipeline follows a modular, multi-stage architecture:

1. **Data Ingestion**
   - Sources: documentation, blogs, and forum discussions
   - Each source is treated independently to preserve context

2. **Text Chunking**
   - Long documents are split into semantically meaningful chunks
   - Ensures better embedding quality and retrieval accuracy

3. **Embedding Generation**
   - Each chunk is converted into a dense vector representation
   - Enables semantic similarity search instead of keyword matching

4. **Vector Index Construction**
   - Embeddings are stored in a vector index
   - Allows fast nearest-neighbor retrieval at query time

5. **Retrieval & Reranking**
   - Top-k relevant chunks are retrieved
   - Results are reranked to prioritize the most relevant context

6. **Contradiction Detection**
   - Retrieved chunks are analyzed for conflicting information
   - Helps prevent hallucinations and inconsistent answers

7. **LLM-Augmented Response Generation**
   - Final context is passed to the LLM
   - The response is generated using grounded, retrieved knowledge

