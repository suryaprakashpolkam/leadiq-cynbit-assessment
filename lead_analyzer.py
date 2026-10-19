import json
import os
import re
from typing import Optional

from dotenv import load_dotenv
from pydantic import BaseModel, Field, ValidationError

from prompts import SYSTEM_PROMPT

load_dotenv()

ALLOWED_CATEGORIES = {
    "AI/ML", "Web Development", "Mobile App", "Cloud/DevOps",
    "CRM Automation", "Data Analytics", "Digital Marketing", "Other", "Unclear"
}

class InquiryAnalysis(BaseModel):
    service_category: str
    requirements: list[str] = Field(default_factory=list)
    budget: Optional[str] = None
    timeline: Optional[str] = None
    urgency: str = "Normal"
    missing_information: list[str] = Field(default_factory=list)
    summary: str
    reply_draft: str

def _fallback_analysis(message: str) -> InquiryAnalysis:
    """Transparent offline fallback. This is rule-based, not an LLM."""
    text = message.lower()
    category = "Unclear"
    patterns = [
        (["machine learning", " ai ", "artificial intelligence", "llm", "chatbot", "rag"], "AI/ML"),
        (["website", "web app", "web application", "dashboard"], "Web Development"),
        (["android", "ios", "mobile app"], "Mobile App"),
        (["aws", "cloud", "devops", "deployment", "infrastructure"], "Cloud/DevOps"),
        (["crm", "lead management", "sales pipeline"], "CRM Automation"),
        (["analytics", "power bi", "data analysis", "reporting"], "Data Analytics"),
        (["seo", "digital marketing", "advertising", "campaign"], "Digital Marketing"),
    ]
    padded = f" {text} "
    for terms, label in patterns:
        if any(term in padded for term in terms):
            category = label
            break

    requirements = []
    for term in [
        "dashboard", "API integration", "CRM integration", "authentication",
        "reporting", "automation", "chatbot", "data analytics", "mobile app",
        "AWS deployment", "payment integration"
    ]:
        if term.lower() in text:
            requirements.append(term)

    budget_match = re.search(r"(?:₹|rs\.?|inr|\$)\s?([\d,]+(?:\s?(?:k|lakh|lakhs))?)", message, re.I)
    timeline_match = re.search(r"\b(?:within|in|by)\s+(\d+\s+(?:days?|weeks?|months?))\b", message, re.I)
    budget = budget_match.group(0) if budget_match else None
    timeline = timeline_match.group(1) if timeline_match else None

    urgency = "High" if any(x in text for x in ["urgent", "asap", "immediately", "critical"]) else "Normal"
    missing = []
    if not budget:
        missing.append("Budget")
    if not timeline:
        missing.append("Target timeline")
    if not requirements:
        missing.append("Specific features or requirements")
    if category == "Unclear":
        missing.append("Service category / project goal")

    summary = f"Inquiry relates to {category.lower()}." if category != "Unclear" else "The inquiry is too vague to classify confidently."
    reply = "Thanks for sharing your project idea. Could you clarify " + ", ".join(missing[:3]).lower() + " so we can understand the scope?"
    return InquiryAnalysis(
        service_category=category,
        requirements=requirements,
        budget=budget,
        timeline=timeline,
        urgency=urgency,
        missing_information=missing,
        summary=summary,
        reply_draft=reply
    )

def analyze_inquiry(message: str) -> tuple[InquiryAnalysis, str]:
    message = message.strip()
    if not message:
        raise ValueError("Please enter a customer inquiry.")
    if len(message) > 5000:
        raise ValueError("Inquiry must be 5,000 characters or fewer.")

    # Streamlit Community Cloud secrets are read from st.secrets; local runs
    # continue to use environment variables/.env. Do not put secrets in source.
    api_key = os.getenv("OPENAI_API_KEY")
    model = os.getenv("OPENAI_MODEL")
    try:
        import streamlit as st
        if not api_key:
            api_key = st.secrets.get("OPENAI_API_KEY", "")
        if not model:
            model = st.secrets.get("OPENAI_MODEL", "")
    except Exception:
        # Streamlit secrets are optional for API-only/local execution.
        pass
    if not api_key or not model:
        return _fallback_analysis(message), "Rule-based demo fallback (LLM not configured)"

    try:
        from openai import OpenAI
        client = OpenAI(
            api_key=api_key,
            base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
        )
        response = client.chat.completions.create(
            model=model,
            temperature=0,
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": message}
            ]
        )
        raw = response.choices[0].message.content
        data = json.loads(raw)
        result = InquiryAnalysis.model_validate(data)
        if result.service_category not in ALLOWED_CATEGORIES:
            result.service_category = "Other"
        if result.urgency not in {"Low", "Normal", "High"}:
            result.urgency = "Normal"
        return result, f"LLM mode ({model})"
    except Exception as exc:
        # Fail visibly but preserve a usable local demo.
        return _fallback_analysis(message), f"Rule-based fallback after LLM error: {type(exc).__name__}"
