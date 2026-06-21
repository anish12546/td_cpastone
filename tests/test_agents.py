from agents.profile_agent import analyze_profile
from agents.risk_agent import analyze_risk

def test_profile_agent():
    data ={"income":40000, "emploment":"Salaried", "credit_score":700, "loan_amount":100000,"liabilities":20000}
    result=analyze_profile(data)

def test_risk_agent():
    data={"income":40000,"loan_amount":100000,"liabilities":20000,"credit_score":700}
    result=analyze_risk(data)
    assert result["credit_risk"]=="Low"