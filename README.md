# LeadIQ — Client Assessment Package

LeadIQ is a proof of concept for AI-assisted project inquiry intake. It extracts structured fields from free-text inquiries, identifies missing information, produces a readiness category, drafts a follow-up, and stores results.

## Current evidence status
- Streamlit UI: screenshots included in `../evidence/`.
- Gemini LLM mode: observed in the screenshot `02_llm_analysis_results.png`.
- Database save: observed in `03_database_save_confirmation.png`.
- FastAPI `/analyze`: the developer reported a successful local smoke test. No screenshot of the Swagger/API response was captured in the evidence set; reproduce using the steps below.
- Automated tests: 6 passed in the reported test run. A pytest cache permission warning was also reported.
- ML evaluation: 3-fold cross-validation accuracy 0.50, macro F1 0.41, on only 16 synthetic examples. This is exploratory and not a production benchmark.

## Setup
Python 3.10+ is recommended. From this folder:

```powershell
python -m pip install -r requirements.txt
Copy-Item .env.example .env
```

Edit `.env` locally. For Gemini OpenAI-compatible mode:
- `OPENAI_API_KEY` = Gemini API key
- `OPENAI_MODEL` = a currently available Gemini model, e.g. `gemini-3.8-flash` if enabled for your account
- Never commit `.env` or include it in client submissions.

## Run Streamlit
```powershell
python -m streamlit run app.py
```

## Run FastAPI in a second terminal
```powershell
python -m uvicorn api:app --reload
```
Open `http://127.0.0.1:8000/docs`, test `GET /health`, then `POST /analyze`.

## Run tests and exploratory evaluation
```powershell
python -m pytest -q
python .\evaluate_model.py
```

## Limitations and safe use
The classifier is trained on 16 synthetic examples and achieved 50% exploratory cross-validation accuracy in the recorded evaluation. Do not describe its output as conversion probability or production-grade qualification. Use synthetic inquiries for demos, review LLM outputs, and require human approval before sending customer-facing messages. This package is a local PoC, not a production deployment.
