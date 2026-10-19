# LeadIQ — AI-Powered Project Inquiry Intelligence

**An AI/ML proof of concept for structured inquiry extraction, lead readiness assessment, and intelligent follow-up recommendations.**

[Live Demo](https://leadiq-cynbit-assessment-i9ktmtrt3zvyrjljwurlcz.streamlit.app/) · [GitHub Repository](https://github.com/suryaprakashpolkam/leadiq-cynbit-assessment)

## 1. Overview

LeadIQ demonstrates how AI and machine learning can help process unstructured project inquiries and support more consistent lead qualification.

The application accepts a project inquiry in natural language, extracts relevant business requirements, identifies missing information, categorizes readiness, and drafts a suggested follow-up response for human review.

The solution is designed as a proof of concept for AI-assisted inquiry intake and qualification workflows.

## 2. Problem Statement

Project inquiries often arrive as free-text messages containing incomplete or ambiguous requirements. Manually reviewing every inquiry can require repetitive effort and make it harder to identify the information needed for an effective discovery conversation.

LeadIQ explores an AI-assisted workflow to:

- Convert free-text inquiries into structured information.
- Extract requested services, requirements, budget, and timeline.
- Identify missing details that need clarification.
- Categorize inquiry readiness using a lightweight ML classifier and deterministic guardrails.
- Generate a suggested follow-up response.
- Store analysis records for review.

These are proposed workflow improvements demonstrated by the prototype, not claims about Cynbit's internal operations.

## 3. Key Features

- **AI-powered information extraction:** Uses Gemini through an OpenAI-compatible SDK interface when configured.
- **Structured output:** Uses Pydantic models to organize extracted inquiry information.
- **Missing-information detection:** Highlights details required for a more useful discovery conversation.
- **ML-based readiness classification:** Uses TF-IDF text features and Logistic Regression to explore readiness categorization.
- **Rule-based guardrails:** Applies deterministic checks to reduce inappropriate readiness classifications.
- **Follow-up drafting:** Produces a suggested response for human review.
- **Database persistence:** Uses SQLAlchemy with SQLite by default to store analysis records.
- **Interactive dashboard:** Provides a Streamlit interface for submitting inquiries and reviewing results.
- **REST API:** Includes FastAPI endpoints for health checks, inquiry analysis, and retrieving saved analyses.

## 4. Technology Stack

| Component | Technology |
|---|---|
| Programming language | Python |
| User interface | Streamlit |
| LLM integration | Gemini via OpenAI-compatible SDK |
| Structured extraction | Pydantic |
| Machine learning | Scikit-learn |
| Text representation | TF-IDF |
| Classification | Logistic Regression |
| API | FastAPI |
| Database access | SQLAlchemy |
| Default database | SQLite |
| Testing | Pytest |
| Deployment | Streamlit Community Cloud |

## 5. Architecture

```text
User Inquiry
     |
     v
Streamlit Interface
     |
     v
AI Extraction and Validation
(Gemini + Pydantic)
     |
     v
Structured Inquiry Fields
     |
     v
ML Readiness Classifier
(TF-IDF + Logistic Regression)
     |
     v
Deterministic Guardrails
     |
     v
Readiness Category and
Missing Information
     |
     v
Suggested Follow-up Response
     |
     v
SQLAlchemy / SQLite Storage
```

The FastAPI module provides a separate programmatic interface to the analysis functionality.

## 6. Project Structure

```text
leadiq-cynbit-assessment/
├── app.py
├── lead_analyzer.py
├── ml_model.py
├── prompts.py
├── database.py
├── api.py
├── evaluate_model.py
├── requirements.txt
├── README.md
├── DEPLOYMENT_README.md
├── data/
└── tests/
```

## 7. Getting Started

### Prerequisites

- Python 3.10 or a compatible newer version.
- pip.
- A Gemini API key for LLM-powered analysis. Without a configured key, the application may use its rule-based fallback where supported.

### Installation

Clone the repository:

```bash
git clone https://github.com/suryaprakashpolkam/leadiq-cynbit-assessment.git
cd leadiq-cynbit-assessment
```

Create and activate a virtual environment.

**Windows:**

```powershell
python -m venv .venv
.venv\Scripts\activate
```

**macOS/Linux:**

```bash
python -m venv .venv
source .venv/bin/activate
```

Install the dependencies:

```bash
python -m pip install -r requirements.txt
```

### Configure environment variables

Configure the following variables through your local environment or the deployment platform's secrets manager:

```text
OPENAI_API_KEY=YOUR_GEMINI_API_KEY
OPENAI_MODEL=YOUR_AVAILABLE_GEMINI_MODEL
```

The project uses an OpenAI-compatible client interface with the Gemini API endpoint. The variable names are retained for compatibility with that client.

**Security:** Never commit API keys, `.env` files, credentials, or private customer information to GitHub.

### Run the Streamlit application

```bash
python -m streamlit run app.py
```

Open the local URL printed in the terminal, normally `http://localhost:8501`.

### Run the FastAPI service

In a separate terminal:

```bash
python -m uvicorn api:app --reload
```

Open `http://127.0.0.1:8000/docs` to explore the API documentation.

Available endpoints:

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/health` | Service health check |
| POST | `/analyze` | Analyze a project inquiry |
| GET | `/analyses` | Retrieve saved analyses |

The API runs locally using the command above; a separate API deployment is required for public API access.

## 8. Testing and Evaluation

Run the automated tests:

```bash
python -m pytest -q
```

Run the exploratory model evaluation:

```bash
python evaluate_model.py
```

The development test run reported six passing tests.

### ML evaluation limitations

The current readiness classifier was trained on a small synthetic dataset of 16 examples. The recorded exploratory three-fold cross-validation results were:

- Accuracy: 0.50
- Macro F1-score: 0.41

These results are preliminary and are not sufficient to establish production reliability. The classifier's readiness labels must not be interpreted as lead conversion probabilities.

A production implementation would require a larger representative dataset, improved validation, class-specific error analysis, and ongoing monitoring.

## 9. Example Use Case

**Sample inquiry**

> We need an AI chatbot integrated with our website and CRM. Our budget is ₹2 lakh, and we want to launch within four weeks.

The expected workflow is to identify the requested AI chatbot, capture the website and CRM integration requirements, extract the stated budget and timeline, flag missing discovery details, assign a readiness category, and suggest a follow-up response.

Actual output depends on the configured LLM, model behavior, and classification guardrails.

## 10. Future Improvements

- Expand the training dataset using representative, appropriately consented and anonymized inquiries.
- Evaluate multiple classification approaches and tune decision thresholds.
- Add confidence-aware abstention and clearer explanations for readiness decisions.
- Introduce role-based access control and stronger data protection.
- Add persistent production database infrastructure and structured logging.
- Implement monitoring for extraction quality, model drift, and API failures.
- Add integration tests and automated CI checks.
- Require human approval before sending AI-generated customer communications.

## 11. Responsible Use

LeadIQ is an assessment prototype, not a production-ready lead-scoring system. LLM outputs may be incomplete or incorrect, and the current ML classifier has limited evaluation evidence.

Use synthetic data for demonstrations, validate outputs before acting on them, and require human review of customer-facing responses. Production use would require additional security, privacy, reliability, and model-performance validation.

## 12. Live Demo

**Try LeadIQ:** [Open the deployed Streamlit application](https://leadiq-cynbit-assessment-i9ktmtrt3zvyrjljwurlcz.streamlit.app/)

**Source code:** [View the public GitHub repository](https://github.com/suryaprakashpolkam/leadiq-cynbit-assessment)

---

*Prepared as an AI/ML assessment proof of concept for Cynbit.*
