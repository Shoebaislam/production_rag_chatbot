# Production RAG Chatbot

A production-style Retrieval-Augmented Generation chatbot built with React, FastAPI, Qdrant, Redis, Docker, and Ollama.

## Features

- Upload `.txt` documents
- Split documents into chunks
- Generate embeddings with Ollama
- Store vectors in Qdrant
- Retrieve relevant context from Qdrant
- Generate answers using a local LLM
- Cache repeated questions with Redis
- React frontend chat interface
- Docker Compose setup for backend, Qdrant, and Redis

## Tech Stack

### Frontend
- React
- Vite
- Axios

### Backend
- FastAPI
- LangChain
- Ollama
- Qdrant
- Redis
- Docker

## Architecture

```text
React Frontend
    ↓
FastAPI Backend
    ↓
Redis Cache
    ↓
Qdrant Vector Database
    ↓
Ollama Embeddings + Local LLM
