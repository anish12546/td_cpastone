from typing import TypedDict, Optional
from langgraph.graph import StateGraph, END

from agents.profile_agent import analyze_profile
from agents.risk_agent import analyze_risk
from agents.decision_agent import make_decision
from agents.compliance_agent import log_compliance


class LoanState(TypedDict, total=False):
    data: dict
    profile: Optional[dict]
    risk: Optional[dict]
    decision: Optional[dict]
    compliance: Optional[dict]
    error: Optional[str]


def profile_step(state: LoanState) -> LoanState:
    try:
        state["profile"] = analyze_profile(state["data"])
    except Exception as e:
        state["error"] = str(e)
    return state


def risk_step(state: LoanState) -> LoanState:
    try:
        state["risk"] = analyze_risk(state["data"])
    except Exception as e:
        state["error"] = str(e)
    return state


def decision_step(state: LoanState) -> LoanState:
    try:
        state["decision"] = make_decision(state["profile"], state["risk"])
    except Exception as e:
        state["error"] = str(e)
    return state


def compliance_step(state: LoanState) -> LoanState:
    try:
        state["compliance"] = log_compliance(state["decision"])
    except Exception as e:
        state["error"] = str(e)
    return state


def rejected_compliance_step(state: LoanState) -> LoanState:
    try:
        state["compliance"] = log_compliance(state["decision"])
        state["compliance"]["manual_review_required"] = True
        state["compliance"]["routing_reason"] = "Rejected applications require additional compliance review"
    except Exception as e:
        state["error"] = str(e)
    return state


def error_handler_step(state: LoanState) -> LoanState:
    state["decision"] = {
        "classification": "Review",
        "risk_score": None,
        "confidence": 0.0,
        "explanation": f"Application moved to manual review because workflow error occurred: {state.get('error')}"
    }

    state["compliance"] = {
        "status": "manual_review_required",
        "error": state.get("error")
    }

    return state


def check_error(state: LoanState) -> str:
    if state.get("error"):
        return "error"
    return "success"


# def route_after_decision(state: LoanState) -> str:
#     if state.get("error"):
#         return "error"

#     classification = state["decision"]["classification"]

#     if classification == "Rejected":
#         return "rejected"

#     return "normal"
def route_after_decision(state):
    if state.get("error"):
        return "error"

    # ✅ NEW: confidence check
    if state["decision"]["confidence"] < 0.7:
        return "manual_review"

    if state["decision"]["classification"] == "Rejected":
        return "rejected"

    return "normal"


workflow = StateGraph(LoanState)

workflow.add_node("profile", profile_step)
workflow.add_node("risk", risk_step)
workflow.add_node("decision", decision_step)
workflow.add_node("compliance", compliance_step)
workflow.add_node("rejected_compliance", rejected_compliance_step)
workflow.add_node("error_handler", error_handler_step)
workflow.add_node("manual_review", compliance_step)


workflow.set_entry_point("profile")

workflow.add_conditional_edges(
    "profile",
    check_error,
    {
        "success": "risk",
        "error": "error_handler"
    }
)

workflow.add_conditional_edges(
    "risk",
    check_error,
    {
        "success": "decision",
        "error": "error_handler"
    }
)

workflow.add_conditional_edges(
    "decision",
    route_after_decision,
    {
        "normal": "compliance",
        "rejected": "rejected_compliance",
        "manual_review": "manual_review",
        "error": "error_handler"
    }
)

workflow.add_edge("compliance", END)
workflow.add_edge("rejected_compliance", END)
workflow.add_edge("error_handler", END)
workflow.add_edge("manual_review", END)


app_graph = workflow.compile()


def run_workflow(data: dict) -> dict:
    result = app_graph.invoke({
        "data": data,
        "profile": None,
        "risk": None,
        "decision": None,
        "compliance": None,
        "error": None
    })

    return {
        "classification": result["decision"]["classification"],
        "risk_score": result["decision"]["risk_score"],
        "confidence": result["decision"]["confidence"],
        "explanation": result["decision"]["explanation"],
        "compliance": result["compliance"]
    }
