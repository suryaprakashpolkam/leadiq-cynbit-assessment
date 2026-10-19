from lead_analyzer import analyze_inquiry, InquiryAnalysis
from ml_model import predict_readiness


def test_empty_inquiry_rejected():
    try:
        analyze_inquiry("   ")
        assert False, "Expected ValueError"
    except ValueError:
        pass


def test_inquiry_has_structured_fields():
    analysis, mode = analyze_inquiry(
        "We need an AI chatbot integrated with our website. "
        "Budget INR 2 lakh and launch within 4 weeks."
    )
    assert analysis.service_category in {
        "AI/ML", "Web Development", "Mobile App", "Cloud/DevOps",
        "CRM Automation", "Data Analytics", "Digital Marketing",
        "Other", "Unclear"
    }
    assert isinstance(analysis.requirements, list)
    assert analysis.budget is not None
    assert analysis.timeline is not None


def make_analysis(
    service_category="AI/ML",
    requirements=None,
    budget="INR 2 lakh",
    timeline="4 weeks",
):
    return InquiryAnalysis(
        service_category=service_category,
        requirements=requirements or ["AI chatbot for website"],
        budget=budget,
        timeline=timeline,
        missing_information=[],
        summary="Build an AI chatbot for a business website",
        urgency="Normal",
        suggested_next_action="Schedule discovery call",
        reply_draft="Thank you for sharing your requirements.",
    )


def test_readiness_prediction_has_valid_label():
    result = predict_readiness(make_analysis())
    assert result["readiness"] in {
        "Ready for discovery",
        "Needs clarification",
        "Low information",
    }


def test_missing_budget_does_not_return_ready():
    result = predict_readiness(make_analysis(budget=None))
    assert result["readiness"] != "Ready for discovery"


def test_missing_timeline_does_not_return_ready():
    result = predict_readiness(make_analysis(timeline=None))
    assert result["readiness"] != "Ready for discovery"


def test_unclear_service_is_low_information():
    result = predict_readiness(
        make_analysis(service_category="Unclear")
    )
    assert result["readiness"] == "Low information"
