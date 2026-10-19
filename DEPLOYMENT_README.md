# LeadIQ — Streamlit Community Cloud deployment copy

This folder is prepared for deploying the LeadIQ dashboard to Streamlit Community Cloud.

## Before deployment
1. Review all files and confirm this is the source version you intend to share.
2. Do not upload `.env`, API keys, local databases, or customer data. `.gitignore` excludes `.env` and `leadiq.db`.
3. Use only synthetic inquiries for the public assessment demo.

## Deploy the dashboard
1. Create a GitHub repository named `leadiq-assessment` (public is simplest for a freely viewable demo; this means the source code is also public).
2. Upload the contents of this folder to the repository root, including `app.py`, `lead_analyzer.py`, `ml_model.py`, `database.py`, `prompts.py`, `requirements.txt`, and `README.md`.
3. Do not upload your local `.env` file or `.venv` folder.
4. Visit https://share.streamlit.io/ and sign in with GitHub.
5. Choose **Create app**, select the repository and branch (usually `main`), and set the main file path to `app.py`.
6. In **Advanced settings / Secrets**, add the following TOML values (replace the model only if your account has a different supported model):

```toml
OPENAI_API_KEY = "YOUR_GEMINI_API_KEY"
OPENAI_MODEL = "gemini-3.8-flash"
```

7. Deploy, wait for the build to finish, then open the generated `https://...streamlit.app` URL.
8. Test with a synthetic inquiry. Confirm the UI says `LLM mode (...)`, not rule-based fallback.

## Important caveats
- The `OPENAI_API_KEY` name is retained because the code uses the OpenAI-compatible SDK interface; the value should be your Gemini API key.
- Never put the real key in a GitHub file, screenshot, report, or chat. If exposed, revoke it and create a new one.
- SQLite storage on hosted app instances should be treated as demo-only; local files may not be durable across restarts/redeployments. Do not store real customer data.
- This step deploys the Streamlit dashboard. It does not deploy the FastAPI service. Deploy the API separately (e.g. as a Python web service) only if you need a public API URL.
- A public GitHub repository makes the source code public. If you do not want to publish source, review the host's current private-repository access limits before proceeding.
- The ML readiness model uses only 16 synthetic examples and its observed exploratory cross-validation accuracy was 50%; do not present it as production-grade or as a conversion probability.
