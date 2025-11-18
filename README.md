# Autonomous Code Review Agent

An AI-powered system that automatically analyzes GitHub pull requests for:
- **Code style** & formatting issues
- **Potential bugs** & errors
- **Performance** improvements
- **Best practices** violations

Built with FastAPI, Celery, Redis, and LangGraph, supporting both OpenAI and Ollama LLMs.

## Features

- **Async Processing**: Celery + Redis handle background tasks
- **Multi-LLM Support**: OpenAI or local Ollama models
- **GitHub Integration**: Fetches PR details, diffs, and changed files
- **Structured Output**: Consistent JSON results with issue categorization
- **Extensible**: Easy to add new analysis rules or LLM providers

## Tech Stack

- **Backend**: FastAPI (Python)
- **Task Queue**: Celery + Redis
- **AI Framework**: LangGraph (for agent workflows)
- **LLM**: OpenAI or Ollama (local)
- **Database**: Redis (for task results)
- **Containerization**: Docker

## Prerequisites

- Python 3.8+
- Docker (for Redis)
- [Ollama](https://ollama.ai/download) (if using local LLMs)
- GitHub Personal Access Token (optional)

## Setup & Installation

### 1. Clone the Repository
```bash
git clone https://github.com/Jitsu-13/Code-Review-Agent
cd code-review-agent

### 2. Set Up Environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

### 3. Install Dependencies
pip install -r requirements.txt

### 4. Create .env file:

# Required
GITHUB_TOKEN=your_github_token
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0

# LLM Configuration (choose one)
LLM_PROVIDER=ollama  # or "openai"
LLM_MODEL=codellama  # e.g., "gpt-4" for OpenAI

# Only if using OpenAI
OPENAI_API_KEY=your_openai_key

Running Locally

Start Redis (in a separate terminal):

bash
docker run -p 6379:6379 redis
Start Celery Worker:

bash
celery -A app.tasks.analyze_pr worker --loglevel=info
Run FastAPI Server:

bash
uvicorn app.main:app --reload

The API will be available at http://localhost:8000

API Endpoints 📡
Endpoint	Method	Description
/analyze-pr	POST	Submit a PR for analysis
/status/<task_id>	GET	Check task status
/results/<task_id>	GET	Get analysis results

