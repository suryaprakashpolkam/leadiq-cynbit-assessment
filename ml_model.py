"""Small reproducible ML baseline trained on synthetic, explicitly labeled examples."""
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

TRAINING_EXAMPLES = [
    ("Need an AI chatbot integrated with our website and CRM, budget approved, launch in 4 weeks", "Ready for discovery"),
    ("We need a web application, requirements and budget are confirmed, launch next month", "Ready for discovery"),
    ("Please build a mobile app with payment integration, budget 500000, deadline in 8 weeks", "Ready for discovery"),
    ("Need AWS migration and monitoring, scope approved and timeline confirmed", "Ready for discovery"),
    ("We need a CRM automation system, budget approved, requirements documented", "Ready for discovery"),
    ("Looking for data analytics dashboards, timeline and budget confirmed", "Ready for discovery"),
    ("Need an AI solution, not sure about budget or timeline yet", "Needs clarification"),
    ("I want a website, still deciding the features and budget", "Needs clarification"),
    ("Can you help with cloud services? Need advice before deciding the scope", "Needs clarification"),
    ("Interested in automation but not sure what kind or what it should do", "Needs clarification"),
    ("We may need a mobile app, can you explain options and approximate costs", "Needs clarification"),
    ("We need something for our business, please contact me", "Low information"),
    ("Hello, I want to know more", "Low information"),
    ("Can you help us improve things?", "Low information"),
    ("Please send details about your services", "Low information"),
    ("Interested. Tell me what you do", "Low information"),
]

def build_model():
    model = Pipeline([
        ("tfidf", TfidfVectorizer(ngram_range=(1, 2), lowercase=True)),
        ("classifier", LogisticRegression(max_iter=1000, random_state=42))
    ])
    X = [x for x, _ in TRAINING_EXAMPLES]
    y = [y for _, y in TRAINING_EXAMPLES]
    model.fit(X, y)
    return model

def predict_readiness(analysis):
    """Use explicit extracted features; don't treat model output as conversion probability."""
    text = " ".join([
        analysis.summary,
        analysis.service_category,
        " ".join(analysis.requirements),
        str(analysis.budget or ""),
        str(analysis.timeline or ""),
    ])
    model = build_model()
    label = model.predict([text])[0]

    # Guardrail rules override weak text-only classification.
    if analysis.service_category == "Unclear" or not analysis.requirements:
        label = "Low information" if analysis.service_category == "Unclear" else "Needs clarification"
    elif not analysis.budget or not analysis.timeline:
        if label == "Ready for discovery":
            label = "Needs clarification"

    return {
        "readiness": label,
        "model_name": "TF-IDF + Logistic Regression (synthetic training data)",
        "note": "Prototype category only; not a conversion probability. Validate with real labeled data before business use."
    }
