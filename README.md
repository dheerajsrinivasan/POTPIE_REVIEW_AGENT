# Github Code Review Agent

An AI-powered system that automatically analyzes GitHub pull requests for:
- **Performance enhancement**
- **Improves Code style & formatting issues**
- **Checks for Potential bugs & errors**

Built with FastAPI, Celery, Redis, and LangGraph, supporting both OpenAI and Ollama LLMs.

## Features
- **Extensible**: Easy to add new analysis rules or LLM providers
- **Structured Output**: Consistent JSON results with issue categorization
- **Multi-LLM Support**: OpenAI or local Ollama models
- **GitHub Integration**: Fetches PR details, diffs, and changed files
- **Async Processing**: Celery + Redis handle background tasks

## Tech Stack
- **Database**: Redis (for task results)
- **Containerization**: Docker
- **Task Queue**: Celery + Redis
- **AI Framework**: LangGraph (for agent workflows)
- **LLM**: OpenAI or Ollama (local)
- **Backend**: FastAPI (Python)


## Prerequisites
- **Docker (for Redis)**
- **GitHub Personal Access Token (optional)**
- **Python 3.8+**
- **[Ollama](if using local LLMs)**




