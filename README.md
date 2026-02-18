The Autonomous Editorial Board
===============================

Quick start
-----------

- Create a virtualenv and install dependencies:

```powershell
C:/path/to/python -m venv venv
venv\Scripts\activate
venv\Scripts\python.exe -m pip install -r requirements.txt
```

- Populate `.env` from `.env.example` (do not commit secrets):

```powershell
copy .env.example .env
# then edit .env to add your keys, or export them into the session:
$env:GROQ_API_KEY = 'your_groq_api_key'
$env:TAVILY_API_KEY = 'your_tavily_api_key'
```

- Run the pipeline interactively:

```powershell
C:/Users/harsh/multi-agent-newsroom/venv/Scripts/python.exe src/newsroom/main.py
```

Or pipe a single-line topic:

```powershell
echo "The future of AI in journalism" | C:/Users/harsh/multi-agent-newsroom/venv/Scripts/python.exe src/newsroom/main.py
```

What I changed to improve the project
------------------------------------
- Removed stored API keys from `.env` (they were present). Please rotate the exposed keys immediately.
- Added this README with run/security notes.
- Improved the mock fallback to produce richer, deterministic test output so you can validate the pipeline without live LLM access.

Security note
-------------
If you previously pasted real API keys into this project, rotate them now at the provider dashboard. Never commit `.env` to version control. Use secrets managers for production.

Next steps I can take
---------------------
- Help debug the Groq/crewai client error for live LLM runs.
- Add unit tests and CI config to validate the pipeline on each change.
- Replace the mock fallback with a local small model runner for offline generation.
