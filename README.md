# The Autonomous Editorial Board

Autonomous Editorial Board is a 4-agent, production-oriented content pipeline that
mimics a publishing house: research, writing, SEO optimization, and final editorial
polish are handled by specialized agents. The system integrates live web
research via Tavily, Groq (LLM) for writing, and CrewAI for orchestration. A
Streamlit UI provides a simple front-end for generating production-ready Markdown
articles.

## Features

- Lead Researcher: live web fact-gathering (Tavily) and source collection.
- Senior Writer: narrative drafting and tone control using the LLM.
- SEO Strategist: keyword recommendations, meta description, and header structure.
- Editor-in-Chief: merges outputs into a production-ready Markdown article.
- Streamlit app: UI for topic input, progress monitoring, and article preview/download.

## Quick start

1. Create a virtual environment and install dependencies:

```powershell
C:/path/to/python -m venv venv
venv\Scripts\activate
venv\Scripts\python.exe -m pip install -r requirements.txt
```

2. Populate secrets (do not commit `.env`):

```powershell
copy .env.example .env
# edit .env and provide your keys, or set them in the environment:
$env:GROQ_API_KEY = 'your_groq_api_key'
$env:TAVILY_API_KEY = 'your_tavily_api_key'
```

3. Run the Streamlit app (recommended):

```powershell
C:/Users/harsh/multi-agent-newsroom/venv/Scripts/python.exe -m streamlit run app.py
```

4. Or run the CLI pipeline directly:

```powershell
C:/Users/harsh/multi-agent-newsroom/venv/Scripts\python.exe src/newsroom/main.py
# or
echo "Topic here" | C:/Users/harsh/multi-agent-newsroom/venv/Scripts/python.exe src/newsroom/main.py
```

## Configuration

- `.env` values (see `.env.example`): `GROQ_API_KEY`, `TAVILY_API_KEY`, `MODEL_NAME`, `OUTPUT_DIR`.
- Output Markdown files are written to the `output/` folder by default.

## Security

- Never commit secrets. If you accidentally add API keys here, rotate them immediately.
- For production, use a secrets manager (GitHub Secrets, AWS Secrets Manager, etc.).

## Development notes

- The repo contains modular code under `src/newsroom/`:
  - `agents.py` — agent personalities and LLM/tool wiring
  - `tasks.py` — task definitions and expected deliverables
  - `main.py` — orchestration/engine and file saving
- `app.py` at project root launches the Streamlit UI.
- `requirements.txt` lists runtime dependencies.

## CI / Next steps

- Add a GitHub Actions workflow to run tests and linting on PRs.
- Add unit/integration tests that validate the pipeline (mock external calls).
- Optionally wire a small local LLM for offline generation in CI or development.

## License & Attribution

This repository is a starter scaffold — adapt licenses and attribution as
appropriate for your project and dependencies.

If you want, I can also add a basic GitHub Actions CI workflow and example tests.
Just tell me which CI checks you prefer.
