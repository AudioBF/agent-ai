# 🤖 Agent AI

An AI conversational agent built with Tool Use (Function Calling), powered by LLaMA 3.3 via Groq. Ask anything in natural language — the agent decides which tools to use automatically.

**[Live Demo](https://agent-ai-ab.streamlit.app)**

---

## Features

- **Natural language understanding** — no hardcoded rules or if/else logic
- **Tool Use / Function Calling** — LLM decides when and how to use each tool
- **Country information** — real-time data from REST Countries API (any country in the world)
- **Math calculations** — safe symbolic computation with SymPy
- **Provider-agnostic** — swap LLM providers in one line via litellm
- **Unit tested** — 10 tests with mocks, no real API calls required

---

## Architecture

```
User
  ↓
Streamlit (frontend) — Streamlit Cloud
  ↓ POST /chat
FastAPI (backend) — Railway
  ↓
Agent Loop (Tool Use)
  ├── get_country_info() → REST Countries API
  └── calculate()        → SymPy
```

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | FastAPI + Uvicorn |
| Agent | litellm + Groq (LLaMA 3.3 70B) |
| Tools | httpx + SymPy |
| Frontend | Streamlit |
| Testing | pytest + unittest.mock |
| Deploy | Docker + Railway + Streamlit Cloud |

---

## Running Locally

**Prerequisites:** Python 3.10+, Groq API key ([free at console.groq.com](https://console.groq.com))

```bash
# Clone the repository
git clone https://github.com/AudioBF/agent-ai.git
cd agent-ai

# Create virtual environment
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env and add your GROQ_API_KEY

# Start backend (terminal 1)
uvicorn app.main:app --reload

# Start frontend (terminal 2)
streamlit run streamlit_app.py
```

Open `http://localhost:8501` to use the chat interface.  
Open `http://localhost:8000/docs` to explore the API.

---

## Running Tests

```bash
pytest tests/ -v
```

---

## Project Structure

```
agent-ai/
├── app/
│   ├── main.py           # FastAPI server
│   ├── agent.py          # Agent loop with Tool Use
│   ├── config.py         # Settings via Pydantic
│   ├── exceptions.py     # Custom exception hierarchy
│   └── tools/
│       ├── countries.py  # REST Countries API tool
│       └── calculator.py # SymPy math tool
├── tests/
│   ├── test_calculator.py
│   └── test_countries.py
├── streamlit_app.py      # Chat frontend
├── Dockerfile
└── requirements.txt
```

---

## Adding a New Tool

1. Create `app/tools/your_tool.py` with a Python function
2. Add the JSON Schema description to `TOOLS` in `app/agent.py`
3. Register the function in `TOOL_MAP` in `app/agent.py`

No other changes needed. The agent loop handles the rest automatically.

---

## License

MIT
